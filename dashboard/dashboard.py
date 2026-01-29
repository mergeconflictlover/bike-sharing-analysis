# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import os

st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon=":bike:",
    layout="wide",
)

# Get the directory where dashboard.py is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# ==================== LOAD DATA ====================
@st.cache_data
def load_data():
    day_df = pd.read_csv(os.path.join(CURRENT_DIR, "main_data.csv"))
    hour_df = pd.read_csv(os.path.join(CURRENT_DIR, "hour_data.csv"))
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# ==================== HEADER ====================
"""
# :material/directions_bike: Bike Sharing Analytics

Analisis pola penyewaan sepeda berdasarkan kondisi cuaca dan waktu.
"""

""  # Spacer

# ==================== FILTERS ====================
cols = st.columns([1, 3])

filter_cell = cols[0].container(border=True)

with filter_cell:
    st.markdown("##### :material/filter_alt: Filters")
    
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    date_range = st.date_input(
        "Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = date_range[0]
    
    ""
    
    season_options = ['All', 'Spring', 'Summer', 'Fall', 'Winter']
    selected_season = st.pills("Season", options=season_options, default='All')
    
    ""
    
    weather_options = ['All'] + list(day_df['weather_name'].unique())
    selected_weather = st.pills("Weather", options=weather_options, default='All')

# ==================== FILTER DATA ====================
filtered_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & 
                      (day_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_name'] == selected_season]

if selected_weather != 'All':
    filtered_df = filtered_df[filtered_df['weather_name'] == selected_weather]

filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & 
                            (hour_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'All':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season_name'] == selected_season]

if selected_weather != 'All':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['weather_name'] == selected_weather]

if filtered_df.empty:
    filter_cell.info("No data for selected filters", icon=":material/info:")
    st.stop()

# ==================== MAIN CHART ====================
chart_cell = cols[1].container(border=True)

with chart_cell:
    chart_data = filtered_df[['dteday', 'casual', 'registered', 'cnt']].copy()
    chart_data = chart_data.melt(
        id_vars=['dteday'], 
        value_vars=['casual', 'registered'],
        var_name='User Type', 
        value_name='Rentals'
    )
    
    chart = alt.Chart(chart_data).mark_area(
        opacity=0.7,
        interpolate='monotone'
    ).encode(
        alt.X('dteday:T', title='Date'),
        alt.Y('Rentals:Q', title='Daily Rentals', stack=True),
        alt.Color('User Type:N', scale=alt.Scale(
            domain=['registered', 'casual'],
            range=['#90CAF9', '#D3D3D3']
        )),
        tooltip=['dteday:T', 'User Type:N', 'Rentals:Q']
    ).properties(height=350)
    
    st.altair_chart(chart, use_container_width=True)

# ==================== METRICS ====================
""

total_rentals = int(filtered_df['cnt'].sum())
avg_rentals = int(filtered_df['cnt'].mean())
total_casual = int(filtered_df['casual'].sum())
total_registered = int(filtered_df['registered'].sum())
pct_casual = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
pct_registered = (total_registered / total_rentals * 100) if total_rentals > 0 else 0

metric_cols = st.columns(4)

with metric_cols[0]:
    cell = st.container(border=True)
    cell.metric(
        ":material/pedal_bike: Total Rentals",
        f"{total_rentals:,}",
        f"{len(filtered_df)} days"
    )

with metric_cols[1]:
    cell = st.container(border=True)
    cell.metric(
        ":material/analytics: Daily Average",
        f"{avg_rentals:,}",
        "per day"
    )

with metric_cols[2]:
    cell = st.container(border=True)
    cell.metric(
        ":material/person: Casual Users",
        f"{total_casual:,}",
        f"{pct_casual:.1f}%"
    )

with metric_cols[3]:
    cell = st.container(border=True)
    cell.metric(
        ":material/verified: Registered Users",
        f"{total_registered:,}",
        f"{pct_registered:.1f}%"
    )

""
""

# ==================== WEATHER ANALYSIS ====================
"""
## :material/cloud: Weather Impact Analysis
"""

weather_cols = st.columns(3)

with weather_cols[0]:
    cell = st.container(border=True)
    
    season_data = filtered_df.groupby('season_name')['cnt'].mean().reset_index()
    season_data.columns = ['Season', 'Average Rentals']
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_data['Season'] = pd.Categorical(season_data['Season'], categories=season_order, ordered=True)
    season_data = season_data.sort_values('Season')
    
    chart = alt.Chart(season_data).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color='#90CAF9'
    ).encode(
        alt.X('Season:N', sort=season_order, title=None),
        alt.Y('Average Rentals:Q', title='Avg Rentals'),
        alt.Tooltip(['Season:N', 'Average Rentals:Q'])
    ).properties(height=280, title='Rentals by Season')
    
    cell.altair_chart(chart, use_container_width=True)

with weather_cols[1]:
    cell = st.container(border=True)
    
    weather_data = filtered_df.groupby('weather_name')['cnt'].mean().reset_index()
    weather_data.columns = ['Weather', 'Average Rentals']
    weather_data = weather_data.sort_values('Average Rentals', ascending=False)
    
    chart = alt.Chart(weather_data).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color='#90CAF9'
    ).encode(
        alt.Y('Weather:N', sort='-x', title=None),
        alt.X('Average Rentals:Q', title='Avg Rentals'),
        alt.Tooltip(['Weather:N', 'Average Rentals:Q'])
    ).properties(height=280, title='Rentals by Weather')
    
    cell.altair_chart(chart, use_container_width=True)

