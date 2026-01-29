import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os

# Set page config
st.set_page_config(
    page_title="Bike Sharing Analytics",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Clean & Elegant Light Theme CSS
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global font */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Clean white background */
    .stApp {
        background-color: #FAFBFC;
    }
    
    /* Sidebar - soft gray */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    
    /* Main container */
    .main .block-container {
        padding: 2rem 3rem;
        max-width: 1200px;
    }
    
    /* Headers */
    h1 {
        color: #111827;
        font-weight: 700;
        font-size: 2rem;
        letter-spacing: -0.02em;
    }
    
    h2 {
        color: #1F2937;
        font-weight: 600;
        font-size: 1.5rem;
        letter-spacing: -0.01em;
    }
    
    h3 {
        color: #374151;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #111827;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        font-weight: 500;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }
    
    div[data-testid="metric-container"] {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1.25rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #F3F4F6;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        color: #4B5563;
        border: none;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #111827;
        color: white;
    }
    
    /* Dataframe */
    .stDataFrame {
        border: 1px solid #E5E7EB;
        border-radius: 8px;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 1px;
        background: #E5E7EB;
        margin: 2rem 0;
    }
    
    /* Section card */
    .section-card {
        background: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
    }
    
    /* Question header */
    .question-header {
        background: #F9FAFB;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 1.5rem 0 1rem 0;
    }
    
    .question-header h3 {
        margin: 0;
        color: #111827;
        font-size: 1rem;
    }
    
    /* Insight card */
    .insight-card {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
    }
    
    .insight-card h4 {
        color: #166534;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .insight-card ul {
        color: #15803D;
        margin: 0;
        padding-left: 1.25rem;
    }
    
    .insight-card li {
        margin: 0.35rem 0;
        font-size: 0.9rem;
    }
    
    /* Conclusion cards */
    .conclusion-card-1 {
        background: linear-gradient(135deg, #EEF2FF 0%, #E0E7FF 100%);
        border: 1px solid #C7D2FE;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    .conclusion-card-2 {
        background: linear-gradient(135deg, #ECFDF5 0%, #D1FAE5 100%);
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 1.5rem;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #9CA3AF;
        font-size: 0.85rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Get the directory where dashboard.py is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Load data
@st.cache_data
def load_data():
    day_df = pd.read_csv(os.path.join(CURRENT_DIR, "main_data.csv"))
    hour_df = pd.read_csv(os.path.join(CURRENT_DIR, "hour_data.csv"))
    
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Color palette - soft & elegant
COLORS = {
    'primary': '#6366F1',      # Indigo
    'secondary': '#8B5CF6',    # Violet
    'success': '#10B981',      # Emerald
    'warning': '#F59E0B',      # Amber
    'danger': '#EF4444',       # Red
    'info': '#3B82F6',         # Blue
    'gray': '#9CA3AF',         # Gray
    'dark': '#111827',         # Dark
    'light': '#F3F4F6',        # Light gray
}

# Chart color palette
CHART_COLORS = ['#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; padding: 1.5rem 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🚲</div>
        <div style='font-size: 1.25rem; font-weight: 700; color: #111827;'>Bike Sharing</div>
        <div style='font-size: 0.8rem; color: #9CA3AF; margin-top: 0.25rem;'>Analytics Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Date filter
    st.markdown("##### 📆 Rentang Tanggal")
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    date_range = st.date_input(
        "Pilih tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = date_range[0]
    
    st.markdown("")
    
    # Season filter
    st.markdown("##### 🍂 Musim")
    season_options = ['Semua'] + list(day_df['season_name'].unique())
    selected_season = st.selectbox("Pilih musim", season_options, label_visibility="collapsed")
    
    st.markdown("")
    
    # Weather filter
    st.markdown("##### ☀️ Cuaca")
    weather_options = ['Semua'] + list(day_df['weather_name'].unique())
    selected_weather = st.selectbox("Pilih cuaca", weather_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Info box
    st.markdown("""
    <div style='background: #F9FAFB; border-radius: 8px; padding: 1rem; font-size: 0.8rem; color: #6B7280;'>
        <div style='font-weight: 600; color: #374151; margin-bottom: 0.5rem;'>ℹ️ Tentang Data</div>
        Data penyewaan sepeda dari Capital Bikeshare, Washington D.C. (2011-2012)
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    st.markdown("")
    
    # Author
    st.markdown("""
    <div style='text-align: center; font-size: 0.75rem; color: #9CA3AF;'>
        <div>Dibuat oleh</div>
        <div style='font-weight: 600; color: #6B7280;'>Muhammad Himbar Buana</div>
    </div>
    """, unsafe_allow_html=True)

# ==================== FILTER DATA ====================
filtered_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & 
                      (day_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'Semua':
    filtered_df = filtered_df[filtered_df['season_name'] == selected_season]

if selected_weather != 'Semua':
    filtered_df = filtered_df[filtered_df['weather_name'] == selected_weather]

filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & 
                            (hour_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'Semua':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season_name'] == selected_season]

if selected_weather != 'Semua':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['weather_name'] == selected_weather]

# Check if data is empty
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih.")
    st.stop()

# ==================== HEADER ====================
st.markdown("""
<div style='margin-bottom: 2rem;'>
    <h1 style='margin-bottom: 0.25rem;'>🚲 Bike Sharing Analytics</h1>
    <p style='color: #6B7280; font-size: 1rem; margin: 0;'>
        Analisis pola penyewaan sepeda berdasarkan kondisi cuaca dan waktu
    </p>
</div>
""", unsafe_allow_html=True)

# ==================== METRICS ====================
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", f"{total_rentals:,}", f"{len(filtered_df)} hari")

with col2:
    avg_rentals = filtered_df['cnt'].mean()
    st.metric("Rata-rata Harian", f"{avg_rentals:,.0f}", "per hari")

with col3:
    total_casual = filtered_df['casual'].sum()
    pct_casual = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
    st.metric("Pengguna Casual", f"{total_casual:,}", f"{pct_casual:.1f}%")

with col4:
    total_registered = filtered_df['registered'].sum()
    pct_registered = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
    st.metric("Pengguna Terdaftar", f"{total_registered:,}", f"{pct_registered:.1f}%")

st.markdown("---")

# ==================== QUESTION 1 ====================
st.markdown("""
<div class="question-header">
    <h3>📊 Pertanyaan 1: Bagaimana pengaruh kondisi cuaca terhadap jumlah penyewaan sepeda?</h3>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["Musim", "Cuaca", "Korelasi"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = filtered_df.groupby('season_name')['cnt'].mean().reindex(season_order).dropna()
        
        if not season_data.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#FAFBFC')
            ax.set_facecolor('#FAFBFC')
            
            max_idx = season_data.values.argmax()
            colors = ['#E5E7EB' if i != max_idx else '#6366F1' for i in range(len(season_data))]
            
            bars = ax.bar(season_data.index, season_data.values, color=colors, 
                         width=0.6, edgecolor='none')
            
            for bar, val in zip(bars, season_data.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                       f'{val:,.0f}', ha='center', fontweight='600', fontsize=11, color='#374151')
            
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=10, color='#6B7280')
            ax.set_xlabel('')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E5E7EB')
            ax.spines['bottom'].set_color('#E5E7EB')
            ax.tick_params(colors='#6B7280')
            ax.set_ylim(0, max(season_data.values) * 1.15)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Insight</h4>
            <ul>
                <li><b>Fall</b> memiliki penyewaan tertinggi</li>
                <li><b>Spring</b> penyewaan terendah</li>
                <li>Perbedaan bisa mencapai ~50%</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Statistik Musim**")
        season_stats = filtered_df.groupby('season_name')['cnt'].agg(['mean', 'sum']).round(0)
        season_stats.columns = ['Rata-rata', 'Total']
        st.dataframe(season_stats, use_container_width=True)

with tab2:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        weather_data = filtered_df.groupby('weather_name')['cnt'].mean().sort_values(ascending=True)
        
        if not weather_data.empty:
            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#FAFBFC')
            ax.set_facecolor('#FAFBFC')
            
            colors = ['#E5E7EB'] * len(weather_data)
            colors[-1] = '#10B981'  # Highlight max
            
            bars = ax.barh(weather_data.index, weather_data.values, color=colors, height=0.5)
            
            for bar, val in zip(bars, weather_data.values):
                ax.text(val + 30, bar.get_y() + bar.get_height()/2, 
                       f'{val:,.0f}', va='center', fontweight='600', fontsize=11, color='#374151')
            
            ax.set_xlabel('Rata-rata Penyewaan', fontsize=10, color='#6B7280')
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E5E7EB')
            ax.spines['bottom'].set_color('#E5E7EB')
            ax.tick_params(colors='#6B7280')
            ax.set_xlim(0, max(weather_data.values) * 1.15)
            
            plt.tight_layout()
            st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Insight</h4>
            <ul>
                <li><b>Cuaca cerah</b> = penyewaan max</li>
                <li>Hujan turunkan hingga <b>60%</b></li>
                <li>Cuaca sangat pengaruhi keputusan</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Statistik Cuaca**")
        weather_stats = filtered_df.groupby('weather_name')['cnt'].agg(['mean', 'count']).round(0)
        weather_stats.columns = ['Rata-rata', 'Hari']
        st.dataframe(weather_stats, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#FAFBFC')
        ax.set_facecolor('#FAFBFC')
        
        ax.scatter(filtered_df['temp_actual'], filtered_df['cnt'], 
                  alpha=0.5, c='#6366F1', s=40, edgecolors='white', linewidth=0.5)
        
        if len(filtered_df) > 1:
            z = np.polyfit(filtered_df['temp_actual'], filtered_df['cnt'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(filtered_df['temp_actual'].min(), filtered_df['temp_actual'].max(), 100)
            ax.plot(x_line, p(x_line), color='#EF4444', linestyle='--', linewidth=2, alpha=0.8)
        
        ax.set_xlabel('Suhu (°C)', fontsize=10, color='#6B7280')
        ax.set_ylabel('Jumlah Penyewaan', fontsize=10, color='#6B7280')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E5E7EB')
        ax.spines['bottom'].set_color('#E5E7EB')
        ax.tick_params(colors='#6B7280')
        ax.grid(True, alpha=0.3, color='#E5E7EB')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        correlation_cols = ['temp_actual', 'hum_actual', 'windspeed_actual', 'cnt']
        corr_matrix = filtered_df[correlation_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        fig.patch.set_facecolor('#FAFBFC')
        
        sns.heatmap(corr_matrix, annot=True, cmap='RdBu_r', center=0, ax=ax,
                   xticklabels=['Suhu', 'Kelembaban', 'Angin', 'Penyewaan'],
                   yticklabels=['Suhu', 'Kelembaban', 'Angin', 'Penyewaan'],
                   fmt='.2f', annot_kws={'size': 11, 'weight': '600'},
                   square=True, linewidths=2, linecolor='white',
                   cbar_kws={'shrink': 0.8})
        
        ax.tick_params(colors='#6B7280')
        
        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")

# ==================== QUESTION 2 ====================
st.markdown("""
<div class="question-header">
    <h3>⏰ Pertanyaan 2: Bagaimana pola penyewaan sepeda berdasarkan waktu?</h3>
</div>
""", unsafe_allow_html=True)

tab4, tab5, tab6 = st.tabs(["Per Jam", "Per Hari", "Trend Bulanan"])

with tab4:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        hourly_avg = filtered_hour_df.groupby('hr')[['casual', 'registered', 'cnt']].mean()
        
        fig, ax = plt.subplots(figsize=(12, 5))
        fig.patch.set_facecolor('#FAFBFC')
        ax.set_facecolor('#FAFBFC')
        
        ax.fill_between(hourly_avg.index, hourly_avg['registered'], alpha=0.15, color='#6366F1')
        ax.fill_between(hourly_avg.index, hourly_avg['casual'], alpha=0.15, color='#F59E0B')
        
        ax.plot(hourly_avg.index, hourly_avg['registered'], 
               color='#6366F1', linewidth=2.5, label='Terdaftar', marker='o', markersize=4)
        ax.plot(hourly_avg.index, hourly_avg['casual'], 
               color='#F59E0B', linewidth=2.5, label='Casual', marker='o', markersize=4)
        
        ax.set_xlabel('Jam', fontsize=10, color='#6B7280')
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=10, color='#6B7280')
        ax.set_xticks(range(0, 24))
        ax.legend(frameon=False, fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E5E7EB')
        ax.spines['bottom'].set_color('#E5E7EB')
        ax.tick_params(colors='#6B7280')
        ax.grid(True, alpha=0.3, color='#E5E7EB', axis='y')
        
        # Rush hour markers
        for h in [8, 17, 18]:
            ax.axvline(x=h, color='#EF4444', linestyle=':', alpha=0.5, linewidth=1)
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Insight</h4>
            <ul>
                <li><b>Peak:</b> 08:00 & 17:00-18:00</li>
                <li>Terdaftar = pola commuter</li>
                <li>Casual aktif siang hari</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Top 5 Jam Tersibuk**")
        peak_hours = hourly_avg.nlargest(5, 'cnt')[['cnt']].round(0)
        peak_hours.columns = ['Rata-rata']
        peak_hours.index.name = 'Jam'
        st.dataframe(peak_hours, use_container_width=True)

with tab5:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_labels = ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min']
        
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['weekday_name'] = pd.Categorical(
            filtered_df_copy['weekday_name'], categories=day_order, ordered=True
        )
        weekday_avg = filtered_df_copy.groupby('weekday_name')[['casual', 'registered']].mean()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#FAFBFC')
        ax.set_facecolor('#FAFBFC')
        
        x = np.arange(len(weekday_avg))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, weekday_avg['registered'], width, 
                      label='Terdaftar', color='#6366F1')
        bars2 = ax.bar(x + width/2, weekday_avg['casual'], width, 
                      label='Casual', color='#F59E0B')
        
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=10, color='#6B7280')
        ax.set_xticks(x)
        ax.set_xticklabels(day_labels)
        ax.legend(frameon=False, fontsize=10)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#E5E7EB')
        ax.spines['bottom'].set_color('#E5E7EB')
        ax.tick_params(colors='#6B7280')
        
        # Weekend highlight
        ax.axvspan(4.5, 6.5, alpha=0.08, color='#10B981')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div class="insight-card">
            <h4>💡 Insight</h4>
            <ul>
                <li>Casual naik di <b>weekend</b></li>
                <li>Terdaftar stabil weekday</li>
                <li>Weekend = target promosi</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("**Hari Kerja vs Weekend**")
        workday_stats = filtered_df.groupby('workingday')[['casual', 'registered']].mean().round(0)
        workday_stats.index = ['Weekend', 'Hari Kerja']
        st.dataframe(workday_stats, use_container_width=True)

with tab6:
    monthly_trend = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M'))['cnt'].mean()
    monthly_trend.index = monthly_trend.index.astype(str)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#FAFBFC')
    ax.set_facecolor('#FAFBFC')
    
    ax.fill_between(range(len(monthly_trend)), monthly_trend.values, alpha=0.15, color='#6366F1')
    ax.plot(range(len(monthly_trend)), monthly_trend.values, 
           color='#6366F1', linewidth=2.5, marker='o', markersize=6)
    
    ax.set_xlabel('Periode', fontsize=10, color='#6B7280')
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=10, color='#6B7280')
    
    step = max(1, len(monthly_trend) // 8)
    ax.set_xticks(range(0, len(monthly_trend), step))
    ax.set_xticklabels(monthly_trend.index[::step], rotation=45, ha='right')
    
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#E5E7EB')
    ax.spines['bottom'].set_color('#E5E7EB')
    ax.tick_params(colors='#6B7280')
    ax.grid(True, alpha=0.3, color='#E5E7EB', axis='y')
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("""
    <div class="insight-card" style="margin-top: 1rem;">
        <h4>💡 Trend Analysis</h4>
        <ul>
            <li>Pola musiman jelas - puncak di bulan hangat</li>
            <li>Pertumbuhan YoY dari 2011 ke 2012</li>
            <li>Bulan dingin (Des-Feb) = penyewaan minimum</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CLUSTERING ====================
st.markdown("""
<div class="question-header">
    <h3>🎯 Analisis Lanjutan: Segmentasi Hari Berdasarkan Volume Penyewaan</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    def categorize_rental(cnt):
        if cnt < 2000: return 'Low'
        elif cnt < 4000: return 'Medium'
        elif cnt < 6000: return 'High'
        else: return 'Very High'
    
    filtered_df_cluster = filtered_df.copy()
    filtered_df_cluster['category'] = filtered_df_cluster['cnt'].apply(categorize_rental)
    
    category_counts = filtered_df_cluster['category'].value_counts()
    category_order = ['Low', 'Medium', 'High', 'Very High']
    category_counts = category_counts.reindex(category_order).fillna(0)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    fig.patch.set_facecolor('#FAFBFC')
    
    colors = ['#FEE2E2', '#FEF3C7', '#D1FAE5', '#C7D2FE']
    explode = [0.02, 0.02, 0.02, 0.05]
    
    wedges, texts, autotexts = ax.pie(
        category_counts, 
        labels=category_counts.index,
        autopct='%1.1f%%', 
        colors=colors, 
        explode=explode,
        startangle=90,
        textprops={'fontsize': 11, 'fontweight': '500', 'color': '#374151'}
    )
    
    for autotext in autotexts:
        autotext.set_fontweight('600')
        autotext.set_color('#374151')
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("""
    <div style='background: #F9FAFB; border-radius: 10px; padding: 1.25rem; margin-bottom: 1rem;'>
        <div style='font-weight: 600; color: #374151; margin-bottom: 0.75rem;'>📊 Kategori Volume</div>
        <table style='width: 100%; font-size: 0.9rem; color: #4B5563;'>
            <tr><td style='padding: 0.3rem 0;'>🔴 Low</td><td>&lt; 2,000 / hari</td></tr>
            <tr><td style='padding: 0.3rem 0;'>🟡 Medium</td><td>2,000 - 4,000 / hari</td></tr>
            <tr><td style='padding: 0.3rem 0;'>🟢 High</td><td>4,000 - 6,000 / hari</td></tr>
            <tr><td style='padding: 0.3rem 0;'>🔵 Very High</td><td>&gt; 6,000 / hari</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("**Karakteristik per Kategori**")
    
    category_stats = filtered_df_cluster.groupby('category').agg({
        'temp_actual': 'mean',
        'hum_actual': 'mean',
        'cnt': ['count', 'mean']
    }).round(1)
    category_stats.columns = ['Suhu (°C)', 'Humidity (%)', 'Hari', 'Avg']
    category_stats = category_stats.reindex(category_order)
    st.dataframe(category_stats, use_container_width=True)
    
    st.markdown("""
    <div style='background: #EFF6FF; border-radius: 8px; padding: 0.75rem; margin-top: 0.75rem; font-size: 0.85rem; color: #1E40AF;'>
        💡 <b>Tip:</b> Hari Very High = suhu hangat + kelembaban rendah
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CONCLUSION ====================
st.markdown("### 📝 Kesimpulan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="conclusion-card-1">
        <div style='font-weight: 600; color: #4338CA; margin-bottom: 0.75rem; font-size: 1rem;'>
            🌤️ Pengaruh Cuaca
        </div>
        <ol style='color: #4B5563; margin: 0; padding-left: 1.25rem; line-height: 1.8;'>
            <li><b>Musim Fall</b> = waktu terbaik penyewaan</li>
            <li><b>Cuaca cerah</b> meningkatkan 2x lipat</li>
            <li><b>Suhu</b> berkorelasi positif (r≈0.63)</li>
            <li><b>Kelembaban tinggi</b> menurunkan minat</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="conclusion-card-2">
        <div style='font-weight: 600; color: #047857; margin-bottom: 0.75rem; font-size: 1rem;'>
            ⏰ Pola Waktu
        </div>
        <ol style='color: #4B5563; margin: 0; padding-left: 1.25rem; line-height: 1.8;'>
            <li><b>Jam puncak:</b> 08:00 dan 17:00-18:00</li>
            <li><b>Pengguna terdaftar</b> = pola commuter</li>
            <li><b>Casual</b> meningkat 2x di weekend</li>
            <li><b>Pertumbuhan YoY</b> 2011 → 2012</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div class="footer">
    <div style='margin-bottom: 0.5rem;'>🚲 <b>Bike Sharing Analytics Dashboard</b></div>
    <div>Muhammad Himbar Buana • Dicoding Indonesia • 2024</div>
</div>
""", unsafe_allow_html=True)
