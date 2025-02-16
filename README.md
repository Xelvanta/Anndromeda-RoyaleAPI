# Anndromeda RoyaleAPI

**Anndromeda RoyaleAPI** (formerly known as Royale High API) is a powerful **Quart API** designed to fetch the names of items from the popular Roblox game **Royale High** and their associated community values from **Traderie**. The API returns results in **JSON format**, making it easy to integrate and use for various applications or analysis.

This API was created to interact with the **Traderie** website, a platform where the Royale High community buys and sells in-game items. With the API, you can easily access the most up-to-date information on item names and their community values, providing the necessary data for further processing or for custom interfaces.

### Key Features:

- **Item Fetching**: The API allows you to retrieve a list of Royale High items and their respective community prices directly from Traderie, providing real-time data for developers, analysts, or any users interested in tracking item trends.
  
- **JSON Output**: The API returns data in **JSON format**, which is easily handled programmatically in most languages or environments, ensuring flexibility for diverse use cases.

---

## Testing Environment

The application has been **tested on Windows 11** but should be compatible with **Linux** and **macOS** systems as well. While it has been primarily tested in a Windows environment, the code should work across these platforms with minor adjustments (if any). For optimal results, it’s recommended to use a system with **Python 3.x** and **Node.js** installed.

---

## Requirements

Before running the application, you’ll need the following:

- **Google Chrome** (required for Puppeteer browser automation)
  - [Download Google Chrome](https://www.google.com/intl/en_ca/chrome/)
- **Node.js** (with npm)
  - [Download Node.js](https://nodejs.org/en) (We'll verify that it's installed later)
- **Python 3.x**
  - [Download Python](https://www.python.org/downloads/)
- **Pip** (Python package manager, usually comes with Python)


We'll install these dependencies later during installation:
- **Puppeteer** (for browser automation)
- **Quart** (Python web framework)
- **Quart-CORS** (to handle CORS for the Quart API)

---

## Installation

### 1. Clone the Repository:

```bash
git clone https://github.com/Xelvanta/Anndromeda-RoyaleAPI
cd Anndromeda-RoyaleAPI
```

### 2. Install Node.js and Puppeteer

Make sure you have **Node.js** installed. If not, follow these steps:

#### **Check Node.js and npm Versions**

To check if Node.js and npm are installed:

1. Open your terminal or command prompt.
2. Run the following commands to check their versions:

    ```bash
    node -v
    npm -v
    ```

   These should return version numbers for both Node.js and npm. If they do, you’re good to go!

#### **If Node.js or npm is not installed**

If you see an error like `'node' is not recognized` or `'npm' is not recognized`, then Node.js (and npm) is not installed.

##### **Step 1: Download Node.js**

1. Go to the official [Node.js website](https://nodejs.org/en).
2. Download and install the **LTS version** (Recommended for most users).
   
Make sure to **add Node.js to your PATH** during installation (usually added by default during the setup wizard).

---

### 3. Manually Install Node Modules:

Before running your script, make sure you have all required dependencies:

1. Open your terminal.
2. Navigate to the directory containing `traderie_scraper.js`:

    ```bash
    cd Anndromeda-RoyaleAPI
    ```

3. Run the following command to install dependencies:

    ```bash
    npm install puppeteer puppeteer-extra puppeteer-extra-plugin-stealth
    ```

This will install **Puppeteer** and related modules, which are required for your script to function correctly.

---

### 4. Install Quart and Quart-CORS:

Install the necessary Python dependencies:

```bash
pip install -r requirements.txt
```

---

### 5. Verify Execution of `traderie_scraper.js`:

1. Open a new terminal.
2. Navigate to the directory containing `traderie_scraper.js`.

3. Run the following command (the `<number>` represents the page number):

    ```bash
    node traderie_scraper.js <number>
    ```

   For example:
   - `node traderie_scraper.js 0` will scrape **page 0**.
   - `node traderie_scraper.js 1` will scrape **page 1**.

If successful, this indicates that the JavaScript side of things is working.

---

## Common Issues

Here are some common issues you may encounter during setup:

- **Node.js not recognized**: Ensure Node.js is installed and properly added to your system's PATH. If you encounter this issue, the instructions to fix it are covered in the **Troubleshooting** section at the bottom.
- **Puppeteer not working**: Make sure you have **Google Chrome** installed on your system, as Puppeteer requires it to run.
- **Missing Python dependencies**: Ensure you have installed `quart` and `quart-cors` using `pip install quart quart-cors`.

---

## Troubleshooting

If you encounter issues, follow the troubleshooting steps below:

### Ensure Node.js is in Your PATH (Common Issue)

If `node` or `npm` is not recognized, it may be a PATH issue.

##### **For Windows:**

1. Search for **"Environment Variables"** in the Start Menu.
2. Click **"Edit the system environment variables"**.
3. Click **"Environment Variables..."**.
4. In the **"System variables"** section, find a variable named `Path`.
5. Select `Path` and click **"Edit..."**.
6. Click **"New"** and add the path to your Node.js installation directory. Common locations include:
   - `C:\Program Files\nodejs\`
   - `C:\Program Files (x86)\nodejs\`
7. Click **OK** on all dialogs to save the changes.

**Important:** You may need to restart your computer for the PATH changes to take effect.

##### **For macOS/Linux:**

1. Open your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`).
2. Add this line to the end of the file, replacing `/path/to/nodejs` with the correct path to your Node.js executable:

    ```bash
    export PATH="/path/to/nodejs:$PATH"
    ```

3. Use `which node` to find the correct path.
4. Save and run:

    ```bash
    source ~/.bashrc  # or source ~/.zshrc
    ```

### Fixing PowerShell Execution Policy for npm

If running `npm -v` results in an error like:

```powershell
npm : File C:\Program Files\nodejs\npm.ps1 cannot be loaded because running scripts is disabled on this system.
```

You can resolve this by changing your PowerShell execution policy.

##### **Step 1: Open PowerShell as Administrator**

1. Search for **"PowerShell"** in the Start menu.
2. Right-click **"Windows PowerShell"** and choose **"Run as administrator"**.

##### **Step 2: Change the Execution Policy**

Run the following command to allow scripts to run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

##### **Step 3: Confirm the Change**

Confirm the change by typing `Y` and pressing **Enter**.

##### **Step 4: Test npm Again**

Close the PowerShell window and open a new one. Then try running:

```powershell
npm -v
```

This should work now! 🎉

---

## Running the Application

To run the Quart app:

1. Open a terminal and navigate to the directory where your app resides.

    ```bash
    cd Anndromeda-RoyaleAPI
    ```

2. Run the following:

    ```bash
    quart run
    ```
    
3. **Access the API**:

    Open any browser or an API client (like Insomnia) and navigate to:

    ```
    http://127.0.0.1:5000/items
    ```

This will start the Quart server and start scraping all pages starting from 0.

📌 **IMPORTANT: See docs/general_api_guide.md for more information.**

---

## Contributing

Feel free to fork the project and submit a pull request to help improve **Anndromeda RoyaleAPI**. Your contributions are welcome!

---

## License

**Anndromeda RoyaleAPI** is open source and available under the GPL-3.0 license. See the LICENSE file for more details.

---

By **Anndromeda**
A sister company to **Xelvanta Group Systems**  
For support or inquiries, please contact us at [enquiry.information@proton.me](mailto:enquiry.information@proton.me).  
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)
