import opsutils
import requests
import time
from tabulate import tabulate


def fetch_building_bas(database_replica):
    database_replica.begin()
    results = database_replica.fetch("""
        select
          id,
          company_id,
          recipient_id,
          to_char(created_at at time zone 'America/Sao_Paulo',
                  'HH24:MI:SS') as time
        from "BulkAnticipations"
        where
          status = 'building' and
          extract(hour from created_at at time zone 'America/Sao_Paulo') < 11;
    """)
    database_replica.end()
    return results


def delete_building_bas(session_id, building_bas):
    admin_api_url = "https://api.admin.internal.pagar.me/1"
    endpoint = "/recipients/%s/bulk_anticipations/%s"
    for ba in building_bas:
        url = admin_api_url + endpoint % (ba["recipient_id"], ba["id"])
        headers = {
            "X-Live": "1"
        }
        params = {
            "impersonation_key": ba["company_id"],
            "session_id": session_id
        }
        result = requests.delete(
            url, headers=headers, params=params, verify=False)
        print(result.text)


def main():
    pagarme_admin = opsutils.PagarmeAdmin()
    pagarme_admin.load_session_id()
    session_id = pagarme_admin.get_session_id()
    access_information = opsutils.load_access_information(look_at="home")
    database_replica = opsutils.DatabaseHandler(
        access_information["database_replica"])
    slack = opsutils.Slack(access_information["slack_loro"]["token"])

    # 3 tries to delete the building BAs
    for i in range(3):
        building_bas = fetch_building_bas(database_replica)
        if(len(building_bas) > 0):
            delete_building_bas(session_id, building_bas)
            time.sleep(5)
        else:
            slack.send_message("#risco", "D0 liberadas")
            break
    else:
        headers = ["id", "company_id", "recipient_id", "time"]
        table = [
            (row["id"], row["company_id"], row["recipient_id"], row["time"])
            for row in building_bas]
        slack.send_message("@gabriel.salla", "```%s```" %
                           tabulate(table, headers=headers))

if(__name__ == "__main__"):
    main()
