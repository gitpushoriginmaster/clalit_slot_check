import json
import winsound
from datetime import datetime
from random import randint
from time import sleep

import requests
from notify_run import Notify

FOUND_BEEP_FREQUENCY = 400
FOUND_BEEP_DURATION = 5000
ERROR_BEEP_FREQUENCY = 200
ERROR_BEEP_DURATION = 2000


def check_slot():
    try:
        r = requests.get(url=request_url, headers=request_headers)
    except Exception as e:
        print(e)
        print(f"{datetime.now().strftime('%H:%M')}: Too many requests!")
        winsound.Beep(frequency=ERROR_BEEP_FREQUENCY,
                      duration=ERROR_BEEP_DURATION * 2)
        sleep(600)
        return

    r = json.loads(r.content)
    curr_time = datetime.now().strftime('%H:%M')

    if r['errorType'] == 0:
        available_days = r['data']['availableDays']
        notify.send(f"SLOT FOUND! {available_days}")
        print(f"{curr_time}: {available_days}")
        winsound.Beep(frequency=FOUND_BEEP_FREQUENCY,
                      duration=FOUND_BEEP_DURATION)

    elif r['errorType'] == 1:
        print(f"{curr_time}: No slots")

    else:
        print(f"{curr_time}: Connection error, {r}")
        winsound.Beep(frequency=ERROR_BEEP_FREQUENCY,
                      duration=ERROR_BEEP_DURATION)

    sleep(180 + randint(0, 60))


if __name__ == '__main__':

    notify = Notify()  # Need to register at first run: notify.register()

    print("Paste request headers:")
    lines = []
    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    request_headers = {}
    for p in lines[1:]:
        key, val = str.split(p, sep=': ')
        request_headers[key] = val

    request_url = f"https://{request_headers['Host']}{str.split(lines[0], sep=' ')[1]}"

    print("Processed request headers, starting requests.")

    while True:
        check_slot()
