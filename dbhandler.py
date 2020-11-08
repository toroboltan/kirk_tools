import pandas as pd
from sqlalchemy import create_engine

def ConnectSQLDb(db_prefix ,db_struct):
    ''' Connect to SQL database '''
    #Seteo el USER : PASS @ HOST / BBDD_NAME
    #sql_engine = create_engine('mysql+pymysql://root:@localhost/etfscreendb')
    print('ConnectSQLDb - beg')
    print('db_prefix ' + db_prefix)
    print('db_struct ' + db_struct)
    sql_engine = create_engine(db_prefix + db_struct)
    print('create_engine executed')
    sql_conn = sql_engine.connect()
    print('sql_engine executed')
    print('ConnectSQLDb - end')
    return sql_conn

def ReadSQLTable(sql_conn, db_table):
    ''' Read data from SQL db and returns pandas df '''
    data_df = pd.read_sql(db_table, con=sql_conn)
    return data_df

def WriteSQLTable(df, sql_conn, db_table):
    ''' Write data from SQL db and returns pandas df '''
    print('WriteSQLTable - beg')
    print('db_table ' + db_table)
    df.to_sql(con=sql_conn, name=db_table, if_exists='replace')
    print('WriteSQLTable - end')

def main(arg):
    # Formatting pandas to have 2 decimal points
    pd.options.display.float_format = "{:,.2f}".format
    print('___Begin main()___')
    if arg == 'test01':
        print('test 01')
    if arg == 'test02':
        print('test 02')
    if arg == 'test03':
        print('test 03')
    if arg == 'test04':
        print('test04')
    print('___End main()___')

if __name__ == "__main__":
    arg = 'test04'
    try:
        main(arg)
    except SystemExit as e:
        print('Error Exception triggered')