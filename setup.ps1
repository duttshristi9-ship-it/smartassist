$ErrorActionPreference = "Stop"

Write-Host "Setting up SmartAssist Virtual Environment..."
# Check if venv exists
if (Test-Path -Path "venv") {
    Write-Host "Removing old venv..."
    Remove-Item -Recurse -Force venv
}

Write-Host "Creating Python 3.12 virtual environment..."
C:\Users\shant\AppData\Local\Programs\Python\Python312\python.exe -m venv venv

Write-Host "Upgrading pip..."
.\venv\Scripts\python.exe -m pip install --upgrade pip

Write-Host "Installing requirements..."
.\venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Downloading spaCy English model..."
.\venv\Scripts\python.exe -m spacy download en_core_web_sm

Write-Host "Setup complete. You can now run the app with '.\venv\Scripts\python.exe app.py'"
Write-Host "Running the application..."
.\venv\Scripts\python.exe app.py
