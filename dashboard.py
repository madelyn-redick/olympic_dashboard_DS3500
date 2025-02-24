import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# convert data to dataframe
df_olympic = pd.read_csv("dataset_olympics.csv")

# select only certain columns
df_olympic = df_olympic[["Team", "Year", "Sport", "Medal"]]

# drop NaN and sort by year
df_olympic = df_olympic.dropna().sort_values(by="Year", ascending=True).reset_index().drop(columns=["index"])

# remove teams not associated with a country
countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia", "Australia",
    "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin",
    "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad", "Chile", "China", "Colombia",
    "Comoros", "Congo (Congo-Brazzaville)", "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
    "Democratic Republic of the Congo (Congo-Kinshasa)", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini",
    "Ethiopia", "Fiji", "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Great Britain","Greece", "Grenada", "Guatemala",
    "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq", "Ireland",
    "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Kosovo", "Kuwait", "Kyrgyzstan",
    "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique", "Myanmar (formerly Burma)", "Namibia", "Nauru", "Nepal",
    "Netherlands", "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea", "North Macedonia", "Norway", "Oman", "Pakistan",
    "Palau", "Palestine State", "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Puerto Rico", "Qatar", "Romania",
    "Russia", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia", "South Africa",
    "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Tajikistan", "Tanzania", "Thailand",
    "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
    "United States", "Uruguay", "Uzbekistan", "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"]
countries_mask = df_olympic["Team"].isin(countries)
df_olympic = df_olympic[countries_mask]

# get sport options
sport_options = []
for sport in df_olympic["Sport"].unique():
    sport_options.append({"label": sport, "value": sport})

# get team options
team_options = []
for team in df_olympic["Team"].unique():
    team_options.append({"label": team, "value": team})

# get the range of available years
available_years = sorted(df_olympic["Year"].unique())

# write description an instructions
instructions = '''
## Olympic Medals Dashboard
Welcome to the Olympic Medals Dashboard. This dashboard allows you to explore Olympic medal data by selecting sports, 
countries, medals, and years.

**Instructions:**
- Select one or more sports from the "Select Sports" dropdown. You can choose one or multiple sports to analyze.
- Choose one or more countries from the "Select Countries" dropdown. Select the countries you want to include in the analysis.
- Use the "Select Medal(s)" checklist to choose the types of medals (Gold, Silver, Bronze) you want to include in the analysis.
- Adjust the year range using the Range Slider to focus on specific years of interest.
- In the "Scatter Plot" tab, you'll see a line chart showing the medal count over time for the selected sports, countries, medals, and years.
- In the "Histogram" tab, a histogram displays the distribution of medals for the selected criteria.

Feel free to enjoy the visualizations and gain insight into Olympic medal statistics.
Enjoy exploring the Olympic Medals Dashboard!
'''

