param(
    [string]$username = "admin"
)

Write-Host "========================================"
Write-Host "ZERO TRUST - REAL DEVICE COLLECTOR"
Write-Host "========================================"

# Get MAC Address
$mac = (Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object -First 1).MacAddress

# Get WiFi SSID
$wifi = (netsh wlan show interfaces | Select-String "SSID" | Select-Object -First 1).ToString().Split(":")[1].Trim()

# Get Hostname
$hostname = $env:COMPUTERNAME

# Get Local IP
$localip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*Wi-Fi*"}).IPAddress

# Get OS
$os = (Get-CimInstance Win32_OperatingSystem).Caption

Write-Host ""
Write-Host "MAC Address: $mac"
Write-Host "WiFi SSID: $wifi"
Write-Host "Hostname: $hostname"
Write-Host "Local IP: $localip"
Write-Host "OS: $os"
Write-Host ""

# Send to backend
$body = @{
    username = $username
    device_id = $hostname
    mac_address = $mac
    os = $os
    wifi_ssid = $wifi
    hostname = $hostname
    ip_address = $localip
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/device/register" -Method Post -Body $body -ContentType "application/json"

Write-Host ""
Write-Host "Device registered successfully!"
