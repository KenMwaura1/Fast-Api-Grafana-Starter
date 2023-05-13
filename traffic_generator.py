import requests
import time

def get_notes():
    url = "http://localhost:8002/notes/"  # Replace with your desired URL

    while True:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("GET request successful")
                # Process the response data if needed
                print(response.json())
            else:
                print("GET request failed with status code:", response.status_code)
        except requests.RequestException as e:
            print("GET request failed:", e)

        time.sleep(5)  # Delay for 5 seconds before sending the next request

get_notes()
