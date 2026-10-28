import pandas as pd
import numpy as np
import streamlit as st
import pickle
import plotly.express as px

# -------------------------------------------------------------
# 1. Page Configuration
# -------------------------------------------------------------
st.set_page_config(
    page_title = "Nassau Candy Supply Chain Analytics",
    page_icon = "📊",
    layout = "wide"
)

st.title("📊 Nassau Candy: Supply Chain Performance Dashboard")
st.markdown("This dashboard monitors and analyzes systemic fulfillment latencies across distribution lanes.")


# -------------------------------------------------------------
# 2. Optimized Data Loading (Using Pickle)
# -------------------------------------------------------------
@st.cache_data
def load_pickle_data():
    data = pd.read_pickle(r"D:\Jupyter_notebooks\Unified Mentor Projects\Nassau Candy Distributor Analysis\clean_shipments.pkl")
    return data


data = load_pickle_data()

# -------------------------------------------------------------
# 3. User Capabilities: Interactive Sidebar Filters
# -------------------------------------------------------------
st.sidebar.header("🎛️ Global Controls")

# Filter A: Date Range Filter
min_date = data['Order Date'].min().to_pydatetime()
max_date = data['Order Date'].max().to_pydatetime()

start_date, end_date = st.sidebar.date_input(
    "Select Order date Range",
    value = (min_date, max_date),
    min_value = min_date,
    max_value = max_date
)

# Filter B: Region selector
all_regions = sorted(data['Region'].dropna().unique())
selected_regions = st.sidebar.multiselect("Filter by Region", options = all_regions, default = 'Pacific')

# Filter C: Ship Mode Filter
all_modes = sorted(data['Ship Mode'].dropna().unique())
selected_modes = st.sidebar.multiselect("Filter by Ship Mode", options = all_modes, default = 'First Class')

# Filter D: Lead-Time Threshold Slider
max_days = int(data['Shipping_Lead_Time'].max())
threshold_days = st.sidebar.slider("Highlight Anomalous Lead Times Exceeding (Days)", min_value = 0, max_value = max_days, value = 1400)

# -------------------------------------------------------------
# 4. Apply Filters Reactively to create data_filtered
# -------------------------------------------------------------
data_filtered = data[
    (data['Order Date'] >= pd.to_datetime(start_date)) &
    (data['Order Date'] <= pd.to_datetime(end_date)) &
    (data['Region'].isin(selected_regions)) &
    (data['Ship Mode'].isin(selected_modes))
]

# -------------------------------------------------------------
# 5. Dashboard Module i: Route Efficiency Overview
# -------------------------------------------------------------
st.header("🏁 Route Efficiency Overview")

# Top level metric display cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label = 'Total Shipments', value = f"{len(data_filtered):,}")
with col2:
    st.metric(label = 'Average Lead Time', value = f"{data_filtered['Shipping_Lead_Time'].mean():.1f} Days")
with col3:
    st.metric(label = 'Anomalies Found (> Threshold)', value = f"{len(data_filtered[data_filtered['Shipping_Lead_Time'] > threshold_days]):,}")

st.subheader("🏆 Route Performance Leaderboard")

# Aggregate metrics dynamically using the filtered data
state_route_summary = data_filtered.groupby('Route_State/Province').agg(
                      Total_Shipments = ('Shipping_Lead_Time', 'count'),
                      Avg_Lead_Time = ('Shipping_Lead_Time', 'mean'),
                      Lead_Time_Variability = ('Shipping_Lead_Time', 'std')
).reset_index()

# Re-apply the fixed mathematical normalization formula reactively to the filtered view
min_lead = state_route_summary['Avg_Lead_Time'].min()
max_lead = state_route_summary['Avg_Lead_Time'].max()

# Handle edge case where max equals min if user filters down to a single route
if max_lead != min_lead:
    state_route_summary['Route_Efficiency_Score'] = (
        (max_lead - state_route_summary['Avg_Lead_Time']) / (max_lead - min_lead) * 100
    ).round(2)
