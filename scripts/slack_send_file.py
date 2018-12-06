import requests
import opsutils
import sys

access_information = opsutils.load_access_information(look_at="home")
slack_token = access_information["slack"]["token"]


def main(file_name, channels):
    try:
        file_type = file_name.split(".")[1]
        print("file_type", file_type)
    except IndexError:
        file_type = ""

    with open(file_name, "rb") as file:
        files = [
            ("file", (file_name, file, ""))
        ]
        params = {
            "token": slack_token,
            "channels": channels,
            "file_type": file_type,
            "title": file_name
        }
        result = requests.post(
            "https://slack.com/api/files.upload",
            params=params,
            files=files
        )
        print(result.status_code, result.text)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Missing parameters 'file_name channels'")
    main(sys.argv[1], sys.argv[2])
