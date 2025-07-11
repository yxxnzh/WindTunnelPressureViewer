import csv
import pymysql
from datetime import datetime

# MySQL 연결
db = pymysql.connect(
    host="mainline.proxy.rlwy.net",
    port=31572,
    user="root",
    password="wDyKBfJCqAeyailHJrWAyJgvKkQNOCbF",
    database="railway"
)
cursor = db.cursor()

with open("pressure_sensor_data.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        # 필요한 값만 출력 (디버그용)
        print("삽입 중:", row)

        # None 값 혹은 공백 있는지 체크
        if not all(row[k] for k in ['P1', 'P2', 'P3', 'P4', 'P5']):
            print("🚫 누락된 값 있어 패스:", row)
            continue

        cursor.execute("""
            INSERT INTO pressure_sensor_data (timestamp, P1, P2, P3, P4, P5)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            datetime.now(),
            row['P1'], row['P2'], row['P3'], row['P4'], row['P5']
        ))

db.commit()
cursor.close()
db.close()

print("✅ CSV import 완료!")
