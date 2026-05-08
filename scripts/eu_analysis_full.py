"""
EU Economic & Social Indicators Analysis
Full analysis script extracted from Jupyter Notebook
"""


# ========== Cell 1 ==========

# --- Data Manipulation Libraries ---

import pandas as pd           # Imports the pandas library, used for working with structured data (DataFrames, CSVs, Excel, etc.)
import numpy as np            # Imports NumPy, used for numerical operations and handling arrays efficiently

# --- Visualization Libraries ---

import matplotlib.pyplot as plt  # Imports matplotlib���s pyplot module for basic plotting (line, bar, scatter, etc.)
import seaborn as sns            # Imports seaborn for advanced statistical plotting (heatmaps, pairplots, etc.)
import plotly.express as px      # Imports plotly express for creating interactive, web-based plots and dashboards

# --- Statistical Analysis Libraries ---

from scipy.stats import ttest_ind, pearsonr  
# Imports specific statistical tools from SciPy:
# - ttest_ind: for conducting independent two-sample t-tests
# - pearsonr: for calculating Pearson correlation coefficient and p-value

import statsmodels.api as sm     
# Imports the full statsmodels API for performing statistical tests, building models (like OLS regression), and more

# --- Machine Learning / Forecasting ---

from sklearn.linear_model import LinearRegression  
# Imports the LinearRegression model from scikit-learn (used for predictive modeling, forecasting trends, etc.)

# --- API Access and Time Management ---

import wbdata                  # Imports wbdata, a package to fetch World Bank data via API (economic and development indicators)
import datetime                # Imports datetime, a built-in module for working with date and time objects
import json                    # Imports json module to read, write, and manipulate JSON-formatted data (useful with APIs)

# --- System Configuration ---

import os                      # Imports os module to interact with the operating system (like file paths and environment variables)os.environ["OMP_NUM_THREADS"] = "1"
# Sets the environment variable to limit the number of threads used by libraries (e.g., NumPy or BLAS).
# Useful for preventing high CPU usage or resolving parallel computing issues in some environments.


# ========== Cell 2 ==========

# --- Import necessary libraries ---

#I continued to import in order to learn and remember and be confident on what libraries or modules i was using.
import wbdata               # Used to fetch economic and development data from the World Bank API
import pandas as pd         # Used for data manipulation, cleaning, and analysis with DataFrames

# --- Step 1: Define countries and indicators ---

eu_countries = [            # List of ISO-2 codes representing all 27 EU member countries
    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI',
    'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU',
    'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE'
]

indicators = {              # Dictionary mapping World Bank indicator codes to human-readable labels
    'NY.GDP.PCAP.CD': 'GDP per capita',                            # GDP per person (US dollars)
    'SE.XPD.TOTL.GD.ZS': 'Education spending (% GDP)',            # % of GDP spent on education
    'SH.XPD.CHEX.PC.CD': 'Health spending per capita (US$)',      # Health spending per person
    'SP.POP.TOTL': 'Population',                                   # Total population
    'NE.GDI.TOTL.ZS': 'Investment (% GDP)',                        # Gross capital formation
	'SL.TLF.CACT.ZS': 'Labor force participation (%)',              # % of population in labor force
}

# --- Step 2: Fetch data from the World Bank API ---

df_raw = wbdata.get_dataframe(indicators, country=eu_countries)
# Downloads data for selected indicators and countries into a DataFrame
# The index includes both 'country' and 'date' by default

df_raw.reset_index(inplace=True)
# Resets the multi-index to convert 'country' and 'date' into columns

# --- Step 3: Clean and process the data ---

df_raw['date'] = pd.to_datetime(df_raw['date'])
# Converts the 'date' column to datetime format

df_raw['year'] = df_raw['date'].dt.year
# Extracts just the year from the datetime object into a new 'year' column

df_raw = df_raw[df_raw['year'] >= 2000].dropna()
# Filters out any rows before the year 2000 and drops rows with missing values

# --- Step 4: Map country names to ISO-2 codes (for consistency or future mapping) ---

df_raw['country_code'] = df_raw['country'].map({
    'Austria': 'AT', 'Belgium': 'BE', 'Bulgaria': 'BG', 'Croatia': 'HR',
    'Cyprus': 'CY', 'Czech Republic': 'CZ', 'Denmark': 'DK', 'Estonia': 'EE',
    'Finland': 'FI', 'France': 'FR', 'Germany': 'DE', 'Greece': 'GR',
    'Hungary': 'HU', 'Ireland': 'IE', 'Italy': 'IT', 'Latvia': 'LV',
    'Lithuania': 'LT', 'Luxembourg': 'LU', 'Malta': 'MT', 'Netherlands': 'NL',
    'Poland': 'PL', 'Portugal': 'PT', 'Romania': 'RO', 'Slovakia': 'SK',
    'Slovenia': 'SI', 'Spain': 'ES', 'Sweden': 'SE'
})
# Maps full country names returned by the API to their ISO-2 codes for easier referencing later

