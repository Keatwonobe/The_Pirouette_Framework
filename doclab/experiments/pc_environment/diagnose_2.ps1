# BSOD Deep Dive & Hex Code Extractor
# Author: Gemini
# Function: Extracts raw BugCheck codes and WHEA details

$StartDate = (Get-Date).AddDays(-30)

Write-Host "--------------------------------------------------" -ForegroundColor Yellow
Write-Host "BSOD HEX CODE EXTRACTOR" -ForegroundColor Yellow
Write-Host "--------------------------------------------------"

# 1. Get BSOD Events (ID 1001) and extract the RAW Hex Code
$BSODs = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ProviderName='Microsoft-Windows-WER-SystemErrorReporting'
    ID=1001
} -ErrorAction SilentlyContinue | Where-Object {$_.TimeCreated -ge $StartDate}

$Report = @()

foreach ($err in $BSODs) {
    # The BugCheck code is usually the first property in the raw data
    if ($err.Properties.Count -gt 0) {
        $RawCode = $err.Properties[0].Value
        # Convert the Decimal code to Hex (Standard Windows Format)
        $HexCode = "0x{0:X8}" -f $RawCode
        
        $Report += [PSCustomObject]@{
            Time     = $err.TimeCreated.ToString("MM/dd HH:mm")
            HexCode  = $HexCode
            BugCheck = $err.Properties[1].Value # Often the decimal conversion or param
        }
    }
}

# Output the BSOD Table
if ($Report.Count -gt 0) {
    $Report | Select-Object -First 15 | Format-Table -AutoSize
} else {
    Write-Host "No BugCheck codes found in logs." -ForegroundColor Gray
}

Write-Host "`n--------------------------------------------------" -ForegroundColor Red
Write-Host "WHEA (HARDWARE) ERROR DETAILS" -ForegroundColor Red
Write-Host "--------------------------------------------------"

# 2. Get WHEA details to see WHAT hardware failed (ID 18, 19, 46, 47 are common)
$WHEA = Get-WinEvent -FilterHashtable @{
    LogName='System'
    ProviderName='Microsoft-Windows-WHEA-Logger'
} -ErrorAction SilentlyContinue | Where-Object {$_.TimeCreated -ge $StartDate}

if ($WHEA.Count -gt 0) {
    foreach ($hw in $WHEA) {
        Write-Host "Time: " -NoNewline; Write-Host $hw.TimeCreated.ToString("MM/dd HH:mm") -NoNewline
        Write-Host " | ID: " -NoNewline; Write-Host $hw.Id -NoNewline -ForegroundColor Cyan
        # Try to grab the error source from the message
        $Msg = $hw.Message.Replace("A corrected hardware error has occurred.","").Trim()
        Write-Host " | Detail: $Msg" 
    }
} else {
    Write-Host "No detailed WHEA logs found."
}
Write-Host "--------------------------------------------------"