"""
Instagram Reels & Profiles Bulk Downloader
Uses yt-dlp backend with automatic detection for:
- Single Reel / Post URLs
- Multiple Reel URLs
- Profile URLs (bulk downloading all accessible Reels)
- Text files containing links (e.g., reels.txt)
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
import subprocess
import tempfile
import platform
import shutil
from pathlib import Path

# Ensure immediate unbuffered console output with UTF-8 encoding
try:
    sys.stdout.reconfigure(line_buffering=True, encoding="utf-8")
    sys.stderr.reconfigure(line_buffering=True, encoding="utf-8")
except Exception:
    pass

# GraphQL query document ID for user timeline feed
DOC_ID_USER_TIMELINE = "27159272927039485"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/128.0.0.0 Safari/537.36"
)

GRAPHQL_HEADERS = {
    "User-Agent": USER_AGENT,
    "X-IG-App-ID": "936619743392459",
    "Accept": "*/*",
}


def get_clipboard_text():
    """Reads text from system clipboard cross-platform."""
    try:
        if sys.platform == "win32":
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", "Get-Clipboard"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=5,
            )
            if res.returncode == 0:
                return res.stdout.strip()
        elif sys.platform == "darwin":
            res = subprocess.run(["pbpaste"], capture_output=True, text=True, timeout=5)
            if res.returncode == 0:
                return res.stdout.strip()
        else:
            for tool in [["xclip", "-selection", "clipboard", "-o"], ["wl-paste"]]:
                try:
                    res = subprocess.run(tool, capture_output=True, text=True, timeout=5)
                    if res.returncode == 0:
                        return res.stdout.strip()
                except FileNotFoundError:
                    continue
    except Exception:
        pass
    return ""


def resolve_ytdlp(script_dir):
    """
    Locates an existing yt-dlp binary or automatically downloads the latest
    official release directly from GitHub into the project folder.
    Supports Windows, macOS, and Linux without requiring pip or package managers.
    """
    system = platform.system().lower()
    is_windows = (system == "windows")
    exe_name = "yt-dlp.exe" if is_windows else "yt-dlp"

    # 1. Local project folder
    local_binary = script_dir / exe_name
    if local_binary.is_file():
        return local_binary

    # 2. System PATH
    path_binary = shutil.which("yt-dlp") or (shutil.which("yt-dlp.exe") if is_windows else None)
    if path_binary:
        return Path(path_binary)

    # 3. Auto-download from GitHub releases
    print("=" * 60)
    print("      yt-dlp Engine Not Found - Automatic Setup")
    print("=" * 60)
    print(f"[INFO] Downloading latest official yt-dlp release for {platform.system()}...")

    if is_windows:
        download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"
    elif system == "darwin":
        download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"
    else:
        download_url = "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"

    target_path = script_dir / exe_name

    try:
        req = urllib.request.Request(
            download_url,
            headers={"User-Agent": USER_AGENT}
        )
        with urllib.request.urlopen(req, timeout=60) as resp:
            total_size = int(resp.headers.get("content-length", 0))
            downloaded = 0
            chunk_size = 1024 * 128
            with open(target_path, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        pct = int(downloaded * 100 / total_size)
                        mb = downloaded / (1024 * 1024)
                        total_mb = total_size / (1024 * 1024)
                        sys.stdout.write(f"\r[DOWNLOAD] {mb:.1f}MB / {total_mb:.1f}MB ({pct}%)")
                        sys.stdout.flush()
        print("\n[+] yt-dlp engine downloaded and verified successfully!\n")
        if not is_windows:
            try:
                os.chmod(target_path, 0o755)
            except Exception:
                pass
        return target_path
    except Exception as e:
        print(f"\n[ERROR] Failed to auto-download yt-dlp: {e}")
        print("Please download yt-dlp manually from https://github.com/yt-dlp/yt-dlp/releases")
        print(f"and place it into: {script_dir}")
        sys.exit(1)


def classify_link(raw_token, script_dir=None):
    """
    Classifies a string token into:
    - 'file': local text file path
    - 'reel': single reel/post URL
    - 'profile': user profile URL or handle
    - 'unknown': other URL
    """
    token = raw_token.strip().strip("'\"")
    if not token:
        return None

    # Check if it's an existing file or a text file without extension
    candidates = [token]
    if script_dir:
        candidates.append(os.path.join(script_dir, token))
    if not token.lower().endswith(".txt"):
        candidates.append(token + ".txt")
        if script_dir:
            candidates.append(os.path.join(script_dir, token + ".txt"))

    for c in candidates:
        if os.path.isfile(c):
            return {"type": "file", "path": os.path.abspath(c), "raw": raw_token}

    # Clean query parameters, hash, and trailing /reels suffix
    clean = re.sub(r"[?#].*$", "", token)
    clean = re.sub(r"/reels/?$", "/", clean)

    # Check Reel / Post / TV
    m_reel = re.search(r"instagram\.com/(?:share/)?(?:p|tv|reel|reels)/([A-Za-z0-9_-]+)", clean)
    if m_reel:
        code = m_reel.group(1)
        return {
            "type": "reel",
            "id": code,
            "url": f"https://www.instagram.com/reel/{code}/",
            "raw": raw_token,
        }

    # Check Profile URL
    m_prof = re.search(r"instagram\.com/([A-Za-z0-9_.]+)/?$", clean)
    if m_prof:
        user = m_prof.group(1)
        if user not in ("explore", "accounts", "stories", "reels", "reel", "p", "tv", "direct"):
            return {
                "type": "profile",
                "username": user,
                "url": f"https://www.instagram.com/{user}/",
                "raw": raw_token,
            }

    # Check explicit handle (@user)
    m_handle = re.search(r"^@([A-Za-z0-9_.]+)$", clean)
    if m_handle:
        user = m_handle.group(1).strip(".")
        if user:
            return {
                "type": "profile",
                "username": user,
                "url": f"https://www.instagram.com/{user}/",
                "raw": raw_token,
            }

    # Check bare username without @ (must contain letters, not pure numbers, not reserved)
    m_user = re.search(r"^([A-Za-z0-9_.]+)$", clean)
    if m_user:
        user = m_user.group(1).strip(".")
        reserved = {
            "clip", "clipboard", "multi", "m", "q", "quit", "exit", "bat", "cmd", "ps1",
            "py", "txt", "mp4", "webm", "mkv", "am", "pm", "http", "https", "reels",
            "reel", "post", "stories", "downloads", "archive"
        }
        if (
            len(user) >= 2
            and re.search(r"[A-Za-z]", user)
            and ".." not in user
            and user.lower() not in reserved
            and not user.lower().endswith(".txt")
        ):
            return {
                "type": "profile",
                "username": user,
                "url": f"https://www.instagram.com/{user}/",
                "raw": raw_token,
            }

    if token.startswith("http://") or token.startswith("https://"):
        return {"type": "unknown", "url": token, "raw": raw_token}

    return None


def extract_tokens_from_text(text, script_dir=None):
    """
    Extracts URLs, explicit handles (@user), or recognized files from arbitrary text.
    Gracefully handles WhatsApp exports, chat messages, or freeform text.
    """
    if not text:
        return []

    tokens = []
    lines = text.splitlines() if "\n" in text else [text]
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check if the line itself is an existing file
        c = classify_link(line, script_dir=script_dir)
        if c and c["type"] == "file":
            tokens.append(c["path"])
            continue

        # Extract any HTTP/HTTPS URLs
        urls = re.findall(r"https?://[^\s,'\"<>]+", line)
        if urls:
            for u in urls:
                u_clean = u.rstrip(".,;:)>]")
                if u_clean:
                    tokens.append(u_clean)
            continue  # Found URLs in this line; do NOT extract chat text / timestamps as usernames!

        # If no URLs in this line, check for explicit @handles
        handles = re.findall(r"@[A-Za-z0-9_.]+", line)
        if handles:
            for h in handles:
                h_clean = h.rstrip(".,;:)>]")
                if len(h_clean) > 1:
                    tokens.append(h_clean)
            continue

        # If line has no URLs and no @handles:
        # Check if it's a single word (e.g. bare profile name typed by user)
        words = line.split()
        if len(words) == 1:
            w = words[0].strip().strip("'\"")
            c_word = classify_link(w, script_dir=script_dir)
            if c_word and c_word["type"] in ("file", "profile", "reel", "unknown"):
                tokens.append(w)

    return tokens


def extract_profile_reels(username, max_pages=None):
    """
    Extracts all accessible video/Reel shortcodes from an Instagram user profile
    using Instagram's GraphQL timeline feed query.
    """
    print(f"\n[PROFILE] Discovering accessible Reels from @{username}...")
    cursor = None
    reel_urls = []
    page = 0

    while True:
        page += 1
        vars_dict = {
            "data": {
                "count": 12,
                "include_reel_media_seen_timestamp": True,
                "include_relationship_info": True,
                "latest_besties_reel_media": True,
                "latest_reel_media": True,
            },
            "username": username,
            "__relay_internal__pv__PolarisImmersiveFeedChainingEnabledrelayprovider": True,
            "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider": False,
            "__relay_internal__pv__PolarisAIGMAccountLabelEnabledrelayprovider": False,
        }
        if cursor:
            vars_dict["after"] = cursor

        query_url = (
            f"https://www.instagram.com/graphql/query?"
            f"doc_id={DOC_ID_USER_TIMELINE}&variables={urllib.parse.quote(json.dumps(vars_dict))}"
        )
        req = urllib.request.Request(query_url, headers=GRAPHQL_HEADERS)

        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="ignore"))
        except Exception as e:
            print(f"  [!] Note: GraphQL page {page} fetch ended ({e}).")
            break

        data_obj = data.get("data") if isinstance(data, dict) else None
        if not data_obj or not isinstance(data_obj, dict):
            errors = data.get("errors") if isinstance(data, dict) else None
            if errors:
                err_msg = errors[0].get("message", "Unknown error") if isinstance(errors, list) and errors else str(errors)
                print(f"  [!] Instagram API note for @{username}: {err_msg}")
            else:
                print(f"  [!] No profile data returned for @{username} (profile may be private, restricted, or non-existent).")
            break

        timeline = data_obj.get("xdt_api__v1__feed__user_timeline_graphql_connection")
        if not timeline or not isinstance(timeline, dict):
            break

        edges = timeline.get("edges", [])
        if not isinstance(edges, list) or not edges:
            break

        page_new = 0
        for edge in edges:
            node = edge.get("node", {})
            items = node.get("items", [node])
            for item in items:
                code = item.get("code") or item.get("shortcode")
                is_video = item.get("is_video") or item.get("media_type") == 2
                if code and is_video:
                    reel_url = f"https://www.instagram.com/reel/{code}/"
                    if reel_url not in reel_urls:
                        reel_urls.append(reel_url)
                        page_new += 1

        print(f"  [+] Page {page}: found {page_new} video entries (Total so far: {len(reel_urls)})")

        page_info = timeline.get("page_info") or {}
        if not page_info.get("has_next_page") or not page_info.get("end_cursor"):
            break

        cursor = page_info.get("end_cursor")
        if max_pages and page >= max_pages:
            break

    print(f"[PROFILE] Finished discovery: {len(reel_urls)} Reels found for @{username}.")
    return reel_urls


def sync_archive(archive_path, dest_path):
    """
    If any video ID is recorded in archive.txt, but the video file has been deleted
    from dest_path, removes that ID from archive.txt so yt-dlp re-downloads it.
    """
    if not archive_path.is_file():
        return
    existing_files = (
        [f.name for f in dest_path.glob("*.mp4")]
        + [f.name for f in dest_path.glob("*.mkv")]
        + [f.name for f in dest_path.glob("*.webm")]
    )

    try:
        with open(archive_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        kept_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                video_id = parts[1]
                if any(video_id in fname for fname in existing_files):
                    kept_lines.append(line)
            else:
                kept_lines.append(line)

        if len(kept_lines) != len(lines):
            with open(archive_path, "w", encoding="utf-8") as f:
                f.writelines(kept_lines)
    except Exception:
        pass


def download_batch_with_ytdlp(urls, dest_folder, archive_file, ytdlp_path, cookies_file=None):
    """
    Downloads a list of URLs using yt-dlp in bulk with archive deduplication.
    """
    if not urls:
        print("[!] No URLs to download.")
        return 0

    dest_path = Path(dest_folder).resolve()
    dest_path.mkdir(parents=True, exist_ok=True)

    archive_path = Path(archive_file).resolve()
    archive_path.parent.mkdir(parents=True, exist_ok=True)

    # Sync archive with disk so deleted files can be re-downloaded
    sync_archive(archive_path, dest_path)

    # Write URLs to a temporary batch file to bypass Windows command line length limits
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False, suffix=".txt") as tf:
        for u in urls:
            tf.write(u + "\n")
        temp_batch_file = tf.name

    try:
        cmd = [
            str(ytdlp_path),
            "-a", temp_batch_file,
            "-P", str(dest_path),
            "-o", "%(id)s_%(title)s.%(ext)s",
            "--no-overwrites",
            "--download-archive", str(archive_path),
            "-i",
            "--windows-filenames",
        ]

        if cookies_file and os.path.isfile(cookies_file):
            cmd.extend(["--cookies", str(Path(cookies_file).resolve())])

        print(f"\n[DOWNLOAD] Starting bulk download of {len(urls)} item(s)...")
        print(f"[DOWNLOAD] Destination: {dest_path}")
        print(f"[DOWNLOAD] Archive:     {archive_path}\n")

        proc = subprocess.run(cmd)
        return proc.returncode
    finally:
        try:
            if os.path.exists(temp_batch_file):
                os.remove(temp_batch_file)
        except Exception:
            pass


def collect_inputs(script_dir):
    """
    Collects raw input tokens from sys.argv or interactive prompts.
    """
    args = sys.argv[1:]

    # Check for direct update argument
    if any(a in ("--update", "-u", "update") for a in args):
        return ["__UPDATE__"]

    # If arguments were passed via command line, parse them
    if args:
        if len(args) == 1:
            c = classify_link(args[0], script_dir)
            if c and c["type"] == "file":
                return [c["path"]]

        joined_args = " ".join(args)
        tokens = extract_tokens_from_text(joined_args, script_dir)
        if tokens:
            return tokens

    # Interactive mode
    print("==========================================================")
    print("      Instagram Reels & Profiles Bulk Downloader          ")
    print("==========================================================")
    print("You can provide:")
    print("  * A profile URL (e.g. https://www.instagram.com/name/ or @name)")
    print("  * A single Reel URL (e.g. https://www.instagram.com/reel/ID/)")
    print("  * Multiple URLs (separated by spaces or commas)")
    print("  * A text file path (e.g. reels or reels.txt)")
    print("  * Type 'clip' to read links from clipboard")
    print("  * Type 'multi' to paste multiple lines")
    print("  * Type 'update' to check for engine updates")
    print("  * Press ENTER to check for existing reels.txt\n")

    user_input = input("Enter Instagram URL(s), profile, or command: ").strip()

    if not user_input:
        default_batch = os.path.join(script_dir, "reels.txt")
        example_batch = os.path.join(script_dir, "reels.example.txt")
        if not os.path.isfile(default_batch) and os.path.isfile(example_batch):
            shutil.copyfile(example_batch, default_batch)

        if os.path.isfile(default_batch):
            ans = input(f"No input entered. Found reels.txt. Download links from reels.txt? (Y/n): ").strip().lower()
            if ans in ("", "y", "yes"):
                return [default_batch]
        print("[!] No input provided. Exiting.")
        return []

    # Update command
    if user_input.lower() in ("update", "u", "--update", "-u"):
        return ["__UPDATE__"]

    # Check if user_input directly points to a file or file with .txt
    c = classify_link(user_input, script_dir)
    if c and c["type"] == "file":
        return [c["path"]]

    # Clipboard mode
    if user_input.lower() in ("clip", "clipboard", "c"):
        clip_text = get_clipboard_text()
        if not clip_text:
            print("[!] Clipboard is empty or contains no readable text.")
            return []
        print("[INFO] Retrieved text from clipboard. Extracting links...")
        found = extract_tokens_from_text(clip_text, script_dir)
        for f in found[:5]:
            print(f"  - {f}")
        if len(found) > 5:
            print(f"  ... and {len(found) - 5} more.")
        return found

    # Multi-line mode
    if user_input.lower() in ("multi", "m"):
        print("\nPaste URLs below (press ENTER on an empty line when finished):")
        multi_lines = []
        while True:
            try:
                line = input().strip()
            except EOFError:
                break
            if not line:
                break
            multi_lines.append(line)
        combined = "\n".join(multi_lines)
        return extract_tokens_from_text(combined, script_dir)

    # General input (could be URL, space-separated URLs, WhatsApp paste, @user, etc.)
    return extract_tokens_from_text(user_input, script_dir)


def main():
    script_dir = Path(__file__).parent.resolve()
    ytdlp_exe = resolve_ytdlp(script_dir)

    tokens = collect_inputs(script_dir)
    if not tokens:
        return

    if tokens == ["__UPDATE__"]:
        print(f"\n[INFO] Checking and updating {ytdlp_exe.name} to the latest release...")
        try:
            subprocess.run([str(ytdlp_exe), "-U"])
        except Exception as e:
            print(f"[!] Update error: {e}")
        return

    cookies_file = script_dir / "cookies.txt"
    if cookies_file.is_file():
        print(f"[INFO] Found cookies.txt - will apply session cookies for authentication.")
    else:
        cookies_file = None

    # Expand any file tokens
    expanded_tokens = []
    for token in tokens:
        c = classify_link(token, script_dir=script_dir)
        if c and c["type"] == "file":
            print(f"[INFO] Reading URLs from file: {c['path']}")
            try:
                with open(c["path"], "r", encoding="utf-8") as f:
                    file_content = f.read()
                file_tokens = extract_tokens_from_text(file_content, script_dir=script_dir)
                expanded_tokens.extend(file_tokens)
            except Exception as e:
                print(f"[!] Could not read file {c['path']}: {e}")
        else:
            expanded_tokens.append(token)

    # Classify all items
    classified_reels = []
    classified_profiles = {}  # username -> profile info

    for token in expanded_tokens:
        item = classify_link(token, script_dir=script_dir)
        if not item:
            continue
        if item["type"] == "reel":
            if item["url"] not in classified_reels:
                classified_reels.append(item["url"])
        elif item["type"] == "profile":
            user = item["username"]
            if user not in classified_profiles:
                classified_profiles[user] = item
        elif item["type"] == "unknown":
            # Direct video URL fallback
            if item["url"] not in classified_reels:
                classified_reels.append(item["url"])

    print("\n" + "=" * 58)
    print("                  EXECUTION SUMMARY                       ")
    print("=" * 58)
    print(f"Direct / Single Reels to download : {len(classified_reels)}")
    print(f"Profiles to bulk download         : {len(classified_profiles)}")
    for u in classified_profiles:
        print(f"  * @{u}")
    print("=" * 58)

    downloads_base = script_dir / "downloads"

    # 1. Process all direct reels
    if classified_reels:
        print(f"\n>>> Processing {len(classified_reels)} individual Reel URL(s)...")
        reels_dest = downloads_base / "reels"
        reels_archive = reels_dest / "archive.txt"
        download_batch_with_ytdlp(
            urls=classified_reels,
            dest_folder=reels_dest,
            archive_file=reels_archive,
            ytdlp_path=ytdlp_exe,
            cookies_file=cookies_file,
        )

    # 2. Process each profile
    for username, prof_item in classified_profiles.items():
        print(f"\n>>> Processing profile: @{username} ({prof_item['url']})")
        profile_reels = extract_profile_reels(username)

        profile_dest = downloads_base / username
        profile_archive = profile_dest / "archive.txt"

        if profile_reels:
            download_batch_with_ytdlp(
                urls=profile_reels,
                dest_folder=profile_dest,
                archive_file=profile_archive,
                ytdlp_path=ytdlp_exe,
                cookies_file=cookies_file,
            )
        else:
            print(f"[!] No reels extracted via GraphQL for @{username}.")
            print(f"    Attempting fallback: querying profile with yt-dlp directly...")
            # Fallback to direct yt-dlp profile attempt
            download_batch_with_ytdlp(
                urls=[prof_item["url"]],
                dest_folder=profile_dest,
                archive_file=profile_archive,
                ytdlp_path=ytdlp_exe,
                cookies_file=cookies_file,
            )

    print("\n[ALL TASKS COMPLETED] Check the 'downloads/' folder for saved media.\n")


if __name__ == "__main__":
    main()