else:
    state_route_summary['Route_Efficiency_Score'] = 100.00

# Sort and Rank
state_route_summary = state_route_summary.sort_values(by = 'Route_Efficiency_Score', ascending = False).reset_index(drop = True)
state_route_summary.index = state_route_summary.index + 1
state_route_summary.index.name = 'Rank'

# Display the clean interactive leaderboard
st.dataframe(
    state_route_summary[['Route_State/Province', 'Route_Efficiency_Score', 'Avg_Lead_Time', 'Total_Shipments']],
    use_container_width = True,
    column_config = {
        'Route_State': 'Shipping Lane (Factory ➔ State/Province)',
        # 'Route_Efficiency_Score' : st.column_config.NumberColumn('Efficiency Score (0-100)', format = '%.2f'),
        'Route_Efficiency_Score': st.column_config.ProgressColumn('Efficiency Score (0-100)',
            help = '100 represent maximum network speed, 0 represents severe delay.',
            format = '%.1f', min_value = 0.0, max_value = 100.0),
        'Avg_Lead_Time': st.column_config.NumberColumn('Avg Duration (Days)', format = '%.1f'),
        # 'Lead_Time_Variability' : st.column_config.NumberColumn('Variability (Std)', format = '%.1f'),
        'Total_Shipments': st.column_config.NumberColumn('Volume (Orders)', format = '%d')
    }
)

# -------------------------------------------------------------
# 6. Dashboard Module ii: Geographic Shipping Map
# -------------------------------------------------------------
st.header('🗺️ Geographic Shipping Map')
st.markdown('Visualizing regional fulfillment efficiency and structural bottlenecks across the united states')

# Dictionary to map full US State names to 2-letter postal abbreviations
us_state_to_abbrev = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY", "District of Columbia": "DC"
}

# Create a copy of the filtered data to safely add our map codes
data_map = data_filtered.copy()

# Map full names to abbreviations (Canadian provinces will map to NaN)
data_map['State_Code'] = data_map['State/Province'].map(us_state_to_abbrev)

# Filter out Canadian rows and missing values for clean US-only mapping
data_map_us = data_map.dropna(subset = ['State_Code'])

if data_map_us.empty:
    st.warning('⚠️ No US-based shipping data available for the selected filters.')
else:
    # Aggregate performance data by State Code
    state_geo_summary = data_map_us.groupby('State_Code').agg(
        State_Name = ('State/Province', 'first'),
        Total_Orders = ('Shipping_Lead_Time', 'count'),
        Avg_Lead_Time = ('Shipping_Lead_Time', 'mean')
    ).reset_index()

# Recalculate a normalized State Efficiency Score (0 to 100) for the map colors
# Lower average lead time = Higher efficiency score
geo_min = state_geo_summary['Avg_Lead_Time'].min()
geo_max = state_geo_summary['Avg_Lead_Time'].max()

if geo_max != geo_min:
    state_geo_summary['State_Efficiency'] = (
        (geo_max - state_geo_summary['Avg_Lead_Time']) / (geo_max - geo_min) * 100
    ).round(2)
else:
    state_geo_summary['State_Efficiency'] = 100.00

# Create two side-by-side columns to separate the Map from its Insights
map_col, insight_col = st.columns([3, 1])

