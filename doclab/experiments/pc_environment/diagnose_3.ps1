# WER Crash Report Analyzer
# Author: Gemini
# Function: Parses Windows Error Reporting text logs for crash signatures

Clear-Host
Write-Host "Searching Windows Error Reporting (WER) Archives..." -ForegroundColor Cyan

# Path where Windows stores crash reports
$WerPath = "C:\ProgramData\Microsoft\Windows\WER\ReportArchive"

# Get folders modified in the last 7 days that are likely System Crashes (Kernel)
$CrashFolders = Get-ChildItem -Path $WerPath -Filter "Kernel_*" -Directory | Where-Object { $_.LastWriteTime -ge (Get-Date).AddDays(-7) } | Sort-Object LastWriteTime -Descending

$ReportList = @()

foreach ($folder in $CrashFolders) {
    $ReportFile = Join-Path $folder.FullName "Report.wer"
    
    if (Test-Path $ReportFile) {
        # Read the file as text
        $Content = Get-Content $ReportFile
        
        # Extract meaningful lines
        $EventTime = $folder.LastWriteTime.ToString("MM/dd HH:mm")
        $BugCheck = ($Content | Where-Object { $_ -like "*Sig[0].Value*" } | Select-Object -First 1) -replace ".*=",""
        $Param1   = ($Content | Where-Object { $_ -like "*Sig[1].Value*" } | Select-Object -First 1) -replace ".*=",""
        $FaultingModule = ($Content | Where-Object { $_ -like "*Sig[3].Value*" } | Select-Object -First 1) -replace ".*=",""
        
        # If Sig[3] is empty, sometimes the fault is hidden in the dynamic signatures
        if ([string]::IsNullOrWhiteSpace($FaultingModule)) {
             $FaultingModule = "Unknown (Kernel)"
        }

        $ReportList += [PSCustomObject]@{
            Time = $EventTime
            Code = $BugCheck
            Fault = $FaultingModule
        }
    }
}

if ($ReportList.Count -gt 0) {
    Write-Host "`nCRASH SIGNATURES FOUND:" -ForegroundColor Yellow
    $ReportList | Format-Table -AutoSize
} else {
    Write-Host "`nNo 'Kernel' crash reports found in WER Archive." -ForegroundColor Gray
    Write-Host "Windows might be failing before it can generate the text report."
}

Write-Host "`n--------------------------------------------------"
Write-Host "INTERPRETATION:"
Write-Host "If 'Fault' varies wildly (ntfs.sys, fltmgr.sys, ntoskrnl.exe) -> HARDWARE (RAM/CPU)."
Write-Host "If 'Fault' is always the same (e.g., nvlddmkm.sys) -> DRIVER."
Write-Host "--------------------------------------------------"