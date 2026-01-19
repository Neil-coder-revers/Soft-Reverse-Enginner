#include "debugger.h"
#include <sstream>

GhostDebugger::GhostDebugger() : hProcess(NULL), targetPid(0), isRunning(false) {}

GhostDebugger::~GhostDebugger() {
    if (hProcess) {
        CloseHandle(hProcess);
    }
}

bool GhostDebugger::Attach(DWORD pid) {
    if (!DebugActiveProcess(pid)) {
        std::cerr << "[-] Failed to attach to process " << pid << ". Error: " << GetLastError() << std::endl;
        return false;
    }
    targetPid = pid;
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, pid);
    std::cout << "[+] Attached to process " << pid << std::endl;
    return true;
}

bool GhostDebugger::Launch(const std::wstring& path) {
    STARTUPINFOW si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };

    if (!CreateProcessW(path.c_str(), NULL, NULL, NULL, FALSE, DEBUG_ONLY_THIS_PROCESS, NULL, NULL, &si, &pi)) {
        std::cerr << "[-] Failed to launch process. Error: " << GetLastError() << std::endl;
        return false;
    }

    targetPid = pi.dwProcessId;
    hProcess = pi.hProcess;
    CloseHandle(pi.hThread);
    std::wcout << "[+] Launched process: " << path << " (PID: " << targetPid << ")" << std::endl;
    return true;
}

void GhostDebugger::Run() {
    DEBUG_EVENT debugEvent = { 0 };
    isRunning = true;

    while (isRunning) {
        if (!WaitForDebugEvent(&debugEvent, INFINITE)) {
            break;
        }

        HandleDebugEvent(debugEvent);
        ContinueDebugEvent(debugEvent.dwProcessId, debugEvent.dwThreadId, DBG_CONTINUE);
    }
}

void GhostDebugger::HandleDebugEvent(const DEBUG_EVENT& debugEvent) {
    switch (debugEvent.dwDebugEventCode) {
        case EXCEPTION_DEBUG_EVENT:
            OnException(debugEvent.dwThreadId, debugEvent.u.Exception);
            break;
        case CREATE_PROCESS_DEBUG_EVENT:
            OnProcessCreate(debugEvent.u.CreateProcessInfo);
            break;
        case EXIT_PROCESS_DEBUG_EVENT:
            OnProcessExit(debugEvent.u.ExitProcess);
            break;
    }
}

void GhostDebugger::OnException(DWORD threadId, const EXCEPTION_DEBUG_INFO& exceptionInfo) {
    std::cout << "[!] Exception Code: 0x" << std::hex << exceptionInfo.ExceptionRecord.ExceptionCode 
              << " at Address: 0x" << exceptionInfo.ExceptionRecord.ExceptionAddress << std::endl;

    if (exceptionInfo.ExceptionRecord.ExceptionCode == EXCEPTION_BREAKPOINT) {
        std::cout << "[*] Breakpoint hit!" << std::endl;
        DumpRegisters(threadId);
    }
}

void GhostDebugger::OnProcessCreate(const CREATE_PROCESS_DEBUG_INFO& createProcessInfo) {
    std::cout << "[*] Process Created. Base Address: 0x" << std::hex << createProcessInfo.lpBaseOfImage << std::endl;
    if (createProcessInfo.hFile) CloseHandle(createProcessInfo.hFile);
}

void GhostDebugger::OnProcessExit(const EXIT_PROCESS_DEBUG_INFO& exitProcessInfo) {
    std::cout << "[*] Process Exited with Code: " << std::dec << exitProcessInfo.dwExitCode << std::endl;
    isRunning = false;
}

void GhostDebugger::DumpRegisters(DWORD threadId) {
    HANDLE hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, threadId);
    if (!hThread) return;

    CONTEXT ctx = { 0 };
    ctx.ContextFlags = CONTEXT_ALL;
    
    if (GetThreadContext(hThread, &ctx)) {
        std::cout << "\n    --- CPU CONTEXT (Thread: " << std::dec << threadId << ") ---" << std::endl;
        std::cout << std::hex << std::uppercase;
        std::cout << "    RAX: " << std::setw(16) << std::setfill('0') << ctx.Rax << "  RBX: " << std::setw(16) << ctx.Rbx << std::endl;
        std::cout << "    RCX: " << std::setw(16) << ctx.Rcx << "  RDX: " << std::setw(16) << ctx.Rdx << std::endl;
        std::cout << "    RSI: " << std::setw(16) << ctx.Rsi << "  RDI: " << std::setw(16) << ctx.Rdi << std::endl;
        std::cout << "    RBP: " << std::setw(16) << ctx.Rbp << "  RSP: " << std::setw(16) << ctx.Rsp << std::endl;
        std::cout << "    RIP: " << std::setw(16) << ctx.Rip << "  EFLAGS: " << std::setw(8) << ctx.EFlags << std::endl;
        std::cout << "    --------------------------------------------\n" << std::endl;
    }

    CloseHandle(hThread);
}

void GhostDebugger::ReadMemory(HANDLE hProcess, LPCVOID address, size_t size) {
}
