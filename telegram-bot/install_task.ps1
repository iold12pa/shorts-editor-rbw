# Dang ky bot Telegram chay nen ben vung qua Windows Task Scheduler:
# tu khoi dong khi Sep dang nhap Windows, tu khoi dong lai neu bi treo/loi.
#
# CHUA TU CHAY - Sep tu chay file nay 1 lan khi san sang (sau khi da lam
# xong Buoc 0 + Buoc 1 trong README.md va thu "python bot.py" bang tay
# chay on dinh roi). Chay bang cach: click phai file nay -> Run with
# PowerShell, hoac mo PowerShell roi go:  .\install_task.ps1

$ErrorActionPreference = "Stop"
$botDir = $PSScriptRoot
$pythonExe = (Get-Command python).Source
$logFile = Join-Path $botDir "bot.log"
$taskName = "RoboworldShortsBot"

$argList = '"' + (Join-Path $botDir "bot.py") + '"'
$action = New-ScheduledTaskAction -Execute $pythonExe -Argument $argList -WorkingDirectory $botDir
$trigger = New-ScheduledTaskTrigger -AtLogOn
$settings = New-ScheduledTaskSettingsSet -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit (New-TimeSpan -Days 0) -DontStopOnIdleEnd

Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Settings $settings -Description "Bot Telegram Shorts Editor Roboworld - tu dong chay khi dang nhap, tu khoi dong lai neu loi" -Force

Write-Host "Da dang ky xong. Bot se tu chay lan dang nhap Windows tiep theo."
Write-Host "Muon chay thu NGAY khong doi dang nhap lai:"
Write-Host "  Start-ScheduledTask -TaskName $taskName"
Write-Host "Xem trang thai:"
Write-Host "  Get-ScheduledTask -TaskName $taskName"
Write-Host "Dung/go bo hoan toan (thay <ten-task> bang gia tri o tren):"
Write-Host ('  Unregister-ScheduledTask -TaskName {0} -Confirm:$false' -f $taskName)
Write-Host ""
Write-Host "LUU Y: bot chay bang python.exe se KHONG co cua so console hien ra."
Write-Host "Muon xem log/loi thi tu sua bien argList trong file nay de ghi output ra file log:"
Write-Host "  $logFile"
Write-Host "Hoac don gian nhat: cu mo PowerShell chay 'python bot.py' bang tay khi can theo doi truc tiep."