# --- Step 5: Preview the final cleaned dataset ---

print("EU dataset shape:", df_raw.shape)
# Prints the dimensions of the cleaned dataset (rows, columns)

df_raw.head(23)
# Displays the first 23 rows of the dataset as a sample


# ========== Cell 3 ==========

# --- Import Required Libraries ---

import pandas as pd                 # For handling and analyzing structured data in DataFrames
import plotly.express as px         # For creating interactive plots (line, scatter, etc.)
import ipywidgets as widgets        # For adding interactive UI elements like dropdowns
from IPython.display import display  # For rendering widgets and outputs in a Jupyter Notebook

# --- Step 1: Create Dropdown for Country Selection ---

country_dropdown = widgets.Dropdown(
    options=sorted(df_raw['country'].unique()),  # Sorted list of unique country names from the dataset
    description='Country:',                      # Label for the dropdown
    layout=widgets.Layout(width='50%')           # Sets the width of the dropdown
)

# --- Step 2: Function to Show Trends for Selected Country ---

def show_country_trends(selected_country):
    country_df = df_raw[df_raw['country'] == selected_country]  # Filter data for selected country

    indicators = [  # List of indicators to visualize
        'GDP per capita',
        'Health spending per capita (US$)',
        'Education spending (% GDP)',
        'Investment (% GDP)',
        'Labor force participation (%)',
        'Population'
    ]

    titles = {  # More readable chart titles for each indicator
        'GDP per capita': 'GDP per Capita (USD)',
        'Health spending per capita (US$)': 'Health Spending per Capita (USD)',
        'Education spending (% GDP)': 'Education Spending (% of GDP)',
        'Investment (% GDP)': 'Investment (% of GDP)',
        'Labor force participation (%)': 'Labor Force Participation (%)',
        'Population': 'Population'
    }

    for indicator in indicators:  # Generate a line chart for each indicator
        fig = px.line(
            country_df,                      # Data filtered to selected country
            x='year',                        # X-axis: year
            y=indicator,                     # Y-axis: selected indicator
            title=f"{selected_country} - {titles[indicator]} Over Time",  # Dynamic title
            markers=True,                    # Show markers at each data point
            template='plotly_white'          # Clean white background for plots
        )
        fig.update_layout(width=800, height=400)  # Set size of the figure
        fig.show()                                # Display the chart

# --- Step 3: Bind Dropdown to Function Using ipywidgets ---

ui = widgets.VBox([country_dropdown])  # Vertical layout for the dropdown UI
out = widgets.interactive_output(      # Create reactive output that updates when dropdown changes
    show_country_trends,
    {'selected_country': country_dropdown}
)

# --- Step 4: Display the Interactive Dashboard in Jupyter Notebook ---

display(ui, out)  # Show the dropdown and output area (charts) together


# ========== Cell 4 ==========

import plotly.express as px  # Import Plotly Express for simple interactive plotting

# --- Create a box plot to show GDP per capita distribution by country ---

fig = px.box(
    df_raw,                         # Data source: cleaned World Bank data
    x='country',                    # X-axis: country names (categorical variable)
    y='GDP per capita',             # Y-axis: GDP per capita values (numeric variable)
    color='country',                # Each country will have a different color for distinction
    title='GDP per Capita Distribution by Country (Box Plot)',  # Chart title
    labels={'GDP per capita': 'GDP per Capita (US$)'},          # Custom label for the Y-axis
    template='plotly_white'         # Uses a clean white background theme for readability
)

# --- Adjust layout size to make the plot more readable ---

fig.update_layout(
    width=1200,   # Sets the width of the figure
    height=550    # Sets the height of the figure
)

# --- Display the box plot in the Jupyter notebook ---

fig.show()  # Render the interactive chart


# ========== Cell 5 ==========

import numpy as np                          # For numerical operations (used here for matrix manipulation)
import plotly.graph_objects as go           # For building custom Plotly visualizations like annotated heatmaps

# --- Step 1: Compute Correlation Matrix ---

numeric_cols = df_raw.select_dtypes(include='number').drop(columns=['year'])  
# Selects only numeric columns from df_raw and removes 'year' (to avoid artificial correlation with time)

corr_matrix = numeric_cols.corr().round(2)  
# Computes the pairwise Pearson correlation matrix and rounds values to 2 decimal places

# --- Step 2: Create Heatmap with Plotly ---

