# Contributing to Anndromeda-RoyaleAPI  

Thank you for your interest in contributing to **Anndromeda-RoyaleAPI**! 🎉 This project is licensed under the **GPL 3.0** license, meaning all contributions must also be open-source under the same license.  

We welcome all kinds of contributions, including **bug reports, feature requests, documentation improvements, and code contributions**. Please follow the guidelines below to ensure a smooth collaboration process.  

---

## 🛠 How to Contribute  

### 1️⃣ Fork the Repository  
Click the **"Fork"** button on the top-right of the repository page to create your own copy.  

### 2️⃣ Clone Your Fork  
```bash
git clone https://github.com/your-username/Anndromeda-RoyaleAPI.git
cd Anndromeda-RoyaleAPI
```

### 3️⃣ Create a New Branch  
Make sure to create a branch for your work rather than working directly on `main`.  
```bash
git checkout -b feature/your-feature-name
```

### 4️⃣ Make Your Changes  
Modify the codebase, fix bugs, or improve documentation as needed.  

### 5️⃣ Format Your Code  

Ensure your code follows the project's formatting and style conventions before committing.  

#### 🐍 Python Formatting  
- Use **4 spaces for indentation** (no tabs).  
- Keep **imports grouped**:  
  - Standard library imports (e.g., `json`, `os`) go first.  
  - Third-party libraries (e.g., `quart`, `quart_cors`) next.  
  - Local imports last.  
- Follow **PEP 8** style guidelines.  
- Run **Black** to auto-format:  
  ```bash
  black .
  ```  
- Keep **docstrings** for functions:  
  ```python
  def scrape_traderie(page_num):
      """
      Scrapes item names and community values from Traderie.com using Puppeteer.
      """
  ```
- Use **f-strings** for formatted output instead of `format()` or `+` concatenation.  
- Avoid **hardcoding paths**, use `os.path.join()` when working with files.  

#### 🚀 JavaScript Formatting  
- Use **4 spaces for indentation** (no tabs).  
- Follow **ES6+ best practices**:  
  - Use `const` and `let` instead of `var`.  
  - Use arrow functions (`()=>{}`) where applicable.  
- Keep **console logs structured**:  
  ```js
  console.log(`🌐 Navigating to ${url}`);
  ```
- Format using **Prettier**:  
  ```bash
  npm run format
  ```  
- Avoid **hardcoded delays** like `setTimeout()`, prefer waiting for selectors instead:  
  ```js
  await page.waitForSelector('div.item-img-container', { timeout: 15000 });
  ```
- Ensure all **async functions handle errors** using try-catch:  
  ```js
  try {
      const scrapedData = await scrapeTraderie(page, pageNumber);
  } catch (error) {
      console.error("❌ Scraping failed:", error);
  }
  ```

Make sure all files are formatted before committing to maintain consistency! 🚀
- Symbols like ✅, ⚠️, ⏳, ❌, 🔍, and 🌐 should be used in console logs and debug messages for better readability.
- Ensure all tests pass before committing.  

### 6️⃣ Commit Your Changes  
Write **clear, concise commit messages**:  
```bash
git commit -m "Fix API timeout issue"
```

### 7️⃣ Push Your Branch  
```bash
git push origin feature/your-feature-name
```

### 8️⃣ Open a Pull Request  
- Go to your fork on GitHub.  
- Click **"Compare & pull request"**.  
- Provide a **clear description** of your changes.  
- **Link any relevant issues** (e.g., `Fixes #42`).  

---

## 🔥 Bug Reports  

If you find a bug, please check the **BUG_REPORT.md** file for details on how to submit a detailed bug report.  

When reporting a bug, include:  
- Steps to reproduce the issue  
- Expected vs. actual behavior  
- System details (OS, terminal, hardware, etc.)  
- **Attach logs and memory dumps (if applicable)**  

---

## 🎯 Feature Requests  

Want to suggest a feature? Create a **GitHub Issue** with:  
- **A detailed description** of the feature  
- **The problem it solves**  
- **Any alternatives you've considered**  

---

## ✅ Code of Conduct  

Be respectful and constructive.

---

## 📜 License  

By contributing, you agree that your code will be **licensed under GPL-3.0**.  

📌 **You must ensure your contributions comply with GPL-3.0, meaning all modifications remain open-source under the same license.**  

---

Thank you for contributing! 🚀
