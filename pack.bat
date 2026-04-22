@echo off
chcp 65001 >nul
echo ========================================
echo        开始打包全栈项目
echo ========================================

echo.
echo [1/4] 清理 Python __pycache__...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
echo       ✅ Python 缓存清理完成

echo.
echo [2/4] 打包前端 Vue 项目...
cd web
call npm run build
cd ..
echo       ✅ 前端打包完成

echo.
echo [3/4] 确认 dist 目录...
if not exist "dist" (
    if exist "web\dist" (
        xcopy /E /I /Y "web\dist" "dist"
        echo       ✅ 已复制 dist 目录
    ) else (
        echo       ❌ dist 目录不存在，请检查前端打包
        pause
        exit /b 1
    )
)

echo.
echo [4/4] 压缩项目文件...
powershell -Command "Compress-Archive -Path app, templates, dist, docker-compose.yml, Dockerfile.backend, Dockerfile.frontend, nginx.conf, .env.production, requirements.txt -DestinationPath ai-test.zip -Force"
echo       ✅ 压缩完成: ai-test.zip

echo.
echo ========================================
echo       ✅ 打包完成！
echo ========================================
pause