"""
Dash app: Airpolution monitoring in Sasolburg and the surrounding area

Creates interaction dashboard to visulise historical and forcasted air pollution in 
Sasolburg and the surrounding area. 

@author: Amy
"""
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots

import pandas as pd
import sqlite3

# Plot colours
forcast_color = ['#131EAA', '#950000', '#003d2d', '#320365', '#672d00', '#04424c', '#6b001f', '#375b11', '#7a007a', '#644701']

# Plotly standard colours 
#['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']

# Site names and pollutants
Site_Names = ['AJ_Jacobs','Bongani_Mabaso_Eco_Park','Leitrim','North_West_University_Vaal_campus','Sharpeville','Vanderbijlpark_NAQI','Zamdela_NAQI']
Pollutants = ['SO2', 'NO2', 'NO', 'NOx', 'O3', 'CO', 'PM2_5', 'PM10']


# Site names and pollutants improved formatting for app
Site_Names_text = ['AJ Jacobs','Bongani Mabaso Eco Park','Leitrim','North West University Vaal campus','Sharpeville','Vanderbijlpark-NAQI','Zamdela-NAQI']
Pollutants_text = ['SO2', 'NO2', 'NO', 'NOx', 'O3', 'CO', 'PM2.5', 'PM10']

# Pollutants with units
Pollutants_unit = ['SO2 (ppb)', 'NO2 (ppb)', 'NO (ppb)', 'NOx (ppb)', 'O3 (ppb)', 'CO (ppm)', 'PM2.5 (\u03BCg/m3)', 'PM10 (\u03BCg/m3)']

# Forcasting start and end dates
forcast_begin = pd.to_datetime('2022-03-01 01:00:00') 
forcast_end = pd.to_datetime('2022-03-07 23:00:00')

# Load data from database
con = sqlite3.connect("air_pollution_database.db")
cur = con.cursor()

df_main = pd.DataFrame()
df_hidden = pd.DataFrame()
for site in Site_Names:
    df = pd.read_sql(f'SELECT * FROM {site}',con)
    
    df['datetime'] = df.year.astype(str)+'-'+df.month.astype(str)+'-'+df.day.astype(str)+' '+df.time.astype(str)+':00:00'
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    df = df.sort_values(by='datetime')
    df['site'] = site
    
    df.reset_index(inplace=True)
    
    df_h = df.loc[(df['datetime'] > forcast_begin)]
    df = df.loc[(df['datetime']<= forcast_begin)]
    df_main = df_main.append(df)
    df_hidden = df_hidden.append(df_h)
    
con.close()

df_main.set_index(['site', 'index'], inplace=True)
df_main = df_main[Pollutants+['time','day','month','year','datetime']]

df_hidden.set_index(['site', 'index'], inplace=True)
df_hidden = df_hidden[Pollutants+['time','day','month','year','datetime']]

############################################################

# Load forcasted data from csv
df_forcast = pd.DataFrame()
for site in Site_Names:
    df = pd.read_csv(site+'_forcast.csv')
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    df = df.sort_values(by='datetime')
    df['site'] = site
    
    df.reset_index(inplace=True)
    
    df_forcast = df_forcast.append(df)
    
df_forcast.set_index(['site', 'index'], inplace=True)
df_forcast = df_forcast[Pollutants+['time','day','month','year','datetime']]

############################################################


