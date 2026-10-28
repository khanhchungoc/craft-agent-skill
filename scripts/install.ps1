<#
.SYNOPSIS
    Installs craft-agent-skill into target AI agent runtimes at either User (global) or Project (workspace) level.

.DESCRIPTION
    Supports GitHub Copilot, Claude Code, OpenAI Codex, Antigravity, and Kiro.
    Can create directory junctions/symlinks (instant updates during development) or standalone copies.

.PARAMETER Scope
    'User' (global for current user) or 'Project' (current workspace directory). Default is 'User'.

.PARAMETER Runtime
    Target runtime harness: 'github-copilot', 'claude-code', 'codex', 'antigravity', 'kiro', or 'all'. Default is 'all'.

.PARAMETER Mode
    'Symlink' (uses NTFS directory junction on Windows without requiring admin) or 'Copy'. Default is 'Symlink'.

.PARAMETER TargetPath
    The workspace root for Project-level installation. Defaults to the current working directory.

.PARAMETER WithAgent
    When installing to github-copilot, also copies the @agent-skill-builder wrapper into .github/agents/.

.EXAMPLE
    # Install globally for Claude Code and Copilot
    .\scripts\install.ps1 -Scope User -Runtime claude-code

    # Install into current project for GitHub Copilot with the agent wrapper
    .\scripts\install.ps1 -Scope Project -Runtime github-copilot -WithAgent

    # Install into all runtimes in the current project via copy
    .\scripts\install.ps1 -Scope Project -Runtime all -Mode Copy
#>
[CmdletBinding()]
param (
    [ValidateSet("User", "Project")]
    [string]$Scope = "User",

    [ValidateSet("all", "github-copilot", "claude-code", "codex", "antigravity", "kiro")]
    [string]$Runtime = "all",

    [ValidateSet("Symlink", "Copy")]
    [string]$Mode = "Symlink",

    [string]$TargetPath = (Get-Location).Path,

    [switch]$WithAgent
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
    $destinations["github-copilot"] = Join-Path $userHome ".copilot\skills\craft-agent-skill"
    $destinations["claude-code"]    = Join-Path $userHome ".claude\skills\craft-agent-skill"
    $destinations["codex"]          = Join-Path $userHome ".agents\skills\craft-agent-skill"
    $destinations["antigravity"]    = Join-Path $userHome ".gemini\antigravity\skills\craft-agent-skill"
    $destinations["kiro"]           = Join-Path $userHome ".kiro\skills\craft-agent-skill"
} else {
    $targetDir = (Resolve-Path $TargetPath).Path
    $destinations["github-copilot"] = Join-Path $targetDir ".github\skills\craft-agent-skill"
    $destinations["claude-code"]    = Join-Path $targetDir ".claude\skills\craft-agent-skill"
    $destinations["codex"]          = Join-Path $targetDir ".agents\skills\craft-agent-skill"
    $destinations["antigravity"]    = Join-Path $targetDir "skills\craft-agent-skill"
    $destinations["kiro"]           = Join-Path $targetDir ".kiro\skills\craft-agent-skill"
}

$runtimesToInstall = if ($Runtime -eq "all") { $destinations.Keys } else { @($Runtime) }

foreach ($rt in $runtimesToInstall) {
    $dest = $destinations[$rt]
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

    # Optional Copilot Agent wrapper installation
    if ($rt -eq "github-copilot" -and $WithAgent) {
        $agentSrc = Join-Path $repoRoot "assets\runtimes\github-copilot\agent-skill-builder.agent.md"
        $agentDir = if ($Scope -eq "User") {
            Join-Path $userHome ".copilot\agents"
        } else {
            Join-Path (Resolve-Path $TargetPath).Path ".github\agents"
        }
        if (-not (Test-Path $agentDir)) { New-Item -ItemType Directory -Path $agentDir -Force | Out-Null }
        $agentDest = Join-Path $agentDir "agent-skill-builder.agent.md"
        Write-Host "    Installing Copilot Agent wrapper -> $agentDest" -ForegroundColor Green
        Copy-Item -Path $agentSrc -Destination $agentDest -Force
    }
}

Write-Host "==> Installation complete!" -ForegroundColor Cyan

