# 🌐 Anndromeda RoyaleAPI | Usage in Postman  
This documentation assumes the program is already installed with all necessary dependencies and binaries. If the server is not yet set up for use, follow the instructions in the `README.md` to set it up.  

### 1️⃣ **Ensure the Quart Server is Running**  
Before attempting to connect Postman to RoyaleAPI, start the Quart server:  

```bash
quart run
```  

### 2️⃣ **Open Postman**  
- Launch **Postman** on your device.  
- Click on **New Request**.  

### 3️⃣ **Create a Request to the API Endpoint**  
- Select the **GET** request type.  
- In the request URL bar, enter the API endpoint:  

```text
http://127.0.0.1:5000/items
```

or add a parameter:

eg.
```text
http://127.0.0.1:5000/items?name=<ITEM_NAME>
```

- Click **Send** to execute the request. The terminal should show that the program is scraping data.  

### 4️⃣ **View the Response**  
- The response should appear in the **Body** section in **JSON format**.  
- Inspect the JSON response to verify that the correct data is returned.  

### 5️⃣ **Save the Request for Future Use**  
- Click **Save** to store the request in Postman for future use.  
- Organize it inside a **collection** for easy access.  

---  

## ⚠️ Troubleshooting  

- **🔍 Connection Issues**: If Postman cannot connect to the endpoint, ensure the **Quart server is running**. If it isn't, Postman will not receive a response.  
- **🔄 Timeout Problems**: If the server takes too long to respond, increase the request timeout under **Settings > General > Request timeout** in Postman.  