heatmap = go.Heatmap(
    z=corr_matrix.values,                   # The 2D correlation values as the Z-axis
    x=corr_matrix.columns,                  # Labels for columns on X-axis
    y=corr_matrix.columns,                  # Labels for rows on Y-axis
    colorscale='YlGnBu',                    # Yellow-Green-Blue color scale for visual contrast
    zmin=-1, zmax=1,                        # Sets correlation value range (-1 = negative, 1 = positive)
    colorbar=dict(title="Correlation"),     # Adds a colorbar legend
    hovertemplate='Variable 1: %{y}<br>Variable 2: %{x}<br>Correlation: %{z}<extra></extra>'
    # Custom hover info showing which variables are being compared and their correlation value
)

# --- Step 3: Add Annotation Text on Each Cell ---

annotations = []  # Create an empty list to hold annotation dictionaries
for i in range(len(corr_matrix)):
    for j in range(len(corr_matrix.columns)):
        annotations.append(
            dict(
                x=corr_matrix.columns[j],            # Column label
                y=corr_matrix.columns[i],            # Row label
                text=str(corr_matrix.values[i][j]),  # Actual correlation value (as text)
                showarrow=False,                     # No arrow, just text
                font=dict(color='black', size=12)    # Font style for annotations
            )
        )

# --- Step 4: Build the Figure Layout ---

fig = go.Figure(data=[heatmap])            # Creates a Plotly figure with the heatmap
fig.update_layout(
    title='Correlation Matrix of Key Indicators (Annotated)',  # Chart title
    annotations=annotations,               # Add annotation text to the heatmap
    width=800, height=700,                 # Set dimensions for the figure
    template='plotly_white'                # Use a clean white background
)

# --- Step 5: Display the Interactive Heatmap ---

fig.show()  # Renders the heatmap with annotations


# ========== Cell 6 ==========

# --- Import Required Libraries ---

import pandas as pd                           # For data manipulation and analysis
import numpy as np                            # For numerical operations
import time                                   # To simulate delays in processing
from sklearn.linear_model import LinearRegression       # For building linear regression models
from sklearn.metrics import r2_score, mean_squared_error  # For evaluating model performance
from tqdm import tqdm                         # For showing a progress bar during loops

# --- Define Input Features and Target Variable ---

features = [  # Independent variables used to predict GDP
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Population',
    'Investment (% GDP)',
    'Labor force participation (%)'
]
target = 'GDP per capita'  # Dependent variable (what we want to predict)

# --- Prepare Clean Dataset ---

df_clean = df_raw.dropna(subset=features + [target])  
# Drops rows that have missing values in either the features or the target column

# --- Get Unique List of Countries in the Cleaned Dataset ---

countries = df_clean['country'].unique()  
# Extracts all distinct country names from the cleaned dataset

# --- Initialize Results Storage ---

results = []  # Empty list to collect regression results per country

# --- Loop Through Countries with Progress Bar ---

print("Running Regression per Country:")
for country in tqdm(countries):  # Iterate through each country with a visual progress bar
    country_df = df_clean[df_clean['country'] == country]  
    # Filter the data to only include rows for the current country

    if len(country_df) >= 5:  # Ensure there's enough data to fit a meaningful regression model
        X = country_df[features]   # Input features
        y = country_df[target]     # Target variable

        # --- Fit Linear Regression Model ---
        model = LinearRegression()  # Initialize the regression model
        model.fit(X, y)             # Train the model on the country-specific data
        y_pred = model.predict(X)   # Predict GDP per capita using the model

        # --- Evaluate Model Performance ---
        r2 = r2_score(y, y_pred)                          # R-squared: how well the model explains variance
        rmse = mean_squared_error(y, y_pred) ** 0.5       # RMSE: how far predictions deviate from actual values

        # --- Store Results ---
        results.append({
            'Country': country,
            'R2 Score': round(r2, 4),
            'RMSE': round(rmse, 2),
            'Observations': len(country_df)
        })

        time.sleep(0.2)  # Optional: slow down loop for visibility (especially when using tqdm)

# --- Convert Collected Results to DataFrame ---

results_df = pd.DataFrame(results)  # Create a DataFrame from the list of dictionaries

# --- Display Results ---

results_df  # Shows model performance (R2, RMSE) per country


# ========== Cell 7 ==========

# --- Import Required Libraries ---

import plotly.express as px                 # For interactive plots with optional trendlines
import pandas as pd                         # For data manipulation with DataFrames
import ipywidgets as widgets                # For creating dropdown widgets
from IPython.display import display         # For displaying widgets and plots in Jupyter Notebook

# --- Create Dropdowns for Country and Variable Selection ---

country_dropdown = widgets.Dropdown(
    options=df_raw['country'].unique(),       # All countries in the dataset
    description='Country:',                   # Label for country selector
    layout=widgets.Layout(width='50%')        # Sets dropdown width
)

