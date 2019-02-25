from argparse import ArgumentParser
from sys import argv
from remotsylib3.api_async import (API, run_remotsy_api_call)


parser = ArgumentParser()
parser.add_argument("-u", "--username", action="store", type=str, required=True)
parser.add_argument("-p", "--password", action="store", type=str, required=True)
args = parser.parse_args(argv[1:])

client = API()

app_creds = dict(
        username=args.username,
        password=args.password
        )

#If login is successfull
login_attempt = run_remotsy_api_call(remotsy_api.login(auth=app_creds))
if login_attempt['data']['msg'] == 'success':
    client.auth_key = login_attempt['data']['auth_key']

#Get the list of the controls
lst_ctl = run_remotsy_api_call(client.list_controls())
for ctl in lst_ctl:
    print("id %s Name %s" % (ctl["_id"], ctl['name']))

#get the list of the available buttons for the first control
lst_bto = run_remotsy_api_call(client.list_buttons(lst_ctl[1]["_id"]))
for bto in lst_bto:
    if bto["key"] == "POWER OFF": #Get the Id of the POWER OFF
        print("id %s Key %s" % (bto["_id"], bto["key"]))
        #Do the infrared blast using the IDDEV of the first control
        #and the id of the POWER OFF
        run_remotsy_api_call(client.blast(lst_ctl[1]["iddev"], bto["_id"]))
