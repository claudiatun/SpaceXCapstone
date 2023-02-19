# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown', options = [ 
                                {'label' : 'All Sites' , 'value': 'ALL' }, {'label' : 'CCAFS LC-40' , 'value': 'CCAFS LC-40' }, {'label' : 'VAFB SLC-4E' , 'value': 'VAFB SLC-4E' }, 
                                {'label' : 'KSC LC-39A' , 'value': 'KSC LC-39A' }, {'label' : 'CCAFS SLC-40' , 'value': 'CCAFS SLC-40' }],
                                value = 'ALL', placeholder = 'Select a Launch Site here',
                                searchable = True
                                
                                 ),


                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                marks={0: '0',
                                100: '100'},
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output to visualize success counts
#If ALL sites are selected, we will use all rows in the dataframe spacex_df to render and return a pie chart graph to show the total success launches (i.e., the total count of class column)
#If a specific launch site is selected, you need to filter the dataframe spacex_df first in order
#to include the only data for the selected site. Then, render and return a pie chart graph to show the success (class=1) count and failed (class=0) count for the selected site.

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

#call back function that return the pie chart of success counts
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class',      #in plotly express, pie chart function automically count the values paramter, in this case, class
        names='Launch Site', 
        title='Total Success Launches by Sites')
        return fig

    else:
        #filter the data by the chosen site
        filtered_df = filtered_df[filtered_df['Launch Site']== entered_site]
        
        #group data by class( 0 or 1), compute size/count of each group and store in a new column called class count that has the count of class values
        filtered_df=filtered_df.groupby(['class']).size().reset_index(name='class count')
        
        fig=px.pie(filtered_df,values='class count',names='class',title=f"Total Success Launches for site {entered_site}")
        return fig
        # return the outcomes piechart for a selected site
        



# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id="payload-slider", component_property="value")])

def get_scatter_chart(entered_site,payload_selected):

    if entered_site=='ALL':
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_selected[0],payload_selected[1])]
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title='Success count on Payload mass for all sites')
        return fig
    else:
        filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_selected[0],payload_selected[1])]
        filtered_df = filtered_df[filtered_df['Launch Site']==entered_site]
        fig=px.scatter(filtered_df ,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Success count on Payload mass for site {entered_site}")
        return fig


'''
def get_scatter_chart(entered_site, payload_selected):


    
    if entered_site == 'ALL':
       
        #filtered_df = filtered_df[ (filtered_df['Payload Mass (kg)'] > payload[0]) & (filtered_df['Payload Mass (kg)'] < payload[1])]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].between(payload[0],payload[1] ) ]
        fig = px.scatter(filtered_df, x="Payload Mass (kg)", y="class", color="Booster Version Category", title='Correlation between Payload and Success for all sites')
        return fig

    else:
        filtered_df= filtered_df[filtered_df['Launch Site']== entered_site]
        filtered_df = filtered_df[filtered_df['Payload Mass (kg)'].between(payload[0],payload[1] ) ]

        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category',title=f"Correlation between Payload and Success for Site {entered_site}")
        return fig

    '''


# Run the app
if __name__ == '__main__':
    app.run_server()
