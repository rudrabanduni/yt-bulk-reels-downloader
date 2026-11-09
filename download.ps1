# PowerShell wrapper for unified Instagram downloader

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }

$pythonCmd = $null
if (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
}

if ($pythonCmd) {
    $downloadPy = Join-Path $scriptDir "download.py"
    if (Test-Path $downloadPy) {
        & $pythonCmd $downloadPy $args
        exit $LASTEXITCODE
    }
}

# Native PowerShell Fallback if Python is unavailable
$ytdlp = Join-Path $scriptDir "yt-dlp.exe"
if (-not (Test-Path $ytdlp)) {
    Write-Host "[INFO] yt-dlp.exe not found. Downloading latest release from GitHub..." -ForegroundColor Cyan
    try {
        Invoke-WebRequest -Uri "https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe" -OutFile $ytdlp -UseBasicParsing
        Write-Host "[+] Successfully downloaded yt-dlp.exe!" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Failed to download yt-dlp.exe: $_" -ForegroundColor Red
        exit 1
    }
}

$inputUrls = @($args)
if ($inputUrls.Count -eq 0) {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "         Instagram Reels Bulk Downloader                  " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    $userIn = Read-Host "Enter Instagram URL(s) or username"
    if ($userIn) {
        $inputUrls = $userIn -split '[\s,]+' | Where-Object { $_ -ne "" }
    }
}

if ($inputUrls.Count -eq 0) {
    $batchFile = Join-Path $scriptDir "reels.txt"
    if (Test-Path $batchFile) {
        Write-Host "`n[INFO] No URL entered. Downloading from reels.txt..." -ForegroundColor Yellow
        $downloadsDir = Join-Path $scriptDir "downloads"
        $archiveFile = Join-Path $downloadsDir "archive.txt"
        & $ytdlp -a $batchFile -P $downloadsDir -o "%(uploader,channel,uploader_id)s/%(id)s_%(title)s.%(ext)s" --no-overwrites --download-archive $archiveFile -i --windows-filenames
        exit $LASTEXITCODE
    } else {
        Write-Host "[ERROR] No input provided." -ForegroundColor Red
        exit 1
    }
}

$downloadsBase = Join-Path $scriptDir "downloads"
foreach ($rawUrl in $inputUrls) {
    $cleanUrl = $rawUrl.Trim() -replace '[?#].*$', '' -replace '/reels/?$', '/'
    if ($cleanUrl -match 'instagram\.com/(?:share/)?(?:p|tv|reel)/([A-Za-z0-9_-]+)') {
        Write-Host "`n[INFO] Downloading Reel: $cleanUrl" -ForegroundColor Green
        $targetDir = Join-Path $downloadsBase "reels"
        $archive = Join-Path $targetDir "archive.txt"
        & $ytdlp $cleanUrl -P $targetDir -o "%(id)s_%(title)s.%(ext)s" --no-overwrites --download-archive $archive -i --windows-filenames
    } elseif ($cleanUrl -match 'instagram\.com/([A-Za-z0-9_.]+)/?$' -or $cleanUrl -match '^@([A-Za-z0-9_.]+)$') {
        $username = $matches[1]
        $targetUrl = "https://www.instagram.com/$username/"
        Write-Host "`n[INFO] Downloading Profile: @$username ($targetUrl)" -ForegroundColor Cyan
        $targetDir = Join-Path $downloadsBase $username
        $archive = Join-Path $targetDir "archive.txt"
        & $ytdlp $targetUrl -P $targetDir -o "%(id)s_%(title)s.%(ext)s" --no-overwrites --download-archive $archive -i --windows-filenames
    } else {
        $targetDir = Join-Path $downloadsBase "other"
        $archive = Join-Path $targetDir "archive.txt"
        & $ytdlp $cleanUrl -P $targetDir -o "%(id)s_%(title)s.%(ext)s" --no-overwrites --download-archive $archive -i --windows-filenames
    }
}
