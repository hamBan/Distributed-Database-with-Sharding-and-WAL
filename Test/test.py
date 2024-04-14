import mysql.connector

connection = mysql.connector.connect(
    host="DB1",
    user="root",
    password="abc",
    database="shardsDB"
)

cursor = connection.cursor()
# cursor.execute("CREATE TABLE IF NOT EXISTS Shard1(Stud_id INT,Stud_name VARCHAR(255),Stud_marks INT);")
# cursor.execute("SELECT * FROM mysql.general_log;")
# cursor.execute("INSERT INTO Shard1 (Stud_id, Stud_name, Stud_marks) VALUES (20, 'Soham', 10);")
# connection.commit()
cursor.execute("SELECT * FROM sh3;")
for row in cursor.fetchall():
  print(row)

connection.close()