variable_dropdown = widgets.Dropdown(
    options=[                                 # List of indicators to compare with GDP
        'Health spending per capita (US$)',
        'Education spending (% GDP)',
        'Population',
        'Investment (% GDP)',
        'Labor force participation (%)'
    ],
    description='Compare to:',                # Label for variable selector
    layout=widgets.Layout(width='50%')
)

# --- Define Function to Update Plot Based on Selections ---

def update_plot(country, variable):
    country_df = df_raw[df_raw['country'] == country]  # Filter data for selected country
    
    fig = px.scatter(
        country_df,
        x=variable,                      # X-axis: selected socioeconomic variable
        y='GDP per capita',              # Y-axis: GDP per capita
        title=f'{country} - GDP per capita vs. {variable}',  # Dynamic plot title
        trendline='ols',                 # Add linear regression trendline
        labels={                         # Axis labels
            variable: variable,
            'GDP per capita': 'GDP per capita (USD)'
        },
        hover_data=['year']              # Show year info on hover
    )

    fig.update_layout(
        template='plotly_white',         # Clean white theme
        width=800,
        height=500
    )
    fig.show()                           # Display the plot

# --- Combine Widgets and Plot Output ---

ui = widgets.VBox([country_dropdown, variable_dropdown])  # Arrange dropdowns vertically

out = widgets.interactive_output(
    update_plot,
    {'country': country_dropdown, 'variable': variable_dropdown}  # Link dropdowns to function
)

# --- Display the Interactive Dashboard ---

display(ui, out)  # Render dropdowns and interactive plot


# ========== Cell 8 ==========

# --- Import Required Libraries ---

import pandas as pd                               # For data manipulation with DataFrames
import numpy as np                                # For numerical calculations
from sklearn.linear_model import LinearRegression # For linear regression modeling
from sklearn.metrics import r2_score, mean_squared_error  # For evaluating model performance
from tqdm.notebook import tqdm                    # For visual progress bar in Jupyter notebooks
import time                                       # To simulate processing delays (optional)

# --- Define Variables to Simulate ---

variables = [
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Population',
    'Investment (% GDP)',
    'Labor force participation (%)'
]

# --- Initialize Result Storage ---

sim_results = []  # List to collect simulation outputs

# --- Simulation Loop Over Countries and Variables ---

for country in tqdm(df_raw['country'].unique(), desc="Running GDP Simulations by Country"):
    country_df = df_raw[df_raw['country'] == country].dropna()  
    # Filter data for current country and drop rows with missing values

    if country_df.empty:  # Skip countries with no valid data
        continue

    for var in variables:  # Simulate one variable at a time
        if var not in country_df.columns:  # Skip if variable is missing
            continue

        X = country_df[[var]]             # Independent variable (single feature)
        y = country_df['GDP per capita']  # Dependent variable (target)

        # --- Train Regression Model ---
        model = LinearRegression()
        model.fit(X, y)

        # --- Simulate a 10% Increase in the Variable ---
        X_sim = X * 1.10                  # Apply a 10% increase to the feature
        y_sim = model.predict(X_sim)     # Predict GDP with increased input
        avg_gdp_change = np.mean(y_sim - y)  # Average difference in GDP per capita

        # --- Store Results ---
        sim_results.append({
            'Country': country,
            'Variable': var,
            'Impact of +10% Change on GDP per capita': round(avg_gdp_change, 2),
            'R2 Score': round(r2_score(y, model.predict(X)), 3),  # Goodness-of-fit measure
            'Observations': len(country_df)                      # Sample size used
        })

        time.sleep(0.1)  # Optional delay for visualization pacing

# --- Convert Simulation Results to DataFrame ---

sim_df = pd.DataFrame(sim_results)  # Create DataFrame from results

# Sort results to highlight largest GDP impacts
sim_df.sort_values(by='Impact of +10% Change on GDP per capita', ascending=False, inplace=True)
sim_df.reset_index(drop=True, inplace=True)

# --- Preview Top Results ---

sim_df.head()  # Display top 5 simulation outcomes


# ========== Cell 9 ==========

# --- Import Required Libraries ---

import pandas as pd                         # For data manipulation with DataFrames
import numpy as np                          # For numerical calculations
from sklearn.preprocessing import StandardScaler  # For standardizing data before clustering
from sklearn.cluster import KMeans          # For performing KMeans clustering
import plotly.express as px                 # For creating interactive visualizations
import ipywidgets as widgets                # For dropdown widgets in Jupyter
from IPython.display import display         # To render widgets and plots
from tqdm import tqdm                       # For a progress bar (for simulation)
import time                                 # To simulate time delay during clustering

