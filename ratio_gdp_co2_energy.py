import psycopg2
import numpy as np
from co2_emissionen import df as df1
from erneuerbare_energien import df as df2
import pandas as pd
import sys
from bokeh.plotting import figure, save, curdoc


param_dic = {
    "host"      : "localhost",
    "database"  : "projekt",
    "user"      : "postgres",
    "password"  : "postgres"
}
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # Verbindung zur PostgreSQL Datenbank aufbauen
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 

    print("Connection successful")
    return conn

def postgresql_to_dataframe(conn, select_query, column_names):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    
    # Wir erhalten eine Liste von Tupeln
    tupples = cursor.fetchall()
    cursor.close()
    
    # Wir packen die Tupel in eine Panda-Datenframe
    df = pd.DataFrame(tupples, columns=column_names)
    return df


conn = connect(param_dic)


df = postgresql_to_dataframe(conn, "select * from gdp", column_names = ["Country Name","Country Code","Indicator Name","Indicator Code","1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"])
df.head(0)

# Transporniere Tabelle für leichtere Zuweisung der Daten
df = pd.melt(df, id_vars=['Country Name', 'Country Code'], value_vars=["1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"])

# Aussortieren von Ländern mit einem BIP von über 350Mrd USD
kriterium1 = df['value'] > 350000000000
kriterium2 = df['variable'] == '2017'
kriterium3 = (df['Country Code'] == 'ARE') | (df['Country Code'] == 'DEU') | (df['Country Code'] == 'ARG') | (df['Country Code'] == 'AUS') | (df['Country Code'] == 'AUT') | (df['Country Code'] == 'BEL') | (df['Country Code'] == 'BRA') | (df['Country Code'] == 'CAN') | (df['Country Code'] == 'CHE') | (df['Country Code'] == 'CHN') | (df['Country Code'] == 'ESP') | (df['Country Code'] == 'FRA') | (df['Country Code'] == 'GBR') | (df['Country Code'] == 'IDN') | (df['Country Code'] == 'IND') | (df['Country Code'] == 'IRN') | (df['Country Code'] == 'ISR') | (df['Country Code'] == 'ITA') | (df['Country Code'] == 'JPN') | (df['Country Code'] == 'KOR') | (df['Country Code'] == 'MEX') | (df['Country Code'] == 'NLD') | (df['Country Code'] == 'NOR') | (df['Country Code'] == 'POL') | (df['Country Code'] == 'RUS') | (df['Country Code'] == 'SAU') | (df['Country Code'] == 'SWE') | (df['Country Code'] == 'THA') | (df['Country Code'] == 'TUR') | (df['Country Code'] == 'USA')

kriterien4 = (df1['code'] == 'ARE') | (df1['code'] == 'DEU') | (df1['code'] == 'ARG') | (df1['code'] == 'AUS') | (df1['code'] == 'AUT') | (df1['code'] == 'BEL') | (df1['code'] == 'BRA') | (df1['code'] == 'CAN') | (df1['code'] == 'CHE') | (df1['code'] == 'CHN') | (df1['code'] == 'ESP') | (df1['code'] == 'FRA') | (df1['code'] == 'GBR') | (df1['code'] == 'IDN') | (df1['code'] == 'IND') | (df1['code'] == 'IRN') | (df1['code'] == 'ISR') | (df1['code'] == 'ITA') | (df1['code'] == 'JPN') | (df1['code'] == 'KOR') | (df1['code'] == 'MEX') | (df1['code'] == 'NLD') | (df1['code'] == 'NOR') | (df1['code'] == 'POL') | (df1['code'] == 'RUS') | (df1['code'] == 'SAU') | (df1['code'] == 'SWE') | (df1['code'] == 'THA') | (df1['code'] == 'TUR') | (df1['code'] == 'USA')
kriterium5 = df1['year'] == 2017

kriterien6 = (df2['code'] == 'ARE') | (df2['code'] == 'DEU') | (df2['code'] == 'ARG') | (df2['code'] == 'AUS') | (df2['code'] == 'AUT') | (df2['code'] == 'BEL') | (df2['code'] == 'BRA') | (df2['code'] == 'CAN') | (df2['code'] == 'CHE') | (df2['code'] == 'CHN') | (df2['code'] == 'ESP') | (df2['code'] == 'FRA') | (df2['code'] == 'GBR') | (df2['code'] == 'IDN') | (df2['code'] == 'IND') | (df2['code'] == 'IRN') | (df2['code'] == 'ISR') | (df2['code'] == 'ITA') | (df2['code'] == 'JPN') | (df2['code'] == 'KOR') | (df2['code'] == 'MEX') | (df2['code'] == 'NLD') | (df2['code'] == 'NOR') | (df2['code'] == 'POL') | (df2['code'] == 'RUS') | (df2['code'] == 'SAU') | (df2['code'] == 'SWE') | (df2['code'] == 'THA') | (df2['code'] == 'TUR') | (df2['code'] == 'USA')
kriterium7 = df2['year'] == 2017

kriterien_gdp = (kriterium1) & (kriterium2) & (kriterium3)
kriterien_co2 = (kriterien4) & (kriterium5)
kriterien_ene = (kriterien6) & (kriterium7)

