import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output
import dash_daq as daq
############################################################################################################################################################



external_stylesheets = ['assets/style.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    'background': '#94b3d1',
    'text': '#111111'
}
############################################################################################################################################################




'''LOADING DATA'''
st = pd.read_csv('weekly_deaths.csv' , sep = ',').fillna(0)
df = pd.read_csv('total_selected_diseases.csv').drop(columns = ['Unnamed: 0', 'Jurisdiction of Occurrence', 'MMWR Year', 'MMWR Week'])
dataset = pd.read_csv('selected_diseases.csv')

##############################################################################
diseases1 = df.iloc[:, 1:].columns

diseases = st.iloc[:, 6:].columns


st['Week Ending Date'] = pd.to_datetime(st['Week Ending Date'])

############################################################################################################################################################
############################################################################################################################################################

dis_colorscale={
        'All Cause': [0, 350000],
        'Natural Cause': [0, 250000],
        'Septicemia':[0,4000],
        'Malignant neoplasms':[0,62000],
        'Diabetes mellitus':[0,12000],
        'Alzheimer disease ':[0,20000],
        'Influenza and pneumonia':[0,7000],
        'Chronic lower respiratory diseases':[0,14000],
        'Other diseases of respiratory system':[0,4000],
        'Nephritis, nephrotic syndrome and nephrosis':[0,5000],
        'Symptoms, signs and abnormal clinical and laboratory findings':[0,5000],
        'Diseases of heart':[0,44000],
        'Cerebrovascular diseases':[0,19000],
        'Multiple Cause of Death + COVID-19':[0,5000],
        'COVID-19 as Underlying Cause of Death':[0,3000]
    }
############################################################################################################################################################


tab_style = {
    #'borderBottom': '1px solid #d6d6d6',
    'padding': '10px',
    #'fontWeight': 'bold',
    'box-shadow': '2px' '2px' '2px' '#cf9696',
    'backgroundColor': '#dce6ef',
    'border-radius': '7px',
    'height': '80px',
    'height': '150%',
    'font-size': '19px',
    'width': '100%',
    'font-family':"Calibri (Body)"
    
}

tab_selected_style = {
    'borderTop': '1px solid #cf9696',
    'borderBottom': '1px solid #cf9696',
    'backgroundColor': '#cf9696',
    'color': 'black',
    'padding': '10px',
    'border-radius': '7px',
    'height': '80px',
    'font-size': '19px',
    'fontWeight': 'bold',
    'width': '100%',
    'height': '130%',
    'font-family':"Calibri (Body)"
}