def main():

    # Create app
    app = Dash(__name__)

    # Design app layout
    app.layout = html.Div([
        dcc.Tabs([

            # First tab for Markdown cell
            dcc.Tab(label='Instructions', children=[
                dcc.Markdown(children=instructions)
            ]),

            # Scatter plot tab
            dcc.Tab(label='Scatter Plot', children=[
                # Scatter plot
                dcc.Graph(id='scatter-plot'),

                # Range slider for year
                dcc.RangeSlider(
                    id="year-range-scatter",
                    min=df_olympic["Year"].min(),
                    max=df_olympic["Year"].max(),
                    step=1,
                    marks={str(year): str(year) for i, year in enumerate(df_olympic["Year"].unique()) if
                           year % 10 == 0},
                    value=[df_olympic["Year"].min(), df_olympic["Year"].max()],
                    tooltip={"placement": "bottom", "always_visible": True},
                ),

                # Button
                html.Button("Clear All Filters", id="clear-all", style={'margin': '10px'}),

                # Select sports - dropdown
                html.Div([dcc.Dropdown(
                    id="sport-dropdown",
                    options=[{"label": sport, "value": sport} for sport in df_olympic["Sport"].unique()],
                    value=[None],
                    multi=True,
                    placeholder="Select Sports..."
                )], style={'margin': '10px'}),

                # Select countries - dropdown
                html.Div([dcc.Dropdown(
                    id="country-input",
                    options=[{"label": team, "value": team} for team in df_olympic["Team"].unique()],
                    value=[None],
                    multi=True,
                    placeholder="Select Countries..."
                )], style={'margin': '10px'}),

                # Select type of medal - checkboxes
                dcc.Markdown(children="#### Select Medal(s):"),
                html.Div([dcc.Checklist(
                    id="medal-checklist",
                    options=[
                        {'label': 'Gold', 'value': 'Gold'},
                        {'label': 'Silver', 'value': 'Silver'},
                        {'label': 'Bronze', 'value': 'Bronze'},
                    ],
                    value=["Gold", "Silver", "Bronze"],
                    inline=True
                )], style={'margin': '10px'})
            ]),

            # Histogram tab
            dcc.Tab(label='Histogram', children=[
                # Histogram
                dcc.Graph(id='histogram-plot')
            ])
        ])
    ])

    def get_title(medals, sports):
        """ creates a title for visualizations based on number of medals and sports

        Arguments:
            medals (list): list of all selected medals
            sports (list): list of all selected sports

        Returns:
            title (str): final result of title
        """

        # default title (no medal or sport selected)
        if (medals is None or len(medals) == 0) or (sports is None or len(sports) == 0):
            title = ""
            return title

        # format commas based on number of each
        title = ""
        for item in [medals, sports]:
            if len(item) > 2:
                title += ", ".join(item[:-1]) + ", and " + item[-1]
            elif len(item) == 2:
                title += item[0] + " and " + item[1]
            else:
                title += item[0]

            if [medals, sports].index(item) == 0:
                title += " Medals Over Time for "

        return title

    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('sport-dropdown', 'value'),
         Input('country-input', 'value'),
         Input('medal-checklist', 'value'),
         Input('year-range-scatter', 'value')]
    )
    def update_scatter_plot(selected_sports, selected_countries, selected_medals, year_range):
        """ re-plots scatter plot based on given selections of sports, countries, and medals

        Arguments:
            selected_sports (list): list of desired sports
            selected_countries (list): list of desired countries
            selected_medals (list): list of desired type of medal
            year_range (list): list of selected years (based on range slider)

        Returns:
            scatter_plot (plotly graph object): updated visualization
        """

        # filter data based on selected sports and countries
        filtered_df = df_olympic[
            (df_olympic['Sport'].isin(selected_sports)) & (df_olympic['Team'].isin(selected_countries))]

        # filter based on selected medals
        filtered_df = filtered_df[filtered_df['Medal'].isin(selected_medals)]

        # group by year, sum medals for each year
        group_df = filtered_df.groupby(['Year', 'Team']).size().reset_index(name='MedalCount')

        # create scatter plot
        scatter_plot = px.line(group_df, title=get_title(selected_medals, selected_sports), x='Year',
                               y='MedalCount', color='Team', markers = True)

        # update range of years
        scatter_plot.update_xaxes(range=[year_range[0], year_range[1]])

        # change y-axis title
        scatter_plot.update_yaxes(title_text="Medal Count")

        # set font
        scatter_plot.update_layout(font=dict(family='Times New Roman', size=14))

        return scatter_plot

    @app.callback(
        Output('histogram-plot', 'figure'),
        [Input('sport-dropdown', 'value'),
         Input('country-input', 'value'),
         Input('medal-checklist', 'value'),
         Input('year-range-scatter', 'value')]
    )
    def update_histogram(selected_sports, selected_countries, selected_medals, year_range):
        """ re-plots histogram based on given selections of sports, countries, and medals

        Arguments:
            selected_sports (list): list of desired sports
            selected_countries (list): list of desired countries
            selected_medals (list): list of desired type of medal
            year_range (list): list of selected years (based on range slider)

        Returns:
            histogram (plotly graph object): updated visualization
        """

        # filter data based on selected sports and countries
        filtered_df = df_olympic[
            (df_olympic['Sport'].isin(selected_sports)) & (df_olympic['Team'].isin(selected_countries))]

        # filter based on selected medals
        filtered_df = filtered_df[filtered_df['Medal'].isin(selected_medals)]

        # create histogram
        histogram = px.histogram(filtered_df, x='Year', color='Team', title='Medal Count Histogram', barmode='overlay')
        histogram.update_yaxes(title_text="Medal Count")

        # set font
        histogram.update_layout(font=dict(family='Times New Roman', size=14))

        # update range of years
        histogram.update_xaxes(range=[year_range[0], year_range[1]])

        return histogram

    @app.callback(
        Output('sport-dropdown', 'value'),
        Output('country-input', 'value'),
        Output('medal-checklist', 'value'),
        Output('year-range-scatter', 'value'),
        Input('clear-all', 'n_clicks')
    )
    def clear_filters(n_clicks):
        """ clears all selected filters (dropdowns, checkboxes, range slider)

        Arguments:
            n_clicks (None): determines if button has been clicked

        Returns:
            dash.no_update: keeps current values unchanged
        """

        # clear selected filters
        if n_clicks:
            return [], [], [], [df_olympic["Year"].min(), df_olympic["Year"].max()]

        return dash.no_update

    # run app
    app.run_server(debug=True)

main()