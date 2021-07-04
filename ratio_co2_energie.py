from co2_emissionen import df as df1
from erneuerbare_energien import df as df2
from bokeh.layouts import column
import pandas as pd
from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.models.tools import BoxSelectTool, HoverTool, BoxZoomTool, PanTool, ResetTool, SaveTool, WheelZoomTool

# wir importieren die Dataframes aus unseren Dateien co2_emissionen und erneuerbare_energien, damit wir uns nicht nochmal mit der SQL Datenbank verbinden müssen
# 
# Für das Verhältnis co2/erneuerbare energien brauchen wir jeweils die Daten aus dem Dataframe der co2_emissionen und der erneuerbaren_energien 

df_ger_co2 = df1.loc[df1['code'] == 'DEU'][['annual co2 emissions(tonnes)']]
df_ger_eng = df2.loc[df2['code'] == 'DEU'][['renewable_energy_consumption']]

# wir haben 2 dataframes, wir brauchen jedoch 1, welches beide Daten enthält (co2 emissionen und den Konsum der erneuerbaren Energien)
# definiere Funktion, die eine Datafram zu einer Liste macht
def df_to_list(dataframe):
    records = dataframe.to_records(index=False)
    result = list(records)

    return result

energy_ger = df_to_list(df_ger_eng)
co2_ger = df_to_list(df_ger_co2)

# Da wir nur die Jahre 1965 - 2017 für die erneuerbaren Energien haben, brauchen wir lediglich die letzten 53 Elemente der Liste mit den Co2_Emissionen (diese hat über 152 Elemente),
# so erhalten wir effektiv die Werte vom Jahr 1965 bis zum Jahr 2017 und die Liste stimmt 1 zu 1 mit der Liste der erneuerbaren Energien überein
# d.h. Element an index 0 beinhaltet den wert für 1965 in beiden Listen

co2_ger = co2_ger[99:]

# Die Werte in der Liste befinden sich in Tupelformat, ungefähr so: [(20,), (24,)]
# hiermit fixen wir dieses Problem und erhalten "normale" Listenelemente
liste_co2 = [list(x) for x in co2_ger]
liste_energie = [list(x) for x in energy_ger]

# Wir überführen die Liste nun in ein Dictionary um es dann zu einer pandas Dataframe zu machen die wir dann für unseren Graphen nutzen können
d = {'co2': liste_co2, 'energy' : liste_energie}
df_ger = pd.DataFrame(d)
source_ger = ColumnDataSource(df_ger)



r = figure(title="Verhältnis zwischen CO2 Emissionen und dem Konsum erneuerbarer Energien in Deutschland im Laufe der Jahre von 1965 - 2017", x_axis_label='CO2 Emissionen in 100 Mio. Tonnen', y_axis_label='Konsum erneuerbarer Energien in TWh', plot_width = 1500, plot_height = 700)

r.circle(x = 'co2', y = 'energy', source=source_ger, size=10, color = 'green')
r.xgrid.grid_line_color = None
curdoc().theme = 'dark_minimal'

# Wir haben einen Slider in unseren Graphen eingebaut, um diesen nutzen zu können nutzen wir eine Callback funktion (update_plot)
def update_plot(attr, old, new):
    yr = slider.value
    new_data = {
        # je nachdem, welchen Wert der Slider hat, springe zu diesem Index in der Dataframe (oder Tabelle) und gibt diesen Wert aus
        # in unserem Fall ist co2 unsere x-Achse und energy unsere y-Achse, die Werte werden demnach für diese Achsen eingetragen
        'co2' : df_ger.loc[yr].co2,
        'energy' : df_ger.loc[yr].energy
    }
    # übergib die Daten
    source_ger.data = new_data

# Sliderobjekt definieren
slider = Slider(start = 0, end = 52, value = 0, title = 'Jahr: 0:1965, 1:1966,..., 52:2017')

# was passiert, wenn der Slider genutzt wird
slider.on_change('value', update_plot)

# Darstellung/Position des Sliders über den Graphen
layout = column((slider),r)
curdoc().add_root(layout)

# bokeh serve --show ratio_co2_energie.py

# andere Länder die wir einfügen könnten, jedoch haben wir uns entschlossen das nicht zu tun, da der Graph sonst zu unübersichtlich wird

# df_chi_co2 = df1.loc[df1['code'] == 'CHN'][['annual co2 emissions(tonnes)']]
# df_chi_eng = df2.loc[df2['code'] == 'CHN'][['renewable_energy_consumption']]