app.layout = html.Div(children=[
        html.Div(children = [
    
       
             html.P('Deaths by Diseases in the USA', style = {'fontSize': 35, 'text-align': 'center', 'margin-bottom': 0,
                                                                       'fontWeight': 'bold',
                                                                       'font-family':"Calibri (Body)"}),
             html.P('Counts of Deaths by Selected Causes from 2014 to 2021', style = {'fontSize': 25, 
                                                                                         'text-align': 'center' , 'margin-top': 0, 
                                                                                         'margin-bottom': 20,
                                                                                         'font-family':"Calibri (Body)"}),
   
         ]),
        
    
    dcc.Tabs( style = {#'width': '80%', 'height': '80%', 
                      'margin-right': '17%', 'margin-left': '17%'
                      },
             id="tabs", value='tab-1', children=[
        dcc.Tab(label='Deaths Timeline', value='tab-1', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Deaths by State', value='tab-2', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Deaths Map', value='tab-4', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Data Table', value='tab-5', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='More Info', value='tab-6', style=tab_style, selected_style=tab_selected_style),
    ]),
    
     html.Div(style = {#'width': '80%', 'height': '80%', 
                      'margin-right': '16%', 'margin-left': '16%'
                      },
                         id='tabs-content'
    ),
    

])
############################################################################################################################################################


@app.callback(
    Output('tabs-content', 'children'),
     Input('tabs', 'value'),
     
     )
############################################################################################################################################################




def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.P('Deaths Timeline of the Selected Diseases, from January 2014 to March 2021', 
                   style = {'fontSize': 25, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            html.P('Monthly and Yearly Data by Average and Total Number of Deaths for the Entire Country', 
                   style = {'fontSize': 20, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            dcc.Dropdown(
                id='line_option',
                options=[{'label': i, 'value': i} for i in diseases1],
                value=['All Cause'],
                style= {'color':'black',
                        'backgroundColor': '#dce6ef',
                        'height': '40px',
                        'font-size': '18px',
                        'font-family':"Calibri (Body)",
                        'margin-bottom': 10},
                multi = True,
                
                ),
            dcc.RadioItems(
                id = 'timely',
                options = [dict(label = 'Yearly', value = 1), 
                           dict(label = 'Monthly', value = 0)],
                value = 0,
                style = {'margin-top': 65, 
                            'margin-bottom': 0,
                         'margin-left': '1.5%',
                         'font-size': '18px'}
                ),
            dcc.RadioItems(
                id = 'aggregates',
                options = [dict(label = 'Mean', value = 0), 
                           dict(label = 'Sum', value = 1)],
                value = 0,
                style = {'font-size': '18px',
                         'margin-top': 8, 
                            'margin-bottom': 0,
                         'margin-left': '1.8%'}
                ),
            dcc.Graph(
                id='lineplot',
                figure=dict(layout=dict(autosize=True)),
                      style={'margin-top': 5,
                                'height': '100%',
                                'width': '100%'}
                )],
            className = 'box'
            )
       

    
    elif tab == 'tab-2':
        return html.Div([
            html.P('Top 10 States with the Highest Number of Deaths by Disease', 
                   style = {'fontSize': 30, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            html.P('Total Number of Deaths Between Years or by Year', 
                   style = {'fontSize': 20, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            dcc.Dropdown(
                id='disease1',
                options=[{'label': i, 'value': i} for i in diseases],
                value='All Cause',
                #className = 'box'
                style= {'color':'black',
                        'backgroundColor': '#dce6ef',
                        'height': '40px',
                        'font-size': '18px',
                        'font-family':"Calibri (Body)"},
                ),
            dcc.Graph(id = 'top10', 
                      figure=dict(layout=dict(autosize=True)),
                      style={
                                'height': '100%',
                                'width': '100%'},
                      #className = 'box'
                      ),
            
            dcc.RangeSlider(
                id = 'range',
                min = 2014,
                max = 2021,
                value = [2015, 2017],
                marks={str(i): '{}'.format(str(i)) for i in
                       [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
                className = 'box',
                
                ),
                ],
            
            #html.Br(),
            className = 'box')

    
        
    elif tab == 'tab-4':
        return html.Div([
            
            html.P('Geographic Distribution of each Disease', 
                   style = {'fontSize': 30, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            html.P('The Total Number of Deaths by Year', 
                   style = {'fontSize': 20, 
                            'text-align': 'center' , 'margin-top': 0, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
            
            dcc.Dropdown(
                id='disease',
                options=[{'label': i, 'value': i} for i in diseases],
                value='All Cause',
               # className = 'box'
               style= {'color':'black',
                        'backgroundColor': '#dce6ef',
                        'height': '40px',
                        'font-size': '18px',
                        'font-family':"Calibri (Body)"
                        },
                ),
            dcc.Graph(id = 'choropleth',
                      figure=dict(layout=dict(autosize=True)),
                      style={
                                'height': '100%',
                                'width': '100%'}
                            
                      ),
            
            daq.Slider(
                id = 'year',
                min = 2014,
                max = 2021,
                value = 2017,
                marks={str(i): '{}'.format(str(i)) for i in
                       [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021]},
                handleLabel={"showCurrentValue": True,"label": " "},
                size=800,
                color = 'cf9696',
                className = 'box'
                
                )
            ],
                                
            className = 'box')

    elif tab == 'tab-5':
        return html.Div([
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in dataset.iloc[:, 1:].columns],
                data=dataset.to_dict('records'),
                style_table={'overflowX': 'auto', 'max-height': '790px'},
                style_cell={
        # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'overflow': 'hidden',
                'textOverflow': 'ellipsis',
                'fontSize': '10px',
                'padding': '5px',
                'font-family':"Calibri (Body)"},
                style_header={
                    'backgroundColor': '#F0AB9E',
                    'fontWeight': 'bold', 
                    'fontSize': '15px',
                    'overflow': 'hidden',
                    'font-family':"Calibri (Body)"
                    },
                style_cell_conditional=[
        {
            'if': {'column_id': c},
            'textAlign': 'left'
        } for c in ['Jurisdiction of Occurrence']
    ],
                )
        ], className = 'box')
    
    
    elif tab == 'tab-6':
        return html.Div([
            
            
                    html.P('Diseases Description:',
                           style = {'fontSize': 26, 
                            'text-align': 'left' , 
                            'margin-top': 10, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
                            
                        
                     dcc.Markdown('''
                        * **All Cause:** deaths caused by all the diseases in this dataset
                            
                        * **Natural Causes**
                            
                        * **Septicemia:** (blood poisoning) invasion of the bloodstream by pathogenic agents and especially bacteria along with their toxins from a localized infection (as of the lungs or skin) that is accompanied by acute systemic illness
                            
                        * **Malignant Neoplasm:** a cancerous tumor, an abnormal growth that can grow uncontrolled and spread to other parts of the body
                            
                        * **Diabetes Mellitus:** (sugar diabetes) condition that occurs when the body can't use glucose (a type of sugar) normally
                            
                        * **Alzheimer:** progressive neurologic disorder that causes the brain to shrink (atrophy) and brain cells to die.
                            
                        * **Influenza & Pnemonia:** viral infection that attacks your respiratory system — your nose, throat and lungs
                            
                        * **Chronic lower Respiratory Disease:** a group of pathologies that obstruct the lungs, which mainly includes chronic obstructive pulmonary disease (COPD) and asthma. 
                            
                        * **Other Diseases of Respiratory System:** diseases that affect the air passages, including the nasal passages, the bronchi and the lungs.
                            
                        * **Nephritis, Nephrotic Syndrome and Nephrosis:** A condition in which the tissues in the kidney become inflamed and have problems filtering waste from the blood
                            
                        * **Symptoms, Signs and Abnormal Clinical and Laboratory Findings Not Elsewhere Found**
                            
                        * **Diseases of Heart:** a range of conditions that affect your heart
                            
                        * **Multiple Cause of Death + COVID-19**
                            
                        * **COVID-19 as Underlying Cause of Death**
                            
                         ''', style = {"margin-left": '30px',
                         "margin-bottom": '30px'}),
            
            
           
                       
                    html.P('Data Sources:',
                           style = {'fontSize': 26, 
                            'text-align': 'left' , 
                            'margin-top': 10, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
                            
                   dcc.Markdown('''    
                                
                        **Weekly Counts of Deaths by State and Select Causes**
                            
                        **Data Time Span:**         January 1, 2014 - March 13, 2021
                            
                        **Data Published By:**     National Center for Health Statistics
                            
                        **For More Details Visit:** ['https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/3yf8-kanr'] 
                        ''', style = {"margin-left": '30px'}),
                        
                    html.P('Downloads:',
                           style = {'fontSize': 26, 
                            'text-align': 'left' , 
                            'margin-top': 10, 
                            'margin-bottom': 10,
                            'font-family':"Calibri (Body)"}),
                            
                        
                     dcc.Markdown('''
                        **Download Data From the Source:** [https://data.cdc.gov/NCHS/Weekly-Counts-of-Deaths-by-State-and-Select-Causes/3yf8-kanr']
                         ''', style = {"margin-left": '30px'}),
                         
                         
                         
                    
        
        
    ] , style={'textAlign': 'left',
                   'background-color': '#dce6ef',
                   'border-radius': '5px',
                   'padding': '15px',
                   'margin': '20px',
                   'box-shadow': '2px' '2px' '2px' '#dce6ef',
                   'height': '100%'})
    

@app.callback(
     Output('lineplot', 'figure'),
    [Input('line_option', 'value'),
     Input('timely', 'value'),
     Input('aggregates', 'value')])
    
      
def lineplot(disease, time, agg):
    gg = pd.read_csv('total_selected_diseases.csv').drop(columns = ['Unnamed: 0', 'Jurisdiction of Occurrence', 'MMWR Year', 'MMWR Week'])
    gg['Week Ending Date'] = pd.to_datetime(gg['Week Ending Date'])
    gg = gg.set_index('Week Ending Date')
    df1 = gg.groupby(pd.Grouper(freq="M")).mean().reset_index()
    data_line = []
    colory = ['rgb(0, 147, 146)','rgb(241, 234, 200)','rgb(250, 235, 162)',
                      'rgb(255, 226, 87)','rgb(229, 185, 173)','rgb(69, 176, 175)','rgb(114, 170, 161)','rgb(130, 181, 135)',
                  'rgb(177, 199, 179)','rgb(207, 250, 211)', 'rgb(250, 167, 145)','rgb(217, 137, 148)',
                          'rgb(208, 88, 126)', 'rgb(250, 167, 145)','rgb(217, 137, 148)','rgb(250, 167, 145)','rgb(217, 137, 148)']

    for i in range(len(disease)):
        if time == 0:
            if agg == 0:
                df1 = gg.groupby(pd.Grouper(freq="M")).mean().reset_index()
            elif agg == 1:
                df1 = gg.groupby(pd.Grouper(freq="M")).sum().reset_index()
        elif time == 1:
            if agg == 0:
                df1 = gg.groupby(pd.Grouper(freq="Y")).mean().reset_index()
            elif agg == 1:
                df1 = gg.groupby(pd.Grouper(freq="Y")).sum().reset_index()
        data_line.append(dict(type='scatter',x=df1['Week Ending Date'], y=df1[disease[i]], 
                              mode='lines',line=dict(color = colory[i], width = 3.5),
                              name = disease[i],
                              ))
        figr = go.Figure(data=data_line)
        figr.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           font = dict(size = 15, color = 'black'),
                           
                           autosize=False,
                            #width=1300,
                            height=550,
                            margin=dict(
                                l=50,
                                r=50,
                                b=50,
                                t=10,
                                pad=4),
                            hoverlabel=dict(
                            bgcolor="white",
                            font_size=16,
                            font_family="Calibri (Body)"))
    
    return figr
 
@app.callback(
     Output('top10', 'figure'),
    [Input('disease1', 'value'),
     Input('range', 'value')])

   
def top10(disease, date):
    
    dis = st.loc[:, [disease, "MMWR Year",'State']]
    between  = dis[(dis['MMWR Year']>=date[0]) & (dis['MMWR Year']<=date[1])]
    sumofdeaths = between.groupby('State').sum().reset_index()
    top10withmoredeaths = sumofdeaths.sort_values(by=disease,ascending=False)[:10]
    top10withmoredeaths = top10withmoredeaths.reset_index().sort_index(ascending=False)
    
    fig= px.bar(top10withmoredeaths, x=disease, y = 'State', 
                          orientation='h', color = disease, 
                          color_continuous_scale= 'Tealrose',
                          range_color = (dis_colorscale[disease][0], dis_colorscale[disease][1]))
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           font = dict(size = 15, color = 'black'),
                            #width=1200,
                            height=550,
                            margin=dict(
                                l=50,
                                r=50,
                                b=100,
                                t=50,
                                pad=4),
                            hoverlabel=dict(
                            bgcolor="white",
                            font_size=16,
                            font_family="Calibri (Body)"
    ))
    
    fig.layout.coloraxis.colorbar.title = ''
    fig.update_yaxes(title_text = ' ')
    
    return fig

@app.callback(
    Output('choropleth', 'figure'),
    [Input('disease', 'value'),
     Input('year', 'value')])

def display_choropleth(disease, year):
    
    

    choropleth_dataset = st[(st['MMWR Year']==year)]
    choropleth_dataset=choropleth_dataset.groupby(['state_abv', 'State']).sum().reset_index()
    fig = px.choropleth(
        choropleth_dataset,
        color = disease,
        locationmode="USA-states",
        locations = 'state_abv',
        hover_name='State',
        range_color = (dis_colorscale[disease][0], dis_colorscale[disease][1]),
        color_continuous_scale="Tealrose",
        scope = 'usa')
    
    fig.update_layout(legend=dict(orientation="h",yanchor="bottom",y=1.02,
                                xanchor="right",x=1),
                           paper_bgcolor= 'rgba(0,0,0,0)',
                           plot_bgcolor= 'rgba(0,0,0,0)',
                           geo=dict(bgcolor= 'rgba(0,0,0,0)'),
                                    margin=dict(l=0, r=100, t=60, b=0),
                            font = dict(size = 15, color = 'black'),
                            autosize=False,
                           # marker =  dict('colorbar' : dict('len': '0.7')),
                            #width=1200,
                            height=550,
                            hoverlabel=dict(
                            bgcolor="white",
                            font_size=16,
                            
                            font_family="Calibri (Body)",
                            ),
                            
        
                           )
    fig.layout.coloraxis.colorbar.title = ''
    #fig.update_traces(colorbar_len = 5, selector = dict(type = 'chloropleth'))
    
    return fig
############################################################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)
    
