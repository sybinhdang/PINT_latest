import sqlite3

import pandas as pd

# Create your connection.

cnx = sqlite3.connect('C:\Users\DAB5HC\Documents\workspace\Tool\Tool_PIN_2\S68T0_90V202439B\.eASEE\snapshot.lws.cc.db3')



df = pd.read_sql_query("SELECT * FROM Artifacts", cnx)

print(df['Name'][0])

print(df['Class'][0])