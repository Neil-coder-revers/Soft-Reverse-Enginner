#include <iostream>
#include <string>
#include <vector>
#include "debugger.h"

void PrintBanner() {
    std::cout << "\n"
              << "   .d8888b.  888                        888    88888888888                                   \n"
              << "  d88P  Y88b 888                        888        888                                       \n"
              << "  888    888 888                        888        888                                       \n"
              << "  888        88888b.   .d88b.  .d8888b  888888     888  888d888  8888b.   .d8888b  .d88b.  888d888 \n"
              << "  888  88888 888 \"88b d88\"\"88b 88K      888        888  888P\"       \"88b d88P\"    d88P\"88b 888P\"   \n"
              << "  888    888 888  888 888  888 \"Y8888b. 888        888  888     .d888888 888      888  888 888     \n"
              << "  Y88b  d88P 888  888 Y88..88P      X88 Y88b.      888  888     888  888 Y88b.    Y88..88P 888     \n"
              << "   \"Y8888P88 888  888  \"Y88P\"   88888P'  \"Y888     888  888     \"Y888888  \"Y8888P  \"Y88P\"  888     \n"
              << "                                                                                                 \n"
              << "       >> Advanced x64 Windows Debugger | v1.0.0 <<\n"
              << "       >> Author: Neil | Target: Windows x64\n"
              << std::endl;
}

void PrintUsage() {
    std::cout << "Usage:\n"
              << "  GhostTracer.exe --attach <PID>\n"
              << "  GhostTracer.exe --launch <PathToExe>\n"
              << std::endl;
}

int main(int argc, char* argv[]) {
    PrintBanner();

    int cpuInfo[4] = {0};
    GhostUtils_GetCpuInfo(cpuInfo);
    std::cout << "[INFO] CPU Check via ASM: ";
    if (cpuInfo[0] != 0 || cpuInfo[1] != 0) {
        std::cout << "Success (CPUID executed)" << std::endl;
    } else {
        std::cout << "Failed" << std::endl;
    }

    if (argc < 3) {
        PrintUsage();
        return 0;
    }

    GhostDebugger dbg;
    std::string command = argv[1];
    std::string argument = argv[2];

    if (command == "--attach") {
        try {
            DWORD pid = std::stoul(argument);
            if (dbg.Attach(pid)) {
                dbg.Run();
            }
        } catch (...) {
            std::cerr << "[-] Invalid PID format." << std::endl;
        }
    } else if (command == "--launch") {
        std::wstring wPath(argument.begin(), argument.end());
        if (dbg.Launch(wPath)) {
            dbg.Run();
        }
    } else {
        PrintUsage();
    }

    return 0;
}
