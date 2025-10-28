# 🧘‍♀️ Fitness Studio REST API

A **Flask-based RESTful API** for managing fitness class bookings. It allows clients to view available classes, book slots, and retrieve bookings — all with **timezone-aware support** and interactive **Swagger documentation**.

---

## 🚀 Features

- 📅 View and book fitness classes with real-time availability
- 🌐 Timezone conversion for datetime fields in responses
- ✅ Input validation using Marshmallow & `email-validator`
- 💬 Interactive API docs via **Swagger UI**
- 🐳 Dockerized app (no need to install Python or dependencies)
- 🗃️ SQLite database preloaded with demo data

---

## 📦 Tech Stack

- **Flask** + Flask-Smorest (Blueprints + OpenAPI)
- **Marshmallow** for request/response schema validation
- **Docker & Docker Compose** for containerized deployment
- **SQLite** for local development DB
- **email-validator** for proper email format checks

---

## 🛠️ Setup & Run Instructions (Docker-Based)

### 1. 📂 Clone the Repository

```bash
git clone https://github.com/saxenaaakashj1/fitness_studio_api.git
cd booking_api
```

### 2. 🐳 Start the API with Docker Compose

```
docker-compose up --build
```

### 3. 🔗 Access the API

```
• Base URL: http://localhost:5005
• Swagger UI: http://localhost:5005/swagger
```

---

## 🌐 API Endpoints

### 1. 📋 Get All Available Classes

```
GET http://127.0.0.1:5005/classes?timezone=UTC
```

Query Parameter
- timezone (default: Asia/Kolkata) (Optional)

### 2. 📝 Book a Class

```
POST http://127.0.0.1:5005/book
```

Request Body:

```
{
  "class_id": 1,
  "client_name": "client_name",
  "client_email": "client@gmail.com"
}
```

### 3. 📋 Get Bookings by Email

```
GET http://http://127.0.0.1:5005/bookings?email=client@gmail.com
```
OR
```
GET http://http://127.0.0.1:5005/bookings?email=client@gmail.com?timezone=America/New_York
```

Query param:
- `email` (required)
- `timezone` (optional)

---

## 📊 Swagger UI for Testing

Explore, test, and document your API via Swagger:

```
👉 http://localhost:5005/swagger
```

## 🗃️ Initial Demo Data

On first run, the following classes are added automatically to the database fitness_studio.sqlite:

| Class Name | Instructor | Scheduled Datetime (UTC) | Available Slots |
|------------|------------|--------------------------|-----------------|
| Yoga       | Rahul      | 10 days from now         | 10              |
| Zumba      | Nidhi      | 10 days from now         | 10              |
| HIIT       | Mohit      | 10 days from now         | 10              |

---

## 📁 File Structure

```
fitness_studio_api/
│
├── app.py                          # Entry point of the application
├── requirements.txt
├── dockerfile
├── docker-compose.yml
├── .gitignore
├── README.md
│
├── instance/
│   └── fitness_studio.sqlite       # Database 
│
├── fitness_studio/
│   ├── __init__.py                 # Initialize Flask app & extensions
│   │
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── db.py
│   │
│   ├── resources/                  # All route handlers (Flask-RESTful resources) 
│   │   ├── __init__.py
│   │   ├── bookings.py
│   │   ├── classes.py
│   │
│   ├── schemas/                  
│   │   ├── __init__.py             # Marshmallow schemas
│   │   ├── schemas.py
│   │
│   ├── utils/                      # Helper functions (timezone, validation, etc.)
│   │   ├── __init__.py
│   │   └── utils.py
│   │
```
