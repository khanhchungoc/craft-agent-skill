<#
.SYNOPSIS
    Installs craft-agent-skill into target AI agent runtimes at either User (global) or Project (workspace) level.

.DESCRIPTION
    Supports Copilot, Claude Code, OpenAI Codex, Gemini/Antigravity, and Kiro.
    Can create directory junctions/symlinks (instant updates during development) or standalone copies.

.PARAMETER Scope
    'User' (global for current user) or 'Project' (current workspace directory). Default is 'User'.

.PARAMETER Runtime
    Target runtime harness: 'copilot', 'claude-code', 'codex', 'gemini', 'kiro', or 'all'. Default is 'all'.

.PARAMETER Mode
    'Symlink' (uses NTFS directory junction on Windows without requiring admin) or 'Copy'. Default is 'Symlink'.

.PARAMETER TargetPath
    The workspace root for Project-level installation. Defaults to the current working directory.

.EXAMPLE
    # Install globally for Claude Code and Copilot
    .\scripts\install.ps1 -Scope User -Runtime claude-code

    # Install into current project for Copilot
    .\scripts\install.ps1 -Scope Project -Runtime copilot

    # Install into all runtimes in the current project via copy
    .\scripts\install.ps1 -Scope Project -Runtime all -Mode Copy
#>
[CmdletBinding()]
param (
    [ValidateSet("User", "Project")]
    [string]$Scope = "User",

    [ValidateSet("all", "copilot", "github-copilot", "claude-code", "codex", "gemini", "antigravity", "kiro")]
    [string]$Runtime = "all",

    [ValidateSet("Symlink", "Copy")]
    [string]$Mode = "Symlink",

    [string]$TargetPath = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$userHome = [System.Environment]::GetFolderPath([System.Environment+SpecialFolder]::UserProfile)

Write-Host "==> Installing craft-agent-skill" -ForegroundColor Cyan
Write-Host "    Source:  $repoRoot"
Write-Host "    Scope:   $Scope"
Write-Host "    Mode:    $Mode"
Write-Host "    Target:  $($Runtime.ToUpper())"

$destinations = @{}

if ($Scope -eq "User") {
    $destinations["copilot"]        = Join-Path $userHome ".copilot\skills\craft-agent-skill"
    $destinations["claude-code"]    = Join-Path $userHome ".claude\skills\craft-agent-skill"
    $destinations["codex"]          = Join-Path $userHome ".agents\skills\craft-agent-skill"
    $destinations["gemini"]         = Join-Path $userHome ".gemini\skills\craft-agent-skill"
    $destinations["antigravity"]    = Join-Path $userHome ".gemini\config\skills\craft-agent-skill"
    $destinations["kiro"]           = Join-Path $userHome ".kiro\skills\craft-agent-skill"
} else {
    $targetDir = (Resolve-Path $TargetPath).Path
    $destinations["copilot"]        = Join-Path $targetDir ".github\skills\craft-agent-skill"
    $destinations["claude-code"]    = Join-Path $targetDir ".claude\skills\craft-agent-skill"
    $destinations["codex"]          = Join-Path $targetDir ".agents\skills\craft-agent-skill"
    $destinations["gemini"]         = Join-Path $targetDir ".gemini\skills\craft-agent-skill"
    $destinations["antigravity"]    = Join-Path $targetDir ".agents\skills\craft-agent-skill"
    $destinations["kiro"]           = Join-Path $targetDir ".kiro\skills\craft-agent-skill"
}

$normalizedRuntime = switch ($Runtime) {
    "github-copilot" { "copilot" }
    default          { $Runtime }
}
$runtimesToInstall = if ($normalizedRuntime -eq "all") { @("copilot", "claude-code", "codex", "gemini", "antigravity", "kiro") } else { @($normalizedRuntime) }

foreach ($rt in $runtimesToInstall) {
    $dest = $destinations[$rt]
    $canonicalDest = [System.IO.Path]::GetFullPath($dest).TrimEnd('\', '/')
    $canonicalRepo = [System.IO.Path]::GetFullPath($repoRoot).TrimEnd('\', '/')

    if ($canonicalDest -eq $canonicalRepo) {
        Write-Host "    Target ($rt) -> $dest is the source repository; skipping to prevent self-deletion." -ForegroundColor Yellow
        continue
    }

    $parentDir = Split-Path $dest -Parent

    if (-not (Test-Path $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }

    if (Test-Path $dest) {
        Write-Host "    Removing existing target at $dest" -ForegroundColor Yellow
        $item = Get-Item $dest -Force
        if ($item.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            # Junction / Symlink
            [System.IO.Directory]::Delete($dest)
        } else {
            Remove-Item $dest -Recurse -Force
        }
    }

    if ($Mode -eq "Symlink") {
        Write-Host "    Linking ($rt) -> $dest" -ForegroundColor Green
        New-Item -ItemType Junction -Path $dest -Target $repoRoot | Out-Null
    } else {
        Write-Host "    Copying ($rt) -> $dest" -ForegroundColor Green
        Copy-Item -Path $repoRoot -Destination $dest -Recurse -Force
        # Clean up git artifacts in copy
        $gitDir = Join-Path $dest ".git"
        if (Test-Path $gitDir) { Remove-Item $gitDir -Recurse -Force }
    }
}

Write-Host "==> Installation complete!" -ForegroundColor Cyan
