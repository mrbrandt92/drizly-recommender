from sqlalchemy import create_engine
import pymysql
import pandas as pd


db_user = 'drizly_user'
db_password = 'DRIZLY2021'
db_host = 'drizly.cpby0wrcbicx.us-east-2.rds.amazonaws.com'
db_database = 'drizly'


def search(user_id):

        db_connection_str = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_database}"
        db_connection = create_engine(db_connection_str)

        cats_df = pd.read_sql('SELECT * FROM drizlycats', con=db_connection)
        user_row_df = pd.read_sql('SELECT * FROM drizlyusers WHERE user_id_hash= \''
                           + str(user_id) + '\'', con=db_connection)

        return cats_df, user_row_df
