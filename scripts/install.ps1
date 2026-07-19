#!/usr/bin/env pwsh
# spec-kit installation script for Hermes Agent (PowerShell)
# Installs skills and templates from this project to ~/.hermes/skills/

$ErrorActionPreference = "Stop"

# Change your skills directory if you want to install somewhere else (e.g., for testing)
$SkillsDir  = Join-Path $HOME "AppData/Local/hermes/skills"
$ProjectDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

Write-Host "Installing spec-kit from $ProjectDir to $SkillsDir..."

# Create skills directory if it doesn't exist
New-Item -ItemType Directory -Force -Path $SkillsDir | Out-Null

# Remove old speckit-* directories (pre-rename format) to prevent conflicts
$oldSpeckitDirs = Get-ChildItem -Path $SkillsDir -Directory -Filter "speckit-*" -ErrorAction SilentlyContinue
$oldSpeckitCount = 0
foreach ($oldDir in $oldSpeckitDirs) {
    Write-Host "  Removing old skill directory: $($oldDir.Name)"
    Remove-Item -Recurse -Force $oldDir.FullName
    $oldSpeckitCount++
}
if ($oldSpeckitCount -gt 0) {
    Write-Host "  -> Cleaned up $oldSpeckitCount old speckit-* skill(s)"
}

# Remove stale flat spec-kit-*.md files (old install format, now replaced by directories)
$staleFiles = Get-ChildItem -Path $SkillsDir -File -Filter "spec-kit-*.md" -ErrorAction SilentlyContinue
$staleCount = 0
foreach ($stale in $staleFiles) {
    Write-Host "  Removing stale flat file: $($stale.Name)"
    Remove-Item -Force $stale.FullName
    $staleCount++
}
if ($staleCount -gt 0) {
    Write-Host "  -> Cleaned up $staleCount stale flat spec-kit-* file(s)"
}

# Remove renamed/obsolete skill directories
$obsoleteDirs = @("spec-kit-analyze", "spec-kit-checklist", "spec-kit-explore", "spec-kit-compare")
foreach ($obsolete in $obsoleteDirs) {
    $obsoletePath = Join-Path $SkillsDir $obsolete
    if (Test-Path $obsoletePath -PathType Container) {
        Write-Host "  Removing obsolete skill directory: $obsolete"
        Remove-Item -Recurse -Force $obsoletePath
    }
}

# Remove obsolete template files
# ($TemplatesDir is defined below; cleanup runs after it's set)

# Copy each skill file from src/skills/ — install as <skill-name>/SKILL.md
$skillFiles = Get-ChildItem -Path (Join-Path $ProjectDir "src/skills") -Filter "*.md" -File -ErrorAction SilentlyContinue
foreach ($skill in $skillFiles) {
    $skillName = [System.IO.Path]::GetFileNameWithoutExtension($skill.Name)
    $skillDir = Join-Path $SkillsDir $skillName
    New-Item -ItemType Directory -Force -Path $skillDir | Out-Null
    Copy-Item -Force $skill.FullName (Join-Path $skillDir "SKILL.md")
    Write-Host "  Installing skill: $skillName"
}

# Copy umbrella SKILL.md to spec-kit/ directory
$UmbrellaSrc = Join-Path $ProjectDir "src/skills/spec-kit/SKILL.md"
$UmbrellaDst = Join-Path $SkillsDir "spec-kit/SKILL.md"
if (Test-Path $UmbrellaSrc -PathType Leaf) {
    New-Item -ItemType Directory -Force -Path (Split-Path $UmbrellaDst -Parent) | Out-Null
    Write-Host "  Installing umbrella SKILL.md"
    Copy-Item -Force $UmbrellaSrc $UmbrellaDst
}

# Copy templates to spec-kit/templates/
$TemplatesDir = Join-Path $SkillsDir "spec-kit/templates"
New-Item -ItemType Directory -Force -Path $TemplatesDir | Out-Null

# Remove obsolete template files
Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $TemplatesDir "checklist-template.md")
Remove-Item -Force -ErrorAction SilentlyContinue (Join-Path $TemplatesDir "comparison-template.md")

