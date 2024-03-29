import json
try:
    from Paalkanakku import os
except:
    from Paalkanakku.Paalkanakku import os
from datetime import datetime
from flask_dance.contrib.google import make_google_blueprint, google

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

home_dir=os.path.expanduser("~")
cred_filename = home_dir+'/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/' \
                'client_secret_367285454255-n45ttmrb1hne9b9j4jm0ftbq6ku21qsk.apps.googleusercontent.com.json'
client_secrets = home_dir+'/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/' \
                'client_secrets.json'

book_name = str(datetime.today().year) + 'Paalkanakku'
sheet_name = datetime.today().today().strftime("%B")

with open(cred_filename,'r') as fp:
    google_data = json.load(fp)['web']



google_blueprint = make_google_blueprint(client_id=google_data['client_id'],
                                         client_secret=google_data['client_secret'],
                                         offline=True,
                                         scope=['profile', 'email'])

sheet_config=home_dir+"/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/config.yaml"