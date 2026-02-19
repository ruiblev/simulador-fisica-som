@echo off
setlocal

:: Try to find Python
set PYTHON_EXE=python
where python >nul 2>nul
if %errorlevel% neq 0 (
    where py >nul 2>nul
    if %errorlevel% eq 0 (
        set PYTHON_EXE=py
    ) else (
        echo Python nao foi encontrado. Por favor, instala o Python antes de continuar.
        pause
        exit /b
    )
)

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo A criar ambiente virtual...
    %PYTHON_EXE% -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate

:: Install requirements
echo A instalar dependencias (isto pode demorar um pouco na primeira vez)...
python -m pip install -r requirements.txt --quiet

:: Run the app
echo A iniciar o simulador...
python -m streamlit run app.py

pause
