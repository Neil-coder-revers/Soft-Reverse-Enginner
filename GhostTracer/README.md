# GhostTracer 👻
> **Advanced x64 User-Mode Debugger & Process Analyzer**

![Platform](https://img.shields.io/badge/Platform-Windows_x64-0078D6?style=for-the-badge&logo=windows)
![Language](https://img.shields.io/badge/Language-C++17_%7C_MASM-yellow?style=for-the-badge&logo=c%2B%2B)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**GhostTracer** is a lightweight, high-performance debugger built from scratch for Windows x64. It demonstrates low-level system interaction using direct **Windows API** calls and **Assembly (MASM)** integration for high-speed context switching verification. Designed for malware analysis and reverse engineering tasks.

## 🚀 Features
- **Flash Attach**: Instant attachment to running processes via PID.
- **Context Awareness**: Full x64 CPU register dumping (`RIP`, `RAX`... `R15`, `EFLAGS`) upon exception.
- **Hybrid Core**: C++ logic engine mixed with pure x64 Assembly routines for CPU feature detection.
- **Event Interception**: Hooks into `EXCEPTION_DEBUG_EVENT`, `CREATE_PROCESS`, and `EXIT_PROCESS`.
- **Memory Inspector**: *(In Progress)* Real-time hex dump of the target process virtual memory.

## 🛠️ Tech Stack & Internals
This project avoids high-level wrappers to interact directly with the OS kernel:
*   **Debug Loop**: Implements the `WaitForDebugEvent` / `ContinueDebugEvent` cycle manually.
*   **WinAPI**: Uses `OpenThread`, `GetThreadContext`, `ReadProcessMemory`.
*   **MASM x64**: Contains raw assembly modules for specialized CPU operations.

## 📦 Build & Run

### Prerequisites
*   Visual Studio (MSVC) with C++ Desktop Development workload.
*   x64 Native Tools Command Prompt.

### Compilation
Simply run the automatic build script:
```cmd
build.bat
```

### Usage
```powershell
# Attach to a running process
GhostTracer.exe --attach 1337

# Launch a new executable under the debugger
GhostTracer.exe --launch "C:\Windows\System32\notepad.exe"
```

## 📸 Demo
*(Screenshot of the CLI interface showing a breakpoint hit and register dump)*

## ⚠️ Disclaimer
This tool is for educational purposes and cybersecurity research only. 

---
*Built with 💀 and C++ by Neil*
