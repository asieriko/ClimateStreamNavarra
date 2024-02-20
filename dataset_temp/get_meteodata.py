import pandas as pd
import requests


def get_data(cod_stations):
    from_day = 1
    from_month = 1
    from_year = 2000
    to_day = 31
    to_month = 12
    to_year = 2023
    from_date = f"{from_day}%2F{from_month}%2F{from_year}"
    to_date = f"{to_day}%2F{to_month}%2F{to_year}"
    
    for c_station in cod_stations:
        print(f"Downloading station {c_station}")
        url = f"http://meteo.navarra.es/download/estacion_datos.cfm?IDEstacion={c_station}&p_d=1001&p_d=1002&p_d=1003&p_d=1012&fecha_desde={from_date}&fecha_hasta={to_date}&dl=csv"
        data = requests.get(url).text
        with open(f'{c_station}.csv', 'w') as f:
            f.write(data)


def process_data(cod_stations):
    dfs = []
    for c_station in cod_stations:
        df = pd.read_csv(f"{c_station}.csv",
                         usecols=[0,1,2,3,4],
                         skiprows=[0,1],
                         skipfooter=4, # last 4 rows are a sort of a summary
                         na_values = '- -', 
                         names = ["date","tav","tmax","tmin","rad"],
                         dtype = {'date': str, 'tav': float, 'tmax': float, 'tmin': float, 'rad':float}).dropna()
        df['date'] = pd.to_datetime(df.date, format="%d/%m/%Y")
        if not df.empty:
            df["station"] = c_station
            dfs.append(df)
        
    df = pd.concat(dfs, axis=0, ignore_index=True)
    return df
 
    
def date_year_ext_season(date):
    day = date.day_of_year
    year = date.year
    if 59 >= day:
        return f"W.{year}"  # Winter    
    elif 243 >= day  and day > 182:
        return f"S.{year}"  # Summer
    else:
        return f"O.{year}"  # Other 
    
def date_year_season(date):
    day = date.day_of_year
    year = date.year
    if 80 >= day:
        return f"1.{year}"
    elif day > 355:
        return f"1.{year+1}"  # Winter
    elif 172 > day  and day > 80:
        return f"2.{year}"  # Spring      
    elif 263 >= day  and day > 172:
        return f"3.{year}"  # Summer
    else:
        return f"4.{year}"  # Fall

def date_season(date):
    day = date.day_of_year
    if 80 >= day  or day > 355:
        return 1  # Winter
    elif 172 > day  and day > 80:
        return 2  # Spring      
    elif 263 >= day  and day > 172:
        return 3  # Summer
    else:
        return 4  # Fall


df = pd.read_csv("/home/asier/Ikerketa/Projects/ClimateStream/dataset_temp/estaciones.csv", index_col=0, header=None)
cod_stations = list(df.index)
df_coord = pd.read_csv("/home/asier/Ikerketa/Projects/ClimateStream/dataset_temp/estaciones_coord.csv")


# get_data(cod_stations)

data = process_data(cod_stations)
data["season"]=data.date.apply(date_season)
data["year_season"]=data.date.apply(date_year_season)
data["year_season_ext"]=data.date.apply(date_year_ext_season)
# data.to_csv("allstations.csv")
df_s=data[data['year_season_ext'].str.startswith('S')]
df_w=data[data['year_season_ext'].str.startswith('W')]
df_s.to_csv("summer.csv")
df_w.to_csv("winter.csv")
data_grouped = data.groupby(['station','year_season_ext','year_season','season']).agg({'tav':'mean', 
                         'tmax':'max', 
                         'tmin':'min', 
                         'rad': 'mean'})
data_grouped = data_grouped.reset_index()
df_coord = df_coord.drop(columns=['1','2','3','4','5','6','7'])
df_coord = df_coord.rename(columns={'0':'station'})
df_s_merged = df_s.merge(df_coord,on="station")
df_w_merged = df_w.merge(df_coord,on="station")
df_s_merged.to_csv("summer_m.csv")
df_w_merged.to_csv("winter_m.csv")
data_merged = data_grouped.merge(df_coord,on="station")
data_merged.to_csv("merged.csv")
