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

### 5️⃣ Format Your Code (Style Guidelines)

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
- Keep **docstrings** for functions. Follow **PEP 257** docstring guidelines:  
  ```python
  async def fetch_traderie_data(page_num):
      """
      Fetches data from the Traderie API using the fetchData.js Node.js script.
    
      :param page_num: The page number to fetch data for.
      :type page_num: int
      :return: A tuple containing a boolean indicating if fetching is done and a list of fetched items.
      :rtype: tuple
      """
  ```
- Use **f-strings** for formatted output instead of `format()` or `+` concatenation.  
- Avoid **hardcoding paths**, use `os.path.join()` when working with files.  

#### 🚀 JavaScript Formatting  
- Use **4 spaces for indentation** (no tabs)
  - if you're using Prettier, make sure your settings reflect this.  
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

When creating a **GitHub issue**, you'll have the option to select the '**Bug Report**' template. Click on that to view instructions on submitting a detailed bug report.

When reporting a bug, include:  
- Steps to reproduce the issue  
- Expected vs. actual behavior  
- System details (OS, terminal, hardware, etc.)  
- **Attach logs and memory dumps (if applicable)**  

---

## 🎯 Feature Requests  

When creating a **GitHub issue**, you'll have the option to select the '**Feature Request**' template. Click on that to view instructions on submitting a detailed feature request.

When requesting a feature, include:  
- **A detailed description** of the feature  
- **The problem it solves**  
- **Any alternatives you've considered**  

---

## ✅ Code of Conduct  

For a detailed guide on fostering a respectful, inclusive, and welcoming environment, please refer to the **CODE_OF_CONDUCT.md** file. It follows the **Contributor Covenant**, which outlines our community standards and expectations for behavior.

---

## 📜 License  

By contributing, you agree that your code will be **licensed under GPL-3.0**.  

📌 **You must ensure your contributions comply with GPL-3.0, meaning all modifications remain open-source under the same license.**  

---

Thank you for contributing! 🚀
