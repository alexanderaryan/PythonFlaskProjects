#import pandas as pd
from Paalkanakku.Paalkanakku import cred_filename, card,  file_name, gc


import gspread

gcc = gspread.oauth(
    credentials_filename='/home/alexanders/Documents/Python/GitPythonWork/apps/Paalkanakku/Paalkanakku/client_secret_367285454255-v4g22iac4c6tlu0c2n5btlp7aeh2nmqp.apps.googleusercontent.com.json'
)


gcc.create("Test")

