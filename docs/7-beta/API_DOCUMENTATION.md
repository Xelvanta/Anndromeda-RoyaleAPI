# Anndromeda RoyaleAPI Documentation

Default Base URL: `http://localhost:5000/`

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

---

## **GET /health**

Check the health of the RoyaleAPI and the Node service.

### **Query Parameters**

* None

### **Responses**

**200 OK**

```json
{
  "status": "ok",
  "node_service": {
    "status": "ok",
    "pid": 12345,
    "consecutive_failures": 0,
    "max_retries_allowed": 5
  },
  "timestamp": "2025-12-30T18:00:00Z"
}
```

* `status`: overall API status (`ok` or `degraded`)
* `node_service.status`: health of the Node service (`ok`, `down`, `unhealthy`, `unreachable`)
* `pid`: current PID of the Node process if running
* `consecutive_failures`: number of consecutive Node failures
* `max_retries_allowed`: maximum retries before marking Node as down
* `timestamp`: UTC timestamp of the check

---

## **POST /node/restart**

Manually restart the Node service. Requires authentication.

### **Headers**

| Header      | Required | Description                 |
| ----------- | -------- | --------------------------- |
| X-API-Key   | yes      | The API key for access      |

### **Responses**

**200 OK**

```json
{
  "status": "success",
  "message": "Node service restarted and ready",
  "new_pid": 12345
}
```

**504 Gateway Timeout**

```json
{
  "status": "error",
  "message": "Node service started but timed out waiting for ready signal"
}
```

**500 Internal Server Error**

```json
{
  "status": "error",
  "message": "Failed to restart Node service"
}
```

* Restart stops the current Node process (if running), resets failure counters, and starts a new process.
* Returns a timeout if the Node service does not signal readiness within 15 seconds.
