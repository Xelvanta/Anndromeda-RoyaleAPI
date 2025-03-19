---
name: Bug Report
about: Create a bug report to help us resolve the bug.
title: '🐞 [BUG]:'
labels: 'bug'
assignees: 'Xelvanta'
---

# Bug Report  

Thank you for taking the time to report a bug! Please follow this template to ensure we can effectively troubleshoot and resolve the issue.  

## 🐞 Bug Description  
- *A clear and concise description of what the bug is.*
- *Is the issue occurring on the Python side, JavaScript side, both, or somewhere else?*
  - *Please specify where the issue seems to be originating. If you’re unsure, provide any additional details that may help us narrow it down.*

## ✅ Steps to Reproduce  
1. **Step 1** – What actions did you take?  
2. **Step 2** – What happened next?  
3. **Step 3** – What was the expected behavior?  

## 📷 Screenshots or Logs (if applicable)  
- Attach screenshots, error logs, videos, or GIFs to show the issue.  
- If applicable, copy and paste terminal output (including your input at the command line).  

## 🔎 Debugging Instructions  
To help us debug effectively, please perform the following:  

### 1️⃣ Check for Errors in Logs  
- If applicable, check log files for errors and provide relevant output.  
- Example for Windows systems:  
  ```bash
  Get-EventLog -LogName System -Newest 50
  ```

### 2️⃣ Debug the Scraper  
- **Run the scraper** with the following command:
  ```bash
  node fetchData.js 0
  ```
  (Note: `0` specifies the page number to scrape.)
1. ✅ If the command works as expected, the JavaScript side is functioning correctly.
2. 🖥️ If you see an error that says 'node' is not recognized, it means that Node.js is either not installed on your computer or it's not on your PATH. To fix this, check the Troubleshooting section in the README.md file for instructions on how to install Node.js and add it to your PATH.
3. ❌ If the scraper doesn't work or returns an error, change the following line in the code:
  ```javascript
  headless: "new"
  ```
  to:
  ```javascript
  headless: false
  ```
- Rerun the scraper after modifying the code.
- **A Chrome for Testing browser should open**, allowing you to see exactly what the scraper is seeing and doing in real-time. Provide details on what happened.
- Attach logs (if applicable) and **copy and paste the terminal output**.
- If possible, take a **screen recording** or **screenshot** of the issue happening.

### 3️⃣ Perform a Memory Dump (if applicable)  
If the program crashes, you can create a memory dump for analysis.  

#### **📌 Memory Dump for Quart**  
1. **Find the Process ID (PID) of the running Quart server:**  
   - **Linux/macOS:**  
     ```bash
     ps aux | grep python
     ```
     OR  
     ```bash
     pgrep -fl quart
     ```
   - **Windows (PowerShell):**  
     ```powershell
     Get-Process | Where-Object {$_.ProcessName -like "*python*"}
     ```

2. **Generate the Memory Dump:**  
   - **Linux/macOS:**  
     ```bash
     gcore -o quart_dump $(pgrep -f "quart run")
     ```
   - **Windows (PowerShell, requires Sysinternals):**  
     ```powershell
     procdump -ma <PID> quart_dump.dmp
     ```

#### **📌 Memory Dump for Node.js**  
1. **Find the Process ID (PID) of the running Node.js application:**  
   - **Linux/macOS:**  
     ```bash
     ps aux | grep node
     ```
     OR  
     ```bash
     pgrep -fl node
     ```
   - **Windows (PowerShell):**  
     ```powershell
     Get-Process | Where-Object {$_.ProcessName -like "*node*"}
     ```

2. **Generate the Memory Dump:**  
   - **Linux/macOS:**  
     ```bash
     gcore -o node_dump $(pgrep -f "node <script_name>.js")
     ```
   - **Windows (PowerShell, requires Sysinternals):**  
     ```powershell
     procdump -ma <PID> node_dump.dmp
     ```

#### **📌 Memory Dump for Python Runtime**  
1. **Attach to the running Python process:**  
   - **Linux/macOS:**  
     ```bash
     strace -p $(pgrep -f "quart run") -o python_trace.log
     ```
   - **Windows (PowerShell, requires Sysinternals):**  
     ```powershell
     procmon /PID <PID> /Minimized /Quiet /Backingfile python_trace.pml
     ```

2. **Dump the current state of the Python process using `faulthandler`:**  
   - If the process is still responsive, send a SIGUSR1 signal to dump the current state:  
     ```bash
     kill -USR1 $(pgrep -f "quart run")
     ```
   - If running in a Windows environment:  
     ```powershell
     python -c "import faulthandler, os; faulthandler.dump_traceback(open('traceback.log', 'w'))"
     ```

3. **Force a full core dump (if needed):**  
   ```bash
   gcore -o python_runtime_dump $(pgrep -f "quart run")
   ```

The resulting **Python trace logs** (`python_trace.log`, `traceback.log`) and memory dumps (`python_runtime_dump`) will help analyze runtime issues.

📌 **Note:** Replace `<PID>` with the actual process ID. The resulting memory dump files (`quart_dump` or `node_dump.dmp`) can be analyzed with debugging tools like **GDB (Linux/macOS)** or **WinDbg (Windows)**.  
⚠️ **IMPORTANT:** Only share memory dumps publicly if it's safe to do so. Memory dumps can contain sensitive or private information, such as login credentials, personal data, or other details about your system. Before sharing, review the dump to ensure that it doesn't contain any private or confidential data.

### 4️⃣ Provide System Information  
- **OS and version** (e.g., Windows 11 24H2, macOS Sonoma, Ubuntu 22.04):
- **Software version numbers** (e.g., Node.js 18.3.0, Python 3.11.2, etc.):
- **Hardware specs** (CPU, RAM, GPU if applicable):
- **Type of terminal used** (PowerShell, Command Prompt, Bash, Zsh, etc.):

## 📌 Expected vs. Actual Behavior  
**Expected Behavior:**  
(Describe what should have happened.)  

**Actual Behavior:**  
(Describe what actually happened.)  

## 🛠 Workarounds (if any)  
(Have you found any temporary solutions?)  

## 📝 Additional Context  
- Any other information that might help us debug the issue?  
- Are you using any special configurations, plugins, or modifications?  
