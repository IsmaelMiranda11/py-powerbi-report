[Console]::OutputEncoding = [Text.Encoding]::Utf8

$pbis_count = 0

$pbis = get-process -ProcessName PBIDesktop | Select-Object Id, MainWindowTitle

$pbis | ForEach-Object -Process {$pbis_count++}

$pbis_json = $pbis | ConvertTo-Json

$as_json = Get-CimInstance -Query "SELECT * from Win32_Process WHERE name LIKE 'msmdsrv%'" | Select-Object ParentProcessId, CommandLine | ConvertTo-Json

if ( $pbis_count -eq 0 )
    {
        Write-Host ''
}else {
    if ( $pbis_count -eq 1 ){
            Write-Host "{" '"PBI"': [$pbis_json] "," '"AS"' : [$as_json]  "}" 
        }else
        {
            Write-Host "{" '"PBI"': $pbis_json "," '"AS"' : $as_json  "}"
        }
}
