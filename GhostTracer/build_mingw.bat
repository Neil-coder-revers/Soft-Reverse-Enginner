@echo off
echo [GhostTracer] MinGW Build initiated...

set PATH=C:\Users\jack\Downloads\w64devkit\bin;%PATH%

:: Check if g++ is available
where g++ >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] MinGW Compiler 'g++' not found in PATH.
    echo Please ensure MinGW-w64 is installed and added to your PATH.
    pause
    exit /b
)

:: Compile C++ and Assembly (GAS syntax)
:: -static to avoid dependency constraints
echo [GCC] Compiling sources...
g++ -o GhostTracer.exe src/main.cpp src/debugger.cpp src/utils.s -static -std=c++17 -Wall

if %errorlevel% neq 0 (
    echo [ERROR] Compilation failed.
    pause
    exit /b
)

echo [SUCCESS] Build complete! Run GhostTracer.exe
pause