numm = 100000000000
df_gdp = df.sort_values(by=['Country Code']).loc[kriterien_gdp][['value']]
df_gdp['value'] /= numm
df_co2 = df1.sort_values(by=['code']).loc[kriterien_co2][['annual co2 emissions(tonnes)']]
df_ene = df2.sort_values(by=['code']).loc[kriterien_ene][['renewable_energy_consumption']]

def df_to_list(dataframe):
    records = dataframe.to_records(index=False)
    result = list(records)

    return result

df_lst_gdp = df_to_list(df_gdp)
df_lst_co2 = df_to_list(df_co2)
df_lst_ene = df_to_list(df_ene)

lst_gdp = sum([list(x) for x in df_lst_gdp], [])
lst_co2 = sum([list(x) for x in df_lst_co2], [])
lst_ene = sum([list(x) for x in df_lst_ene], [])
ratio_co2_ene = []

# Verhältnis co2 / erneuerbare energien 
for i in range(0,30):
    ratio_co2_ene.append(np.divide(lst_co2[i], lst_ene[i]))



e = figure(title="Verhältnis zwischen (CO2 Emissionen / Konsum erneuerbarer Energien) und dem BIP verschiedener Länder im Jahr 2017", x_axis_label='GDP in 100 Mrd.', y_axis_label='CO2 100mio.T/Energie TWh', plot_width = 1500, plot_height = 700)

e.circle(x = float(lst_gdp[0]), y = float(ratio_co2_ene[0]), size=5, legend_label = 'Vereinigte Arabische Emirate')
e.circle(x = float(lst_gdp[1]), y = float(ratio_co2_ene[1]), size=5, legend_label = 'Argentinien')
e.circle(x = float(lst_gdp[2]), y = float(ratio_co2_ene[2]), size=5, legend_label = 'Australien')
e.circle(x = float(lst_gdp[3]), y = float(ratio_co2_ene[3]), size=5, legend_label = 'Österreich')
e.circle(x = float(lst_gdp[4]), y = float(ratio_co2_ene[4]), size=5, legend_label = 'Belgien')
e.circle(x = float(lst_gdp[5]), y = float(ratio_co2_ene[5]), size=5, legend_label = 'Brasilien')
e.circle(x = float(lst_gdp[6]), y = float(ratio_co2_ene[6]), size=5, legend_label = 'Kanada')
e.circle(x = float(lst_gdp[7]), y = float(ratio_co2_ene[7]), size=5, legend_label = 'Schweiz')
e.circle(x = float(lst_gdp[8]), y = float(ratio_co2_ene[8]), size=5, legend_label = 'China')
e.circle(x = float(lst_gdp[9]), y = float(ratio_co2_ene[9]), size=5, legend_label = 'Deutschland')
e.circle(x = float(lst_gdp[10]), y = float(ratio_co2_ene[10]), size=5, legend_label = 'Spanien')
e.circle(x = float(lst_gdp[11]), y = float(ratio_co2_ene[11]), size=5, legend_label = 'Frankreich')
e.circle(x = float(lst_gdp[12]), y = float(ratio_co2_ene[12]), size=5, legend_label = 'England')
e.circle(x = float(lst_gdp[13]), y = float(ratio_co2_ene[13]), size=5, legend_label = 'Indonesien')
e.circle(x = float(lst_gdp[14]), y = float(ratio_co2_ene[14]), size=5, legend_label = 'Indien')
e.circle(x = float(lst_gdp[15]), y = float(ratio_co2_ene[15]), size=5, legend_label = 'Iran')
e.circle(x = float(lst_gdp[16]), y = float(ratio_co2_ene[16]), size=5, legend_label = 'Israel')
e.circle(x = float(lst_gdp[17]), y = float(ratio_co2_ene[17]), size=5, legend_label = 'Italien')
e.circle(x = float(lst_gdp[18]), y = float(ratio_co2_ene[18]), size=5, legend_label = 'Japan')
e.circle(x = float(lst_gdp[19]), y = float(ratio_co2_ene[19]), size=5, legend_label = 'Südkorea')
e.circle(x = float(lst_gdp[20]), y = float(ratio_co2_ene[20]), size=5, legend_label = 'Mexico')
e.circle(x = float(lst_gdp[21]), y = float(ratio_co2_ene[21]), size=5, legend_label = 'Niederlande')
e.circle(x = float(lst_gdp[22]), y = float(ratio_co2_ene[22]), size=5, legend_label = 'Norwegen')
e.circle(x = float(lst_gdp[23]), y = float(ratio_co2_ene[23]), size=5, legend_label = 'Polen')
e.circle(x = float(lst_gdp[24]), y = float(ratio_co2_ene[24]), size=5, legend_label = 'Russland')
e.circle(x = float(lst_gdp[25]), y = float(ratio_co2_ene[25]), size=5, legend_label = 'Saudi Arabien')
e.circle(x = float(lst_gdp[26]), y = float(ratio_co2_ene[26]), size=5, legend_label = 'Schweden')
e.circle(x = float(lst_gdp[27]), y = float(ratio_co2_ene[27]), size=5, legend_label = 'Thailand')
e.circle(x = float(lst_gdp[28]), y = float(ratio_co2_ene[28]), size=5, legend_label = 'Türkei')
e.circle(x = float(lst_gdp[29]), y = float(ratio_co2_ene[29]), size=5, legend_label = 'USA')

e.legend.visible = False
curdoc().theme = 'dark_minimal'

save(e)
conn.close()