# df_ind_co2 = df1.loc[df1['code'] == 'IND'][['annual co2 emissions(tonnes)']]
# df_ind_eng = df2.loc[df2['code'] == 'IND'][['renewable_energy_consumption']]

# df_usa_co2 = df1.loc[df1['code'] == 'USA'][['annual co2 emissions(tonnes)']]
# df_usa_eng = df2.loc[df2['code'] == 'USA'][['renewable_energy_consumption']]

# df_afr_co2 = df1.loc[df1['code'] == 'ZAF'][['annual co2 emissions(tonnes)']]
# df_afr_eng = df2.loc[df2['code'] == 'ZAF'][['renewable_energy_consumption']]

# df_can_co2 = df1.loc[df1['code'] == 'CAN'][['annual co2 emissions(tonnes)']]
# df_can_eng = df2.loc[df2['code'] == 'CAN'][['renewable_energy_consumption']]

# df_jap_co2 = df1.loc[df1['code'] == 'JPN'][['annual co2 emissions(tonnes)']]
# df_jap_eng = df2.loc[df2['code'] == 'JPN'][['renewable_energy_consumption']]

# df_bra_co2 = df1.loc[df1['code'] == 'BRA'][['annual co2 emissions(tonnes)']]
# df_bra_eng = df2.loc[df2['code'] == 'BRA'][['renewable_energy_consumption']]

# df_aus_co2 = df1.loc[df1['code'] == 'AUS'][['annual co2 emissions(tonnes)']]
# df_aus_eng = df2.loc[df2['code'] == 'AUS'][['renewable_energy_consumption']]

# df_kor_co2 = df1.loc[df1['code'] == 'KOR'][['annual co2 emissions(tonnes)']]
# df_kor_eng = df2.loc[df2['code'] == 'KOR'][['renewable_energy_consumption']]

# df_rus_co2 = df1.loc[df1['code'] == 'RUS'][['annual co2 emissions(tonnes)']]
# df_rus_eng = df2.loc[df2['code'] == 'RUS'][['renewable_energy_consumption']]

# df_sau_co2 = df1.loc[df1['code'] == 'SAU'][['annual co2 emissions(tonnes)']]
# df_sau_eng = df2.loc[df2['code'] == 'SAU'][['renewable_energy_consumption']]

# df_swi_co2 = df1.loc[df1['code'] == 'CHE'][['annual co2 emissions(tonnes)']]
# df_swi_eng = df2.loc[df2['code'] == 'CHE'][['renewable_energy_consumption']]

# df_nor_co2 = df1.loc[df1['code'] == 'NOR'][['annual co2 emissions(tonnes)']]
# df_nor_eng = df2.loc[df2['code'] == 'NOR'][['renewable_energy_consumption']]

# energy_chi = df_to_list(df_chi_eng)
# co2_chi = df_to_list(df_chi_co2)

# energy_ind = df_to_list(df_ind_eng)
# co2_ind = df_to_list(df_ind_co2)

# energy_usa = df_to_list(df_usa_eng)
# co2_usa = df_to_list(df_usa_co2)

# energy_afr = df_to_list(df_afr_eng)
# co2_afr = df_to_list(df_afr_co2)

# energy_can = df_to_list(df_can_eng)
# co2_can = df_to_list(df_can_co2)

# energy_jap = df_to_list(df_jap_eng)
# co2_jap = df_to_list(df_jap_co2)

# energy_bra = df_to_list(df_bra_eng)
# co2_bra = df_to_list(df_bra_co2)

# energy_aus = df_to_list(df_aus_eng)
# co2_aus = df_to_list(df_aus_co2)

# energy_kor = df_to_list(df_kor_eng)
# co2_kor = df_to_list(df_kor_co2)

# energy_rus = df_to_list(df_rus_eng)
# co2_rus = df_to_list(df_rus_co2)

# energy_sau = df_to_list(df_sau_eng)
# co2_sau = df_to_list(df_sau_co2)

# energy_swi = df_to_list(df_swi_eng)
# co2_swi = df_to_list(df_swi_co2)

# energy_nor = df_to_list(df_nor_eng)
# co2_nor = df_to_list(df_nor_co2)


# co2_chi = co2_chi[86:]
# co2_ind = co2_ind[88:]
# co2_usa = co2_usa[99:]
# co2_afr = co2_afr[81:]
# co2_can = co2_can[99:]
# co2_jap = co2_jap[97:]
# co2_bra = co2_bra[64:]
# co2_aus = co2_aus[99:]
# co2_kor = co2_kor[20:]
# co2_rus = co2_rus[26:]
# co2_sau = co2_sau[28:]
# co2_swi = co2_swi[99:]
# co2_nor = co2_nor[99:]