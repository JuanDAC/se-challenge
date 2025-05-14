# Definiciones de variables (similares al Makefile)
$PythonVersion = "3.12"
$VenvName = "venv"
$Pip = "$VenvName/Scripts/pip"
$Python = "$VenvName/Scripts/python"
$Pytest = "$VenvName/Scripts/pytest"
$Uvicorn = "$VenvName/Scripts/uvicorn"
$RequirementsFile = "requirements.txt"
$MainApp = "main:app"
$ProjectHost = "0.0.0.0"
$Port = "8000"

# Crear el entorno virtual
function CreateVenv {
    py -m venv $VenvName
}

# Activar el entorno virtual
function ActivateVenv {
    Write-Host "Activa el entorno virtual con: .$VenvName/Scripts/Activate.ps1" -ForegroundColor Yellow
    Set-Clipboard ".\$VenvName\Scripts\Activate.ps1"
    Write-Host "El script de activación ha sido copiado al portapapeles." -ForegroundColor Green
    exit
}

# Instalar las dependencias
function InstallDependencies {
    & $Pip install -r $RequirementsFile
}

# Volcar las dependencias
function FreezeDependencies {
    & $Pip freeze > $RequirementsFile
}

# Ejecutar en desarrollo
function RunDev {
    & $Uvicorn $MainApp --host $ProjectHost --port $Port --reload
}

# Ejecutar en producción
function RunProd {
    & $Uvicorn $MainApp --host $ProjectHost --port $Port
}

# Ejecutar pruebas
function RunTests {
    & $Pytest
}

# Ejecutar pruebas con cobertura
function RunTestsWithCoverage {
    & $Pytest --cov=. --cov-report term-missing
}

# Formatear código
function FormatCode {
    pip install --upgrade black
    & black .
}

# Analizar código
function LintCode {
    pip install --upgrade flake8
    & flake8 .
}

# Ejecutar formateo y linting
function CheckCode {
    FormatCode
    LintCode
}

# Tareas de Terraform (ejemplos)
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

# Menú interactivo (opcional, pero útil)
while ($true) {
    Write-Host "`nSelecciona una acción:"
    Write-Host "1. Crear entorno virtual"
    Write-Host "2. Activar entorno virtual"
    Write-Host "3. Instalar dependencias"
    Write-Host "4. Volcar dependencias"
    Write-Host "5. Ejecutar en desarrollo"
    Write-Host "6. Ejecutar en producción"
    Write-Host "7. Ejecutar pruebas"
    Write-Host "8. Ejecutar pruebas con cobertura"
    Write-Host "9. Formatear código"
    Write-Host "10. Analizar código"
    Write-Host "11. Ejecutar formateo y linting"
    Write-Host "12. Terraform Init"
    Write-Host "13. Terraform Plan"
    Write-Host "14. Terraform Apply"
    Write-Host "15. Terraform Destroy"
    Write-Host "q. Salir"

    $selection = Read-Host "Ingresa el número de la acción"

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
        "12" { TerraformInit }
        "13" { TerraformPlan }
        "14" { TerraformApply }
        "15" { TerraformDestroy }
        "q" { Write-Host "Saliendo..." -ForegroundColor Green; exit }
        default { Write-Host "Opción inválida." -ForegroundColor Red }
    }
}