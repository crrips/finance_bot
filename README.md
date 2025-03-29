# Finance Bot

This is a finance bot that provides control over your expnses.

## 🚀 Launch

Firstly, create .env file in the bot directory and set the following values, replacing the placeholders with your actual values:
```
TOKEN = "your_token"

API_URL = "http://backend:8000"

DB_NAME = "finance_db"
DB_USER = "user"
DB_PASSWORD = "password"
DB_HOST = "finance_db"
DB_PORT = 5432
```

To start the bot using Docker and docker-compose, run:
```
docker-compose up --build
```

## 🛠️ Development

* API: FastAPI
* Bot: Aiogram
* Database: PostgreSQL
* ORM: SQLAlchemy
* Containerization: Docker
* Excel: pandas and openpyxl

## 📩 Feedback

If you have any suggestions or find any issues, feel free to contact me.