import opsutils
import tkinter
from psycopg2 import ProgrammingError
from tabulate import tabulate
import time
import sys

def connect(database_key):
    access_information = opsutils.load_access_information(look_at="home")
    if(database_key == "172"):
        print("Connecting to database 172")
        return opsutils.DatabaseHandler(access_information["database_172"])
    elif(database_key == "finops"):
        print("Connecting to database finops")
        return opsutils.DatabaseHandler(access_information["database_finops_ops"])

def load_file(file):
    with open(file, "r") as input_file:
        return input_file.read()

def get_clipboard():
    root = tkinter.Tk()
    return root.clipboard_get()

def execute(database_handler, query):
    try:
        return database_handler.fetch(query)
    except ProgrammingError as pgerror:
        error_message = "Unable to run query:\n\n    "
        error_message += query.replace("\n", "\n    ")
        print(error_message)
        print(pgerror.pgerror)
        exit(1)

def show(result):
    try:
        headers = [key for key in result[0]]
        data = [[row[key] for key in headers] for row in result]
        print(tabulate(data, headers=headers))
    except IndexError:
        print("Empty result")

def main():
    if(len(sys.argv) < 2):
        sys.exit("Missing database parameter")
    database_key = sys.argv[1]
    if(database_key not in ["172", "finops"]):
        sys.exit("Invalid database %s" % database_key)

    if(len(sys.argv) < 3):
        option = "clipboard"
    else:
        option = sys.argv[2]

    database_handler = connect(database_key)

    if(option == "clipboard"):
        query = get_clipboard()
    else:
        query = load_file(option)
    print("Querying " + option)

    start_time = time.time()
    result = execute(database_handler, query)
    show(result)
    spent_time = int((time.time() - start_time) * 1000)
    print("Query time: %sms" % spent_time)
    exit(0)

if(__name__ == "__main__"):
    main()
