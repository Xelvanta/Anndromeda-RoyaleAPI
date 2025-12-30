# Anndromeda RoyaleAPI Documentation

Base URL: `http://localhost:5000/`

---

## **GET /items**

Retrieve all items from Traderie with their metadata.

### **Query Parameters**

* None

### **Responses**

**200 OK**

```json
{
  "items": [
    {
      "id": "171450405",
      "name": "Sewer Rat",
      "active": true,
      "buy_price": null,
      "created_at": "2021-01-13T16:19:40.841Z",
      "description": "turn into rat. very cool rat...",
      "img": "https://cdn.nookazon.com/royalehigh/items/6159435874.png",
      "mode": null,
      "prices": [
        {
          "avg": 4054.023,
          "demand": 1,
          "user_value": 4000,
          "value_change": 4000,
          "variant_id": null
        }
      ],
      "slug": "sewer-rat",
      "tags": [
        {"category": "style", "format": null, "tag": "Fun", "tag_id": 61}
      ],
      "type": "Accessory",
      "unlocked_at": null,
      "variants": null
    }
  ],
  "version": "1.3.0"
}
```

---

## **GET /item**

Retrieve a single item by **id**.

### **Query Parameters**

| Parameter | Type   | Required | Description                  |
| --------- | ------ | -------- | ---------------------------- |
| id        | string | yes      | The ID of the item to fetch. |

### **Responses**

**200 OK**

```json
{
  "item": {
    "id": "171450405",
    "name": "Sewer Rat",
    "active": true,
    "buy_price": null,
    "created_at": "2021-01-13T16:19:40.841Z",
    "description": "turn into rat. very cool rat...",
    "img": "https://cdn.nookazon.com/royalehigh/items/6159435874.png",
    "mode": null,
    "prices": [
      {
        "avg": 4054.023,
        "demand": 1,
        "user_value": 4000,
        "value_change": 4000,
        "variant_id": null
      }
    ],
    "slug": "sewer-rat",
    "tags": [
      {"category": "style", "format": null, "tag": "Fun", "tag_id": 61}
    ],
    "type": "Accessory",
    "unlocked_at": null,
    "variants": null
  },
  "version": "1.3.0"
}
```

**400 Bad Request**

```json
{
  "error": "Item id required"
}
```

* Returned if the `id` query parameter is missing or empty.

**404 Not Found**

```json
{
  "error": "Item not found"
}
```

* Returned if no item with the given `id` exists.