# --- Step 1: Compute Average Values Per Country ---

avg_df = df_raw.groupby('country')[[
    'GDP per capita',
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Investment (% GDP)',
    'Labor force participation (%)',
    'Population'
]].mean().dropna()
# Groups data by country and calculates the mean for each selected variable.
# Drops any countries with missing values.

# --- Step 2: Normalize the Data ---

scaler = StandardScaler()
scaled_data = scaler.fit_transform(avg_df)
# Standardizes all columns so they have mean = 0 and standard deviation = 1
# This avoids bias in clustering due to differing units/scales

# --- Step 3: Simulate Clustering Progress with tqdm ---

n_clusters = 4                               # Number of clusters to form
pbar = tqdm(total=100, desc='Clustering Simulation', ncols=90)
for i in range(5):
    time.sleep(0.5)                          # Simulated delay
    pbar.update(20)                          # Simulate progress step
pbar.close()                                 # Close the progress bar

# --- Step 4: Apply KMeans Clustering ---

kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
avg_df['Cluster'] = kmeans.fit_predict(scaled_data)
# Fit KMeans to the scaled data and assign each country to a cluster
df_viz = avg_df.reset_index()
# Reset index so 'country' becomes a column again for plotting

# --- Step 5: Create Dropdown for X-axis Variable ---

x_dropdown = widgets.Dropdown(
    options=[col for col in avg_df.columns if col not in ['GDP per capita', 'Cluster']],
    description='Compare to:',
    layout=widgets.Layout(width='50%')
)
# Dropdown menu lets user choose a variable to compare with GDP per capita

# --- Step 6: Define the Plotting Function ---

def update_plot(x_axis):
    fig = px.scatter(
        df_viz,
        x=x_axis,
        y='GDP per capita',
        color='Cluster',                        # Color points by cluster group
        size='GDP per capita',                  # Bubble size represents GDP per capita
        hover_name='country',                   # Hover shows country name
        hover_data={                            # Custom hover display formatting
            x_axis: ':.2f',
            'GDP per capita': ':.2f',
            'Education spending (% GDP)': ':.2f',
            'Health spending per capita (US$)': ':.2f',
            'Investment (% GDP)': ':.2f',
            'Labor force participation (%)': ':.2f',
            'Population': ':,'
        },
        title=f'GDP per Capita vs {x_axis}',     # Dynamic title
        template='plotly_white',
        width=950,
        height=600
    )
    fig.update_traces(
        marker=dict(opacity=0.85, line=dict(width=0.5, color='gray'))  # Improve visual clarity
    )
    fig.update_layout(legend_title_text='Cluster Group')  # Title for legend
    fig.show()

# --- Step 7: Display the Dashboard ---

out = widgets.interactive_output(update_plot, {'x_axis': x_dropdown})
display(x_dropdown, out)
# Renders the dropdown menu and corresponding plot output


# ========== Cell 10 ==========

# --- Step 1: Compute Mean Profile for Each Cluster ---

cluster_profile = avg_df.groupby('Cluster')[[
    'GDP per capita',
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Investment (% GDP)',
    'Labor force participation (%)',
    'Population'
]].mean().round(2)
# Groups countries by their cluster and computes the mean of each socioeconomic indicator
# Rounds the values to 2 decimal places for cleaner presentation

# --- Optional: Rename the Index for Clarity ---

cluster_profile.index.name = 'Cluster ID'  # Makes the index label more explicit

# --- Step 2: Display the Cluster Profile Table ---

from IPython.display import display
display(cluster_profile)  # Nicely formats the DataFrame for display in Jupyter


# ========== Cell 11 ==========

# --- Manually assign descriptive names based on profile characteristics ---

cluster_labels = {
    0: 'Emerging Economies',          # Cluster 0 contains countries with growing but moderate indicators
    1: 'Developed Nations',           # Cluster 1 represents countries with high GDP and balanced social investment
    2: 'Low-Investment Countries',    # Cluster 2 includes countries with relatively low capital and social investment
    3: 'Social-Focused Economies'     # Cluster 3 has moderate GDP but strong health/education focus
}

# --- Apply the descriptive labels to the DataFrame ---

avg_df['Cluster Label'] = avg_df['Cluster'].map(cluster_labels)
# Creates a new column 'Cluster Label' by mapping each numeric cluster to its label

# --- Display a preview of country names with cluster ID and label ---

display(
    avg_df.reset_index()[['country', 'Cluster', 'Cluster Label']]
)
# Shows country name, numeric cluster, and descriptive cluster label for reference


# ========== Cell 12 ==========

# --- Step: Create ISO Alpha-3 Mapping for EU Countries ---

