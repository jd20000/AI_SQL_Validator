**README.md**

# SQL Query Validator

## Overview
This is a Flask-based web application that validates SQL query syntax entered by the user. The app checks whether the syntax is correct and highlights errors if present. The frontend is built using Tailwind CSS, and the backend uses SQLite for query validation.

## Features
- **SQL Syntax Validation**: Checks for correct SQL syntax without executing the query.
- **Error Suggestions**: Identifies syntax errors and missing elements in SQL queries.
- **User-Friendly Interface**: Built with Tailwind CSS for a clean and responsive design.
- **Lightweight & Fast**: Uses Flask and SQLite's in-memory database for validation.

## Installation
### Prerequisites
- Python 3.x
- pip

### Steps to Install & Run
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd sql-query-validator
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On macOS/Linux
   venv\Scripts\activate      # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```bash
   python app.py
   ```
5. Open your browser and visit `http://127.0.0.1:5000/`

## Folder Structure
```
SQL Validator/
│── database/
│   ├── schema.sql
│── static/
│   ├── style.css
│── templates/
│   ├── index.html
│── app.py
│── requirements.txt
│── README.md
```

## API Endpoint
- **POST /validate**
  - Request Body: `{ "query": "SQL_QUERY_HERE" }`
  - Response:
    ```json
    { "status": "success", "message": "SQL syntax is correct." }
    ```
    ```json
    { "status": "error", "message": "Invalid SQL syntax: Missing data type." }
    ```

