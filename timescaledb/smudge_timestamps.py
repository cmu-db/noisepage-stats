import psycopg2
import argparse
from datetime import timedelta
from random import randrange

def fetch_all_time(conn, table):
    query = f"""
    SELECT
        time,
        id
    FROM {table}
    ORDER BY time ASC
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def find_times_with_duplicates(conn, table):
    query = f"""
    SELECT
        time,
        COUNT(*)
    FROM {table}
    GROUP BY time
    HAVING COUNT(*) > 1
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def find_records_with_duplicate_times(conn, table, time):
    query = f"""
    SELECT
        time,
        id
    FROM {table}
    WHERE
        time = '{time}'
    """
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

def update_with_smudge(conn, table, record):
    old_time = record[0]
    new_time = old_time + timedelta(milliseconds=randrange(10))
    sql_statement = f"""
    UPDATE {table}
    SET time = '{new_time}'
    WHERE
        id = '{record[1]}'
    """
    with conn.cursor() as cur:
        cur.execute(sql_statement)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, help='Database username')
    parser.add_argument('--password', type=str, help='Datatbase password')
    parser.add_argument('--host', type=str, default='incrudibles-production.db.pdl.cmu.edu', help='Hostname of the database (i.e. incrudibles-production.db.pdl.cmu.edu')
    parser.add_argument('--port', type=str, default='32003', help='Port that the DB is running on.')
    args = parser.parse_args()
    username = args.username
    password = args.password
    host = args.host
    port = args.port

    conn = psycopg2.connect(f'postgres://{username}:{password}@{host}:{port}/pss_database')

    table = 'microbenchmark_results'
    all_table_records = find_times_with_duplicates(conn, table)
    count = 1
    for time, _ in all_table_records:
        print(count)
        count +=1
        duplicate_time_records = find_records_with_duplicate_times(conn, table, time)
        for record in duplicate_time_records:
            update_with_smudge(conn, table, record)
    conn.commit()

if __name__ == "__main__":
    main()