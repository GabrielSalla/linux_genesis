import opsutils
from tabulate import tabulate

def main():
    access_information = opsutils.load_access_information(look_at="home")
    database_172 = opsutils.DatabaseHandler(access_information["database_172"])
    slack = opsutils.Slack(access_information["slack_loro"]["token"])

    building_bas = database_172.fetch("""
        select
          id,
          to_char(created_at at time zone 'America/Sao_Paulo', 'HH24:MI:SS') as time
        from "BulkAnticipations"
        where
          status = 'building' and
          extract(hour from created_at at time zone 'America/Sao_Paulo') < 11;""")

    if(len(building_bas) == 0):
        slack.send_message("#risco", "D0 liberadas")
    else:
        headers = ["id", "time"]
        table = [(row["id"], row["time"]) for row in building_bas]
        slack.send_message("@gabriel.salla", "```%s```" % tabulate(table, headers=headers))

if(__name__ == "__main__"):
    main()
