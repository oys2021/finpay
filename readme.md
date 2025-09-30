# 💳 Wallet & Transactions API with Django REST Framework

This project is a wallet management API built with Django and Django REST Framework. It allows authenticated users to manage their wallets, view balances in multiple currencies, send and withdraw funds, convert currencies, deposit money via third-party providers, and track income/expense transactions.

This is the deployment link: https://your-deployment-link.com

---

## 🚀 Features

-  JWT-authenticated  API endpoints
- Retrieve wallet balances (all currencies or specific currency)
- View income vs. expense transaction summaries
- Send funds to recipient accounts or mobile money agents
- Withdraw funds to bank accounts or mobile money agents
- Currency conversion between supported currencies
- Deposit money via third-party provider integrations (with webhook support)
- Transaction records with statuses (pending, successful, failed)
- Swagger API documentation

---

## 🛠 Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- SQLite 
- JWT Authentication (djangorestframework-simplejwt)

---



## 📦 Installation

1. **Clone the Repository**

```bash
git clone https://github.com/oys2021/finpay.git
cd finpay

```

2. **Create & Activate a Virtual Environment**

```bash
python -m venv venv
venv\Scripts\activate
```


3.**Install Dependencies**
```bash
pip install -r requirements.txt
```

4.**Apply Migrations**
```bash
python manage.py migrate.
Note : connect to your prefered Database before applying migrations.This current code uses Postgresql
```

5. 📘 **Swagger Docs**
Visit http://localhost:8000/api/docs/ for interactive Swagger documentation.

To enable Swagger, make sure you've installed and configured drf-yasg.
