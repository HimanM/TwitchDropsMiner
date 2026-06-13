$ErrorActionPreference = "Stop"

$Repo = if ($env:TDMINER_REPO) { $env:TDMINER_REPO } else { "HimanM/TwitchDropsMiner" }
$InstallDir = if ($env:TDMINER_INSTALL_DIR) {
    $env:TDMINER_INSTALL_DIR
} else {
    Join-Path $env:LOCALAPPDATA "tdminer\bin"
}

$Asset = "Twitch.Drops.Miner.TUI.Windows.zip"
$Url = "https://github.com/$Repo/releases/latest/download/$Asset"
$TempDir = Join-Path ([System.IO.Path]::GetTempPath()) ("tdminer-" + [System.Guid]::NewGuid())
$ZipPath = Join-Path $TempDir "tdminer.zip"

New-Item -ItemType Directory -Force -Path $TempDir | Out-Null
New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null

try {
    Write-Host "Downloading $Url"
    Invoke-WebRequest -Uri $Url -OutFile $ZipPath
    Expand-Archive -LiteralPath $ZipPath -DestinationPath $TempDir -Force
    $Binary = Get-ChildItem -Path $TempDir -Recurse -Filter "tdminer.exe" | Select-Object -First 1
    if (-not $Binary) {
        throw "Could not find tdminer.exe in release asset."
    }
    Copy-Item -LiteralPath $Binary.FullName -Destination (Join-Path $InstallDir "tdminer.exe") -Force

    $UserPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $PathParts = @()
    if ($UserPath) {
        $PathParts = $UserPath -split ";"
    }
    if ($PathParts -notcontains $InstallDir) {
        $NewPath = if ($UserPath) { "$UserPath;$InstallDir" } else { $InstallDir }
        [Environment]::SetEnvironmentVariable("Path", $NewPath, "User")
        Write-Host "Added $InstallDir to your user PATH. Open a new terminal before running tdminer."
    }

    Write-Host "Installed tdminer to $(Join-Path $InstallDir 'tdminer.exe')"
    Write-Host "Run: tdminer"
}
finally {
    Remove-Item -LiteralPath $TempDir -Recurse -Force -ErrorAction SilentlyContinue
}
