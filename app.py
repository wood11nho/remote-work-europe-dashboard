import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Remote Work in Europe Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. DATA LOADING AND PREPARATION
@st.cache_data
def load_data(filepath):
    """Loads and prepares data, including adding ISO Alpha-3 codes for the map."""
    try:
        df = pd.read_csv(filepath)
        # Add ISO ALPHA-3 codes required for the Plotly choropleth map.
        # This is a crucial step for mapping country names to the map's location identifiers.
        country_codes = {
            'Belgium': 'BEL', 'Bulgaria': 'BGR', 'Czechia': 'CZE', 'Denmark': 'DNK',
            'Germany': 'DEU', 'Estonia': 'EST', 'Ireland': 'IRL', 'Greece': 'GRC',
            'Spain': 'ESP', 'France': 'FRA', 'Croatia': 'HRV', 'Italy': 'ITA',
            'Cyprus': 'CYP', 'Latvia': 'LVA', 'Lithuania': 'LTU', 'Luxembourg': 'LUX',
            'Hungary': 'HUN', 'Malta': 'MLT', 'Netherlands': 'NLD', 'Austria': 'AUT',
            'Poland': 'POL', 'Portugal': 'PRT', 'Romania': 'ROU', 'Slovenia': 'SVN',
            'Slovakia': 'SVK', 'Finland': 'FIN', 'Sweden': 'SWE', 'Norway': 'NOR',
            'Albania': 'ALB', 'Bosnia and Herzegovina': 'BIH', 'European Union - 27 countries (from 2020)': 'EU27',
            'Montenegro': 'MNE', 'North Macedonia': 'MKD', 'Serbia': 'SRB', 'Türkiye': 'TUR'
        }
        df['iso_alpha'] = df['Country'].map(country_codes)
        return df
    except FileNotFoundError:
        st.error(f"Error: The file '{filepath}' was not found.")
        return None

df = load_data('romania_remote_work_prepared_data.csv')

# 3. MAIN DASHBOARD LAYOUT
st.title("Remote Work Adoption in Europe: A 2022-2024 Analysis")