with weather_cols[2]:
    cell = st.container(border=True)
    
    temp_data = filtered_df[['temp_actual', 'cnt']].copy()
    
    scatter = alt.Chart(temp_data).mark_circle(
        opacity=0.5,
        size=40,
        color='#90CAF9'
    ).encode(
        alt.X('temp_actual:Q', title='Temperature (°C)'),
        alt.Y('cnt:Q', title='Rentals'),
        tooltip=['temp_actual:Q', 'cnt:Q']
    )
    
    trend = scatter.transform_regression('temp_actual', 'cnt').mark_line(
        color='#1565C0', 
        strokeDash=[4, 4]
    )
    
    chart = (scatter + trend).properties(height=280, title='Temperature vs Rentals')
    
    cell.altair_chart(chart, use_container_width=True)

""
""

# ==================== TIME ANALYSIS ====================
"""
## :material/schedule: Time Pattern Analysis
"""

time_cols = st.columns(2)

with time_cols[0]:
    cell = st.container(border=True)
    
    hourly_data = filtered_hour_df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    hourly_data = hourly_data.melt(
        id_vars=['hr'],
        value_vars=['casual', 'registered'],
        var_name='User Type',
        value_name='Average Rentals'
    )
    
    chart = alt.Chart(hourly_data).mark_line(
        point=True,
        strokeWidth=2.5
    ).encode(
        alt.X('hr:O', title='Hour'),
        alt.Y('Average Rentals:Q', title='Avg Rentals'),
        alt.Color('User Type:N', scale=alt.Scale(
            domain=['registered', 'casual'],
            range=['#90CAF9', '#D3D3D3']
        )),
        tooltip=['hr:O', 'User Type:N', 'Average Rentals:Q']
    ).properties(height=300, title='Hourly Rental Pattern')
    
    cell.altair_chart(chart, use_container_width=True)

with time_cols[1]:
    cell = st.container(border=True)
    
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    daily_data = filtered_df.groupby('weekday_name')[['casual', 'registered']].mean().reset_index()
    daily_data['weekday_name'] = pd.Categorical(daily_data['weekday_name'], categories=day_order, ordered=True)
    daily_data = daily_data.sort_values('weekday_name')
    daily_data = daily_data.melt(
        id_vars=['weekday_name'],
        value_vars=['casual', 'registered'],
        var_name='User Type',
        value_name='Average Rentals'
    )
    
    chart = alt.Chart(daily_data).mark_bar().encode(
        alt.X('weekday_name:N', sort=day_order, title=None),
        alt.Y('Average Rentals:Q', title='Avg Rentals'),
        alt.Color('User Type:N', scale=alt.Scale(
            domain=['registered', 'casual'],
            range=['#90CAF9', '#D3D3D3']
        )),
        alt.XOffset('User Type:N'),
        tooltip=['weekday_name:N', 'User Type:N', 'Average Rentals:Q']
    ).properties(height=300, title='Daily Rental Pattern')
    
    cell.altair_chart(chart, use_container_width=True)

""
""

# ==================== INSIGHTS ====================
"""
## :material/lightbulb: Key Insights
"""

insight_cols = st.columns(3)

with insight_cols[0]:
    cell = st.container(border=True)
    cell.markdown("##### :material/schedule: Peak Hours")
    
    hourly_avg = filtered_hour_df.groupby('hr')['cnt'].mean()
    top_hours = hourly_avg.nlargest(3)
    
    for hour, val in top_hours.items():
        cell.markdown(f"**{hour:02d}:00** — {val:,.0f} avg")

