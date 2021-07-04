import psycopg2
import pandas as pd
import sys
from bokeh.io import curdoc
from bokeh.palettes import Category20
from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource
from bokeh.models.tools import BoxSelectTool, HoverTool, BoxZoomTool, PanTool, ResetTool, SaveTool, WheelZoomTool


# Ablauf dieses Codes ist fast analog wie in "co2_emissionen.py", für ausführliche Kommentierung bitte dort nachsehen


param_dic = {
    "host"      : "localhost",
    "database"  : "projekt",
    "user"      : "postgres",
    "password"  : "postgres"
}
def connect(params_dic):
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

column_names = ["country", "code", "year", "annual co2 emissions(tonnes)"]

# Wir nutzen das Query "COALESCE(hydropower,0) + COALESCE(solar,0) + COALESCE(wind,0) + COALESCE(other)" 
# um den gesamten Konsum aller erneuerbaren Energien zu erhalten, da die einzelnen für unsere Fragestellung unwichtig sind
df = postgresql_to_dataframe(conn, "SELECT country, code, year, COALESCE(hydropower,0) + COALESCE(solar,0) + COALESCE(wind,0) + COALESCE(other) from energy where year < 2018", column_names = ["country", "code", "year", "renewable_energy_consumption"])
df.head(0)

source = ColumnDataSource(df)
source_ger = ColumnDataSource(df.loc[df['code'] == 'DEU'])
source_fra = ColumnDataSource(df.loc[df['code'] == 'FRA'])
source_ind = ColumnDataSource(df.loc[df['code'] == 'IND'])
source_usa = ColumnDataSource(df.loc[df['code'] == 'USA'])
source_chi = ColumnDataSource(df.loc[df['code'] == 'CHN'])
source_afr = ColumnDataSource(df.loc[df['code'] == 'ZAF'])
source_can = ColumnDataSource(df.loc[df['code'] == 'CAN'])
source_jap = ColumnDataSource(df.loc[df['code'] == 'JPN'])
source_bra = ColumnDataSource(df.loc[df['code'] == 'BRA'])
source_aus = ColumnDataSource(df.loc[df['code'] == 'AUS'])
source_kor = ColumnDataSource(df.loc[df['code'] == 'KOR'])
source_rus = ColumnDataSource(df.loc[df['code'] == 'RUS'])
source_sau = ColumnDataSource(df.loc[df['code'] == 'SAU'])
source_swi = ColumnDataSource(df.loc[df['code'] == 'CHE'])
source_nor = ColumnDataSource(df.loc[df['code'] == 'NOR'])


tools = [PanTool(), BoxSelectTool(), SaveTool(), WheelZoomTool(), HoverTool()]

p = figure(title="Konsum erneuerbarer Energien", x_axis_label='Jahr', y_axis_label='Konsum erneuerbarer Energien in TWh', plot_width = 1750, plot_height = 800, tools = tools, tooltips = [("Jahr", "@year"),("Energiekonsum in TWh", "@renewable_energy_consumption")])

def draw_plot(source_country, colornumber, label):
    p.line(x='year', y='renewable_energy_consumption', source=source_country, line_color = Category20[20][colornumber], legend_label = label, line_width = 2)
    p.legend.location = 'top_left'
    p.legend.background_fill_alpha = 0.3
    p.xgrid.grid_line_color = None
    p.legend.click_policy="hide"
    curdoc().theme = 'dark_minimal'
    return p

# Zeichne Graphen
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

save(p)
conn.close()