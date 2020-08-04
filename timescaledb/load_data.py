import json
import psycopg2
from pathlib import Path
import xml.etree.ElementTree as et
import os
import argparse
import wget
import csv
import subprocess
from time import time

# I guess I shouldn't set password here?
CONNECTION = "postgres://username:password@localhost:30003/pss_database"
TABLENAME = 'oltpbench_results'
UNKNOWN_RESULT = 'unknown'
LATENCY_ATTRIBUTE_MAPPING = [
    ('l_25','25'),('l_75','75'),('l_90','90'), ('l_95','95'), ('l_99','99'),
    ('avg','average'),('median','median'),('min','minimum'), ('max','maximum')]

def get_value_by_pattern(dict_obj, pattern, default):
    """
    This is similar to .get() for a dict but it matches the
    key based on a substring. This function is case insensitive.
    """
    for key, value in dict_obj.items():
        if pattern.lower() in key.lower():
            return value
    return default

def create_table(conn):
    """Create and install timescaledb plug-in if not exists.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
    
    """
    CREATE_SQL = """
        CREATE TABLE %s (
            id SERIAL,
            time TIMESTAMPTZ,
            git_branch TEXT,
            git_commit_id TEXT,
            jenkins_job_id TEXT,
            db_version TEXT,
            environment JSONB,
            benchmark_type TEXT,
            query_mode TEXT,
            scale_factor NUMERIC,
            terminals NUMERIC,
            client_time NUMERIC,
            weights JSONB,
            metrics JSONB,
            incremental_metrics JSONB
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
    # These data are not included in expconfig and summary file.
    branch = 'master'
    query_mode = 'extended'
    jenkins_job_id = 35
    git_commit_id = '4ed4617'
    environment = json.dumps({'os_version': 'Linux-4.15.0-101-generic-x86_64-with-Ubuntu-18.04-bionic', 'cpu_socket': '2', 'cpu_number': '16'})

    for subdir, dirs, files in os.walk(path):
        if subdir != str(path):
            db_version, timestamp, benchmark_type, scalefactor, terminals, metrics = read_from_summary(
                os.path.join(subdir, 'oltpbench.summary'))
            weight, client_time = read_from_expconfig(
                os.path.join(subdir, 'oltpbench.expconfig'))
            incremental_metrics = read_from_res(
                os.path.join(subdir, 'oltpbench.res'))
            insert_data(conn, time=timestamp, git_branch=branch,
            git_commit_id=git_commit_id, jenkins_job_id=jenkins_job_id,
            db_version=db_version, environment=environment, benchmark_type=benchmark_type, query_mode=query_mode,scale_factor=scalefactor, terminals=terminals, client_time=client_time, weights=weight, metrics=metrics, incremental_metrics=incremental_metrics)


def read_from_summary(path):
    """Read data from file ends with ".summary".

    Args:
        path (str): The position of the summary file.
        
    Returns:
        benchmark_type (str): The type of benchmark. It could be noop/smallbank/tatp
        timestamp (str): The timestamp when the benchmark was created in milliseconds.
        db_version (str): The version of NoisePage Database.
        scalefactor (str): The scalefactor used for benchmark testing.
        terminals (str): The number of terminals used for benchmark testing.
        metrics (json): The benchmark test result.

    """
    with open(path) as summary_file:
        summary = json.load(summary_file)
        db_version = summary.get('DBMS Version', UNKNOWN_RESULT)
        timestamp = int(get_value_by_pattern(summary, 'timestamp', str(time())))
        type = summary.get('Benchmark Type', UNKNOWN_RESULT)
        scalefactor = summary.get('scalefactor', '-1.0')
        terminals = int(summary.get('terminals', -1))
        metrics = parse_metrics(summary)
    return db_version, timestamp, type, scalefactor, terminals, metrics


def parse_metrics(summary):
    return json.dumps({
        "throughput" : get_value_by_pattern(summary, 'throughput', '-1.0'),
        "latency": parse_latency_data(summary.get('Latency Distribution',{}))
    })


def parse_latency_data(latency_dict):
    """
    Parses the latency data from the format it is stored in the summary
    file to the format we need for the API request.
    Args:
        latency_dict (dict): The "Latency Distribution" json object in the OLTPBench
        summary file.
    Returns:
        latency (dict): The latency dict required to send to the performance storage
        service.
    """
    latency = {}
    for key, pattern in LATENCY_ATTRIBUTE_MAPPING:
        value = get_value_by_pattern(latency_dict, pattern, None)
        latency[key] = float(value) if value else value
    return latency


def read_from_expconfig(path):
    """Read data from file ends with ".expconfig".

    Args:
        path (str): The position of the expconfig file.
        
    Returns:
        json_data (json): The weight used for benchmark.
        client_time (int): How long did the test run.

    """
    weight_data = {}
    root = et.parse(path).getroot()
    transactiontypes = root.find('transactiontypes').findall('transactiontype')
    client_time = int(root.find('works').find('work').find('time').text)
    weights = root.find('works').find('work').findall('weights')
    for weight, transactiontype in zip(weights, transactiontypes):
        weight_data[transactiontype.find('name').text] = int(weight.text)
    json_data = json.dumps(weight_data)
    return json_data, client_time

def read_from_res(path):
    """Read data from file ends with ".res".

    Args:
        path (str): The position of the res file.
        
    Returns:
        incremental_metrics (list, json array): The throughput at different time.

    """
    time, throughput, min_lat, lat_25th, median_lat, avg_lat, lat_75th, lat_90th, lat_95th, lat_99th, max_lat= [], [], [], [], [], [], [], [], [], [], []
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            time.append(float(row['time(sec)']))
            throughput.append(float(row[' throughput(req/sec)']))
            min_lat.append(float(row[' min_lat(ms)']))
            lat_25th.append(float(row[' 25th_lat(ms)']))
            median_lat.append(float(row[' median_lat(ms)']))
            avg_lat.append(float(row[' avg_lat(ms)']))
            lat_75th.append(float(row[' 75th_lat(ms)']))
            lat_90th.append(float(row[' 90th_lat(ms)']))
            lat_95th.append(float(row[' 95th_lat(ms)']))
            lat_99th.append(float(row[' 99th_lat(ms)']))
            max_lat.append(float(row[' max_lat(ms)']))

    incremental_metrics = [{"time": t, "throughput": tp, "latency": {"min": ml, "l_25": l25, "median": mel, "avg": al, "l_75": l75, "l_90": l90, "l_95": l95, "l_99": l99, "max": mal}} for t, tp, ml, l25, mel, al, l75, l90, l95, l99, mal in zip(time, throughput, min_lat, lat_25th, median_lat, avg_lat, lat_75th, lat_90th, lat_95th, lat_99th, max_lat)]
    return json.dumps(incremental_metrics)

def insert_data(conn, time, git_branch, git_commit_id, jenkins_job_id, db_version, environment, benchmark_type, query_mode, scale_factor, terminals, client_time, weights, metrics, incremental_metrics):
    """Insert data to TimeScaleDB.

    # TODO(benliangw): Use pgcopy to insert rows faster (https://docs.timescale.com/latest/tutorials/quickstart-python#create_table)

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
        time (int): Start time of the performance testing.
        client_time (int): The number of seconds the test was run for.
        db_version (str): The version of NoisePage.
        branch (str): The branch name of the tested pull request.
        query_mode (str): The query mode when running the run_junit.py.
        jenkins_job_id (str): The build ID in Jenkins.
        git_commit_id (str): The commit ID of the pull request.
        benchmark_type (str): The type of benchmark testing.
        scalefactor (str): The size of the database to load.
        terminals (str): The number of client threads that will issue requests to the DBMS.
        weight (json): The weight of transactions.
        metrics (json): The benchmark test results.
        incre_metrics (json): The results at different time during a long benchmark testing.
        environment (json): The information of the server.
    """

    INSERT_SQL = """
        INSERT INTO %s (
            time, git_branch, git_commit_id, jenkins_job_id, db_version, environment, benchmark_type, query_mode, scale_factor, terminals, client_time, weights, metrics, incremental_metrics
        ) VALUES (
            to_timestamp(%s/1000), '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s, 
            %s, %s, '%s', '%s', '%s'
        );
    """ % (TABLENAME, time, git_branch, git_commit_id, jenkins_job_id, db_version, environment, benchmark_type, query_mode, scale_factor, terminals, client_time, weights, metrics, incremental_metrics)

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
def query_database(conn, QUERY_SQL):
    """View all results within the TimeScaleDB. This is only used for testing purpose.

    Args:
        conn (psycopg2.extensions.connection): The connection to PostgreSQL database.
        QUERY_SQL (str): The SQL to be executed.

    """
    cur = conn.cursor()
    cur.execute(QUERY_SQL)
    for i in cur.fetchall():
        print(i)
    cur.close()


def main():
    parser = argparse.ArgumentParser(description='Load sample data into timescaledb.')
    parser.add_argument('--clear', action='store_true', help='Clear old table.')
    parser.add_argument('--index', type=str, help='The location of data that need to be stored.')
    parser.add_argument('--show_detail', action='store_true', help='Display the data in the database.')
    parser.add_argument('--show_size', action='store_true', help='Display how many data are there in the database.')
    args = parser.parse_args()

    conn = psycopg2.connect(CONNECTION)

    if args.clear:
        drop_table(conn)
        create_table(conn)
        subprocess.run(["rm", "-rf", "/tmp/archive"])

    if args.index:
        table_existence = check_table_exist(conn)
        if table_existence == False:
            create_table(conn) 
            print("Finish creating")

        index_list = args.index.split(',')
        for index in index_list:
            url = "http://jenkins.db.cs.cmu.edu:8080/job/terrier-nightly/%s/artifact/*zip*/archive.zip" % index
            print("Downloading data from %s" % url)
            subprocess.run(["wget", "-O", "/tmp/archive.zip", url])
            subprocess.run(["rm", "-rf", "/tmp/archive"])
            subprocess.run(["unzip", "-q", "/tmp/archive.zip", "-d", "/tmp/"])

            read_and_insert_from_folder(conn, '/tmp/archive/build/oltp_result')

    if args.show_detail:
        query_database(conn, "SELECT * FROM %s;" % TABLENAME)
    if args.show_size:
        query_database(conn, "SELECT COUNT(*) FROM %s;" % TABLENAME)
    print("Done")
    conn.close()


if __name__ == "__main__":
    main()
