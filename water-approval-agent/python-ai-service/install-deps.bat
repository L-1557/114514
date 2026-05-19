@echo off
echo ========================================
echo 安装 Python 依赖包
echo ========================================

echo.
echo 正在安装基础依赖...
python -m pip install --user --upgrade pip

echo.
echo 正在安装 FastAPI 和相关依赖...
python -m pip install --user fastapi uvicorn python-multipart pypdf docx2txt pydantic

echo.
echo 安装完成！
pause
