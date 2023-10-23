JSON to Relational SQL Table Converter

This is a Python script that converts a JSON file into relational SQL tables using the SQLite database engine. The script leverages the sqlite3 library for database operations and the jsonpath library to extract data from the JSON file.

Args:
json_file: The path to the input JSON file. The json_file is going to be user-provided
mapping_config: User defined relational schema mapping(config.json).
db_file: The path to the SQL database file. 
sql_query: Query that user wants to execute (Note: Currently single query is being supported)

Prerequisites:
pip install requirements.txt
Before using this script, ensure that you have the following prerequisites installed:

Python (3.x recommended)
sqlite3: The sqlite3 library is included in the Python standard library, so no additional installation is required.
jsonpath_ng: You can install this library using pip:
Copy code


Usage
Download or clone the repository containing the script to your local machine.

Place your JSON file that you want to convert into the same directory as the script.
Edit the script and modify the json_file variable with the name of your JSON file. For example:

python
Copy code
json_file = 'your_data.json'
Define the structure of your JSON file by specifying JSONPath expressions in the table_structure dictionary. For example:

python
Copy code
"db_config": 
    {
    "table_name": {"columns": ["attr1", "attr2".....]}
    }
    
Run the script:

Copy code
python json_to_sql.py
The script will create an SQLite database file named data.db and generate relational tables based on the structure defined in the table_structure dictionary.

You can now use the SQLite database for querying and data analysis.




