from flask import Flask, render_template, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# ---- Database Connection ----
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # your MySQL username
        password="",          # your MySQL password (default empty for XAMPP)
        database="movie_prediction"
    )

# ---- Ensure Table Exists ----
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            movie_name VARCHAR(255),
            rating FLOAT,
            review TEXT,
            prediction_result VARCHAR(50),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

init_db()

@app.route("/")
def index():
    return render_template("index1.html")

@app.route("/save", methods=["POST"])
def save():
    data = request.get_json()
    movie_name = data.get("movie_name")
    rating = data.get("rating")
    review = data.get("review")
    prediction = data.get("prediction")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (movie_name, rating, review, prediction_result, created_at) VALUES (%s, %s, %s, %s, %s)",
            (movie_name, rating, review, prediction, datetime.now())
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"status": "success", "message": "Prediction saved!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
