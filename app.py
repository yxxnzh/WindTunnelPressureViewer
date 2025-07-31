
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pymysql
import os

app = Flask(__name__)
CORS(app)

def get_connection():
    return pymysql.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASS"),
        database=os.environ.get("DB_NAME"),
        connect_timeout=5,
        read_timeout=10, 
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index_html():
    return render_template('index.html')

@app.route('/Sensor_Data')
def Sensor_Data():
    return render_template('Sensor_Data.html')

@app.route('/Correlation_Analysis')
def Correlation_Analysis():
    return render_template('Correlation_Analysis.html')

@app.route('/Prediction')
def Prediction():
    return render_template('Prediction.html')

@app.route('/page4')
def page4():
    return render_template('page4.html')

@app.route('/page5')
def page5():
    return render_template('page5.html')

@app.route('/api/pressure')
def get_all_pressure_data():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT P1, P2, P3, P4, P5 FROM pressure_sensor_data")
            rows = cursor.fetchall()
        return jsonify(rows)
    except pymysql.MySQLError as e:
        print("[MYSQL ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    except Exception as e:
        print("[GENERIC ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/pressure/<sensor_name>')
def get_sensor_history(sensor_name):
    conn = None
    try:
        valid_sensors = ['P1', 'P2', 'P3', 'P4', 'P5']
        if sensor_name not in valid_sensors:
            return jsonify({'error': 'Invalid sensor name'}), 400

        conn = get_connection()
        with conn.cursor() as cursor:
            query = f"""
                SELECT `{sensor_name}` AS value
                FROM pressure_sensor_data
                ORDER BY timestamp DESC
                LIMIT 4500
            """
            cursor.execute(query)
            rows = cursor.fetchall()[::-1]  # 최신 데이터부터 가져와서 다시 정순으로

        return jsonify(rows)
    except pymysql.MySQLError as e:
        print("[MYSQL ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    except Exception as e:
        print("[GENERIC ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    finally:
        if conn:
            conn.close()

@app.route('/api/pressure/latest')
def get_latest_pressure():
    conn = None
    try:
        conn = get_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT P1, P2, P3, P4, P5
                FROM pressure_sensor_data
                ORDER BY timestamp DESC
                LIMIT 1
            """)
            row = cursor.fetchone()

        if not row:
            return jsonify({'error': 'No data found'}), 404

        result = [
            {"sensor": "P1", "value": row["P1"]},
            {"sensor": "P2", "value": row["P2"]},
            {"sensor": "P3", "value": row["P3"]},
            {"sensor": "P4", "value": row["P4"]},
            {"sensor": "P5", "value": row["P5"]}
        ]
        return jsonify(result)
    except pymysql.MySQLError as e:
        print("[MYSQL ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    except Exception as e:
        print("[GENERIC ERROR]", repr(e))
        return jsonify({'error': repr(e)}), 500
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
