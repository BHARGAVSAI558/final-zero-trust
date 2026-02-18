@echo off
echo ========================================
echo ZERO TRUST - REAL DEVICE COLLECTOR
echo ========================================

set USERNAME=%1
if "%USERNAME%"=="" (
    set /p USERNAME="Enter username: "
)

echo Collecting real device information...

:: Get MAC Address
for /f "tokens=2 delims=:" %%a in ('ipconfig /all ^| findstr /c:"Physical Address"') do (
    set MAC=%%a
    goto :mac_done
)
:mac_done
set MAC=%MAC:~1%

:: Get WiFi SSID
for /f "tokens=2 delims=:" %%a in ('netsh wlan show interfaces ^| findstr "SSID"') do (
    set WIFI=%%a
    goto :wifi_done
)
:wifi_done
set WIFI=%WIFI:~1%

:: Get Hostname
set HOSTNAME=%COMPUTERNAME%

:: Get Local IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr "IPv4"') do (
    set LOCALIP=%%a
    goto :ip_done
)
:ip_done
set LOCALIP=%LOCALIP:~1%

echo.
echo MAC Address: %MAC%
echo WiFi SSID: %WIFI%
echo Hostname: %HOSTNAME%
echo Local IP: %LOCALIP%
echo.

:: Send to backend
curl -X POST http://localhost:8000/device/register ^
  -H "Content-Type: application/json" ^
  -d "{\"username\":\"%USERNAME%\",\"device_id\":\"%HOSTNAME%\",\"mac_address\":\"%MAC%\",\"os\":\"Windows\",\"wifi_ssid\":\"%WIFI%\",\"hostname\":\"%HOSTNAME%\",\"ip_address\":\"%LOCALIP%\"}"

echo.
echo Device registered successfully!
pause