# Dash app
app = dash.Dash()
app.layout = html.Div([
    
    html.Div([
        html.H1('Air pollution in Sasolburg and the surrounding area',style = {'text-align': 'center'}),
        #dcc.Markdown('''
        #              ## bhbhb
        #              '''),
        
        html.Div([
            html.H2('Map of sites'),
            html.Img(src=app.get_asset_url('image121.png'), width = '80%')
            ],style={'width': '75%', 'display': 'inline-block','text-align': 'center'}),
        
        
        
        
        html.Div([
            html.H2('Select a site'),
            dcc.Checklist(id = 'site-select', 
                          options = [{'value':0, 'label':Site_Names_text[0]},
                                     {'value':1, 'label':Site_Names_text[1]},
                                     {'value':2, 'label':Site_Names_text[2]},
                                     {'value':3, 'label':Site_Names_text[3]},
                                     {'value':4, 'label':Site_Names_text[4]},
                                     {'value':5, 'label':Site_Names_text[5]},
                                     {'value':6, 'label':Site_Names_text[6]}],
                          labelStyle={'display': 'block'},
                          value=[6]),
            #],style={'width': '33%', 'display': 'inline-block'}),
        

        
        #html.Div([
            html.H2('Select an air pollutant'),
            dcc.RadioItems(id = 'pol-select', 
                           options = [{'value':0, 'label':Pollutants_text[0]},
                                      {'value':1, 'label':Pollutants_text[1]},
                                      {'value':2, 'label':Pollutants_text[2]},
                                      {'value':3, 'label':Pollutants_text[3]},
                                      {'value':4, 'label':Pollutants_text[4]},
                                      {'value':5, 'label':Pollutants_text[5]},
                                      {'value':6, 'label':Pollutants_text[6]},
                                      {'value':7, 'label':Pollutants_text[7]}],
                           labelStyle={'display': 'block'},
                           value=0)
            ],style={'width': '25%', 'display': 'inline-block'}),
    
        
        html.Div([html.H2('Select dates',style={'textAlign': 'center'}) ]),
        
        html.Div([ 
            dcc.Slider(id='month1-slider', 
                   min=1,
                   max=12,
                   value=2,
                   step=1,
                   marks={1:'Jan', 
                          2:'Feb',
                          3:'Mac',
                          4:'Apr',
                          5:'May',
                          6:'Jun',
                          7:'Jul',
                          8:'Aug',
                          9:'Sep',
                          10:'Oct',
                          11:'Nov',
                          12:'Dec'
                          }
                   )],style={'width': '50%', 'display': 'inline-block'}),
        html.Div([ 
            dcc.Slider(id='month2-slider', 
                   min=1,
                   max=12,
                   value=4,
                   step=1,
                   marks={1:'Jan', 
                          2:'Feb',
                          3:'Mac',
                          4:'Apr',
                          5:'May',
                          6:'Jun',
                          7:'Jul',
                          8:'Aug',
                          9:'Sep',
                          10:'Oct',
                          11:'Nov',
                          12:'Dec'
                          }
                   )],style={'width': '50%', 'display': 'inline-block'}),
        
        dcc.RangeSlider(id='year-slider', 
                   min=df_main.year.min(),
                   max=df_main.year.max(),
                   allowCross=False,
                   value=[df_main.year.max(), df_main.year.max()],
                   marks={str(year): str(year) for year in df_main.year.unique()}
                   ),
        
        dcc.Graph(id='graph-out',figure={}),
        
        html.Div([
            html.H2('Air pollutant information'),
            html.Div(id='my-output')
            ],style={'width': '80%', 'display': 'inline-block','text-align': 'justify'}),
        
        html.Div([
            html.H2('Pollution level guide'),
            html.Img(src=app.get_asset_url('table.png'), width = '100%')
            ],style={'width': '95%', 'display': 'inline-block','text-align': 'center'}),
        
        ],style={'width': '90%', 'display': 'inline-block'})
],style={'display': 'flex', 'flex-direction': 'row'})



#  Callback to update plot
@app.callback(
    Output(component_id='graph-out', component_property='figure'),
    [Input(component_id='pol-select', component_property='value'),
     Input(component_id='site-select', component_property='value'),
     Input(component_id='month1-slider', component_property='value'),
     Input(component_id='month2-slider', component_property='value'),
     Input(component_id='year-slider', component_property='value')],
    prevent_initial_call=False
)
def update_my_graph(pol_chosen,site_chosen, month1, month2, year_chosen ):
    if len([site_chosen]) > 0:
        
        fig = make_subplots()
        for i in site_chosen:
            df = df_main.loc[Site_Names[i]]
            df = df.loc[(df['datetime']>=pd.to_datetime(str(round(month1))+str(round(year_chosen[0])),format='%m%Y'))]
            df = df.loc[(df['datetime']<=pd.to_datetime(str(round(month2))+str(round(year_chosen[1])),format='%m%Y'))]

            trace = go.Scatter(x=df['datetime'],
                               y=df[Pollutants[pol_chosen]],
                               name=Site_Names[i], mode='markers',
                               marker={
                                   'symbol': 'circle',
                                   'color': px.colors.qualitative.Plotly[i]
                                   })
            fig.add_trace(trace)
            
            
            df = df_hidden.loc[Site_Names[i]]
            df = df.loc[(df['datetime']>=pd.to_datetime(str(round(month1))+str(round(year_chosen[0])),format='%m%Y'))]
            df = df.loc[(df['datetime']<=pd.to_datetime(str(round(month2))+str(round(year_chosen[1])),format='%m%Y'))]

            trace = go.Scatter(x=df['datetime'],
                               y=df[Pollutants[pol_chosen]],
                               name=Site_Names[i], mode='markers',
                               showlegend=False,
                               marker={
                                   'symbol': 'circle-open',
                                   'color': px.colors.qualitative.Plotly[i]
                                   })
            fig.add_trace(trace)
            
            df = df_forcast.loc[Site_Names[i]]
            df = df.loc[(df['datetime']>=pd.to_datetime(str(round(month1))+str(round(year_chosen[0])),format='%m%Y'))]
            df = df.loc[(df['datetime']<=pd.to_datetime(str(round(month2))+str(round(year_chosen[1])),format='%m%Y'))]

            trace = go.Scatter(x=df['datetime'],
                               y=df[Pollutants[pol_chosen]],
                               name=Site_Names[i], mode='markers',
                               showlegend=False,
                               marker={
                                   'symbol': 'circle',
                                   'color': forcast_color[i]
                                   })
            fig.add_trace(trace)
            
            
        fig.update_layout(yaxis_title = Pollutants_unit[pol_chosen] )

        
        return fig
    elif len(pol_chosen) == 0:
        raise dash.exceptions.PreventUpdate
  
