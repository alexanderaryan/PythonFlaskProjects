import pandas as pd
from Moikanakku import cred_filename, card, data, file_name

header = data[0]
dataframe = pd.DataFrame(data, columns=data.pop(0))

dataframe['பானை'] = dataframe['பானை'].str.slice(0,1)
dataframe['சேலை'] = dataframe['சேலை'].str.slice(0,1)
dataframe[['மொய்', 'பக்கம்', 'நோட்','பானை','சேலை']] = dataframe[['மொய்', 'பக்கம்', 'நோட்','பானை','சேலை']].apply(pd.to_numeric)

moi_data = dataframe.groupby(['ஊர்']).sum()['மொய்'].sort_values(ascending=False)

moi_data_l = [[oor,moi] for oor,moi in moi_data.items()][:11]
moi_data_s = [[oor,moi] for oor,moi in moi_data.items()][-11:][::-1]

moi_by_name = dataframe.groupby(['ஊர்', 'பெயர்/விபரம்']).sum()['மொய்'].sort_values(ascending=False)


moi_data_by_name_l = [[oor_name[0]+' '+oor_name[1], moi] for oor_name, moi in moi_by_name.items()][:11]
moi_data_by_name_s = [[oor_name[0]+' '+oor_name[1], moi] for oor_name, moi in moi_by_name.items()][-11:][::-1]


list_details = {'moi_data_l': [["ஊர்", "மொய்"], moi_data_l],
                'moi_data_s': [["ஊர்", "மொய்"], moi_data_s],
                'moi_data_by_name_l': [["பெயர்", "மொய்"], moi_data_by_name_l],
                'moi_data_by_name_s': [["பெயர்", "மொய்"], moi_data_by_name_s]
                }