iso_map = {
    'Austria': 'AUT', 'Belgium': 'BEL', 'Bulgaria': 'BGR', 'Croatia': 'HRV',
    'Cyprus': 'CYP', 'Czech Republic': 'CZE', 'Denmark': 'DNK', 'Estonia': 'EST',
    'Finland': 'FIN', 'France': 'FRA', 'Germany': 'DEU', 'Greece': 'GRC',
    'Hungary': 'HUN', 'Ireland': 'IRL', 'Italy': 'ITA', 'Latvia': 'LVA',
    'Lithuania': 'LTU', 'Luxembourg': 'LUX', 'Malta': 'MLT', 'Netherlands': 'NLD',
    'Poland': 'POL', 'Portugal': 'PRT', 'Romania': 'ROU', 'Slovakia': 'SVK',
    'Slovenia': 'SVN', 'Spain': 'ESP', 'Sweden': 'SWE'
}
# This dictionary links full country names to their ISO alpha-3 codes

# --- Step: Map ISO Codes to the DataFrame ---

avg_df['iso_alpha'] = avg_df.index.map(iso_map)
# Adds a new column 'iso_alpha' to avg_df by mapping the index (which contains country names)
# This will be useful for choropleth or geographic visualizations later


# ========== Cell 13 ==========

import plotly.express as px

# --- Step 1: Reset Index for Plotly Compatibility ---
map_df = avg_df.reset_index()
# Ensures 'country' is a column instead of an index (needed for hover info)

# --- Step 2: Define Custom Colors for Each Cluster Label ---
custom_colors = {
    'Emerging Economies': '#ffffcc',           # Light yellow
    'Developed Nations': '#41b6c4',            # Medium blue
    'Low-Investment Countries': '#1c9099',     # Darker blue-green
    'Social-Focused Economies': '#006837'      # Deep green
}
# These colors make it easier to distinguish clusters visually

# --- Step 3: Build Choropleth Map ---
fig = px.choropleth(
    map_df,
    locations='iso_alpha',                   # ISO-3 country codes for map alignment
    color='Cluster Label',                   # Use human-readable cluster labels for coloring
    color_discrete_map=custom_colors,        # Apply custom colors to the cluster labels
    hover_name='country',                    # Country name on hover
    hover_data={                             # Display detailed indicators on hover
        'GDP per capita': ':.2f',
        'Health spending per capita (US$)': ':.2f',
        'Education spending (% GDP)': ':.2f',
        'Investment (% GDP)': ':.2f',
        'Labor force participation (%)': ':.2f',
        'Population': ':,'
    },
    locationmode='ISO-3',                    # Specify that 'locations' column contains ISO-3 codes
    scope='europe',                          # Limit map view to Europe only
    title='EU Clusters: GDP, Health & Social Indicators',  # Map title
    template='plotly_white'                  # Clean white background
)

# --- Step 4: Refine Layout and Map Appearance ---
fig.update_geos(fitbounds="locations", visible=False)  # Zoom to visible countries only
fig.update_layout(
    margin={"r": 0, "t": 50, "l": 0, "b": 0},          # Tight margins
    legend_title_text='Cluster Type'                  # Rename legend title
)

# --- Step 5: Display the Map ---
fig.show()


# ========== Cell 14 ==========

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import MinMaxScaler

# --- Step 1: Define Indicators to Analyze ---

indicators = [
    'GDP per capita',
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Investment (% GDP)',
    'Labor force participation (%)',
    'Population'
]
# These are the variables we'll use to profile each cluster

# --- Step 2: Compute Mean Profile per Cluster Label ---

cluster_profile = avg_df.groupby('Cluster Label')[indicators].mean().round(2)
# Groups data by descriptive cluster labels and computes average indicator values

# --- Step 3: Normalize Values for Radar Chart Display ---

scaler = MinMaxScaler()  # Initialize the scaler to scale values between 0 and 1

profile_scaled = pd.DataFrame(
    scaler.fit_transform(cluster_profile),      # Fit and transform the data
    index=cluster_profile.index,                # Preserve cluster label index
    columns=cluster_profile.columns             # Preserve column names
)
# The result is a normalized DataFrame where all values are between 0 and 1,
# ready to be plotted in a radar/spider chart


# ========== Cell 15 ==========

# NBA player strengths and weaknesses inspired feature
# --- Step: Create Radar Chart of Cluster Profiles ---

fig = go.Figure()  # Initialize a blank radar chart figure

# Loop through each cluster and add its profile to the chart
for cluster in profile_scaled.index:
    fig.add_trace(go.Scatterpolar(
        r=profile_scaled.loc[cluster].values,    # Radius values (normalized indicators)
        theta=profile_scaled.columns,            # Axis categories (indicator names)
        fill='toself',                           # Fill the area inside the polygon
        name=cluster                             # Cluster label shown in legend
    ))

