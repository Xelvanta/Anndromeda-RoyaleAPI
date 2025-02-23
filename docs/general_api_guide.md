# 🚀 Anndromeda RoyaleAPI | General API Guide  

**Base URL**  
```
http://127.0.0.1:5000
```

---

## **Endpoints Overview**

| Request Type | Endpoint         | Description                                                  |
|--------------|------------------|--------------------------------------------------------------|
| GET          | `/items`         | Returns a list of all items scraped from Traderie.            |
| GET          | `/item`          | Returns the value of a specific item. Requires `name` query parameter. |

---

### **1️⃣ Get All Items**  

| Request Type | GET              |
|--------------|------------------|
| Endpoint     | `/items`         |
| Description  | Returns a list of all items scraped from Traderie, including item names and values. |
| Example URL  | `GET http://127.0.0.1:5000/items` |

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

**Status Codes for `/items`:**

| Status Code | Meaning  | Example Response                     |
|-------------|----------|---------------------------------------|
| `200`       | OK       | `[{"name": "14 Karat Gold Infinity Chain","value": "14,000"},{"name": "2019 Party Hat","value": "10,000"},{"name": "2020 Lunar Rat Ears","value": "4,000"}]`                   |

---

### **2️⃣ Get a Specific Item's Value**  

| Request Type | GET              |
|--------------|------------------|
| Endpoint     | `/item`          |
| Description  | Returns the value of a specific item based on the `name` query parameter. Stops scraping once the item is found. |
| Query Parameter | `name` (string) - The URL-encoded name of the item. Required. |
| Example URL  | `GET http://127.0.0.1:5000/item?name=2019%20Party%20Hat` |

**Query Parameter Table:**

| Parameter | Type   | Required | Description                                            |
|-----------|--------|----------|--------------------------------------------------------|
| `name`    | string | ✅ Required | The URL-encoded name of the item to look up. |

**URL Encoding Example:**  
For special characters or spaces, use their URL-encoded versions.  
Example:  
`"2019 Party Hat"` → `2019%20Party%20Hat`

**Example Response (with `name` parameter):**  
```json
{
  "value": 1200
}
```

**If the item is not found:**  
```json
{
  "error": "Item not found"
}
```

**Status Codes for `/item`:**

| Status Code | Meaning  | Example Response                     |
|-------------|----------|---------------------------------------|
| `200`       | OK       | `{ "value": 1200 }`                   |
| `400`       | Bad Request | `{ "error": "Item name is required"}` |
| `404`       | Not Found | `{ "error": "Item not found" }`       |

---

## **Usage Notes**  

- `/items` scrapes **all pages** and returns all available items.
- `/item?name=...` is **faster** since it **stops scraping** once it finds the item.
- Be sure to **URL-encode** any spaces or special characters in item names (e.g., `"2019 Party Hat"` → `2019%20Party%20Hat`, `"ALIEN INVASION!!!"` → `ALIEN%20INVASION%21%21%21`).
