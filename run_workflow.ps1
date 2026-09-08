param(
    [Parameter(Position = 0)]
    [string]$Requirement
)

if ([string]::IsNullOrWhiteSpace($Requirement)) {
    $Requirement = Read-Host "Hvad skal systemet kunne?"
}

python .\ollama_workflow.py $Requirement