# --- Step: Customize Layout ---

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]                         # All values normalized between 0 and 1
        )
    ),
    title="Radar Chart: Cluster Profiles Across Key Indicators",  # Chart title
    showlegend=True,
    height=600,
    template="plotly_white"                      # Clean background for readability
)

# --- Step: Show Radar Chart ---

fig.show()


# ========== Cell 16 ==========

#Aerospace launch success rate inspired feature 
import plotly.express as px

# --- Step 1: Reset index so 'country' becomes a column ---
df_sunburst = avg_df.reset_index()

# --- Step 2: Choose which variable to use for sizing chart segments ---
size_variable = 'GDP per capita'  # You can change this to 'Population' if needed

# --- Step 3: Create the Sunburst Chart ---

fig = px.sunburst(
    df_sunburst,
    path=['Cluster Label', 'country'],   # Defines hierarchy: Cluster ��� Country
    values=size_variable,               # Size of each segment (GDP or Population)
    color='Cluster Label',              # Color-coded by cluster group
    color_discrete_sequence=px.colors.sequential.YlGnBu,  # Yellow-Green-Blue color scale
    title=f'Sunburst Chart: {size_variable} by Cluster and Country',
    height=700                          # Sets chart height
)

# --- Step 4: Tidy Layout and Display ---

fig.update_layout(
    margin=dict(t=60, l=0, r=0, b=0)    # Adds top margin for title
)

fig.show()  # Displays the interactive chart


# ========== Cell 17 ==========

import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import plotly.express as px

# --- Step 1: Define Input Features and Target Variable ---

features = [
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Population',
    'Investment (% GDP)',
    'Labor force participation (%)'
]
target = 'GDP per capita'  # This is the outcome we want to model

# --- Step 2: Clean and Average Dataset by Country ---

df_clean = df_raw.dropna(subset=features + [target])  # Drop rows with missing data
df_avg = df_clean.groupby('country')[features + [target]].mean().reset_index()
# Group by country and compute average values for each feature and target

# --- Step 3: Train Decision Tree Model ---

X = df_avg[features]  # Input variables
y = df_avg[target]    # Target variable

model = DecisionTreeRegressor(random_state=42)  # Initialize model with fixed randomness
model.fit(X, y)  # Fit model to the data

# --- Step 4: Extract and Format Feature Importance ---

importances = model.feature_importances_  # Extract importance values from model
importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': np.round(importances * 100, 2)  # Convert to percentage
}).sort_values(by='Importance', ascending=True)   # Sort for better chart flow

# --- Step 5: Create Horizontal Bar Chart with Plotly ---

fig = px.bar(
    importance_df,
    x='Importance',
    y='Feature',
    orientation='h',
    text='Importance',
    color='Importance',
    color_continuous_scale='YlGnBu',
    title='Smoothed Feature Importance for GDP per Capita (Decision Tree)',
    labels={'Importance': '% Importance'},
    height=450
)

# --- Step 6: Tweak Visual Styling ---

fig.update_traces(
    texttemplate='%{text:.1f}%',       # Format percentage label on bars
    textposition='outside'             # Display labels outside the bars
)
fig.update_layout(
    template='plotly_white',
    xaxis=dict(
        title='% Influence',
        range=[0, max(importance_df['Importance']) + 5],  # Extend X-axis slightly
        tick0=0,
        dtick=5
    ),
    margin=dict(l=100, r=30, t=60, b=40)
)

# --- Step 7: Show Chart ---

fig.show()


# ========== Cell 18 ==========

# Gapminder Inspired feature
import plotly.express as px

# --- Step 1: Filter and Prepare Data for Animation ---

df_anim = df_raw.copy()
df_anim = df_anim[df_anim['year'].between(2000, 2020)]  # Keep only years 2000���2020

# Remove duplicate entries per country-year
df_anim = df_anim.sort_values(by=['country', 'year']).drop_duplicates(
    subset=['country', 'year'], keep='first'
)

# Convert year to string for animation frame usage
df_anim['year_str'] = df_anim['year'].astype(str)

# --- Y-axis Settings for GDP per Capita Range ---

