# ============================================================
# Rockwell Documentation Database - Auto Index Generator
# Run: .\Update-Index.ps1
# ============================================================

$root = $PSScriptRoot
$indexPath = Join-Path $root "README.md"

$categoryNames = @{
    "01_PLCs"                 = "PLCs and Controllers"
    "02_Drives"               = "Variable Frequency Drives"
    "03_Servos"               = "Servo Drives"
    "04_Safety"               = "Safety Systems"
    "05_IO_Modules"           = "I/O Modules"
    "06_Networking"           = "Networking and Communications"
    "07_Software"             = "Software and Programming"
    "08_HMI"                  = "HMI and Operator Interface"
    "09_Motor_Control"        = "Motor Control and Protection"
    "10_Pilot_Devices"        = "Pilot Devices Relays and Timers"
    "11_Sensors"              = "Sensors and Detection"
    "12_Panel_Components"     = "Panel Components and Wiring"
    "13_Motion"               = "Motion Control and Servo Motors"
    "14_Migration_Conversion" = "Migration and Conversion Guides"
    "15_Cognex"               = "Cognex Vision Systems"
    "16_SICK"                 = "SICK Sensors and Safety"
    "17_Banner"               = "Banner Engineering"
    "18_Festo"                = "Festo Pneumatics"
    "19_Keyence"              = "Keyence Sensors and Vision"
    "20_Endress_Hauser"       = "Endress+Hauser Process Instruments"
    "21_nVent_Hoffman"        = "nVent HOFFMAN Enclosures"
    "22_Belden"               = "Belden Industrial Networking"
    "23_Wonderware_AVEVA"     = "Wonderware AVEVA InTouch HMI"
    "24_CIP_EtherNetIP"       = "CIP and EtherNet/IP Protocol"
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm"
$allPdfs = Get-ChildItem -Path $root -Recurse -Filter "*.pdf" -File
$totalCount = $allPdfs.Count
$totalSizeMB = [math]::Round(($allPdfs | Measure-Object -Property Length -Sum).Sum / 1MB, 1)

$lines = [System.Collections.ArrayList]::new()

[void]$lines.Add("# Rockwell Automation Documentation Database")
[void]$lines.Add("")
[void]$lines.Add("> **$totalCount documents** | **$totalSizeMB MB** total | Last updated: **$timestamp**")
[void]$lines.Add(">")
[void]$lines.Add("> This index is automatically updated via GitHub Actions.")
[void]$lines.Add("> You can also run ``.\Update-Index.ps1`` locally to refresh after adding new documents.")
[void]$lines.Add("")
[void]$lines.Add("---")
[void]$lines.Add("")

# Table of Contents
[void]$lines.Add("## Quick Navigation")
[void]$lines.Add("")
[void]$lines.Add("| Category | Documents |")
[void]$lines.Add("|:---------|----------:|")

$topDirs = Get-ChildItem -Path $root -Directory | Sort-Object Name
foreach ($dir in $topDirs) {
    $pdfs = Get-ChildItem $dir.FullName -Recurse -Filter "*.pdf" -File
    if ($pdfs.Count -eq 0) { continue }
    $name = if ($categoryNames[$dir.Name]) { $categoryNames[$dir.Name] } else { $dir.Name }
    $anchor = ($name.ToLower() -replace '[^a-z0-9 ]', '' -replace ' ', '-').Trim('-')
    [void]$lines.Add("| [$name](#$anchor) | $($pdfs.Count) docs |")
}
[void]$lines.Add("")
[void]$lines.Add("---")
[void]$lines.Add("")

# Each category
foreach ($dir in $topDirs) {
    $pdfs = Get-ChildItem $dir.FullName -Recurse -Filter "*.pdf" -File
    if ($pdfs.Count -eq 0) { continue }

    $name = if ($categoryNames[$dir.Name]) { $categoryNames[$dir.Name] } else { $dir.Name }
    $sizeMB = [math]::Round(($pdfs | Measure-Object -Property Length -Sum).Sum / 1MB, 1)

    [void]$lines.Add("## $name")
    [void]$lines.Add("")
    [void]$lines.Add("*$($pdfs.Count) documents - $sizeMB MB*")
    [void]$lines.Add("")

    $subDirs = Get-ChildItem $dir.FullName -Directory | Sort-Object Name
    if ($subDirs.Count -gt 0) {
        foreach ($sub in $subDirs) {
            $subPdfs = Get-ChildItem $sub.FullName -Filter "*.pdf" -File | Sort-Object Name
            if ($subPdfs.Count -eq 0) { continue }

            $subName = $sub.Name -replace '_', ' '
            [void]$lines.Add("### $subName")
            [void]$lines.Add("")
            [void]$lines.Add("| Publication | Document | Size |")
            [void]$lines.Add("|:------------|:---------|-----:|")

            foreach ($pdf in $subPdfs) {
                $parts = $pdf.BaseName -split ' - ', 3
                $pubNum = if ($parts.Count -ge 1) { $parts[0].Trim() } else { "" }
                if ($parts.Count -ge 3) {
                    $desc = "$($parts[1].Trim()) - $($parts[2].Trim())"
                }
                elseif ($parts.Count -ge 2) {
                    $desc = $parts[1].Trim()
                }
                else {
                    $desc = $pdf.BaseName
                }
                $fsize = "$([math]::Round($pdf.Length/1MB,1)) MB"
                [void]$lines.Add("| ``$pubNum`` | $desc | $fsize |")
            }
            [void]$lines.Add("")
        }
    }

    [void]$lines.Add("---")
    [void]$lines.Add("")
}

# Footer
[void]$lines.Add("## Notes")
[void]$lines.Add("")
[void]$lines.Add("- All documents sourced from [Rockwell Automation Literature Library](https://literature.rockwellautomation.com)")
[void]$lines.Add("- Publication numbers follow Rockwell standard format: ``{Bulletin}-{Type}{Sequence}``")
[void]$lines.Add("- To add new documents, place PDFs in the appropriate folder and push to GitHub (Action will run automatically)")
[void]$lines.Add("- File naming convention: ``{PubNumber} - {Product} - {DocType}.pdf``")

$lines -join "`n" | Out-File -FilePath $indexPath -Encoding utf8 -Force
Write-Host "Index generated: $indexPath"
Write-Host "Cataloged $totalCount documents, $totalSizeMB MB total"
