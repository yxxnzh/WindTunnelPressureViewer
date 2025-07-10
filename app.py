from flask import Flask, jsonify, render_template
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

db = pymysql.connect(
    host='localhost',
    user='root',      
    password='1234',  
    database='pressure_sensor_data', 
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/pressure')
def get_all_pressure_data():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT P1, P2, P3, P4, P5 FROM pressure_sensor_data")
            rows = cursor.fetchall()
            return jsonify(rows)
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'error': str(e)}), 500


@app.route('/api/pressure/<sensor_name>')
def get_sensor_history(sensor_name):
    try:
        if sensor_name not in ['P1', 'P2', 'P3', 'P4', 'P5']:
            return jsonify({'error': 'Invalid sensor name'}), 400

        with db.cursor() as cursor:
            # 해당 센서의 전체 값 이력 가져오기
            query = f"SELECT {sensor_name} AS value FROM pressure_sensor_data"
            cursor.execute(query)
            rows = cursor.fetchall()
            return jsonify(rows)
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/api/pressure/latest')
def get_latest_pressure():
    try:
        with db.cursor() as cursor:
            cursor.execute("""
                SELECT P1, P2, P3, P4, P5
                FROM pressure_sensor_data
                ORDER BY 1 DESC
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
    except Exception as e:
        print("[ERROR]", str(e))
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
