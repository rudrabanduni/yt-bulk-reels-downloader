"""
Instagram Reels & Profiles Bulk Downloader - Graphical User Interface (GUI)
Zero-dependency native Tkinter GUI for Windows, macOS, and Linux.
"""

import sys
import os
import queue
import threading
import subprocess
import platform
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText

# Import core downloader engine
SCRIPT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(SCRIPT_DIR))
import download


class DownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Bulk Reels Downloader")
        self.root.geometry("680x740")
        self.root.minsize(580, 620)

        # Ensure correct window icon or styling where supported
        self.is_mac = (platform.system().lower() == "darwin")
        self.is_win = (platform.system().lower() == "windows")

        # Background colors
        self.bg_main = "#F8FAFC"
        self.card_bg = "#FFFFFF"
        self.text_dark = "#0F172A"
        self.text_muted = "#64748B"
        self.accent_color = "#4F46E5"
        self.accent_hover = "#4338CA"
        self.terminal_bg = "#0B0F19"
        self.terminal_fg = "#E2E8F0"

        self.root.configure(bg=self.bg_main)

        # Thread queue for safe GUI logging
        self.log_queue = queue.Queue()
        self.is_downloading = False

        self._init_styles()
        self._build_ui()
        self._check_log_queue()

        # Check / resolve engine in background on launch
        self._async_check_engine()

    def _init_styles(self):
        self.style = ttk.Style()
        try:
            if self.is_win:
                self.style.theme_use("vista")
            elif self.is_mac:
                self.style.theme_use("aqua")
            else:
                self.style.theme_use("clam")
        except Exception:
            pass

    def _build_ui(self):
        main_frame = tk.Frame(self.root, bg=self.bg_main, padx=20, pady=16)
        main_frame.pack(fill="both", expand=True)

        # 1. Header Card
        header_card = tk.Frame(main_frame, bg=self.card_bg, padx=16, pady=14, relief="ridge", bd=1)
        header_card.pack(fill="x", pady=(0, 12))

        title_lbl = tk.Label(
            header_card,
            text="🎬 Instagram Bulk Reels Downloader",
            font=("Segoe UI" if self.is_win else "Helvetica", 16, "bold"),
            bg=self.card_bg,
            fg=self.text_dark,
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = tk.Label(
            header_card,
            text="Download accessible Reels from creator profiles, multiple links, or text lists.",
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg=self.card_bg,
            fg=self.text_muted,
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # 2. Mode Selection Card
        mode_card = tk.LabelFrame(
            main_frame,
            text=" 1. What would you like to download? ",
            font=("Segoe UI" if self.is_win else "Helvetica", 10, "bold"),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=14,
            pady=10,
            relief="groove",
            bd=1,
        )
        mode_card.pack(fill="x", pady=(0, 12))

        self.mode_var = tk.StringVar(value="profile")

        rb1 = tk.Radiobutton(
            mode_card,
            text="👤  All Reels from a Profile (Bulk download all videos)",
            variable=self.mode_var,
            value="profile",
            command=self._on_mode_change,
            bg=self.card_bg,
            fg=self.text_dark,
            activebackground=self.card_bg,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
        )
        rb1.pack(anchor="w", pady=2)

        rb2 = tk.Radiobutton(
            mode_card,
            text="🔗  Single Reel or Multiple Reel Links",
            variable=self.mode_var,
            value="reels",
            command=self._on_mode_change,
            bg=self.card_bg,
            fg=self.text_dark,
            activebackground=self.card_bg,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
        )
        rb2.pack(anchor="w", pady=2)

        rb3 = tk.Radiobutton(
            mode_card,
            text="📄  Batch from Text File (e.g. reels.txt or chat notes)",
            variable=self.mode_var,
            value="file",
            command=self._on_mode_change,
            bg=self.card_bg,
            fg=self.text_dark,
            activebackground=self.card_bg,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
        )
        rb3.pack(anchor="w", pady=2)

        # 3. Input Section Card
        input_card = tk.LabelFrame(
            main_frame,
            text=" 2. Provide Link or Username ",
            font=("Segoe UI" if self.is_win else "Helvetica", 10, "bold"),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=14,
            pady=10,
            relief="groove",
            bd=1,
        )
        input_card.pack(fill="x", pady=(0, 12))

        self.input_hint_lbl = tk.Label(
            input_card,
            text="Paste Instagram profile URL (e.g. https://www.instagram.com/username/ or @username):",
            bg=self.card_bg,
            fg=self.text_muted,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
        )
        self.input_hint_lbl.pack(anchor="w", pady=(0, 6))

        # Text Input Box (multi-line)
        self.text_input = tk.Text(
            input_card,
            height=4,
            wrap="word",
            font=("Consolas" if self.is_win else "Menlo", 10),
            bg="#FFFFFF",
            relief="solid",
            bd=1,
        )
        self.text_input.pack(fill="x", pady=(0, 8))

        # Quick input action buttons
        input_btns_frame = tk.Frame(input_card, bg=self.card_bg)
        input_btns_frame.pack(fill="x")

        self.btn_paste = tk.Button(
            input_btns_frame,
            text="📋 Paste from Clipboard",
            command=self._paste_clipboard,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg="#E2E8F0",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
        )
        self.btn_paste.pack(side="left", padx=(0, 8))

        self.btn_browse = tk.Button(
            input_btns_frame,
            text="📂 Browse File...",
            command=self._browse_file,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg="#E2E8F0",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
        )
        # Hidden initially; shown in "file" mode
        self.btn_browse.pack(side="left", padx=(0, 8))
        self.btn_browse.pack_forget()

        self.btn_clear = tk.Button(
            input_btns_frame,
            text="🧹 Clear",
            command=self._clear_input,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg="#F1F5F9",
            relief="flat",
            padx=10,
            pady=4,
            cursor="hand2",
        )
        self.btn_clear.pack(side="left")

        # 4. Action Buttons Bar
        action_frame = tk.Frame(main_frame, bg=self.bg_main)
        action_frame.pack(fill="x", pady=(0, 12))

        self.btn_download = tk.Button(
            action_frame,
            text="⬇️  Start Download",
            command=self._start_download_thread,
            font=("Segoe UI" if self.is_win else "Helvetica", 11, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            activeforeground="#FFFFFF",
            relief="flat",
            padx=18,
            pady=8,
            cursor="hand2",
        )
        self.btn_download.pack(side="left", padx=(0, 10))

        self.btn_open_folder = tk.Button(
            action_frame,
            text="📁  Open Downloads",
            command=self._open_downloads_folder,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg="#E2E8F0",
            fg=self.text_dark,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2",
        )
        self.btn_open_folder.pack(side="left", padx=(0, 10))

        self.btn_update = tk.Button(
            action_frame,
            text="🔄  Check Updates",
            command=self._async_update_engine,
            font=("Segoe UI" if self.is_win else "Helvetica", 9),
            bg="#F1F5F9",
            fg=self.text_muted,
            relief="flat",
            padx=10,
            pady=7,
            cursor="hand2",
        )
        self.btn_update.pack(side="right")

        # 5. Live Log / Progress Console
        log_frame = tk.LabelFrame(
            main_frame,
            text=" Real-time Progress & Status ",
            font=("Segoe UI" if self.is_win else "Helvetica", 9, "bold"),
            bg=self.card_bg,
            fg=self.text_dark,
            padx=10,
            pady=8,
            relief="groove",
            bd=1,
        )
        log_frame.pack(fill="both", expand=True)

        self.log_text = ScrolledText(
            log_frame,
            wrap="word",
            font=("Consolas" if self.is_win else "Menlo", 9),
            bg=self.terminal_bg,
            fg=self.terminal_fg,
            insertbackground="#FFFFFF",
            relief="flat",
            bd=0,
        )
        self.log_text.pack(fill="both", expand=True)

        # Status Bar
        self.status_bar = tk.Label(
            main_frame,
            text="Status: Ready",
            font=("Segoe UI" if self.is_win else "Helvetica", 8),
            bg=self.bg_main,
            fg=self.text_muted,
            anchor="w",
        )
        self.status_bar.pack(fill="x", pady=(4, 0))

        # Initial prompt
        self.log("Ready. Select an option above, enter a link, and click 'Start Download'.\n")

    def log(self, message):
        """Thread-safe logging to the text box."""
        self.log_queue.put(str(message))

    def _check_log_queue(self):
        """Pulls log messages from queue and renders them."""
        while not self.log_queue.empty():
            msg = self.log_queue.get_nowait()
            self.log_text.insert("end", msg + "\n")
            self.log_text.see("end")
        self.root.after(100, self._check_log_queue)

    def _on_mode_change(self):
        mode = self.mode_var.get()
        if mode == "profile":
            self.input_hint_lbl.config(
                text="Paste Instagram profile URL (e.g. https://www.instagram.com/username/ or @username):"
            )
            self.btn_browse.pack_forget()
        elif mode == "reels":
            self.input_hint_lbl.config(
                text="Paste Reel URL(s) (one or several, separated by spaces or newlines):"
            )
            self.btn_browse.pack_forget()
        elif mode == "file":
            self.input_hint_lbl.config(
                text="Enter path to text file containing links (defaults to reels.txt if empty):"
            )
            self.btn_browse.pack(side="left", padx=(0, 8))

    def _paste_clipboard(self):
        text = download.get_clipboard_text()
        if text:
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", text.strip())
        else:
            try:
                clip = self.root.clipboard_get()
                self.text_input.delete("1.0", "end")
                self.text_input.insert("1.0", clip.strip())
            except Exception:
                messagebox.showinfo("Clipboard", "Clipboard is empty.")

    def _clear_input(self):
        self.text_input.delete("1.0", "end")

    def _browse_file(self):
        f = filedialog.askopenfilename(
            title="Select Text File with Links",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            initialdir=str(SCRIPT_DIR),
        )
        if f:
            self.text_input.delete("1.0", "end")
            self.text_input.insert("1.0", f)

    def _open_downloads_folder(self):
        dl_folder = SCRIPT_DIR / "downloads"
        dl_folder.mkdir(parents=True, exist_ok=True)
        try:
            if self.is_win:
                os.startfile(dl_folder)
            elif self.is_mac:
                subprocess.run(["open", str(dl_folder)])
            else:
                subprocess.run(["xdg-open", str(dl_folder)])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open downloads folder: {e}")

    def _async_check_engine(self):
        def worker():
            try:
                ytdlp = download.resolve_ytdlp(SCRIPT_DIR)
                self.log(f"[INFO] Download engine active: {ytdlp.name}")
            except Exception as e:
                self.log(f"[!] Engine notice: {e}")
        threading.Thread(target=worker, daemon=True).start()

    def _async_update_engine(self):
        if self.is_downloading:
            messagebox.showwarning("Busy", "Please wait until the current download finishes.")
            return

        def worker():
            self.status_bar.config(text="Status: Checking for engine updates...")
            self.log("\n[UPDATE] Checking latest release of download engine...")
            try:
                ytdlp = download.resolve_ytdlp(SCRIPT_DIR)
                proc = subprocess.run([str(ytdlp), "-U"], capture_output=True, text=True)
                out = (proc.stdout or "") + (proc.stderr or "")
                for l in out.splitlines():
                    if l.strip():
                        self.log("  " + l.strip())
                self.log("[UPDATE] Check finished.\n")
                self.status_bar.config(text="Status: Engine update check completed.")
            except Exception as e:
                self.log(f"[!] Update error: {e}")
                self.status_bar.config(text="Status: Update check failed.")

        threading.Thread(target=worker, daemon=True).start()

    def _start_download_thread(self):
        if self.is_downloading:
            return

        user_raw = self.text_input.get("1.0", "end").strip()
        mode = self.mode_var.get()

        if not user_raw and mode != "file":
            messagebox.showwarning("Input Required", "Please enter a profile link, reel link, or username first.")
            return

        self.is_downloading = True
        self.btn_download.config(text="⏳ Downloading...", state="disabled")
        self.status_bar.config(text="Status: Downloading in background...")

        def worker():
            try:
                self._execute_download(mode, user_raw)
            finally:
                self.is_downloading = False
                self.root.after(0, self._on_download_complete)

        threading.Thread(target=worker, daemon=True).start()

    def _on_download_complete(self):
        self.btn_download.config(text="⬇️  Start Download", state="normal")
        self.status_bar.config(text="Status: Completed!")
        self.log("\n[SUCCESS] Task completed! Click 'Open Downloads' to view your videos.\n")

    def _execute_download(self, mode, raw_input):
        script_dir = SCRIPT_DIR
        ytdlp_exe = download.resolve_ytdlp(script_dir)
        cookies_file = script_dir / "cookies.txt"
        if not cookies_file.is_file():
            cookies_file = None

        downloads_base = script_dir / "downloads"

        # 1. Profile Mode
        if mode == "profile":
            clean = raw_input.strip()
            # If user entered multi-token, take first
            tokens = download.extract_tokens_from_text(clean, script_dir)
            target = tokens[0] if tokens else clean
            item = download.classify_link(target, script_dir)

            username = None
            if item and item["type"] == "profile":
                username = item["username"]
            else:
                # Try fallback extraction of handle
                import re
                m = re.search(r"instagram\.com/([A-Za-z0-9_.]+)", target)
                if m:
                    username = m.group(1)
                else:
                    username = clean.lstrip("@").strip()

            if not username:
                self.log("[ERROR] Could not detect Instagram profile username.")
                return

            self.log(f"\n==========================================================")
            self.log(f"       Processing Profile Bulk Download: @{username}")
            self.log(f"==========================================================")
            reels = download.extract_profile_reels(username, log_fn=self.log)

            profile_dest = downloads_base / username
            profile_archive = profile_dest / "archive.txt"

            if reels:
                download.download_batch_with_ytdlp(
                    urls=reels,
                    dest_folder=profile_dest,
                    archive_file=profile_archive,
                    ytdlp_path=ytdlp_exe,
                    cookies_file=cookies_file,
                    log_fn=self.log,
                )
            else:
                self.log(f"[!] No Reels found via GraphQL. Querying profile directly with yt-dlp...")
                prof_url = f"https://www.instagram.com/{username}/"
                download.download_batch_with_ytdlp(
                    urls=[prof_url],
                    dest_folder=profile_dest,
                    archive_file=profile_archive,
                    ytdlp_path=ytdlp_exe,
                    cookies_file=cookies_file,
                    log_fn=self.log,
                )

        # 2. Reels Mode
        elif mode == "reels":
            tokens = download.extract_tokens_from_text(raw_input, script_dir)
            if not tokens:
                self.log("[!] No valid URLs found in your input.")
                return

            reels_dest = downloads_base / "reels"
            reels_archive = reels_dest / "archive.txt"
            self.log(f"\n==========================================================")
            self.log(f"        Processing {len(tokens)} Reel URL(s)")
            self.log(f"==========================================================")
            download.download_batch_with_ytdlp(
                urls=tokens,
                dest_folder=reels_dest,
                archive_file=reels_archive,
                ytdlp_path=ytdlp_exe,
                cookies_file=cookies_file,
                log_fn=self.log,
            )

        # 3. File Mode
        elif mode == "file":
            target_file = raw_input.strip() if raw_input.strip() else str(script_dir / "reels.txt")
            if not os.path.isfile(target_file):
                ex = script_dir / "reels.example.txt"
                if ex.is_file():
                    import shutil
                    shutil.copyfile(ex, target_file)

            if not os.path.isfile(target_file):
                self.log(f"[ERROR] File not found: {target_file}")
                return

            self.log(f"[INFO] Reading links from file: {target_file}")
            try:
                with open(target_file, "r", encoding="utf-8") as f:
                    content = f.read()
                tokens = download.extract_tokens_from_text(content, script_dir)
            except Exception as e:
                self.log(f"[ERROR] Could not read file: {e}")
                return

            if not tokens:
                self.log("[!] No valid links found in the selected file.")
                return

            reels_dest = downloads_base / "reels"
            reels_archive = reels_dest / "archive.txt"
            self.log(f"\n==========================================================")
            self.log(f"        Processing {len(tokens)} Link(s) from File")
            self.log(f"==========================================================")
            download.download_batch_with_ytdlp(
                urls=tokens,
                dest_folder=reels_dest,
                archive_file=reels_archive,
                ytdlp_path=ytdlp_exe,
                cookies_file=cookies_file,
                log_fn=self.log,
            )


def main():
    root = tk.Tk()
    app = DownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
