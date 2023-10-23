import json
import sqlite3
import itertools
from jsonpath_ng.ext import parse

def json_to_sql_multiple_tables(json_file, mapping_config, db_file):
    """Converts a JSON file to multiple SQL database tables.

    Args:
    json_file: The path to the JSON file.
    mapping_config: User defined relational schema mapping(config.json).
    db_file: The path to the SQL database file.
    """

    # Create a connection to the SQL database.
    conn = sqlite3.connect(db_file)

    # Create a cursor.
    cur = conn.cursor()
              
    # Insert the data into the tables.
    with open(json_file, "r") as f:
        json_data = json.load(f)
    key_values = []
    insert_queries = []
    for item_name, table_config in mapping_config.items():
        if item_name == 'db_config':
            for item, item_config in table_config.items():
                #delete table if exists
                del_sql = "DROP TABLE IF EXISTS {}".format(item)
                cur.execute(del_sql)
                #create table
                sql = "CREATE TABLE IF NOT EXISTS {} ({})".format(item, ",".join(item_config['columns']))
                cur.execute(sql)
                #key_values for preparing insert queries
                key_values.append([item.split(' ')[0] for item in item_config['columns']])
                for key in key_values:
                    insert_sql = "INSERT INTO {} ({}) VALUES ({})".format(item, ",".join(key), ",".join(["?"] * len(key)))
                insert_queries.append(insert_sql)
        elif item_name == 'schema_map':
            for i in range(len(key_values)):
                values = []
                for j in range(len(key_values[i])):
                    #collecting values for keys using schema_map
                    #autoincrement - ids not specified in json file (created in else)
                    if table_config[key_values[i][j]] != 'autoincrement':
                        matches = []
                        jsonpath_expr = parse(table_config[key_values[i][j]])
                        for arow in json_data:
                            amatch = [match.value for match in jsonpath_expr.find(arow)]
                            if len(amatch)>1:
                                matches.append(', '.join([str(match.value) for match in jsonpath_expr.find(arow)]))
                            else:
                                matches.append([match.value for match in jsonpath_expr.find(arow)][0])
                        values.append(matches)
                    else:
                        values.append([item for item in range(1, len(json_data)+1)])
                #creating tuples to insert into SQL tables
                for k in range(len(json_data)):
                    tuple_array = []
                    for l in range(len(values)):
                        tuple_array.append(values[l][k])
                    tuple_array = tuple(tuple_array)
                    cur.execute(insert_queries[i], tuple_array)
                    conn.commit()
        else:
                pass
                                    

    # Commit the changes.
    conn.commit()
    
    #returning cur and conn to execute queries outside the function
    return cur, conn

#Preparing to execute
config_file = 'config.json'
with open(config_file, "r") as f:
    mapping_config = json.load(f)
#json file, db file and sql query from mapping config    
json_file = mapping_config['json_file']
db_file = mapping_config['db_file']
sql_query = mapping_config['sql_query']

#run the function
cur, conn = json_to_sql_multiple_tables(json_file, mapping_config, db_file)

#run and print sql query results
cur.execute(sql_query)
print(cur.fetchall())

#close cursor and connection
cur.close()
conn.commit()