# BSOD and Crash Diagnosis Script
# Author: Gemini
# Function: Scrapes System Event Logs for Critical Failures and BugChecks

Clear-Host
Write-Host "Gathering Crash Data... Please wait." -ForegroundColor Cyan

# 1. Define the timeframe (Look back 30 days)
$StartDate = (Get-Date).AddDays(-30)

# 2. Search for BugCheck Events (Event ID 1001 in System Log often holds the BSOD info)
$BSODs = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ProviderName='Microsoft-Windows-WER-SystemErrorReporting'
    ID=1001
} -ErrorAction SilentlyContinue | Where-Object {$_.TimeCreated -ge $StartDate}

# 3. Search for WHEA-Logger Events (Hardware Errors - CPU/PCIe)
$HardwareErrors = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ProviderName='Microsoft-Windows-WHEA-Logger'
} -ErrorAction SilentlyContinue | Where-Object {$_.TimeCreated -ge $StartDate}

# 4. Search for Unexpected Shutdowns (Event 41)
$UnexpectedShutdowns = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ID=41
} -ErrorAction SilentlyContinue | Where-Object {$_.TimeCreated -ge $StartDate}

# --- OUTPUT SECTION ---

Write-Host "`n--------------------------------------------------" -ForegroundColor Yellow
Write-Host "CRASH REPORT (Last 30 Days)" -ForegroundColor Yellow
Write-Host "--------------------------------------------------"
Write-Host "Total Unexpected Shutdowns: " -NoNewline; Write-Host $UnexpectedShutdowns.Count -ForegroundColor Red
Write-Host "Total Confirmed BSOD Logs:  " -NoNewline; Write-Host $BSODs.Count -ForegroundColor Red
Write-Host "Total Hardware (WHEA) errs: " -NoNewline; Write-Host $HardwareErrors.Count -ForegroundColor Red

if ($HardwareErrors.Count -gt 0) {
    Write-Host "`n[!] CRITICAL HARDWARE ERRORS DETECTED [!]" -ForegroundColor Red
    Write-Host "WHEA errors usually indicate CPU voltage issues or overheating."
    $HardwareErrors | Select-Object -First 5 TimeCreated, Message | Format-Table -AutoSize
}

if ($BSODs.Count -gt 0) {
    Write-Host "`n--- Recent BSOD Details ---" -ForegroundColor Cyan
    # Process the BSOD messages to make them readable
    $Report = @()
    foreach ($err in $BSODs) {
        # Try to extract the BugCheck code from the raw data if possible, otherwise use message
        $Report += [PSCustomObject]@{
            Time = $err.TimeCreated
            Message = $err.Message.Split(".")[0] # Grab the first sentence usually containing the code
        }
    }
    $Report | Select-Object -First 10 | Format-Table -AutoSize
} else {
    Write-Host "`nNo explicit BugCheck logs found via WER (Windows might be crashing too fast to log)." -ForegroundColor Gray
}

Write-Host "`n--------------------------------------------------"
Write-Host "RECOMMENDATION:" -ForegroundColor Green
if ($HardwareErrors.Count -gt 0) {
    Write-Host "Focus on CPU/GPU hardware. Remove Overclocks/XMP."
} elseif ($BSODs.Count -gt 0) {
    Write-Host "Focus on Drivers and Storage System integrity."
} else {
    Write-Host "If counts are low but crashes are high, the PSU might be cutting power before logs are written."
}
Write-Host "--------------------------------------------------"