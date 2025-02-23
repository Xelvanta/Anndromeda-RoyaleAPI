# 🚀 Anndromeda RoyaleAPI | General API Guide   

📌 Note: When you enter a URL into your browser’s address bar, a **GET request** is automatically triggered. This is the default HTTP method used by browsers to retrieve data from a server. You do not need to specify the GET method explicitly in the browser; it is handled automatically.

## **Base URL**  
```
http://127.0.0.1:5000
```

## **Endpoints**  

### **1️⃣ Get All Items**  
**Base Endpoint:**  
```
GET /items
```
**Description:**  
- Returns a list of all items scraped from Traderie.
- The response includes **item names** and **values**.

**Example Request:**  
```
GET http://127.0.0.1:5000/items
```

**Example Response:**  
```json
[
  {
    "name": "14 Karat Gold Infinity Chain",
    "value": "14,000"
  },
  {
    "name": "2019 Party Hat",
    "value": "10,000"
  },
  {
    "name": "2020 Lunar Rat Ears",
    "value": "4,000"
  }
]
```

---

### **2️⃣ Get a Specific Item's Value**  
**Base Endpoint:**  
```
GET /item
```
**Description:**  
- if the `name` query parameter is provided.
  - Returns the value of a specific item.
  - **Stops scraping as soon as it finds the item** (faster than `/items` when searching for a specific item).

**Query Parameter:**  

| Parameter | Type   | Required | Description                        |
|-----------|--------|----------|------------------------------------|
| `name`    | string | ✅ Required   | The **URL-encoded** name of the item to look up. If not provided, returns all items. |

### **URL Encoding Example**
If the item name contains **spaces** or special characters like `&`, `=`, or `#`, replace them with their URL-encoded versions (e.g., `"2019 Party Hat"` → `2019%20Party%20Hat`, `"ALIEN INVASION!!!"` → `ALIEN%20INVASION%21%21%21`).
```
GET /item?name=2019%20Party%20Hat
```

**Example Request (with `name` parameter):**  
```
GET http://127.0.0.1:5000/item?name=2019%20Party%20Hat
```

**Example Response (with `name` parameter):**  
```json
{ "value": 1200 }
```

**If the item is not found (with `name` parameter):**  
```json
{ "error": "Item not found" }
```

---

## **Error Handling**  
| Status Code | Meaning                        | Example Response                     |
|-------------|--------------------------------|--------------------------------------|
| `200`       | OK                | `{ "value": 1200 }` |
| `400`       | Bad Request                | `{"error": "Item name is required"}` |
| `404`       | Not Found                | `{ "error": "Item not found" }` |

---

## **Usage Notes**  
- `/items` scrapes **all pages** and returns everything.  
- `/item?name=...` is **faster** since it **stops scraping** once it finds the item.
- Make sure to **URL-encode spaces** and special characters (e.g., `"2019 Party Hat"` → `2019%20Party%20Hat`, `"ALIEN INVASION!!!"` → `ALIEN%20INVASION%21%21%21`).  
