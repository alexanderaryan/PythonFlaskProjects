import yaml
try:
    from Paalkanakku.config import sheet_config
except:
    from Paalkanakku.Paalkanakku.config import sheet_config

def config_data():
    stream = open(sheet_config, 'r')
    data = yaml.load(stream, Loader=yaml.FullLoader)

    return data