import json
try:
    from Paalkanakku import os
except:
    from Paalkanakku.Paalkanakku import os
from datetime import datetime
from flask_dance.contrib.google import make_google_blueprint, google

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


cred_filename = '/home/alexanders/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/' \
                'client_secret_367285454255-v4g22iac4c6tlu0c2n5btlp7aeh2nmqp.apps.googleusercontent.com.json'
client_secrets = '/home/alexanders/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/' \
                'client_secrets.json'

book_name = str(datetime.today().year) + 'Paalkanakku'
sheet_name = datetime.today().today().strftime("%B")

with open(cred_filename,'r') as fp:
    google_data = json.load(fp)['web']



google_blueprint = make_google_blueprint(client_id=google_data['client_id'],
                                         client_secret=google_data['client_secret'],
                                         offline=True,
                                         scope=['profile', 'email'])




