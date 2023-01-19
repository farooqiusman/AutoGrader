from website import app
import os
import json
import sys

# getting config details
with open('config.json') as f:
    data = json.load(f)

# initializing db if it doesn't exist yet (change this if not using sqlite)
# if not os.path.exists("website/site.db"):
#     db.create_all()

# running site
if __name__=='__main__':
    # run this command with any additional arg to run in production
    # for example, "python3 run.py PROD"
    if len(sys.argv) > 1:
        print('<< PROD >>')
        os.system(f"python3 -m gunicorn -b '0.0.0.0:{data['port']}' website:app")
    # or just run without an additional arg to run in debug
    # for example, "python3 run.py"
    else:
        print('<< DEBUG >>')
        app.run(host='0.0.0.0', debug=True)