# Callback to update pollution info box
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='pol-select', component_property='value')
)
def update_output_div(pol_chosen):
    if pol_chosen == 0:
        text = dcc.Markdown('''### Sulphur Dioxide
The most common source of SO2 emissions is fossil fuel combustion, for example at power plants and other industrial facilities. Short-term exposures to SO2 can harm the human respiratory system and make breathing difficult. People with asthma, particularly children, are sensitive to these effects of SO2. High concentrations of SO2 in the air can also lead to the formation of other sulphur oxides (SOx). SOx reacts with other compounds in the atmosphere to form small particles. These particles contribute to particulate matter (PM) pollution.
            ''')
    if pol_chosen == 1 or pol_chosen == 2 or pol_chosen == 3:
         text = dcc.Markdown('''### Nitrogen Oxides
Nitrogen oxides (NOx) is a group of highly reactive gasses, including nitrogen dioxide, nitrous acid, and nitric acid. Nitrogen dioxide (NO2) commonly comes from fuel combustion, such as mobiles, power plants, and off-road equipment. The nitrogen oxides combine with volatile organic compounds (VOCs) to form ground-level ozone. Particulate matter is also formed from nitrogen oxides when they react with VOCs, sulfur oxides and ammonia.

Exposure to NO2 over short periods can aggravate respiratory diseases, particularly asthma. Longer exposures to elevated concentrations of NO2 may contribute to the development of asthma and potentially increase susceptibility to respiratory infections. People with asthma, as well as children and the elderly are generally at greater risk for the health effects of NO2.       
''')       
    if pol_chosen == 4:
         text = dcc.Markdown('''### Tropospheric Ozone
Tropospheric, or ground level ozone, is not emitted directly into the air, but is formed by chemical reactions between oxides of nitrogen (NOx) and volatile organic compounds (VOC). This happens when pollutants emitted by fuel combustion chemically react in the presence of sunlight.

Ozone in the air we breathe can harm our health, especially on hot sunny days when ozone can reach unhealthy levels. Ozone is a strong oxidant that can cause damage to cells and the lining fluids of the airways, as well as provoke an immune-inflammatory responses within and beyond the lung. People at greatest risk of harm from breathing air containing ozone include people with asthma.
             ''') 
    if pol_chosen == 5:
           text = dcc.Markdown('''### Carbon monoxide
Carbon monoxide (CO) is a colourless, odourless gas that can be harmful when inhaled in large amounts. The greatest sources of CO in outdoor air are cars, trucks and other vehicles or machinery that burn fossil fuels. At very high levels, which are possible indoors or in other enclosed environments, CO can cause dizziness, confusion, unconsciousness and death.
               ''')        
    if pol_chosen == 6 or pol_chosen == 7:
          text = dcc.Markdown('''### Particulate matter
Particulate matter is the term for a mixture of solid particles and liquid droplets found in the air. Particles of diameter 2.5 and 10 micrometres, or smaller, are referred to as PM2.5 and PM10, respectively.  Numerous scientific studies have linked particle pollution exposure to a variety of problems, including: premature death in people with heart or lung disease, nonfatal heart attacks, irregular heartbeat, aggravated asthma, decreased lung function and increased respiratory symptoms, such as irritation of the airways, coughing or difficulty breathing.
                                ''') 

    return text

# Run dashboard
if __name__ == '__main__':
    app.run_server()
