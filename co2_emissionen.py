import psycopg2
import sys
import pandas as pd
from bokeh.palettes import Category20
from bokeh.plotting import figure, save, curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.tools import BoxSelectTool, HoverTool, BoxZoomTool, PanTool, ResetTool, SaveTool, WheelZoomTool


# Verbindung zum PostgreSQL Server aufbauen
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


# Wir nutzen "Pandas" zum verwalten und zugreifen auf unsere Datenbank aus PostgreSQL, wir überführen die Tabellen aus PostgreSQL in eine Dataframe, die wir für Python nutzen können
# Diese Funktion ist der erste Schritt um das zu ermöglichen, pandas verbindet sich hier mit der postgreSQL Datenbank
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

# SQL-Query für PostgreSQL, um alle Daten (in unserem Fall alle Daten aus der Tabelle "co2" mit einem jahr > 1865) in die Dataframe zu überführen
df = postgresql_to_dataframe(conn, "select * from co2 where year > 1865", column_names)
df.head(0)

# wir teilen die Werte für die CO2 Emissionen durch num, damit wir eine lesbarere Zahl erhalten
num = 100000000
df['annual co2 emissions(tonnes)'] /= num

# Wir teilen den jeweiligen Ländern die entsprechenden Daten zu:
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

# zum Graphen-Zeichnen nutzen wir das Modul "Bokeh", unten stehender Code zeichnet den Graphen

tools = [PanTool(), BoxSelectTool(), SaveTool(), WheelZoomTool(), HoverTool()]

p = figure(title="jährliche CO2 Emissionen verschiedener Länder", x_axis_label='Jahr', y_axis_label='CO2 Emissionen in 100 Mio. Tonnen', plot_width = 1750, plot_height = 800, tools = tools, tooltips = [("Jahr", "@year"),("CO2 Emissionen", "@{annual co2 emissions(tonnes)}")])

# Funktion zum zeichnen eines Graphen, wir müssen lediglich nur noch die nötigen Daten eines Landes bereitstellen "source_country", farben und label ebenfalls zur Identifizierung später im Graphen
def draw_plot(source_country, colornumber, label):
    p.left[0].formatter.use_scientific = False
    p.line(x='year', y='annual co2 emissions(tonnes)', source=source_country, line_color = Category20[20][colornumber], legend_label = label, line_width = 3)
    p.legend.location = 'top_left'
    p.legend.background_fill_alpha = 0.3
    p.xgrid.grid_line_color = None
    p.legend.click_policy="hide"
    curdoc().theme = 'dark_minimal'
    return p


# zeichne Graphen
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