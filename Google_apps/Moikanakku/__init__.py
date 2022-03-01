import gspread


cred_filename = "/home/alexanders/Documents/Python/Python_work/Localgit/Google/" \
                "google_apps/MoiKanakku/Moikanakku/moikanakku-341816-5b7d7ef75ff9.json"
file_name = "Aruna Swetha Sadangu"

card = {
    "படங்கள்": ["/static/Images/20201004_144328.jpg", "இங்கே தொட்டால் பூப்புனித நீராட்டு விழாவன்று "
                                                   "எடுக்கப்பட்ட சில புகைப்படங்களை காணலாம் !", "images"],
    "மொய் நோட்டு": ["/static/Images/card_img/Moi.png", "இங்கே தொட்டால் மொய் நோட்டு அட்டவணையை  "
                                                       "முழுதாக காணலாம் !", "ledger"],
    "விளக்கப்படம்": ["/static/Images/card_img/charts.jpg", "இங்கே மொய் கணக்குகளை விளக்கும் "
                                                        "வண்ணமயமான விளக்கப்படங்கள் உள்ளன!", "charts"]
    }

gc = gspread.service_account(filename=cred_filename)

sheet = gc.open(file_name).sheet1

#sheet = client.open("Aruna Swetha Sadangu").sheet1
total_rows = str(sheet.row_count)

data = sheet.get('A1:H'+total_rows)