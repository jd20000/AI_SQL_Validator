from flask import Flask, request, jsonify, render_template
import sqlparse
import re
import google.generativeai as genai  

app = Flask(__name__)

# OpenAI API Key (Replace with your actual key)
genai.configure(api_key="AIzaSyA2IN2hnsRRweAg1T1Io10ArjCsqxpcMKc")
# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

def validate_syntax(query):
    """Validate the syntax of the SQL query using sqlparse."""
    try:
        sqlparse.parse(query)
        return True, "Syntax is valid."
    except Exception as e:
        return False, f"Syntax error: {str(e)}"

def validate_logic(query):
    parsed = sqlparse.parse(query)
    if not parsed:
        return False, "Invalid query."

    # Extract the first statement
    statement = parsed[0]
    query_type = statement.get_type()

    # 🔥 Fix: Handle UNKNOWN query type properly
    if query_type == "UNKNOWN":
        return False, "Unsupported or malformed SQL command."

    # ✅ Logic Validation for Known Queries
    if query_type == "SELECT":
        if "FROM" not in query.upper():
            return False, "Invalid SELECT query. Expected 'SELECT ... FROM ...'."

    elif query_type == "INSERT":
        if "INTO" not in query.upper() or "VALUES" not in query.upper():
            return False, "Invalid INSERT query. Expected 'INSERT INTO ... VALUES (...)'."

    elif query_type == "UPDATE":
        if "SET" not in query.upper():
            return False, "Invalid UPDATE query. Expected 'UPDATE ... SET ...'."

    elif query_type == "DELETE":
        if "FROM" not in query.upper():
            return False, "Invalid DELETE query. Expected 'DELETE FROM ...'."

    elif query_type == "CREATE":
        if "TABLE" not in query.upper() and "DATABASE" not in query.upper():
            return False, "Invalid CREATE query. Expected 'CREATE TABLE ...' or 'CREATE DATABASE ...'."

    elif query_type == "ALTER":
        if "TABLE" not in query.upper():
            return False, "Invalid ALTER query. Expected 'ALTER TABLE ... ADD/DROP/MODIFY ...'."

    elif query_type == "DROP":
        if "TABLE" not in query.upper() and "DATABASE" not in query.upper():
            return False, "Invalid DROP query. Expected 'DROP TABLE ...' or 'DROP DATABASE ...'."

    else:
        return False, f"Unsupported SQL command: {query_type}."

    return True, "Query is logically valid."


def correct_query_with_ai(query):
    try:
        response = model.generate_content(f"Correct this SQL query: {query}")
        return response.text.strip() if hasattr(response, "text") else "AI correction unavailable. Please check manually."
    except Exception as e:
        print("Google AI API Error:", str(e))
        return "AI correction unavailable. Please check manually."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/validate', methods=['POST'])
def validate():
    data = request.json
    print("Received Data:", data)  # Debugging step

    if not data or "query" not in data:
        return jsonify({"message": "No query provided."}), 400

    query = data["query"].strip()
    if not query:
        return jsonify({"message": "Query is empty."}), 400

    # Validate and correct query
    is_syntax_valid, syntax_message = validate_syntax(query)

    is_logic_valid, logic_message = validate_logic(query)

    if is_syntax_valid and is_logic_valid:
        return jsonify({"message": "Query is valid!"}), 200

    suggestion = correct_query_with_ai(query)
    print(f"Syntax Valid: {is_syntax_valid}, Logic Valid: {is_logic_valid}, AI Suggestion: {suggestion}")  # Debugging
   
    return jsonify({
        "message": logic_message if not is_logic_valid else syntax_message,
        "suggestion": suggestion
    }), 400

if __name__ == '__main__':
    app.run(debug=True)
