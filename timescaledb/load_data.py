import numpy
import psycopg2


CONNECTION = "postgres://postgres:postgres@localhost:5433/test_db"


def create_table(conn):
    CREATE_SQL = """
        CREATE TABLE test_table (
            id SERIAL,
            time TIMESTAMPTZ,
            branch TEXT,
            query_mode TEXT,
            build_id TEXT,
            git_commit_id TEXT,
            benchmark_type TEXT,
            scalefactor NUMERIC,
            terminals NUMERIC,
            weight JSONB, 
            result JSONB
        );
    """
    INSTALL_TIMESCALE = """
        CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
    """
    CONVERT_TO_HYPERTABLE_SQL = """
        SELECT create_hypertable('test_table', 'time');
    """
    CREATE_INDEX_SQL = """
        CREATE INDEX ON test_table (git_commit_id, time DESC);
    """
    cur = conn.cursor()
    cur.execute(CREATE_SQL)
    cur.execute(INSTALL_TIMESCALE)
    cur.execute(CONVERT_TO_HYPERTABLE_SQL)
    cur.execute(CREATE_INDEX_SQL)
    conn.commit()
    cur.close()


def read_and_insert_from_folder(conn, path):
    # TODO(benliangw): Add read part later.
    insert_data(conn, 123456789, 'master', 'extended', 35, '4ed4617', 'smallbank', 1.0, 4, '{"Amalgamate": 15, "Balance": 15, "DepositChecking": 10, "Others": 25, "TransactSavings": 15, "WriteCheck": 15}', '{"throughput": "20.36"}')


def insert_data(conn, time, branch, query_mode, build_id, git_commit_id, benchmark_type, scalefactor, terminals, weight, result):
    INSERT_SQL = """
        INSERT INTO test_table (
            time, branch, query_mode, build_id, git_commit_id, benchmark_type, scalefactor, terminals, weight, result
        ) VALUES (
            to_timestamp(%s), '%s', '%s', '%s', '%s', '%s', %s, %s, '%s', '%s'
        );
    """ % (time, branch, query_mode, build_id, git_commit_id, benchmark_type, scalefactor, terminals, weight, result)
    cur = conn.cursor()
    try:
        cur.execute(INSERT_SQL)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)
    conn.commit()



def check_table_exist(conn):
    CHECK_SQL = """
        SELECT EXISTS (
            SELECT FROM pg_tables
            WHERE tablename = 'test_table'
        );
    """
    cur = conn.cursor()
    cur.execute(CHECK_SQL)
    result = cur.fetchall()[0][0]
    return result


# TODO(benliangw): This is only used for testing purpose.
def view_all_results(conn):
    # QUERY_SQL = """
    #     SELECT * FROM test_table;
    # """
    QUERY_SQL = """
        SELECT * FROM test_table WHERE weight @> '{"Others": 25}';
    """
    # QUERY_SQL = """
    #     SELECT * FROM test_table WHERE weight ? 'Others';
    # """
    cur = conn.cursor()
    cur.execute(QUERY_SQL)
    for i in cur.fetchall():
        print(i)
    cur.close()

# TODO(benliangw): Use pgcopy to insert rows faster (https://docs.timescale.com/latest/tutorials/quickstart-python#create_table)
def main():
    print("Hello world")
    conn = psycopg2.connect(CONNECTION)
    table_existence = check_table_exist(conn)
    print(table_existence)
    if table_existence == False:
        create_table(conn)
        print("Finish creating")
    # read_and_insert_from_folder(conn, "./testdata")
    view_all_results(conn)
    print("Done")

if __name__ == "__main__":
    main()