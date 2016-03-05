import sqlite3

def sqlite_parser(filepath):
    formatted_output = {}
    conn = sqlite3.connect(filepath)
    c = conn.cursor()
    tables = c.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    for table in tables:
        table_name = str(table[1])
        columns = c.execute("PRAGMA table_info('" + table_name + "')").fetchall()
        columns_names = [str(column[1]) for column in columns]
        values_list = []
        for values in c.execute("SELECT * from " + table_name).fetchall():
            formatted_row = {}
            for i in range(0, len(values)):
                formatted_row[columns_names[i]] = str(values[i])
            values_list.append(formatted_row)
        formatted_output[table_name] = values_list
    return formatted_output


"""
sqlitefile = "/media/daudau/ce551a8e-94b5-4b2c-889c-51f906c103a5/disk2/Users/IEUser/AppData/Local/Google/Chrome/User Data/Default/Cookies"
for i in sqlite_parser(sqlitefile)['cookies']:
    print i
    print "\n"
"""

