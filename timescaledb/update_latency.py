import json
import psycopg2
import argparse


benchmark_types = ['ycsb','tatp','tpcc','noop','smallbank']
terminal_values = [1,2,4,8,16,32]
wal_devices = ['HDD', 'RAM disk', 'None']
client_times = [60,600]
VALID_DATE = '2020-09-22 00:00:00.000+00'


def find_last_valid_latency(conn, benchmark, terminals, wal_device, client_time):
    query = f"""
    SELECT
        metrics->'latency' AS "latency",
        time
    FROM oltpbench_results
    WHERE
        git_branch = 'origin/master' AND
        (metrics->'latency'->>'min')::numeric != 0.0 AND
        time > '{VALID_DATE}' AND
        benchmark_type = '{benchmark}' AND
        terminals = '{terminals}' AND
        wal_device = '{wal_device}' AND
        client_time = '{client_time}'
    ORDER BY time ASC
    """
    with conn.cursor() as cur:
        cur.execute(query)
        #print(f'{benchmark}, {terminals}, {wal_device}, {client_time}')
        #print(cur.fetchone())
        return cur.fetchone()

def update_latency(conn, benchmark, terminals, wal_device, client_time, latency):
    sql_statement = f"""
        UPDATE oltpbench_results
        SET metrics = jsonb_set(metrics, '{{latency}}', '{json.dumps(latency)}')
        WHERE
	        time < '{VALID_DATE}' AND
            benchmark_type = '{benchmark}' AND
            terminals = '{terminals}' AND
            wal_device = '{wal_device}' AND
            client_time = '{client_time}'           
    """
    #print(sql_statement)
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

    for benchmark in benchmark_types:
        for wal_device in wal_devices:
            for terminals in terminal_values:
                for client_time in client_times:
                    row = find_last_valid_latency(conn, benchmark, terminals, wal_device, client_time)
                    if row:
                        update_latency(conn, benchmark, terminals, wal_device, client_time, row[0])

    conn.commit()

if __name__ == "__main__":
    main()

