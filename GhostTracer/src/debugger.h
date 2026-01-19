#pragma once
#include <windows.h>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>

extern "C" void GhostUtils_GetCpuInfo(int* info);

class GhostDebugger {
public:
    GhostDebugger();
    ~GhostDebugger();

    bool Attach(DWORD pid);
    bool Launch(const std::wstring& path);
    void Run();

private:
    void HandleDebugEvent(const DEBUG_EVENT& debugEvent);
    void OnException(DWORD threadId, const EXCEPTION_DEBUG_INFO& exceptionInfo);
    void OnProcessCreate(const CREATE_PROCESS_DEBUG_INFO& createProcessInfo);
    void OnProcessExit(const EXIT_PROCESS_DEBUG_INFO& exitProcessInfo);
    
    void DumpRegisters(DWORD threadId);
    void ReadMemory(HANDLE hProcess, LPCVOID address, size_t size);

    HANDLE hProcess;
    DWORD targetPid;
    bool isRunning;
};