if df is not None:
    # Separate EU data from country-specific data for charting
    df_countries = df[~df['Country'].str.contains("European Union")].copy()
    df_eu = df[df['Country'].str.contains("European Union")]

    # 4.1. KEY METRICS (KPIs)
    st.markdown("### Key Insights for Romania")
    romania_data = df_countries[df_countries['Country'] == 'Romania'].iloc[0]
    eu_avg_2024 = df_eu['Remote_Work_2024'].iloc[0]

    col1, col2, col3 = st.columns(3)
    col1.metric(
        label="Romania Remote Work % (2024)",
        value=f"{romania_data['Remote_Work_2024']:.2f}%",
        delta=f"{romania_data['Remote_Work_Change']:.2f} vs 2022"
    )
    col2.metric(
        label="Romania vs EU Average (2024)",
        value=f"{romania_data['Remote_Work_2024'] - eu_avg_2024:.2f} pts",
        help="Difference between Romania's rate and the EU average."
    )
    col3.metric(
        label="Romania Internet Access % (2024)",
        value=f"{romania_data['Internet_Access_2024']:.2f}%",
        delta=f"{romania_data['Internet_Access_Change']:.2f} vs 2022"
    )
    st.markdown("---")


    # 4.2 & 4.3. SIDE BY SIDE VISUALIZATIONS
    viz_col1, viz_col2 = st.columns([1, 1])  # Equal width columns
    
    with viz_col1:
        # PRIMARY VISUALIZATION: DUMBBELL CHART
        st.markdown("### The Evolution of Remote Work (2022 vs. 2024)")
        
        # Sorting options for the main chart - moved to chart column
        sort_option = st.selectbox(
            'Sort Countries By:',
            ['Remote Work 2024 (High to Low)', 'Remote Work Growth (High to Low)', 'Alphabetical']
        )

        # Apply sorting based on user selection
        if sort_option == 'Remote Work 2024 (High to Low)':
            df_sorted = df_countries.sort_values('Remote_Work_2024', ascending=False)
        elif sort_option == 'Remote Work Growth (High to Low)':
            df_sorted = df_countries.sort_values('Remote_Work_Change', ascending=False)
        else:
            df_sorted = df_countries.sort_values('Country', ascending=True)
        
        fig_dumbbell = go.Figure()

        # Define colors
        COLOR_ROMANIA = '#FFD700'  # A gold/yellow to stand out
        COLOR_EU_AVG = '#0033A0'    # A distinct blue
        COLOR_2022 = '#B0C4DE'     # Light Steel Blue
        COLOR_2024 = '#4682B4'     # Steel Blue
        COLOR_LINE = '#D3D3D3'     # Light Grey
        COLOR_INTERNET = "#CD29AF"

        # Add lines connecting the dots (the "dumbbell" part)
        for i, row in df_sorted.iterrows():
            if pd.notna(row['Remote_Work_2022']) and pd.notna(row['Remote_Work_2024']):
                fig_dumbbell.add_shape(
                    type='line',
                    x0=row['Remote_Work_2022'], y0=row['Country'],
                    x1=row['Remote_Work_2024'], y1=row['Country'],
                    line=dict(color=COLOR_LINE, width=2)
                )

        # Add 2022 data points
        fig_dumbbell.add_trace(go.Scatter(
            x=df_sorted['Remote_Work_2022'],
            y=df_sorted['Country'],
            mode='markers',
            name='2022',
            marker=dict(color=COLOR_2022, size=10)
        ))

        # Add 2024 data points with strategic coloring
        marker_colors = [COLOR_ROMANIA if country == 'Romania' else COLOR_2024 for country in df_sorted['Country']]
        fig_dumbbell.add_trace(go.Scatter(
            x=df_sorted['Remote_Work_2024'],
            y=df_sorted['Country'],
            mode='markers',
            name='2024',
            marker=dict(color=marker_colors, size=10, symbol='diamond'),
            # This is where we add all the extra info for the hover tooltip!
            customdata=df_sorted[['Remote_Work_Change', 'Internet_Access_2024', 'Internet_Access_Change', 'Remote_Work_Trend']],
            hovertemplate=(
                "<b>%{y}</b><br>" +
                "Remote Work 2024: %{x:.2f}%<br>" +
                "Change since 2022: %{customdata[0]:.2f} pts<br>" +
                "Trend: %{customdata[3]}<br>" +
                "Internet Access 2024: %{customdata[1]:.2f}%<br>" +
                "Internet Change: %{customdata[2]:.2f} pts" +
                "<extra></extra>" # Hides the trace name
            )
        ))

        # Add Internet Access 2024 data points
        internet_marker_colors = [COLOR_ROMANIA if country == 'Romania' else COLOR_INTERNET for country in df_sorted['Country']]
        fig_dumbbell.add_trace(go.Scatter(
            x=df_sorted['Internet_Access_2024'],
            y=df_sorted['Country'],
            mode='markers',
            name='Internet Access 2024',
            marker=dict(color=internet_marker_colors, size=8, symbol='circle', line=dict(width=2, color='white')),
            customdata=df_sorted[['Internet_Access_Change', 'Remote_Work_2024', 'Remote_Work_Change']],
            hovertemplate=(
                "<b>%{y}</b><br>" +
                "Internet Access 2024: %{x:.2f}%<br>" +
                "Internet Change: %{customdata[0]:.2f} pts<br>" +
                "Remote Work 2024: %{customdata[1]:.2f}%<br>" +
                "<extra></extra>"
            )
        ))
        
        # Add a vertical line for the EU average
        fig_dumbbell.add_vline(x=eu_avg_2024, line_width=2, line_dash="dash", line_color=COLOR_EU_AVG,
                      annotation_text="EU Average 2024", annotation_position="top right")

        # Add Remote_Work_Change annotations at the end of each row
        for i, row in df_sorted.iterrows():
            change_value = row['Remote_Work_Change']
            change_color = '#228B22' if change_value >= 0 else '#DC143C'  # Green for positive, red for negative
            change_text = f"+{change_value:.1f}" if change_value >= 0 else f"{change_value:.1f}"
            
            fig_dumbbell.add_annotation(
                x=max(df_sorted['Remote_Work_2022'].max(), df_sorted['Remote_Work_2024'].max(), df_sorted['Internet_Access_2024'].max()) + 3,  # Position at the end of all rows
                y=row['Country'],
                text=change_text,
                showarrow=False,
                font=dict(color=change_color, size=11, family="Arial"),
                xanchor='left'
            )

        # Update layout for a clean, professional look
        fig_dumbbell.update_layout(
            template='plotly_white',
            height=800,
            xaxis_title="Percentage (%) of enterprises conducting meetings remotely",
            yaxis_title="",
            yaxis=dict(autorange="reversed"), # Puts the highest value at the top
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis=dict(range=[0, max(df_sorted['Remote_Work_2024'].max(), df_sorted['Remote_Work_2022'].max(), df_sorted['Internet_Access_2024'].max()) + 8])  # Extend x-axis to accommodate annotations
        )
        st.plotly_chart(fig_dumbbell, use_container_width=True)

    with viz_col2:
        # SUPPORTING VISUALIZATION: CHOROPLETH MAP
        st.markdown("### Supporting Context: Household Internet Access")
        
        # Add context and help information
        st.markdown("""
        This map shows household internet access across European countries, which is a key enabler 
        for remote work adoption. Countries with higher internet penetration typically have better 
        infrastructure to support remote work practices.
        """)
        
        map_metric = st.radio(
            "Select Map Metric:",
            ('Internet Access % (2024)', 'Change in Access (2022-2024)'),
            help="Choose between viewing current internet access levels or the change over the 2022-2024 period. Higher internet access generally correlates with greater remote work capabilities."
        )

        if map_metric == 'Internet Access % (2024)':
            z_data = df_countries['Internet_Access_2024']
            colorscale = "Blues"
            colorbar_title = "Internet Access %"
            help_text = "Darker blue indicates higher percentage of households with internet access in 2024"
        else:
            z_data = df_countries['Internet_Access_Change']
            colorscale = "RdYlBu" # Red-Yellow-Blue is great for diverging data (negative/positive)
            colorbar_title = "Change in Access (pts)"
            help_text = "Blue shows improvement, red shows decline in internet access from 2022 to 2024"

        # Add help text below the radio button
        st.caption(f"{help_text}")

        fig_map = go.Figure(data=go.Choropleth(
            locations=df_countries['iso_alpha'],
            z=z_data,
            colorscale=colorscale,
            colorbar_title=colorbar_title,
            marker_line_color='darkgray',
            marker_line_width=0.5,
            customdata=df_countries['Country'],
            hovertemplate="<b>%{customdata}</b><br>%{z:.2f}",
            name=''
        ))

        fig_map.update_layout(
            geo=dict(
            scope='world',
            projection=go.layout.geo.Projection(type='mercator'),
            center=dict(lat=54, lon=15),  # Center on Europe
            lonaxis=dict(range=[-15, 50]),  # Longitude range to focus on Europe
            lataxis=dict(range=[35, 75]),   # Latitude range to focus on Europe
            showlakes=False,
            landcolor='rgb(243, 243, 243)',
            countrycolor='rgb(204, 204, 204)',
            ),
            height=800,  # Match the height of the dumbbell chart
            margin={"r":0,"t":0,"l":0,"b":0} # Remove margins for a tight fit
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # 5. DATA EXPLORER
    with st.expander("Explore the Full Dataset"):
        st.dataframe(df)

else:
    st.warning("Data could not be loaded. Please check the file path and format.")