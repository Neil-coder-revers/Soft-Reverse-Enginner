@echo off
echo [GhostTracer] Build initiated...

:: Check if cl.exe is available
where cl.exe >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] MSVC Compiler 'cl.exe' not found in PATH.
    echo Please run this script from the "x64 Native Tools Command Prompt for VS".
    pause
    exit /b
)

:: 1. Assemble the ASM file
echo [ASM] Compiling src/utils.asm...
ml64 /c /nologo /Cx /Fo"utils.obj" "src/utils.asm"
if %errorlevel% neq 0 (
    echo [ERROR] ASM Compilation failed.
    pause
    exit /b
)

:: 2. Compile C++ and Link
echo [CPP] Compiling core sources...
cl /nologo /EHsc "src/main.cpp" "src/debugger.cpp" "utils.obj" /Fe"GhostTracer.exe" /link /MACHINE:X64
if %errorlevel% neq 0 (
    echo [ERROR] C++ Compilation failed.
    pause
    exit /b
)

:: Cleanup
del *.obj
echo [SUCCESS] Build complete! Run GhostTracer.exe
pause
