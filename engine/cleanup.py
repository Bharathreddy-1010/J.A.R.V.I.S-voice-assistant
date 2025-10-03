import sqlite3

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Delete duplicate Safari entries
'''cursor.execute("""
    DELETE FROM sys_commands
    WHERE rowid NOT IN (
        SELECT MIN(rowid)
        FROM sys_commands
        WHERE name = 'Safari'
        GROUP BY name, path
    )
""")

con.commit()
con.close()

print("✅ Duplicate 'Safari' rows removed.")'''





'''cursor.execute("DELETE FROM contacts_1;")

# Reset auto-increment ID (optional)


con.commit()
con.close()

print("✅ All contacts deleted.")'''