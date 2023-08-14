@echo off

if not exist "%~dp0\venv\Scripts" (
    echo Creating venv...
    python -m venv venv
)

echo Checked the venv folder. Now installing requirements..
cd /d "%~dp0\venv\Scripts"
call activate.bat

cd /d "%~dp0"
pip install torch torchvision torchaudio
pip install git+https://github.com/m-bain/whisperx.git
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo Requirements installation failed. Please remove venv folder and run install.bat again.
) else (
    echo.
    echo Requirements installed successfully.
)
pause