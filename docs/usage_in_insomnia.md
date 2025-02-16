# 🌐 Anndromeda RoyaleAPI | Usage in Insomnia
This documentation assumes the program is already installed with all necessary dependencies and binaries. If the server is not yet set up for use, follow the instructions in the `README.md` to set it up.

### 1️⃣ **Ensure the Quart Server is Running**  
Before attempting to connect Insomnia to RoyaleAPI, start the Quart server:

```bash
quart run
```

### 2️⃣ **Open Insomnia**  
- Open Insomnia.
- Click on **New Request**.

### 3️⃣ **Create a Request to the API Endpoint**  
- Choose a **GET** request type.
- In the URL bar, enter the API endpoint:

```text
http://127.0.0.1:5000/items
```

or add a parameter:

eg.
```text
http://127.0.0.1:5000/items?name=<ITEM_NAME>
```

- Click **Send** to initiate the request. You will see the program start scraping data in the terminal.

### 4️⃣ **View the Response**  
- The data should appear in the **Response** section in JSON format.
- Inspect the JSON response to ensure the correct data is returned.

### 5️⃣ **Save the Request for Future Use**  
Once you are satisfied with the request and its response, save it by clicking the **Save** button in Insomnia. This allows you to reuse the request at any time.

---

## ⚠️ Troubleshooting

- **🔍 Connection Issue**: If Insomnia is unable to connect to the endpoint, double-check that the Quart server is running. If the server isn't running, Insomnia won’t be able to fetch the data.
- **🔄 Timeout Issues**: If the server takes too long to respond, you may need to adjust the request timeout settings in Insomnia under **Preferences > General > Request Timeout**.
