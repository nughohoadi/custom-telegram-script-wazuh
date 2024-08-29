#!/var/ossec/framework/python/bin/python3

import time
import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth


def generate_msg(alert):
    """
    Function that will provide the custom body for the message.
    It takes as input a dictionary object generated from the json alert
    """
    t = time.strptime(alert['timestamp'].split('.')[0],'%Y-%m-%dT%H:%M:%S')
    timestamp = time.strftime('%c',t)
    fname = alert['syscheck']['path'] if 'path' in alert['syscheck'] else ''
    agent = alert['agent']['name'] if 'name' in alert['agent'] else ''
    event = alert['syscheck']['event'] if 'event' in alert['syscheck'] else ''
    mode = alert['syscheck']['mode'] if 'mode' in alert['syscheck'] else ''
    if 'audit' in alert['syscheck']:
        uname = alert['syscheck']['audit']['effective_user']['name']
        pname = alert['syscheck']['audit']['process']['name']
        execut = alert['syscheck']['audit']['process']['cwd']
    else:
        uname = alert['syscheck']['uname_after']
        pname = ''
        execut = ''

    if mode != 'scheduled':
        message = """
        Agent Name : {a}
        \nFile : {b} has been {c} by : {d} at {h}
        \n{e} - {f} - {g}
        """.format(a=agent,b=fname,c=event,d=uname,e=pname,f=execut,g=mode,h=timestamp)
    else:
        message =''

    return message


# Additional global vars
pwd = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
json_alert = {}
now = time.strftime("%a %b %d %H:%M:%S %Z %Y")

# Set paths
log_file = '{0}/logs/integrations-telegram.log'.format(pwd)
log_file2 = '{0}/logs/lasttele.log'.format(pwd)

def main(args):
    """
    Main function. This will call the functions to prepare the message and send the chat message
    """
    # Read args
    alert_file_location = args[1]
    recipients = args[3]
    tokenkey = args[2]

    # debug(alert_file_location)
    # debug(tokenkey)
    # debug(recipients)

    # Load alert. Parse JSON object.
    with open(alert_file_location) as alert_file:
        json_alert = json.load(alert_file)

    msg = generate_msg(json_alert)
    #debug(msg)
    if msg:
        send_tele(recipients, tokenkey, msg)
    else:
        debug("Alert tidak dikirim ke telegram karena hanya mengandung informasi")

def send_tele(recipients, tokenkey, body):
    """
    Send telegram message
    """
    url = f"http://192.168.100.168:8081/bot{tokenkey}/sendMessage"
    params = {
        'chat_id': recipients,
        'text': body
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        debug("Pesan berhasil dikirim ke telegram chat id:{a}".format(a=recipients))
    else:
        debug(f"Terjadi kesalahan: {response.status_code}, {response.text}")

def debug(msg):
    """
    Function to generate debug logs
    """
    msg = "{0}: {1}\n".format(now, msg)
    print(msg)
    f = open(log_file, "a")
    f.write(msg)
    f.close()

    f = open(log_file2, "w")
    f.write(now)
    f.close()

if __name__ == "__main__":
    try:
        # Read arguments
        bad_arguments = False
        if len(sys.argv) >= 4:
            msg = '{0} {1} {2} {3} {4}'.format(
                now,
                sys.argv[1],
                sys.argv[2],
                sys.argv[3],
                sys.argv[4] if len(sys.argv) > 4 else '',
            )
            debug_enabled = (len(sys.argv) > 4 and sys.argv[4] == 'debug')
        else:
            msg = '{0} Wrong arguments'.format(now)
            bad_arguments = True

        # Logging the call
        f = open(log_file, 'a')
        f.write(msg + '\n')
        f.close()

        if bad_arguments:
            debug("# Exiting: Bad arguments.")
            sys.exit(1)

        # Main function
        main(sys.argv)

    except Exception as e:
        debug(str(e))
        raise
