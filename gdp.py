import psycopg2
import pandas as pd
import sys
from bokeh.palettes import Category20
from bokeh.plotting import figure, save, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.tools import BoxSelectTool, HoverTool, BoxZoomTool, PanTool, ResetTool, SaveTool, WheelZoomTool

# Der Verbindungsprozess ist analog wie in allen anderen py Dateien, für eine ausführliche Erklärung bitte in "co2_emissionen.py" nachschauen
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
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 

    print("Connection successful")
    return conn

def postgresql_to_dataframe(conn, select_query, column_names):
    cursor = conn.cursor()
    try:
        cursor.execute(select_query)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    tupples = cursor.fetchall()
    cursor.close()
    
    df = pd.DataFrame(tupples, columns=column_names)
    return df


conn = connect(param_dic)

# Aufgrund der "schlechten" Formatierung der Daten in der CSV Datei, ist diese lange Liste an "column_names" notwendig
df = postgresql_to_dataframe(conn, "select * from gdp", column_names = ["Country Name","Country Code","Indicator Name","Indicator Code","1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"])
df.head(0)

# um die Daten nun übersichtlicher zu gestalten, transponieren wir die Tabelle.
# so löschen wir alle "Jahresspalten" und erzeugen 2 neue Spalten, einmal mit dem Jahreswert und einmal mit dem dazugehörigen GDP des zugehörigen Landes
df = pd.melt(df, id_vars=['Country Name', 'Country Code'], value_vars=["1960","1961","1962","1963","1964","1965","1966","1967","1968","1969","1970","1971","1972","1973","1974","1975","1976","1977","1978","1979","1980","1981","1982","1983","1984","1985","1986","1987","1988","1989","1990","1991","1992","1993","1994","1995","1996","1997","1998","1999","2000","2001","2002","2003","2004","2005","2006","2007","2008","2009","2010","2011","2012","2013","2014","2015","2016","2017","2018","2019"])

num = 100000000000
df['value'] /= num


source_ger = ColumnDataSource(df.loc[df['Country Code'] == 'DEU'])
source_fra = ColumnDataSource(df.loc[df['Country Code'] == 'FRA'])
source_ind = ColumnDataSource(df.loc[df['Country Code'] == 'IND'])
source_usa = ColumnDataSource(df.loc[df['Country Code'] == 'USA'])
source_chi = ColumnDataSource(df.loc[df['Country Code'] == 'CHN'])
source_afr = ColumnDataSource(df.loc[df['Country Code'] == 'ZAF'])
source_can = ColumnDataSource(df.loc[df['Country Code'] == 'CAN'])
source_jap = ColumnDataSource(df.loc[df['Country Code'] == 'JPN'])
source_bra = ColumnDataSource(df.loc[df['Country Code'] == 'BRA'])
source_aus = ColumnDataSource(df.loc[df['Country Code'] == 'AUS'])
source_kor = ColumnDataSource(df.loc[df['Country Code'] == 'KOR'])
source_rus = ColumnDataSource(df.loc[df['Country Code'] == 'RUS'])
source_sau = ColumnDataSource(df.loc[df['Country Code'] == 'SAU'])
source_swi = ColumnDataSource(df.loc[df['Country Code'] == 'CHE'])
source_nor = ColumnDataSource(df.loc[df['Country Code'] == 'NOR'])

tools = [PanTool(), BoxSelectTool(), SaveTool(), WheelZoomTool(), HoverTool()]
c = figure(title="Bruttoinlandsprodukt verschiedener Länder", x_axis_label='Jahr', y_axis_label='GDP in 100Mrd', plot_width = 1750, plot_height = 800, tools = tools, tooltips = [("Jahr", "@variable"),("GDP in 100Mrd.", "@value $")])


def draw_plot(source_country, colornumber, label):
    c.line(x= 'variable', y='value', source=source_country, line_color = Category20[20][colornumber], legend_label = label, line_width = 3)
    c.legend.location = 'top_left'
    c.legend.background_fill_alpha = 0.3
    c.xgrid.grid_line_color = None
    c.legend.click_policy="hide"
    curdoc().theme = 'dark_minimal'
    return c


draw_plot(source_ger, 0, 'Deutschland')
draw_plot(source_chi, 1, 'China')
draw_plot(source_ind, 2, 'Indien')
draw_plot(source_usa, 3, 'USA')
draw_plot(source_afr, 4, 'Süd-Afrika')
draw_plot(source_can, 5, 'Kanada')
draw_plot(source_jap, 6, 'Japan')
draw_plot(source_bra, 7, 'Brasilien')
draw_plot(source_aus, 8, 'Australien')
draw_plot(source_kor, 9, 'Südkorea')
draw_plot(source_rus, 10, 'Russland')
draw_plot(source_sau, 12, 'Saudi Arabien')
draw_plot(source_swi, 13, 'Schweiz')
draw_plot(source_nor, 14, 'Norwegen')


save(c)

conn.close() 