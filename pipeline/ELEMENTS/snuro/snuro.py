# snuro mariadb api
import pandas as pd

xlsx = pd.read_excel('./pipeline/snuro/스누로_3기_matching.xlsx')
pd.set_option('display.max_rows', None)
print(xlsx) # col : 스누링커 스누씨드