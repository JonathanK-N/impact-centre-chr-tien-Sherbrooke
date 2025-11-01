@echo off
echo Building frontend locally...
cd frontend
npm run build
cd ..

echo Copying frontend to backend...
xcopy frontend\dist\* backend\app\static\frontend\ /E /Y

echo Frontend integrated successfully!
echo Now deploy with Railway/Docker

echo.
echo Files ready for deployment:
echo - backend/ (Flask API + integrated frontend)
echo - Dockerfile (Ultra-simple)
echo.
echo Deploy command: railway up
pause