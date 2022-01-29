import config

def replace(re):
    re_new= re[0][4].replace('{{config}}', config.host)
    re_list = list(re[0])
    re_list[4] = re_new
    re_value = [[1]]
    re_value[0] = re_list
    return re_value