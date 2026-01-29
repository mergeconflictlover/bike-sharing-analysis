import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
import os

# Set page config
st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS untuk UI yang lebih menarik
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 2px solid #0f3460;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #e8e8e8;
    }
    
    /* Main content area */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 2rem 3rem;
        margin: 1rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* Header styling */
    h1 {
        color: #1a1a2e;
        font-weight: 700;
        text-align: center;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
        margin-bottom: 20px;
    }
    
    h2, h3 {
        color: #16213e;
        font-weight: 600;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 1rem;
        font-weight: 500;
        color: #444;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f0f2f6;
        border-radius: 10px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #667eea;
        color: white;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 30px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Info boxes */
    .info-box {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
    }
    
    .insight-box {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #28a745;
        margin: 10px 0;
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #667eea, transparent);
        margin: 30px 0;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #666;
        padding: 20px;
        font-size: 0.9rem;
    }
    
    /* Sidebar text */
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #fff !important;
    }
    
    /* Warning message */
    .stAlert {
        border-radius: 10px;
    }
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

# ==================== SIDEBAR ====================
with st.sidebar:
    # Logo and title
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='font-size: 3rem; margin: 0;'>🚴</h1>
        <h2 style='margin: 10px 0; font-size: 1.5rem;'>Bike Sharing</h2>
        <p style='color: #a0a0a0; font-size: 0.9rem;'>Analytics Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Date filter with icon
    st.markdown("### 📅 Filter Tanggal")
    min_date = day_df['dteday'].min().date()
    max_date = day_df['dteday'].max().date()
    
    date_range = st.date_input(
        "Pilih Rentang Tanggal",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date,
        label_visibility="collapsed"
    )
    
    # Handle single date selection
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date = date_range[0]
        end_date = date_range[0]
    
    st.markdown("---")
    
    # Season filter with icon
    st.markdown("### 🌸 Filter Musim")
    season_options = ['Semua Musim'] + list(day_df['season_name'].unique())
    selected_season = st.selectbox("Pilih Musim", season_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    # Weather filter
    st.markdown("### ☀️ Filter Cuaca")
    weather_options = ['Semua Cuaca'] + list(day_df['weather_name'].unique())
    selected_weather = st.selectbox("Pilih Cuaca", weather_options, label_visibility="collapsed")
    
    st.markdown("---")
    
    # About section
    st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;'>
        <h4 style='margin: 0 0 10px 0;'>📊 Tentang Dataset</h4>
        <p style='font-size: 0.85rem; color: #b0b0b0; line-height: 1.5;'>
            Data penyewaan sepeda dari <b>Capital Bikeshare</b> di Washington D.C. 
            pada tahun 2011-2012.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Credits
    st.markdown("""
    <div style='text-align: center; padding: 20px 0; margin-top: 30px;'>
        <p style='color: #666; font-size: 0.8rem;'>Made with ❤️ by</p>
        <p style='color: #fff; font-weight: bold;'>Muhammad Himbar Buana</p>
    </div>
    """, unsafe_allow_html=True)

# ==================== FILTER DATA ====================
filtered_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & 
                      (day_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'Semua Musim':
    filtered_df = filtered_df[filtered_df['season_name'] == selected_season]

if selected_weather != 'Semua Cuaca':
    filtered_df = filtered_df[filtered_df['weather_name'] == selected_weather]

filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & 
                            (hour_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'Semua Musim':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season_name'] == selected_season]

if selected_weather != 'Semua Cuaca':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['weather_name'] == selected_weather]

# Check if data is empty
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data untuk filter yang dipilih. Silakan ubah filter Anda.")
    st.stop()

# ==================== MAIN CONTENT ====================
# Header
st.markdown("""
<div style='text-align: center; margin-bottom: 30px;'>
    <h1 style='font-size: 2.5rem; margin-bottom: 10px;'>🚴 Bike Sharing Analytics Dashboard</h1>
    <p style='color: #666; font-size: 1.1rem;'>Analisis pola penyewaan sepeda berdasarkan kondisi cuaca dan waktu</p>
</div>
""", unsafe_allow_html=True)

# ==================== METRICS ROW ====================
st.markdown("### 📈 Ringkasan Data")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric(
        label="🚲 Total Penyewaan",
        value=f"{total_rentals:,}",
        delta=f"{len(filtered_df)} hari"
    )

with col2:
    avg_rentals = filtered_df['cnt'].mean()
    st.metric(
        label="📊 Rata-rata Harian",
        value=f"{avg_rentals:,.0f}",
        delta="per hari"
    )

with col3:
    total_casual = filtered_df['casual'].sum()
    pct_casual = (total_casual / total_rentals * 100) if total_rentals > 0 else 0
    st.metric(
        label="🎯 Casual Users",
        value=f"{total_casual:,}",
        delta=f"{pct_casual:.1f}%"
    )

with col4:
    total_registered = filtered_df['registered'].sum()
    pct_registered = (total_registered / total_rentals * 100) if total_rentals > 0 else 0
    st.metric(
        label="⭐ Registered Users",
        value=f"{total_registered:,}",
        delta=f"{pct_registered:.1f}%"
    )

st.markdown("---")

# ==================== QUESTION 1: WEATHER IMPACT ====================
st.markdown("""
<div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 25px; border-radius: 15px; margin: 20px 0;'>
    <h3 style='margin: 0; color: white;'>📊 Pertanyaan 1: Bagaimana pengaruh kondisi cuaca terhadap penyewaan sepeda?</h3>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌸 Analisis Musim", "☁️ Kondisi Cuaca", "🌡️ Korelasi Suhu"])

with tab1:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = filtered_df.groupby('season_name')['cnt'].mean().reindex(season_order).dropna()
        
        if not season_data.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # Color palette
            colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95E1D3']
            max_idx = season_data.values.argmax()
            bar_colors = ['#D3D3D3' if i != max_idx else colors[i] for i in range(len(season_data))]
            
            bars = ax.bar(season_data.index, season_data.values, color=bar_colors, 
                         edgecolor='white', linewidth=2)
            
            # Add value labels
            for bar, val in zip(bars, season_data.values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 80, 
                       f'{val:,.0f}', ha='center', fontweight='bold', fontsize=12)
            
            ax.set_title('Rata-rata Penyewaan per Musim', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Musim', fontsize=12)
            ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_ylim(0, max(season_data.values) * 1.15)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Tidak ada data untuk ditampilkan.")
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #4ECDC4;'>
            <h4 style='color: #16213e; margin-top: 0;'>💡 Insight Utama</h4>
            <ul style='color: #444; line-height: 1.8;'>
                <li><b>Musim Fall (Gugur)</b> memiliki rata-rata penyewaan tertinggi</li>
                <li><b>Musim Spring (Semi)</b> memiliki penyewaan terendah</li>
                <li>Perbedaan antara musim tertinggi dan terendah bisa mencapai <b>50%</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Statistik per Musim:**")
        
        season_stats = filtered_df.groupby('season_name').agg({
            'cnt': ['mean', 'sum'],
            'casual': 'mean',
            'registered': 'mean'
        }).round(0)
        season_stats.columns = ['Avg', 'Total', 'Casual', 'Registered']
        st.dataframe(season_stats, use_container_width=True)

with tab2:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        weather_data = filtered_df.groupby('weather_name')['cnt'].mean().sort_values(ascending=True)
        
        if not weather_data.empty:
            fig, ax = plt.subplots(figsize=(10, 6))
            
            colors = ['#FF6B6B', '#FFE66D', '#4ECDC4', '#667eea'][:len(weather_data)]
            bars = ax.barh(weather_data.index, weather_data.values, color=colors[::-1],
                          edgecolor='white', linewidth=2, height=0.6)
            
            for bar, val in zip(bars, weather_data.values):
                ax.text(val + 50, bar.get_y() + bar.get_height()/2, 
                       f'{val:,.0f}', va='center', fontweight='bold', fontsize=11)
            
            ax.set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=16, fontweight='bold', pad=20)
            ax.set_xlabel('Rata-rata Penyewaan', fontsize=12)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.set_xlim(0, max(weather_data.values) * 1.15)
            
            plt.tight_layout()
            st.pyplot(fig)
        else:
            st.info("Tidak ada data untuk ditampilkan.")
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #FFE66D;'>
            <h4 style='color: #16213e; margin-top: 0;'>💡 Insight Utama</h4>
            <ul style='color: #444; line-height: 1.8;'>
                <li><b>Cuaca Cerah (Clear)</b> menghasilkan penyewaan tertinggi</li>
                <li><b>Hujan/Salju</b> menurunkan penyewaan hingga <b>60%</b></li>
                <li>Cuaca buruk sangat mempengaruhi keputusan bersepeda</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📋 Statistik per Cuaca:**")
        
        weather_stats = filtered_df.groupby('weather_name').agg({
            'cnt': ['mean', 'count'],
        }).round(0)
        weather_stats.columns = ['Rata-rata', 'Jumlah Hari']
        st.dataframe(weather_stats, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        
        scatter = ax.scatter(filtered_df['temp_actual'], filtered_df['cnt'], 
                            alpha=0.6, c=filtered_df['cnt'], cmap='viridis', 
                            s=50, edgecolors='white', linewidth=0.5)
        
        # Trend line
        if len(filtered_df) > 1:
            z = np.polyfit(filtered_df['temp_actual'], filtered_df['cnt'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(filtered_df['temp_actual'].min(), filtered_df['temp_actual'].max(), 100)
            ax.plot(x_line, p(x_line), "r--", alpha=0.8, linewidth=2, label='Trend Line')
        
        ax.set_title('Hubungan Suhu dengan Penyewaan', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Suhu (°C)', fontsize=12)
        ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        
        plt.colorbar(scatter, ax=ax, label='Jumlah Penyewaan')
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        correlation_cols = ['temp_actual', 'hum_actual', 'windspeed_actual', 'cnt']
        corr_matrix = filtered_df[correlation_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(corr_matrix, annot=True, cmap='RdYlBu_r', center=0, ax=ax,
                   xticklabels=['Suhu', 'Kelembaban', 'Kec. Angin', 'Penyewaan'],
                   yticklabels=['Suhu', 'Kelembaban', 'Kec. Angin', 'Penyewaan'],
                   fmt='.2f', annot_kws={'size': 12, 'weight': 'bold'},
                   square=True, linewidths=2, linecolor='white')
        ax.set_title('Matriks Korelasi Faktor Cuaca', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        st.pyplot(fig)

st.markdown("---")

# ==================== QUESTION 2: TIME PATTERNS ====================
st.markdown("""
<div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 15px 25px; border-radius: 15px; margin: 20px 0;'>
    <h3 style='margin: 0; color: white;'>⏰ Pertanyaan 2: Bagaimana pola penyewaan sepeda berdasarkan waktu?</h3>
</div>
""", unsafe_allow_html=True)

tab4, tab5, tab6 = st.tabs(["🕐 Pola per Jam", "📅 Pola per Hari", "📈 Trend Bulanan"])

with tab4:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        hourly_avg = filtered_hour_df.groupby('hr')[['casual', 'registered', 'cnt']].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.fill_between(hourly_avg.index, hourly_avg['registered'], alpha=0.3, color='#667eea')
        ax.fill_between(hourly_avg.index, hourly_avg['casual'], alpha=0.3, color='#FF6B6B')
        
        ax.plot(hourly_avg.index, hourly_avg['registered'], marker='o', 
               label='Registered', color='#667eea', linewidth=2.5, markersize=6)
        ax.plot(hourly_avg.index, hourly_avg['casual'], marker='s', 
               label='Casual', color='#FF6B6B', linewidth=2.5, markersize=6)
        
        ax.set_title('Pola Penyewaan Sepeda per Jam', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Jam', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax.set_xticks(range(0, 24))
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.3)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Mark peak hours
        ax.axvline(x=8, color='gray', linestyle='--', alpha=0.5)
        ax.axvline(x=17, color='gray', linestyle='--', alpha=0.5)
        ax.text(8, ax.get_ylim()[1]*0.95, 'Rush Hour', ha='center', fontsize=9, color='gray')
        ax.text(17, ax.get_ylim()[1]*0.95, 'Rush Hour', ha='center', fontsize=9, color='gray')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #667eea;'>
            <h4 style='color: #16213e; margin-top: 0;'>💡 Insight Utama</h4>
            <ul style='color: #444; line-height: 1.8;'>
                <li><b>Jam Puncak:</b> 08:00 (pagi) dan 17:00-18:00 (sore)</li>
                <li><b>Registered</b> menunjukkan pola commuter (bimodal)</li>
                <li><b>Casual</b> lebih aktif di siang hari (11:00-16:00)</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**🏆 Top 5 Jam Tersibuk:**")
        
        peak_hours = hourly_avg.nlargest(5, 'cnt')[['cnt', 'casual', 'registered']].round(0)
        peak_hours.columns = ['Total', 'Casual', 'Registered']
        peak_hours.index.name = 'Jam'
        st.dataframe(peak_hours, use_container_width=True)

with tab5:
    col1, col2 = st.columns([3, 2])
    
    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['weekday_name'] = pd.Categorical(
            filtered_df_copy['weekday_name'], 
            categories=day_order, 
            ordered=True
        )
        weekday_avg = filtered_df_copy.groupby('weekday_name')[['casual', 'registered']].mean()
        
        fig, ax = plt.subplots(figsize=(12, 6))
        x = np.arange(len(weekday_avg))
        width = 0.35
        
        bars1 = ax.bar(x - width/2, weekday_avg['registered'], width, 
                      label='Registered', color='#667eea', edgecolor='white', linewidth=2)
        bars2 = ax.bar(x + width/2, weekday_avg['casual'], width, 
                      label='Casual', color='#FF6B6B', edgecolor='white', linewidth=2)
        
        ax.set_title('Pola Penyewaan per Hari dalam Seminggu', fontsize=16, fontweight='bold', pad=20)
        ax.set_xlabel('Hari', fontsize=12)
        ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'], fontsize=11)
        ax.legend(fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        # Highlight weekend
        ax.axvspan(4.5, 6.5, alpha=0.1, color='green')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        <div style='background: #f8f9fa; padding: 20px; border-radius: 15px; border-left: 5px solid #FF6B6B;'>
            <h4 style='color: #16213e; margin-top: 0;'>💡 Insight Utama</h4>
            <ul style='color: #444; line-height: 1.8;'>
                <li><b>Casual</b> meningkat signifikan di <b>weekend</b></li>
                <li><b>Registered</b> relatif stabil sepanjang minggu</li>
                <li>Weekend cocok untuk program <b>promosi casual users</b></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**📊 Perbandingan Hari Kerja vs Weekend:**")
        
        workday_stats = filtered_df.groupby('workingday').agg({
            'casual': 'mean',
            'registered': 'mean',
            'cnt': 'mean'
        }).round(0)
        workday_stats.index = ['Weekend/Holiday', 'Working Day']
        workday_stats.columns = ['Casual', 'Registered', 'Total']
        st.dataframe(workday_stats, use_container_width=True)

with tab6:
    monthly_trend = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M'))[['cnt', 'casual', 'registered']].mean()
    monthly_trend.index = monthly_trend.index.astype(str)
    
    fig, ax = plt.subplots(figsize=(14, 6))
    
    ax.fill_between(range(len(monthly_trend)), monthly_trend['cnt'], alpha=0.3, color='#667eea')
    ax.plot(range(len(monthly_trend)), monthly_trend['cnt'], marker='o', 
           color='#667eea', linewidth=2.5, markersize=8, label='Total')
    
    ax.set_title('Trend Penyewaan Bulanan', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Periode', fontsize=12)
    ax.set_ylabel('Rata-rata Penyewaan', fontsize=12)
    
    # Show fewer x-ticks for readability
    step = max(1, len(monthly_trend) // 12)
    ax.set_xticks(range(0, len(monthly_trend), step))
    ax.set_xticklabels(monthly_trend.index[::step], rotation=45, ha='right')
    
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    
    st.markdown("""
    <div style='background: #e8f5e9; padding: 20px; border-radius: 15px; margin-top: 20px;'>
        <h4 style='color: #2e7d32; margin-top: 0;'>📈 Trend Analysis</h4>
        <ul style='color: #444; line-height: 1.8;'>
            <li>Terdapat <b>pola musiman</b> yang jelas dengan puncak di bulan-bulan hangat</li>
            <li><b>Pertumbuhan year-over-year</b> dari 2011 ke 2012 menunjukkan adopsi yang meningkat</li>
            <li>Bulan-bulan dingin (Des-Feb) memiliki penyewaan terendah</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CLUSTERING ANALYSIS ====================
st.markdown("""
<div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 15px 25px; border-radius: 15px; margin: 20px 0;'>
    <h3 style='margin: 0; color: white;'>🔍 Analisis Lanjutan: Kategorisasi Hari Berdasarkan Tingkat Penyewaan</h3>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])

with col1:
    def categorize_rental(cnt):
        if cnt < 2000:
            return 'Low'
        elif cnt < 4000:
            return 'Medium'
        elif cnt < 6000:
            return 'High'
        else:
            return 'Very High'
    
    filtered_df_cluster = filtered_df.copy()
    filtered_df_cluster['rental_category'] = filtered_df_cluster['cnt'].apply(categorize_rental)
    
    category_counts = filtered_df_cluster['rental_category'].value_counts()
    category_order = ['Low', 'Medium', 'High', 'Very High']
    category_counts = category_counts.reindex(category_order).fillna(0)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['#FF6B6B', '#FFE66D', '#4ECDC4', '#667eea']
    explode = [0.02, 0.02, 0.02, 0.05]
    
    wedges, texts, autotexts = ax.pie(category_counts, labels=category_counts.index, 
                                       autopct='%1.1f%%', colors=colors, explode=explode,
                                       shadow=True, startangle=90,
                                       textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
    
    ax.set_title('Distribusi Hari Berdasarkan\nKategori Penyewaan', fontsize=16, fontweight='bold', pad=20)
    
    # Add legend
    ax.legend(wedges, [f'{cat}: {int(val)} hari' for cat, val in zip(category_order, category_counts)],
             title="Kategori", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=10)
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.markdown("""
    <div style='background: #fff3e0; padding: 20px; border-radius: 15px; border-left: 5px solid #ff9800;'>
        <h4 style='color: #e65100; margin-top: 0;'>🏷️ Kategori Penyewaan</h4>
        <table style='width: 100%; color: #444;'>
            <tr><td>🔴 <b>Low</b></td><td>&lt; 2,000 penyewaan/hari</td></tr>
            <tr><td>🟡 <b>Medium</b></td><td>2,000 - 4,000 penyewaan/hari</td></tr>
            <tr><td>🟢 <b>High</b></td><td>4,000 - 6,000 penyewaan/hari</td></tr>
            <tr><td>🔵 <b>Very High</b></td><td>&gt; 6,000 penyewaan/hari</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**📋 Karakteristik per Kategori:**")
    
    category_stats = filtered_df_cluster.groupby('rental_category').agg({
        'temp_actual': 'mean',
        'hum_actual': 'mean',
        'cnt': ['count', 'mean']
    }).round(1)
    category_stats.columns = ['Avg Temp (°C)', 'Avg Humidity (%)', 'Jumlah Hari', 'Avg Rentals']
    category_stats = category_stats.reindex(category_order)
    st.dataframe(category_stats, use_container_width=True)
    
    st.markdown("""
    <div style='background: #e3f2fd; padding: 15px; border-radius: 10px; margin-top: 15px;'>
        <p style='color: #1565c0; margin: 0; font-size: 0.9rem;'>
            <b>💡 Tip:</b> Hari dengan penyewaan Very High cenderung memiliki suhu lebih hangat dan kelembaban lebih rendah.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ==================== CONCLUSION ====================
st.markdown("""
<div style='background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); color: white; padding: 25px; border-radius: 20px; margin: 20px 0;'>
    <h2 style='text-align: center; color: white; margin-bottom: 25px;'>📝 Kesimpulan & Rekomendasi</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 25px; border-radius: 15px; height: 100%;'>
        <h4 style='color: white; margin-top: 0;'>🌤️ Pengaruh Cuaca</h4>
        <ol style='line-height: 2;'>
            <li><b>Musim Fall</b> adalah waktu terbaik untuk penyewaan sepeda</li>
            <li><b>Cuaca cerah</b> meningkatkan penyewaan hingga 2x lipat</li>
            <li><b>Suhu</b> memiliki korelasi positif kuat (r≈0.63)</li>
            <li><b>Kelembaban tinggi</b> menurunkan minat bersepeda</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style='background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); color: white; padding: 25px; border-radius: 15px; height: 100%;'>
        <h4 style='color: white; margin-top: 0;'>⏰ Pola Waktu</h4>
        <ol style='line-height: 2;'>
            <li><b>Jam puncak:</b> 08:00 dan 17:00-18:00</li>
            <li><b>Registered users</b> dominan dengan pola commuter</li>
            <li><b>Casual users</b> meningkat 2x di weekend</li>
            <li>Terdapat <b>pertumbuhan YoY</b> dari 2011 ke 2012</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

# ==================== FOOTER ====================
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 30px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 15px; margin-top: 20px;'>
    <p style='margin: 0; color: #666; font-size: 1rem;'>
        <b>🚴 Bike Sharing Analytics Dashboard</b>
    </p>
    <p style='margin: 5px 0 0 0; color: #888; font-size: 0.9rem;'>
        Created with ❤️ by <b>Muhammad Himbar Buana</b> | Data Source: Capital Bikeshare System
    </p>
    <p style='margin: 5px 0 0 0; color: #aaa; font-size: 0.8rem;'>
        Dicoding Indonesia - Belajar Analisis Data dengan Python
    </p>
</div>
""", unsafe_allow_html=True)