with map_col:
    # Build the Interactive US Heatmap using Plotly
    fig = px.choropleth(state_geo_summary,
                        locations = 'State_Code',       # Expects two-letter state codes (e.g., 'CA', 'NY', 'TX')
                        locationmode = 'USA-states',        # Tells Plotly to render a US Map
                        color = 'State_Efficiency',         # Color scale tied to our calculated efficiency
                        scope = 'usa',                      # Zooms the map view specifically into the USA
                        color_continuous_scale = 'RdYlGn',  # Red (Inefficient/Bottleneck) to Green (Highly Efficient)
                        labels = {'State_Efficiency': 'Efficiency Score', 'Avg_Lead_Time': 'Avg Lead Time (Days)'},
                        hover_data = {'State_Code': False,
                                      'State_Name': True,  # Show the nice full name on hover!
                                      'Avg_Lead_Time': ':.1f',
                                      'Total_Orders': ':,',
                                      'State_Efficiency': ':.2f'}
                        )

    fig.update_layout(
        title_text = 'US Regional Shipping Efficiency Heatmap',
        geo = dict(bgcolor = 'rgba(0,0,0,0)'),
        margin = dict(l = 0, r = 0, t = 0, b = 0)
    )

    # Render the interactive plotly object inside Streamlit
    st.plotly_chart(fig, use_container_width = True)

with insight_col:
    st.subheader('⚠️ Regional Bottlenecks')
    st.markdown('The 3 states experiencing the highest systematic transit delays:')

    # Identify the top 3 worst bottleneck states (highest average lead times)
    bottlenecks = state_geo_summary.sort_values(by = 'Avg_Lead_Time', ascending = False).head(3)

    for idx, row in bottlenecks.iterrows():
        st.error(f"**{row['State_Name']} ({row['State_Code']})** \n⏱️ Avg Duration: '{row['Avg_Lead_Time']:.1f} days' \n📦 Vol : '{int(row['Total_Orders']):,}' orders")


# -------------------------------------------------------------
# 7. Dashboard Module iii: Ship Mode Comparison
# -------------------------------------------------------------
st.header("🚢 Ship Mode Comparison")
st.markdown("Evaluating transit latency and operational consistency across different fulfillment channels.")

# 1. Aggregate metrics by Ship Mode reactively based on global sidebar filters
ship_mode_summary = data_filtered.groupby('Ship Mode').agg(
     Total_Orders = ('Shipping_Lead_Time', 'count'),
     Avg_Lead_Time = ('Shipping_Lead_Time', 'mean'),
     Lead_Time_Std = ('Shipping_Lead_Time', 'std')
).reset_index().sort_values(by = 'Avg_Lead_Time')

# 2. Layout: Create two uneven columns (Left for the Chart, Right for deep-dive metrics)
chart_col, metrics_col = st.columns([2, 1])

with chart_col:
    # Build an interactive bar chart to compare average lead times
    fig_mode = px.bar(ship_mode_summary,
                      x = 'Ship Mode',
                      y = 'Avg_Lead_Time',
                      color = 'Avg_Lead_Time',
                      color_continuous_scale = 'Viridis',
                      text_auto = '.1f',   # Automatically displays the average days on top of the bars
                      labels = {'Ship Mode': 'Shipping Methods',
                                'Avg_Lead_Time': 'Average Lead Time (Days)'},
                      title = 'Average Lead Time by Shipping Method'
                      )

    fig_mode.update_layout(xaxis_title = 'Shipping Method',
                           yaxis_title = 'Average Duration (Days)',
                           coloraxis_showscale = False,    # Hides the color legend bar to keep it clean
                           margin = dict(l = 20, r = 20, t = 40, b = 20)
                           )

    # Render the chart
    st.plotly_chart(fig_mode, use_container_width = True)

with metrics_col:
    st.subheader('📋 Channel Breakdown')
    st.markdown('Detailed stability and volume metrics for each mode:')

    # Dynamically generate styled cards for each shipping method present in the filtered data
    for idx, row in ship_mode_summary.iterrows():
        # Handle cases where std deviation is NaN (if a ship mode has only 1 order)
        variability = f"{row['Lead_Time_Std']:.1f} days" if not pd.isna(row['Lead_Time_Std']) else 'N/A'

        st.info(f"**Mode: {row['Ship Mode']}**\n"
                f"⏱️ Avg Speed: '{row['Avg_Lead_Time']:.1f} days'\n"
                f"📈 Variability (Std Dev): '{variability}'\n"
                f"📦 Total Volume: '{int(row['Total_Orders']):,}' orders"
                )


