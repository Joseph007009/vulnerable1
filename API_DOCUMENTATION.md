# API Documentation - ShopCorp Training Lab

## Base URL
`http://localhost:5000/api`

## Endpoints

### GET /api/products/search
Search products by query string.

**Parameters:**
- `query` (string): Search term

**Example:**
```bash
curl "http://localhost:5000/api/products/search?query=laptop"
```

**Response:**
```json
{"status": "ok", "count": 1, "results": [...]}
```

---

### GET /api/orders/status
Get order status by ID.

**Parameters:**
- `order_id` (string): Order identifier

**Example:**
```bash
curl "http://localhost:5000/api/orders/status?order_id=1"
```

---

### POST /api/orders/bulk
Insert multiple orders.

**Body (JSON):**
```json
{
  "items": [
    {"user_id": 2, "product_id": 1, "quantity": 2}
  ]
}
```

---

### POST /api/search
Advanced product search with filters.

**Body (JSON):**
```json
{
  "query": "laptop",
  "filters": {
    "category": "Electronics",
    "price_max": 1500
  }
}
```

---

### GET /api/user/profile
Get user profile (authenticated).

**Headers:**
- `X-User-ID` (integer): User ID (or use session)

**Example:**
```bash
curl -H "X-User-ID: 1" "http://localhost:5000/api/user/profile"
```

---

## Injection Points Summary

| Endpoint | Method | Vulnerable Parameter | Level |
|----------|--------|---------------------|-------|
| `/api/products/search` | GET | `query` | 2 |
| `/api/orders/status` | GET | `order_id` | 3 |
| `/api/orders/bulk` | POST | JSON `items[]` | 4 |
| `/api/search` | POST | JSON `query`, `filters.category` | 4 |
| `/api/user/profile` | GET | `X-User-ID` header | 4 |