with insight_cols[1]:
    cell = st.container(border=True)
    cell.markdown("##### :material/wb_sunny: Best Conditions")
    
    best_season = filtered_df.groupby('season_name')['cnt'].mean().idxmax()
    best_weather = filtered_df.groupby('weather_name')['cnt'].mean().idxmax()
    temp_corr = filtered_df['temp_actual'].corr(filtered_df['cnt'])
    
    cell.markdown(f"**Season:** {best_season}")
    cell.markdown(f"**Weather:** {best_weather}")
    cell.markdown(f"**Temp Corr:** {temp_corr:.2f}")

with insight_cols[2]:
    cell = st.container(border=True)
    cell.markdown("##### :material/group: User Behavior")
    
    weekend_casual = filtered_df[filtered_df['workingday'] == 0]['casual'].mean()
    weekday_casual = filtered_df[filtered_df['workingday'] == 1]['casual'].mean()
    if weekday_casual > 0:
        casual_increase = ((weekend_casual - weekday_casual) / weekday_casual) * 100
        cell.markdown(f"**Weekend ↑:** +{casual_increase:.0f}%")
    
    cell.markdown(f"**Registered:** {pct_registered:.0f}%")
    cell.markdown(f"**Casual:** {pct_casual:.0f}%")

""
""

# ==================== SEGMENTATION ====================
"""
## :material/donut_large: Volume Segmentation
"""

seg_cols = st.columns([2, 1])

with seg_cols[0]:
    cell = st.container(border=True)
    
    def categorize(cnt):
        if cnt < 2000: return 'Low (<2k)'
        elif cnt < 4000: return 'Medium (2k-4k)'
        elif cnt < 6000: return 'High (4k-6k)'
        else: return 'Very High (>6k)'
    
    filtered_df_cat = filtered_df.copy()
    filtered_df_cat['category'] = filtered_df_cat['cnt'].apply(categorize)
    
    cat_counts = filtered_df_cat['category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Days']
    
    cat_order = ['Low (<2k)', 'Medium (2k-4k)', 'High (4k-6k)', 'Very High (>6k)']
    cat_counts['Category'] = pd.Categorical(cat_counts['Category'], categories=cat_order, ordered=True)
    cat_counts = cat_counts.sort_values('Category')
    
    chart = alt.Chart(cat_counts).mark_bar(
        cornerRadiusTopLeft=4,
        cornerRadiusTopRight=4,
        color='#90CAF9'
    ).encode(
        alt.X('Category:N', sort=cat_order, title=None),
        alt.Y('Days:Q', title='Number of Days'),
        tooltip=['Category:N', 'Days:Q']
    ).properties(height=300, title='Days by Rental Volume')
    
    cell.altair_chart(chart, use_container_width=True)

with seg_cols[1]:
    cell = st.container(border=True)
    cell.markdown("##### :material/bar_chart: Category Stats")
    
    cat_stats = filtered_df_cat.groupby('category').agg({
        'cnt': ['count', 'mean'],
        'temp_actual': 'mean'
    }).round(1)
    cat_stats.columns = ['Days', 'Avg', 'Temp']
    cat_stats = cat_stats.reindex(cat_order)
    
    cell.dataframe(cat_stats, use_container_width=True)

""
""

# ==================== CONCLUSIONS ====================
"""
## :material/summarize: Conclusions
"""

conc_cols = st.columns(2)

with conc_cols[0]:
    cell = st.container(border=True)
    cell.markdown("##### :material/cloud: Weather Impact")
    cell.markdown("""
    1. **Fall** has highest average rentals
    2. **Clear weather** increases rentals ~2x
    3. **Temperature** correlation: r≈0.63
    4. **High humidity** reduces activity
    """)

with conc_cols[1]:
    cell = st.container(border=True)
    cell.markdown("##### :material/schedule: Time Patterns")
    cell.markdown("""
    1. **Peak:** 8 AM & 5-6 PM (commuters)
    2. **Registered** = bimodal pattern
    3. **Casual** ↑ significantly on weekends
    4. **YoY growth** from 2011 to 2012
    """)

# ==================== FOOTER ====================
st.divider()

footer_cols = st.columns([2, 1])

with footer_cols[0]:
    st.caption(":material/database: Data: Capital Bikeshare System, Washington D.C. (2011-2012)")

with footer_cols[1]:
    st.caption(":material/person: Created by **Muhammad Himbar Buana** • Dicoding Indonesia")
