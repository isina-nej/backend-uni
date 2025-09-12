@echo off
REM Windows batch script for PythonAnywhere deployment preparation
REM اسکریپت آماده‌سازی برای استقرار در PythonAnywhere

echo 🚀 Preparing project for PythonAnywhere deployment...

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo 📚 Installing requirements...
pip install -r requirements_pythonanywhere.txt

REM Generate new secret key
echo 🔐 Generating new secret key...
python generate_secret_key.py > secret_key.txt

echo ✅ Project prepared for PythonAnywhere deployment!
echo.
echo 📝 Next steps:
echo    1. Upload project files to PythonAnywhere
echo    2. Update .env.pythonanywhere with your actual values
echo    3. Follow the deployment guide in PYTHONANYWHERE_DEPLOYMENT_GUIDE.md
echo.
echo 🔑 Your new secret key is saved in secret_key.txt
echo    Copy this to your .env.pythonanywhere file

pause
