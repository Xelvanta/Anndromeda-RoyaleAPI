# 🌐 Anndromeda RoyaleAPI | Usage in Any Browser

This documentation assumes the program is already installed with all necessary dependencies and binaries. If the server is not yet set up for use, follow the instructions in the `README.md` to set it up.

### 1️⃣ **Ensure the Quart Server is Running**  
Before attempting to access RoyaleAPI in a browser, make sure the Quart server is running:

```bash
quart run
```

### 2️⃣ **Open Your Browser**  
- Open your preferred browser (Chrome, Firefox, Safari, etc.).

### 3️⃣ **Enter the API Endpoint in the URL Bar**  
- In the browser’s URL bar, enter the following API endpoint:

```text
http://127.0.0.1:5000/items
```

- Press **Enter** to load the API response. You will see the program start scraping data in the terminal.

### 4️⃣ **Pretty Print Option**  
- The response will be in in JSON format. You may see the raw JSON data in the browser.
- To make the data more readable, ensure the **Pretty Print** option is enabled. This option can usually be found as a checkbox or button at the top of the JSON response view. It may also automatically appear in the browser for pretty printing if you are using a browser with built-in JSON formatting (e.g., Chrome or Firefox).
  - **Chrome**: Pretty Print will automatically format the JSON in a human-readable form.
  - **Firefox**: There’s an option to **"Format"** the JSON response under the "Actions" menu or just by navigating directly to the raw JSON page.

### 5️⃣ **View the Response**  
- The browser will display the API response in JSON format, either as raw or formatted (Pretty Printed) data.
- Inspect the data in the browser to ensure it contains the information you need. You can scroll through the formatted data to examine specific fields or objects. You can search for specific text using **Ctrl+F** or **Find in Page**.

---

## ⚠️ Troubleshooting

- **🔍 Connection Issue**: If the browser is unable to access the endpoint, double-check that the Quart server is running. If the server isn't running, the browser won’t be able to fetch the data.
- **📝 Raw Response**: If Pretty Print isn't automatically applied or there is no option to enable it, you may need to use a browser extension for better JSON formatting or manually view the raw JSON if necessary.
