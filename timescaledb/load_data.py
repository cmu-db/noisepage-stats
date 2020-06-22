import json
import psycopg2
from pathlib import Path
import xml.etree.ElementTree as et
import os


CONNECTION = "postgres://postgres:postgres@localhost:5433/test_db"
BASEPATH = Path(__file__).parent
TABLENAME = 'test_table'


def create_table(conn):
    """Create and install timescaledb plug-in if not exists.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
    
    """
    CREATE_SQL = """
        CREATE TABLE %s (
            id SERIAL,
            time TIMESTAMPTZ,
            db_version TEXT,
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
    """ % TABLENAME
    INSTALL_TIMESCALE = """
        CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;
    """
    CONVERT_TO_HYPERTABLE_SQL = """
        SELECT create_hypertable('%s', 'time');
    """ % TABLENAME
    CREATE_INDEX_SQL = """
        CREATE INDEX ON %s (git_commit_id, time DESC);
    """ % TABLENAME
    cur = conn.cursor()
    cur.execute(CREATE_SQL)
    cur.execute(INSTALL_TIMESCALE)
    cur.execute(CONVERT_TO_HYPERTABLE_SQL)
    cur.execute(CREATE_INDEX_SQL)
    conn.commit()
    cur.close()


def read_and_insert_from_folder(conn, path):
    """Read data from folder and insert those data into database.

    Currently this only support the structure as show in test_data. If we want
    to read data from folders with other structure, we need to re-write the
    reading part.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
        path (str): The parent destination folder.

    """
    # TODO(benliangw): These data are not included in expconfig and summary file.
    branch = 'master'
    query_mode = 'extended'
    build_id = 35
    git_commit_id = '4ed4617'

    for subdir, dirs, files in os.walk(path):
        if subdir != str(path):
            benchmark_type, timestamp, db_version, throughput, scalefactor, terminals = read_from_summary(
                os.path.join(subdir, 'oltpbench.summary'))
            weight = read_from_expconfig(
                os.path.join(subdir, 'oltpbench.expconfig'))
            insert_data(conn, time=timestamp, db_version=db_version, 
                        branch=branch, query_mode=query_mode, build_id=35, 
                        git_commit_id=git_commit_id, benchmark_type=benchmark_type, 
                        scalefactor=scalefactor, terminals=terminals, weight=weight, 
                        result=json.dumps({'throughput': throughput}))


def read_from_summary(path):
    """Read data from file ends with ".summary".

    Args:
        path (str): The position of the summary file.
        
    Returns:
        benchmark_type (str): The type of benchmark. It could be noop/smallbank/tatp
        timestamp (str): The timestamp when the benchmark was created in milliseconds.
        db_version (str): The version of NoisePage Database.
        throughput (str): The throughtput calculated by benchmark testing.
        scalefactor (str): The scalefactor used for benchmark testing.
        terminals (str): The number of terminals used for benchmark testing.

    """
    f = open((BASEPATH / path).resolve())
    summary = json.load(f)
    f.close()
    result = {}
    return summary['Benchmark Type'], summary['Current Timestamp (milliseconds)'], summary['DBMS Version'], summary['Throughput (requests/second)'], summary['scalefactor'], summary['terminals']


def read_from_expconfig(path):
    """Read data from file ends with ".expconfig".

    Args:
        path (str): The position of the expconfig file.
        
    Returns:
        json_data (json): The weight used for benchmark.

    """
    weight_data = {}
    root = et.parse((BASEPATH / path).resolve()).getroot()
    transactiontypes = root.find('transactiontypes').findall('transactiontype')
    weights = root.find('works').find('work').findall('weights')
    for weight, transactiontype in zip(weights, transactiontypes):
        weight_data[transactiontype.find('name').text] = int(weight.text)
    json_data = json.dumps(weight_data)
    return json_data


def insert_data(conn, time, db_version, branch, query_mode, build_id, git_commit_id, benchmark_type, scalefactor, terminals, weight, result):
    """Insert data to TimeScaleDB.

    # TODO(benliangw): Use pgcopy to insert rows faster (https://docs.timescale.com/latest/tutorials/quickstart-python#create_table)

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
        time (int): Start time of the performance testing.
        db_version (str): The version of NoisePage.
        branch (str): The branch name of the tested pull request.
        query_mode (str): The query mode when running the run_junit.py.
        build_id (str): The build ID in Jenkins.
        git_commit_id (str): The commit ID of the pull request.
        benchmark_type (str): The type of benchmark testing.
        scalefactor (str): The size of the database to load.
        terminals (str): The number of client threads that will issue requests to the DBMS.
        weight (json): The weight of transactions.
        result (json): Currently we only have one result needed to be stored. Possible values are throughput.

    """
    INSERT_SQL = """
        INSERT INTO %s (
            time, db_version, branch, query_mode, build_id, git_commit_id, 
            benchmark_type, scalefactor, terminals, weight, result
        ) VALUES (
            to_timestamp(%s/1000), '%s', '%s', '%s', '%s', '%s', '%s', 
            %s, %s, '%s', '%s'
        );
    """ % (TABLENAME, time, db_version, branch, query_mode, build_id, 
        git_commit_id, benchmark_type, scalefactor, terminals, weight, result)
    cur = conn.cursor()
    try:
        cur.execute(INSERT_SQL)
    except (Exception, psycopg2.Error) as error:
        print(error.pgerror)
    conn.commit()
    cur.close()


def check_table_exist(conn):
    """Check if a table exists. 
    
    We do not use IF EXISTS in creating the table so as to we will not create
    hyper table twice when the table already exists.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
        
    Returns:
        True if table exists. False is table does not exist.

    """
    CHECK_SQL = """
        SELECT EXISTS (
            SELECT FROM pg_tables
            WHERE tablename = '%s'
        );
    """ % TABLENAME
    cur = conn.cursor()
    cur.execute(CHECK_SQL)
    result = cur.fetchall()[0][0]
    cur.close()
    return result


def drop_table(conn):
    """Drop a table. This is only used for testing purpose.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.

    """
    DROP_SQL = """
        DROP TABLE IF EXISTS %s
    """ % TABLENAME
    cur = conn.cursor()
    cur.execute(DROP_SQL)
    conn.commit()
    cur.close()


# TODO(benliangw): This is only used for testing purpose.
def view_all_results(conn):
    """View all results within the TimeScaleDB. This is only used for testing purpose.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.

    """
    QUERY_SQL = """
        SELECT * FROM %s;
    """ % TABLENAME
    # QUERY_SQL = """
    #     SELECT * FROM %s WHERE weight @> '{"Others": 25}';
    # """ % TABLENAME
    # QUERY_SQL = """
    #     SELECT * FROM %s WHERE weight ? 'Others';
    # """ % TABLENAME
    cur = conn.cursor()
    cur.execute(QUERY_SQL)
    for i in cur.fetchall():
        print(i)
    cur.close()


def main():
    conn = psycopg2.connect(CONNECTION)
    # drop_table(conn)
    table_existence = check_table_exist(conn)
    if table_existence == False:
        create_table(conn)
        print("Finish creating")
    read_and_insert_from_folder(conn, (BASEPATH / 'test_data').resolve())
    view_all_results(conn)
    print("Done")


if __name__ == "__main__":
    main()
