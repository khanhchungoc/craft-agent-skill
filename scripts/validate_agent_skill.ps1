# Compatibility entrypoint. Validation rules and CLI help live in validate_agent_skill.py.
$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot 'validate_agent_skill.py'
$pythonCommand = $null
foreach ($candidate in @('python', 'python3', 'py')) {
    $pythonCommand = Get-Command $candidate -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($pythonCommand) { break }
}
if (-not $pythonCommand) {
    [Console]::Error.WriteLine('Python 3.10+ is required. Install Python and the dependency declared in scripts/requirements.txt.')
    exit 2
}
if ($pythonCommand.Name -match '^py(?:\.exe)?$') {
    & $pythonCommand.Source -3 $validator @args
} else {
    & $pythonCommand.Source $validator @args
}
exit $LASTEXITCODE
