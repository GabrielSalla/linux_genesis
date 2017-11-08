import opsutils

query = """
    SELECT
      pid,
      age(clock_timestamp(), query_start) as age,
      pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE
      state = 'active' and
      usename = user and
      query NOT ILIKE '%pg_stat_activity%' and
      age(current_timestamp, query_start) > '1 minute' :: interval
    ORDER BY query_start desc;
"""

databases_names = ["database_replica_ops", "database_replica_readonly"]
access_information = opsutils.load_access_information(look_at="home")

for database_name in databases_names:
    db = opsutils.DatabaseHandler(access_information[database_name])
    try:
        print(db.fetch(query))
    finally:
        db.close()