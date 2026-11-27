$ErrorActionPreference = "Stop"

$ReportDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$LocalTectonic = Join-Path $ReportDir ".tools\tectonic\tectonic.exe"
$BuildDir = Join-Path $ReportDir "build"
$MainFile = Join-Path $ReportDir "main.tex"

New-Item -ItemType Directory -Path $BuildDir -Force | Out-Null

if (Test-Path -LiteralPath $LocalTectonic) {
    $Tectonic = $LocalTectonic
}
else {
    $Tectonic = "tectonic"
}

& $Tectonic -X compile $MainFile --outdir $BuildDir --keep-logs
if ($LASTEXITCODE -ne 0) {
    throw "Tectonic failed with exit code $LASTEXITCODE"
}

Write-Output "Built: $BuildDir\main.pdf"