$templateFiles = Get-ChildItem -Path (Join-Path $ProjectDir "src/templates") -Filter "*-template.md" -File -ErrorAction SilentlyContinue
foreach ($tmpl in $templateFiles) {
    Write-Host "  Installing template: $($tmpl.Name)"
    Copy-Item -Force $tmpl.FullName (Join-Path $TemplatesDir $tmpl.Name)
}

# Copy references to spec-kit/references/
$ReferencesDir = Join-Path $SkillsDir "spec-kit/references"
New-Item -ItemType Directory -Force -Path $ReferencesDir | Out-Null

$referenceFiles = Get-ChildItem -Path (Join-Path $ProjectDir "src/references") -Filter "*.md" -File -ErrorAction SilentlyContinue
foreach ($ref in $referenceFiles) {
    Write-Host "  Installing reference: $($ref.Name)"
    Copy-Item -Force $ref.FullName (Join-Path $ReferencesDir $ref.Name)
}

# --- SOUL.md prompt ---
$SoulTemplate = Join-Path $TemplatesDir "soul-template.md"
$SoulDst = Join-Path $HOME ".hermes/SOUL.md"
if (Test-Path $SoulTemplate -PathType Leaf) {
    Write-Host ""
    if (Test-Path $SoulDst -PathType Leaf) {
        $currentSoulSize = (Get-Item $SoulDst).Length
        if ($currentSoulSize -gt 100) {
            Write-Host "  Note: ~/.hermes/SOUL.md exists and appears to have custom content ($currentSoulSize bytes)."
        }
    }
    Write-Host "  spec-kit includes a SOUL.md persona template (neutral, multi-mode)."
    $answer = Read-Host "  Replace ~/.hermes/SOUL.md with the spec-kit version? [y/N]"
    if ($answer -match '^(?i:y|yes)$') {
        Copy-Item -Force $SoulTemplate $SoulDst
        Write-Host "  -> Installed spec-kit SOUL.md to ~/.hermes/SOUL.md"
        # Also flip display.personality to none if it's currently a non-default value
        $hermesCmd = Get-Command hermes -ErrorAction SilentlyContinue
        if ($hermesCmd) {
            $currentPersonality = (& hermes config show display.personality 2>$null)
            if ($currentPersonality -and $currentPersonality -ne "none" -and $currentPersonality -ne "default") {
                $pAnswer = Read-Host "  Current display.personality is '$currentPersonality'. Set it to 'none' to avoid personality overlay conflicts? [Y/n]"
                if ($pAnswer -match '^(?i:n|no)$') {
                    Write-Host "  -> Keeping display.personality as '$currentPersonality'"
                } else {
                    try {
                        & hermes config set display.personality none 2>$null | Out-Null
                        Write-Host "  -> Set display.personality to none"
                    } catch {
                        Write-Host "  -> (could not auto-set display.personality)"
                    }
                }
            }
        }
    } else {
        Write-Host "  -> Skipping SOUL.md (left unchanged)"
    }
}

Write-Host ""
Write-Host "Done. Installed to $SkillsDir"
Write-Host ""
Write-Host "Skills:"
$topLevelSkills = Get-ChildItem -Path $SkillsDir -Filter "*.md" -File -ErrorAction SilentlyContinue
if ($topLevelSkills) {
    $topLevelSkills | ForEach-Object { Write-Host "  $($_.Name)" }
} else {
    Write-Host "  (none)"
}
Write-Host ""
Write-Host "Umbrella SKILL.md:"
if (Test-Path $UmbrellaDst -PathType Leaf) {
    Write-Host "  $UmbrellaDst"
}
Write-Host ""
Write-Host "Templates:"
$topLevelTemplates = Get-ChildItem -Path $TemplatesDir -Filter "*.md" -File -ErrorAction SilentlyContinue
if ($topLevelTemplates) {
    $topLevelTemplates | ForEach-Object { Write-Host "  $($_.Name)" }
} else {
    Write-Host "  (none)"
}
Write-Host ""

# Auto-creation: when a spec-kit skill first runs in any project, preflight.md
# creates specs/git-conventions.md from the template automatically.
# No manual copy needed.
Write-Host "---"
Write-Host "git-conventions.md is auto-created per-project when spec-kit skills first run."
Write-Host "No manual copy needed -- preflight.md handles it on demand."