# -------------------------------------------------------------
# 8. Dashboard Module iv: Route Drill-Down
# -------------------------------------------------------------
st.header("🔍 Route Drill-Down & Order Timelines")
st.markdown("Drill deep into state-level performance dynamics and audit individual order fulfillment lifecycles.")

# Extract the available states dynamically from the globally filtered dataframe
available_states = sorted(data_filtered['State/Province'].dropna().unique())

if not available_states:
    st.warning('⚠️ No data available for the selected filters to perform a drill-down analysis.')
else:
    # 1. State-Level Performance Insights Selection
    selected_drill_state = st.selectbox('Select a State / Province to Inspect Natively: ',
                                        options = available_states)

    # Isolate the data for the chosen drill-down target
    data_drill = data_filtered[data_filtered['State/Province'] == selected_drill_state]

    st.subheader(f"📊 Performance Distribution for {selected_drill_state}")

    # Contextual KPI cards for the specific selected location
    d_col1, d_col2, d_col3 = st.columns(3)
    with d_col1:
        st.metric('Total Deliveries: ', f"{len(data_drill):,}")
    with d_col2:
        st.metric('Mean Lead Time: ', f"{data_drill['Shipping_Lead_Time'].mean():.1f} Days")
    with d_col3:
        st.metric('Maximum Latency: ', f"{data_drill['Shipping_Lead_Time'].max()} Days")

    # Build a Plotly histogram to show the distribution of transit timelines
    fig_hist = px.histogram(data_drill,
                            x = 'Shipping_Lead_Time',
                            nbins = 15,
                            title = f"Fulfillment Latency Spread: {selected_drill_state}",
                            labels = {'Shipping_lead_Time': 'Lead Time (Days)', 'count': 'Number of Shipments'},
                            color_discrete_sequence = ['#2ca02c']    # Clean operational green color scheme
                            )

    fig_hist.update_layout(xaxis_title = 'Fulfillment Windows (Days)',
                           yaxis_title = 'Volume of Shipments',
                           margin = dict(l = 20, r = 20, t = 40, b = 20)
                           )

    st.plotly_chart(fig_hist, use_container_width = True)

    # 2. Order-Level Shipment Timelines
    st.subheader("📦 Order-Level Shipment Timelines")
    st.markdown(f"Detailed timeline registry for all individual shipments routed to **{selected_drill_state}**.")

    # Define and check columns to prevent schema conflicts
    target_columns = ['Order ID', 'Factory', 'Ship Mode', 'Order Date', 'Ship Date', 'Shipping_Lead_Time']
    available_cols = [col for col in target_columns if col in data_drill.columns]

    # Sort by the most recent order dates for logistical relevance
    data_timeline = data_drill[available_cols].sort_values(by = 'Order Date', ascending = False).reset_index(drop = True)

    # Convert datetime to clean readable strings for the data table UI
    if 'Order Date' in data_timeline.columns:
        data_timeline['Order Date'] = data_timeline['Order Date'].dt.strftime('%Y-%m-%d')
    if 'Ship Date' in data_timeline.columns:
        data_timeline['Ship Date'] = data_timeline['Ship Date'].dt.strftime('%Y-%m-%d')

    # Render the interactive order spreadsheet
    st.dataframe(data_timeline,
                 use_container_width = True,
                 column_config = {"Order ID": "Order Reference",
                                  "Factory": "Origin Plant",
                                  "Ship Mode": "Service Type",
                                  "Order Date": "Placement Date",
                                  "Ship Date": "Dispatch Date",
                                  "Shipping_Lead_Time": st.column_config.NumberColumn("Total Lead Time (Days)", format = "%d")
                                  }
                 )
