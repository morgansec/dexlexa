Steps to get this working:

Enable the voicemonkey.io skill in your alexa app.
Create routine triggers for each of the alerts using your voicemonkey.io account.
Create the alexa routine for each alert. The voice monkey devices will show up as doorbells under your account
Add your Dexcom account info and customize the thresholds and trends for your desired alerts in the dexlexa.json file
create a scheduled task or cron job to run your script at the desired interval


Dexcom trend values found on the share2nightscout project https://github.com/nightscout/share2nightscout-bridge:

NONE: 0
DoubleUp: 1
SingleUp: 2
FortyFiveUp: 3
Flat: 4
FortyFiveDown: 5
SingleDown: 6
DoubleDown: 7
'NOT COMPUTABLE': 8
'RATE OUT OF RANGE': 9
