@echo off
echo Building frontend locally...
cd frontend
npm run build
cd ..

echo Frontend built successfully!
echo Now deploy with Railway/Docker

echo.
echo Files ready for deployment:
echo - backend/ (Flask API)
echo - frontend/dist/ (Built React app)
echo - Dockerfile (Simple backend-only)
echo.
echo Deploy command: railway up
pause