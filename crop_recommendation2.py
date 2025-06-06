import csv
import mysql.connector


def load_csv_data(filename="Crop_recommendation.csv"):
    data = []
    with open(filename, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append({
                "N": float(row["N"]),
                "P": float(row["P"]),
                "K": float(row["K"]),
                "temperature": float(row["temperature"]),
                "humidity": float(row["humidity"]),
                "ph": float(row["ph"]),
                "rainfall": float(row["rainfall"]),
                "label": row["label"]
            })
    return data

def recommend_crop(user_input, data):
    min_diff = float("inf")
    recommended_crop = None
    for row in data:
        diff = sum([
            abs(row["N"] - user_input["N"]),
            abs(row["P"] - user_input["P"]),
            abs(row["K"] - user_input["K"]),
            abs(row["temperature"] - user_input["temperature"]),
            abs(row["humidity"] - user_input["humidity"]),
            abs(row["ph"] - user_input["ph"]),
            abs(row["rainfall"] - user_input["rainfall"])
        ])
        if diff < min_diff:
            min_diff = diff
            recommended_crop = row["label"]
    return recommended_crop

def save_to_mysql(user_input, recommendation):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",  
        password="Jesus@840",  
        database="crop_db"
    )
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recommendations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            N FLOAT, P FLOAT, K FLOAT,
            temperature FLOAT, humidity FLOAT, ph FLOAT, rainfall FLOAT,
            recommended_crop VARCHAR(100)
        )
    """)
    cursor.execute("""
        INSERT INTO recommendations 
        (N, P, K, temperature, humidity, ph, rainfall, recommended_crop)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        user_input["N"], user_input["P"], user_input["K"],
        user_input["temperature"], user_input["humidity"],
        user_input["ph"], user_input["rainfall"], recommendation
    ))
    conn.commit()
    conn.close()

def get_user_input():
    return {
        "N": float(input("Enter Nitrogen level (N): ")),
        "P": float(input("Enter Phosphorus level (P): ")),
        "K": float(input("Enter Potassium level (K): ")),
        "temperature": float(input("Enter Temperature (°C): ")),
        "humidity": float(input("Enter Humidity (%): ")),
        "ph": float(input("Enter pH: ")),
        "rainfall": float(input("Enter Rainfall (mm): "))
    }

def main():
    data = load_csv_data()
    user_input = get_user_input()
    recommended_crop = recommend_crop(user_input, data)
    print("Recommended Crop:", recommended_crop)
    save_to_mysql(user_input, recommended_crop)

if __name__ == "__main__":
    main()


import mysql.connector

def fetch_recommendations():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",         
            password="Jesus@840",   
            database="crop_db"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM recommendations")
        rows = cursor.fetchall()
        
        print("\n Stored Recommendations:")
        for row in rows:
            print(row)

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

if __name__ == "__main__":
    fetch_recommendations()
