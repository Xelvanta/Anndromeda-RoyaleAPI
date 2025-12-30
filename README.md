# 🚀 Anndromeda RoyaleAPI

![License](https://img.shields.io/github/license/Xelvanta/Anndromeda-RoyaleAPI?label=License\&color=orange)
![Puppeteer Version](https://img.shields.io/github/package-json/dependency-version/Xelvanta/Anndromeda-RoyaleAPI/puppeteer?label=Puppeteer)
![Release](https://img.shields.io/github/v/release/Xelvanta/Anndromeda-RoyaleAPI?include_prereleases\&label=Release\&color=green)

**Anndromeda RoyaleAPI**, also known as Royale High API or RHAPI, is a powerful **Quart + Puppeteer API** designed to fetch the names of items from the popular Roblox game **Royale High** and their associated community values from **Traderie**. The API returns results in **JSON format**, making it easy to integrate and use for various applications or analysis. This API was created to interact with the **Traderie** website, a platform where the Royale High community buys and sells in-game items. With the API, you can easily access the most up-to-date information on item names and their community values, providing the necessary data for further processing or for custom interfaces.

---

## 📦 Features

* **Item Fetching**: Real-time retrieval of items and values.
* **Targeted Queries**: Fetch specific items by the item's `id`.
* **JSON Output**: Easy parsing in Python, JS, Power Query, etc.
* **Bulk Retrieval**: Optimize performance for full item lists.
* **Integration Ready**: Works with Excel, Google Sheets, Power BI, or custom apps.

---

## 🧪 Supported Platforms

* **Tested:** Windows 11
* **Compatible:** Linux, macOS
* **Requirements:** Python 3.x, Node.js, Google Chrome

---

## ⚙️ Requirements

### System Requirements

* **Python 3.x** & **pip**
* **Node.js** & **npm**
* **Google Chrome** (required by Puppeteer)

### Core Dependencies

* **Python:** `quart`, `quart-cors`
* **Node:** `puppeteer`

> See [requirements.txt](requirements.txt) and [package.json](package.json) for details.

---

## 🚀 Installation

### 1. Clone Repository

```bash
git clone https://github.com/Xelvanta/Anndromeda-RoyaleAPI
cd Anndromeda-RoyaleAPI
```

### 2. Optional: Python Virtual Environment

```powershell
py -3.13 -m venv venv
venv\Scripts\activate
```

### 3. Install Node Dependencies

```bash
npm ci
```

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the API

```bash
python app.py
```

* **Access endpoints:** [http://127.0.0.1:5000/items](http://127.0.0.1:5000/items) or `/item?id=<ID>`
* **Documentation:** See [API_DOCUMENTATION.md](docs/7-beta/API_DOCUMENTATION.md)

---

## ⚠️ Common Issues

* **Node.js not recognized:** Ensure Node.js is installed and in your PATH.
* **Puppeteer Chrome error:** Make sure Google Chrome is installed.
* **Dependencies missing:** Ensure `pip install -r requirements.txt` or `npm ci` completed successfully.
* **Windows PATH for Node.js:** Add Node.js folder to system PATH.
* **PowerShell Execution Policy:** `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

---

## 💡 Contributing

Fork, contribute, and submit PRs. See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📝 License

GPL-3.0. See [LICENSE](LICENSE).

---

## 📬 Contact

**Anndromeda / Xelvanta Group Systems**
Email: [Xelvanta@proton.me](mailto:Xelvanta@proton.me)
GitHub: [https://github.com/Xelvanta](https://github.com/Xelvanta)
