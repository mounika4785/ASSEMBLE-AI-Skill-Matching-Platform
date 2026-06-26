# Import Flask to create server
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import our AI function

from model import match_students

# Create app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/')
def home():
    return "Server is running"


# Create API route
@app.route('/match', methods=['POST'])
def match():

    data = request.get_json()

    # 🔥 SAFE CHECK
    if not data:
        return jsonify({"error": "No data received"}), 400

    print("Received:", data)

    students = data.get('students', [])
    opportunity = data.get('opportunity', {})

    # 🔥 EXTRA SAFETY
    if "required_skills" not in opportunity:
        return jsonify({"error": "Missing required_skills"}), 400

    results = match_students(students, opportunity)

    return jsonify(results)

# Run server
if __name__ == "__main__":
    app.run(debug=True)