import csv
import sqlite3
con = sqlite3.connect("jarvis.db")     
cursor = con.cursor()   


'''query = "CREATE TABLE IF NOT EXISTS sys_commands (id integer primary key,name VARCHAR(100),path VARCHAR(100))"
cursor.execute(query)

#insert into table
query = "INSERT INTO sys_commands VALUES(null,'Safari','/System/Applications/Calculator.app')"
cursor.execute(query)
con.commit()

#table web_command
query = "CREATE TABLE IF NOT EXISTS web_commands (id integer primary key,name VARCHAR(100),url VARCHAR(1000))"
cursor.execute(query)'''

'''query = "INSERT INTO web_commands VALUES(null,'youtube','https://www.youtube.com')"
cursor.execute(query)
con.commit()'''


#cursor.execute('''CREATE TABLE IF NOT EXISTS contacts_1 (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255), email VARCHAR(255) NULL)''')



# These are the correct indices based on your CSV
'''NAME_INDEX = 0
PHONE_INDEX = 18

with open('contacts_1.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    headers = next(csvreader)  # Skip header row

    for row_num, row in enumerate(csvreader, start=1):
        if len(row) > PHONE_INDEX:
            name = row[NAME_INDEX].strip()
            phone = row[PHONE_INDEX].strip()

            if name and phone:
                cursor.execute(
                    "INSERT INTO contacts_1 (id, name, mobile_no) VALUES (NULL, ?, ?)",
                    (name, phone)
                )
            else:
                print(f"⚠️ Row {row_num}: Missing name or phone")
        else:
            print(f"⚠️ Row {row_num}: Not enough columns (has {len(row)})")

# Commit and close
con.commit()
con.close()
print("✅ Contacts imported successfully.")'''

'''query = 'vinay'
query = query.strip().lower()

cursor.execute("SELECT mobile_no FROM contacts_1 WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?", ('%' + query + '%', query + '%'))
results = cursor.fetchall()
print(results[0][0])'''


#query = "INSERT INTO contacts_1 VALUES (null,'vinay D', '8019271429', 'null')"
#cursor.execute(query)
#con.commit()