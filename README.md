# Reverse Engineering 

**Author:** Neil
**Focus:** Malware Analysis, Tool Development, Low-Level Research (C++/Python/ASM)

---

## 🇺🇸 English Version

This repository contains my personal research tools for Windows binary analysis and debugging.

### 📂 Project 1: VortexLogic
**Advanced Static PE Analyzer** (Python 3 + CustomTkinter)

A professional GUI tool for inspecting Windows Executables (`.exe`, `.dll`) without running them. Features a custom "Hacker-Style" UI, entropy visualization for packer detection, and a built-in disassembler.

#### 📥 Installation
1.  Ensure you have **Python 3.10+** installed.
2.  Open a terminal in the `VortexLogic` folder.
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

#### 🚀 How to Run
```bash
python main.py
```
*Wait for the "System Initialization" splash screen to finish.*

#### 📖 Usage
*   **Load Binary:** Click the large "LOAD BINARY" button or drag-and-drop a file.
*   **Dashboard:** View file metadata (MD5, Timestamp, EntryPoint).
*   **Sections:** Check the "Entropy" bars. Red bars (> 7.0) indicate packed or encrypted code (suspicious).
*   **Code View:** See the x64 assembly instructions at the Entry Point.
*   **Hex Dump:** Inspect raw file bytes.

---

### 📂 Project 2: GhostTracer
**x64 Windows Debugger** (C++ / MASM)

A lightweight user-mode debugger built from scratch using Native Windows API. It bypasses standard debugger detection by manually handling debug events.

#### 📥 Installation
No installation required for the binary.
To compile from source (optional):
```cmd
build.bat
```

#### 🚀 How to Run
This is a Command Line Interface (CLI) tool. Open `cmd.exe` or PowerShell as Administrator.

#### 📖 Usage
**1. Attach to a running process:**
```powershell
GhostTracer.exe --attach <PID>
```

**2. Launch a new process:**
```powershell
GhostTracer.exe --launch "C:\Path\To\File.exe"
```

---
---

## 🇷🇺 Русская Версия

Этот репозиторий содержит мои личные инструменты для реверс-инжиниринга и анализа бинарных файлов Windows.

### 📂 Проект 1: VortexLogic
**Продвинутый Статический Анализатор PE** (Python 3 + CustomTkinter)

Профессиональный GUI-инструмент для анализа исполняемых файлов Windows (`.exe`, `.dll`) без их запуска. Имеет кастомный интерфейс в хакерском стиле, визуализацию энтропии для детекта пакеров и встроенный дизассемблер.

#### 📥 Установка
1.  Установите **Python 3.10+**.
2.  Откройте терминал в папке `VortexLogic`.
3.  Установите библиотеки:
    ```bash
    pip install -r requirements.txt
    ```

#### 🚀 Запуск
```bash
python main.py
```
*Дождитесь окончания загрузочного экрана "System Initialization".*

#### 📖 Использование
*   **Load Binary:** Нажмите кнопку загрузки или перетащите файл в окно.
*   **Dashboard:** Основная инфа (MD5 хеш, Дата сборки, EntryPoint).
*   **Sections:** Следите за полосками "Entropy". Красные (> 7.0) означают, что код упакован или зашифрован (подозрительно).
*   **Code View:** Показывает ассемблерный код (x64) на точке входа (Entry Point).
*   **Hex Dump:** Просмотр сырых байтов файла.

---

### 📂 Проект 2: GhostTracer
**x64 Windows Отладчик** (C++ / MASM)

Легковесный отладчик пользовательского режима (User-Mode), написанный с нуля на чистом Windows API. Обходит стандартные детекты отладчиков, вручную обрабатывая debug-события.

#### 📥 Установка
Установка не требуется.
Для компиляции исходников (опционально):
```cmd
build.bat
```

#### 🚀 Запуск
Это консольная утилита (CLI). Запускайте через `cmd.exe` или PowerShell от имени Администратора.

#### 📖 Использование
**1. Подключиться к запущенному процессу:**
```powershell
GhostTracer.exe --attach <PID>
# Пример: GhostTracer.exe --attach 1234
```

**2. Запустить новый процесс под отладкой:**
```powershell
GhostTracer.exe --launch "Путь\К\Файлу.exe"
# Пример: GhostTracer.exe --launch "C:\Windows\System32\notepad.exe"
```

---
*Created by Neil*