gdp_min = int(df_anim['GDP per capita'].min() // 1000) * 1000
gdp_max = int(df_anim['GDP per capita'].max() // 1000 + 2) * 1000
tick_step = 4000
tick_vals = list(range(gdp_min, gdp_max + tick_step, tick_step))

# --- Step 2: Create Animated Bubble Chart ---

fig = px.scatter(
    df_anim,
    x="year",
    y="GDP per capita",
    animation_frame="year_str",         # Each year is an animation frame
    animation_group="country",          # Groups data points by country over time
    size="Population",                  # Bubble size represents population
    color="country",                    # Color-coded by country
    color_discrete_sequence=px.colors.qualitative.Set1,
    hover_name="country",               # Show country name on hover
    size_max=60,                        # Max bubble size
    range_x=[1999, 2021],               # X-axis range for years
    range_y=[gdp_min, gdp_max],         # Y-axis range for GDP
    labels={
        "year": "Year",
        "GDP per capita": "GDP per Capita (USD)",
        "Population": "Population"
    },
    title="Animated GDP per Capita Growth in EU (2000���2020)",
    template="simple_white",
    width=1200,
    height=700
)

# --- Step 3: Style and Layout Settings ---

fig.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=tick_vals,
        tickfont=dict(size=12)
    ),
    xaxis=dict(
        tickmode='linear',
        tick0=2000,
        dtick=2
    ),
    paper_bgcolor="rgb(255, 253, 240)",  # Cream background
    plot_bgcolor="rgb(255, 253, 240)",   # Cream plot area
    font=dict(size=13, color='black'),
    title_font=dict(size=22),
    legend_title_text="Country",
    margin=dict(l=60, r=60, t=60, b=60)
)

# --- Step 4: Display Chart ---

fig.show()


# ========== Cell 19 ==========

# --- Import necessary libraries ---
import pandas as pd                           # For creating and manipulating dataframes
import numpy as np                            # For numerical operations
from sklearn.tree import DecisionTreeRegressor  # Machine learning model: decision tree for regression
import ipywidgets as widgets                  # For interactive UI widgets in Jupyter
from IPython.display import display, clear_output  # To control outputs in notebook cells


# Reuse same features used in training
features = [
    'Health spending per capita (US$)',
    'Education spending (% GDP)',
    'Population',
    'Investment (% GDP)',
    'Labor force participation (%)'
]

# Using a dummy model cause i did not train any data 
X_dummy = pd.DataFrame({
    'Health spending per capita (US$)': np.random.uniform(500, 5000, 50),   # Random values between 500 and 5000
    'Education spending (% GDP)': np.random.uniform(3, 8, 50),              # Between 3% and 8% of GDP
    'Investment (% GDP)': np.random.uniform(15, 35, 50),                    # Between 15% and 35% of GDP
    'Labor force participation (%)': np.random.uniform(50, 75, 50),         # Between 50% and 75%
    'Population': np.random.uniform(1e6, 8e7, 50)                           # Between 1 million and 80 million
})
# Reorder X_dummy to match `features` list
X_dummy = X_dummy[features]  # Ensuring column order exactly matches the training feature list

# the code for simulating the target variable (GDP per capita) using my formula
y_dummy = X_dummy['Health spending per capita (US$)'] * 2.5 + \
          X_dummy['Education spending (% GDP)'] * 1200 + \
          np.random.normal(0, 3000, 50)

#training the decision tree regression model
model = DecisionTreeRegressor(random_state=42) # creating a model with fixed random state for reproducability
model.fit(X_dummy, y_dummy)  #trainging model with features and target variable



# Widgets for user input
health_input = widgets.FloatSlider(min=200, max=8000, step=100, value=2500, description="Health ($)")  # AI generated , cause i did not have an idea of the arguments needed for the floater slider
education_input = widgets.FloatSlider(min=2, max=10, step=0.1, value=5, description="Education (%)") #implemented myself after understanding
population_input = widgets.IntSlider(min=1_000_000, max=90_000_000, step=1_000_000, value=10_000_000, description="Population")
investment_input = widgets.FloatSlider(min=10, max=40, step=0.5, value=25, description="Investment (%)")
labor_input = widgets.FloatSlider(min=40, max=80, step=0.5, value=60, description="Labor (%)")

simulate_button = widgets.Button(description="Simulate", button_style='success')
output = widgets.Output()

# Simulation logic
def run_simulation(button):
    with output:
        clear_output()
        input_dict = {
            'Health spending per capita (US$)': health_input.value,
            'Education spending (% GDP)': education_input.value,
            'Population': population_input.value,
            'Investment (% GDP)': investment_input.value,
            'Labor force participation (%)': labor_input.value
        }

        input_df = pd.DataFrame([input_dict])[features]  # Ensure exact order

        predicted_gdp = model.predict(input_df)[0]

        print("---- Simulation Output ----")
        print(f"Estimated GDP per capita: ${predicted_gdp:,.2f}")
        for k, v in input_dict.items():
            print(f"{k}: {v}")
        print("---------------------------")

simulate_button.on_click(run_simulation)

# Display the interface
display(widgets.VBox([
    health_input, education_input, population_input, investment_input, labor_input,
    simulate_button, output
]))

