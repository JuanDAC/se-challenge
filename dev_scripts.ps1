# Variable definitions (similar to Makefile)
$PythonVersion = "3.12"
$VenvName = "venv"
$Pip = "$VenvName/Scripts/pip"
$Python = "$VenvName/Scripts/python"
$Pytest = "$VenvName/Scripts/pytest"
$Uvicorn = "$VenvName/Scripts/uvicorn"
$RequirementsFile = "requirements.txt"
$MainApp = "app:presentation:http:app"
$ProjectHost = "0.0.0.0"
$Port = "8000"

# Create virtual environment
function CreateVenv {
    py -m venv $VenvName
}

# Activate virtual environment
function ActivateVenv {
    Write-Host "Activate the virtual environment with: .\$VenvName\Scripts\Activate.ps1" -ForegroundColor Yellow
    Set-Clipboard ".\$VenvName\Scripts\Activate.ps1"
    Write-Host "Activation script has been copied to clipboard." -ForegroundColor Green
    exit
}

# Install dependencies
function InstallDependencies {
    & $Pip install -r $RequirementsFile
}

# Freeze dependencies
function FreezeDependencies {
    & $Pip freeze > $RequirementsFile
}

# Run in development
function RunDev {
    & $Uvicorn $MainApp --host $ProjectHost --port $Port --reload
}

# Run in production
function RunProd {
    & $Uvicorn $MainApp --host $ProjectHost --port $Port
}

# Run tests
function RunTests {
    & $Pytest
}

# Run tests with coverage
function RunTestsWithCoverage {
    & $Pytest --cov=. --cov-report term-missing
}

# Format code
function FormatCode {
    pip install --upgrade black
    & black . --exclude $VenvName
}

# Lint code
function LintCode {
    pip install --upgrade flake8
    & flake8 . --exclude=$VenvName
}

# Run formatting and linting
function CheckCode {
    FormatCode
    LintCode
}

# Clean project
function CleanProject {
    Write-Host "Cleaning temporary and junk files..." -ForegroundColor Yellow
    Get-ChildItem -Path . -Recurse -Filter "__pycache__" | Remove-Item -Force -Recurse
    Get-ChildItem -Path . -Recurse -Filter "*.pyc" | Remove-Item -Force
    Get-ChildItem -Path . -Recurse -Filter "*.log" | Remove-Item -Force
    Remove-Item -Path ".\.pytest_cache" -Force -Recurse -ErrorAction Ignore
    Remove-Item -Path ".\$VenvName" -Force -Recurse -ErrorAction Ignore
    Write-Host "Cleanup completed." -ForegroundColor Green
}

# Terraform tasks (examples)
function TerraformInit {
    terraform init
}

function TerraformPlan {
    terraform plan
}

function TerraformApply {
    terraform apply -auto-approve
}

function TerraformDestroy {
    terraform destroy -auto-approve
}

# Interactive menu (optional, but useful)
while ($true) {
    Write-Host "`nSelect an action:"
    Write-Host "1. Create virtual environment"
    Write-Host "2. Activate virtual environment"
    Write-Host "3. Install dependencies"
    Write-Host "4. Freeze dependencies"
    Write-Host "5. Run in development"
    Write-Host "6. Run in production"
    Write-Host "7. Run tests"
    Write-Host "8. Run tests with coverage"
    Write-Host "9. Format code"
    Write-Host "10. Lint code"
    Write-Host "11. Run formatting and linting"
    Write-Host "12. Clean project"
    Write-Host "13. Terraform Init"
    Write-Host "14. Terraform Plan"
    Write-Host "15. Terraform Apply"
    Write-Host "16. Terraform Destroy"
    Write-Host "q. Quit"

    $selection = $(Read-Host "Enter the action number").Trim().ToLower()

    switch ($selection) {
        "1" { CreateVenv }
        "2" { ActivateVenv }
        "3" { InstallDependencies }
        "4" { FreezeDependencies }
        "5" { RunDev }
        "6" { RunProd }
        "7" { RunTests }
        "8" { RunTestsWithCoverage }
        "9" { FormatCode }
        "10" { LintCode }
        "11" { CheckCode }
        "12" { CleanProject }
        "13" { TerraformInit }
        "14" { TerraformPlan }
        "15" { TerraformApply }
        "16" { TerraformDestroy }
        "q" { Write-Host "Exiting..." -ForegroundColor Green; exit }
        default { Write-Host "Invalid option." -ForegroundColor Red }
    }
}