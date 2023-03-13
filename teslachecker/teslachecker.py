import requests
import json
import time
import pytz
from datetime import datetime

def get_current_time_pst():
    # Set timezone to Pacific Time
    tz = pytz.timezone('America/Los_Angeles')
    # Get current time in Pacific Time
    current_time = datetime.now(tz)
    return current_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

def filter_item(d):
    return d.get("year") == 2023 and d.get("stateProvince") == "WA" and (d.get("trimCode") == "LRAWD" or d.get("trimCode") == "PAWD") and d.get("isAvailable") == True and d.get("isDemo") == False

def send_twilio_sms(message):
    # Replace these values with your own
    twilio_account_sid = "XXX"
    twilio_auth_token = "XXX"
    twilio_number = "+11234567890"
    your_number = "+11234567890"
    # Set up the request data
    url = f"https://api.twilio.com/2010-04-01/Accounts/{twilio_account_sid}/Messages"
    data = {
        "Body": message,
        "From": twilio_number,
        "To": your_number,
    }

    # Send the request
    response = requests.post(url, data=data, auth=(twilio_account_sid, twilio_auth_token))

    # Print the response
    print(response.text)

def get_and_send_sms():
    url = 'https://api.waitingfortesla.com/api/v1/inventory?countryCode=US&vehicleModel=my&vehicleTitle=NEW'
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7",
        # "if-none-match": 'W/"2cd38-oG3umw9/7u8n8BHoJgWNyNWLd2U"',
        "origin": "https://waitingfortesla.com",
        "referer": "https://waitingfortesla.com/",
        "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "x-api-version": "2"
    }
    # Make the GET request
    response = requests.get(url, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Parse the JSON response
        data = json.loads(response.text)

        # Use filter() to filter the data array
        filtered_data = list(filter(filter_item, data['data']))

        output_data = [{"trimName": d.get("trimName"), "titleStatus": d.get("titleStatus"), "exteriorColor": d.get("exteriorColor"), "interiorColor": d.get("interiorColor"), "wheels": d.get("wheels"), "price": d.get("price"), "city": d.get("city")} for d in list(filtered_data)]

        if len(output_data) > 0:
            send_twilio_sms(json.dumps(output_data, indent=4))
        else:
            send_twilio_sms("No available model Y " + get_current_time_pst())
    else:
        print(f"Request failed with status code {response.status_code}")

counter = 0

while counter < 10:
    get_and_send_sms()
    time.sleep(1800)  # 30 minutes in seconds
    counter += 1