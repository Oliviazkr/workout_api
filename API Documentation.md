
# Nutrition Calculator API Documentation

## Base URL
```
http://localhost:8000/
```

---

## Authentication

| Endpoint | Method | Description | Auth Required |
|----------|--------|-------------|---------------|
| `/register/` | POST | User registration | No |
| `/login/` | POST | User login | No |
| `/logout/` | GET | User logout | Yes |

### Register
**POST** `/register/`
```
Request (form-data):
username: newuser
email: user@example.com
password1: password123
password2: password123

Response: Redirect to / (302)
```

### Login
**POST** `/login/`
```
Request (form-data):
username: newuser
email: user@example.com
password1: password123
password2: password123

Response: Redirect to / (302)
```

---

## Food Library

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/foods/` | GET | List all foods | Yes |
| `/foods/add/` | POST | Add new food | Yes |
| `/foods/<id>/edit/` | POST | Edit food | Yes |
| `/foods/<id>/delete/` | GET | Delete food | Yes |
| `/foods/import/` | POST | Import CSV | Yes |

### List Foods
**GET** `/foods/`
```
Query Parameters:
- search: Filter by name
- category: Filter by category

Response: HTML page with food table
```

### Add Food
**POST** `/foods/add/`
```
Request (form-data):
name: Banana
category: fruits
calories: 89
protein: 1.1
carbs: 22.8
fat: 0.3
fiber: 2.6
sugar: 12.2

Response: Redirect to /foods/
```

### CSV Import Format
```csv
food,Caloric Value,Fat,Carbohydrates,Protein
Apple,52,0.2,13.8,0.3
Banana,89,0.3,22.8,1.1
```

---

## Nutrition Calculation

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/calculate/` | POST | Calculate nutrition | No* |
| `/api/search/` | GET | Search foods (AJAX) | No |

### Calculate Nutrition
**POST** `/calculate/`
```
Headers:
Content-Type: application/json
X-CSRFToken: <csrf_token>

Request Body:
{
  "items": [
    {"id": 1, "weight": 200},
    {"id": 2, "weight": 150}
  ]
}

Response:
{
  "success": true,
  "total_weight": 350.0,
  "total_calories": 520.5,
  "total_protein": 35.2,
  "total_carbs": 45.8,
  "total_fat": 18.3,
  "details": [
    {
      "id": 1,
      "name": "Chicken Breast",
      "weight": 200,
      "calories": 330.0,
      "protein": 62.0,
      "carbs": 0.0,
      "fat": 7.2
    }
  ]
}
```

### Search Foods
**GET** `/api/search/?q=chicken`
```
Response:
[
  {
    "id": 1,
    "name": "Chicken Breast",
    "calories": 165.0,
    "category": "Meat"
  }
]
```

---

## History

| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/history/` | GET | List history | Yes |
| `/history/<id>/` | GET | View detail | Yes |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 302 | Redirect after form submit |
| 404 | Resource not found |
| 500 | Server error |
```

