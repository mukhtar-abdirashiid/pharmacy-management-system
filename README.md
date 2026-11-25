# Pharmacy Management System

A Django web application for managing medicine categories, medicine inventory, customers, and medicine sales.

## Features
- Dashboard with medicine, customer, and sales summaries
- Category CRUD
- Medicine CRUD, stock quantities, expiry dates, and search by name/category
- Customer CRUD
- Record sales with stock validation and automatic stock deduction
- SQLite database, Django ModelForms validation, Bootstrap navigation

## Requirements
- Python 3.10+
- Git
- Visual Studio Code

## Run locally (Windows PowerShell)
1. Open this folder in VS Code.
2. Create a virtual environment:
   ```powershell
   py -m venv .venv
   ```
3. Activate it:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt:
   ```cmd
   .venv\Scripts\activate.bat
   ```
4. Install Django:
   ```powershell
   python -m pip install -r requirements.txt
   ```
5. Create database tables:
   ```powershell
   python manage.py makemigrations
   python manage.py migrate
   ```
6. (Optional) Create an administrator:
   ```powershell
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```powershell
   python manage.py runserver
   ```
8. Open http://127.0.0.1:8000/ in your browser.

## GitHub collaboration
- Follow your instructor's repository/fork instructions first.
- One member can create the project repository and invite teammates as collaborators (or use the instructor's repository).
- Each student should work on a separate branch:
  ```bash
  git checkout -b feature/student-name
  ```
- Make meaningful changes, then:
  ```bash
  git add .
  git commit -m "Add medicine search and inventory form"
  git push -u origin feature/student-name
  ```
- Open a Pull Request on GitHub, ask another member to review it, then merge it.
- Each student must make at least three meaningful commits. Do not create empty commits just to reach the number; make real improvements and explain them in commit messages.
- Do not commit `.venv/`, `db.sqlite3`, passwords, or secret keys.

## Suggested team responsibilities
- Member 1: categories and medicines
- Member 2: customers and customer forms
- Member 3: sales and stock deduction
- Member 4: dashboard, styling, testing, and README
All members should review, test, and integrate one another's work.

## Important
This is an educational demonstration. It is not a validated production pharmacy or medical-record system. Use test data only.
