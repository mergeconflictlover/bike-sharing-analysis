import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import os

# Set page config
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

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

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/dicodingacademy/assets/main/logo.png", width=200)
    st.title("🚲 Bike Sharing Dashboard")
    st.markdown("---")
    
    # Date filter
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    
    start_date, end_date = st.date_input(
        "Pilih Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    st.markdown("---")
    
    # Season filter
    season_options = ['All'] + list(day_df['season_name'].unique())
    selected_season = st.selectbox("Pilih Musim", season_options)
    
    st.markdown("---")
    st.markdown("### Tentang Dataset")
    st.markdown("""
    Dataset ini berisi data penyewaan sepeda harian dari sistem Capital Bikeshare 
    di Washington D.C. pada tahun 2011-2012.
    """)

# Filter data
filtered_df = day_df[(day_df['dteday'] >= pd.Timestamp(start_date)) & 
                      (day_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'All':
    filtered_df = filtered_df[filtered_df['season_name'] == selected_season]

filtered_hour_df = hour_df[(hour_df['dteday'] >= pd.Timestamp(start_date)) & 
                            (hour_df['dteday'] <= pd.Timestamp(end_date))]

if selected_season != 'All':
    filtered_hour_df = filtered_hour_df[filtered_hour_df['season_name'] == selected_season]

# Main content
st.title("🚲 Bike Sharing Analysis Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis pola penyewaan sepeda berdasarkan kondisi cuaca dan waktu.")

# Metrics
st.markdown("---")
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_rentals = filtered_df['cnt'].sum()
    st.metric("Total Penyewaan", f"{total_rentals:,}")
    
with col2:
    avg_rentals = filtered_df['cnt'].mean()
    st.metric("Rata-rata Harian", f"{avg_rentals:,.0f}")
    
with col3:
    total_casual = filtered_df['casual'].sum()
    st.metric("Total Casual", f"{total_casual:,}")
    
with col4:
    total_registered = filtered_df['registered'].sum()
    st.metric("Total Registered", f"{total_registered:,}")

st.markdown("---")

# Visualization 1: Weather Impact
st.subheader("📊 Pertanyaan 1: Pengaruh Kondisi Cuaca terhadap Penyewaan Sepeda")

tab1, tab2, tab3 = st.tabs(["Musim", "Kondisi Cuaca", "Korelasi"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        season_order = ['Spring', 'Summer', 'Fall', 'Winter']
        season_data = filtered_df.groupby('season_name')['cnt'].mean().reindex(season_order)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#D3D3D3' if x != season_data.idxmax() else '#72BCD4' for x in season_data.index]
        bars = ax.bar(season_data.index, season_data.values, color=colors)
        ax.set_title('Rata-rata Penyewaan per Musim', fontsize=14, fontweight='bold')
        ax.set_xlabel('Musim')
        ax.set_ylabel('Rata-rata Penyewaan')
        for bar, val in zip(bars, season_data.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50, 
                   f'{val:.0f}', ha='center', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **Insight:**
        - **Musim Fall (Gugur)** memiliki rata-rata penyewaan tertinggi
        - **Musim Spring (Semi)** memiliki penyewaan terendah
        - Perbedaan antara musim tertinggi dan terendah bisa mencapai 50%
        """)
        
        # Data table
        season_stats = filtered_df.groupby('season_name').agg({
            'cnt': ['mean', 'sum'],
            'casual': 'mean',
            'registered': 'mean'
        }).round(0)
        season_stats.columns = ['Rata-rata', 'Total', 'Casual', 'Registered']
        st.dataframe(season_stats)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        weather_data = filtered_df.groupby('weather_name')['cnt'].mean().sort_values(ascending=True)
        
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = ['#D3D3D3' if x != weather_data.idxmax() else '#72BCD4' for x in weather_data.index]
        bars = ax.barh(weather_data.index, weather_data.values, color=colors[::-1])
        ax.set_title('Rata-rata Penyewaan per Kondisi Cuaca', fontsize=14, fontweight='bold')
        ax.set_xlabel('Rata-rata Penyewaan')
        for bar, val in zip(bars, weather_data.values):
            ax.text(val + 50, bar.get_y() + bar.get_height()/2, 
                   f'{val:.0f}', va='center', fontweight='bold')
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **Insight:**
        - **Cuaca Cerah (Clear)** menghasilkan penyewaan tertinggi
        - **Hujan/Salju Ringan** menurunkan penyewaan hingga 60%
        - Cuaca buruk sangat mempengaruhi keputusan untuk bersepeda
        """)
        
        weather_stats = filtered_df.groupby('weather_name').agg({
            'cnt': ['mean', 'count'],
        }).round(0)
        weather_stats.columns = ['Rata-rata', 'Jumlah Hari']
        st.dataframe(weather_stats)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(filtered_df['temp_actual'], filtered_df['cnt'], alpha=0.5, c='#72BCD4')
        
        # Trend line
        import numpy as np
        z = np.polyfit(filtered_df['temp_actual'], filtered_df['cnt'], 1)
        p = np.poly1d(z)
        ax.plot(filtered_df['temp_actual'].sort_values(), 
               p(filtered_df['temp_actual'].sort_values()), 
               "r--", alpha=0.8, label='Trend Line')
        
        ax.set_title('Hubungan Suhu dengan Penyewaan', fontsize=14, fontweight='bold')
        ax.set_xlabel('Suhu (°C)')
        ax.set_ylabel('Jumlah Penyewaan')
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        correlation_cols = ['temp_actual', 'hum_actual', 'windspeed_actual', 'cnt']
        corr_matrix = filtered_df[correlation_cols].corr()
        
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax,
                   xticklabels=['Suhu', 'Kelembaban', 'Kec. Angin', 'Penyewaan'],
                   yticklabels=['Suhu', 'Kelembaban', 'Kec. Angin', 'Penyewaan'])
        ax.set_title('Matriks Korelasi', fontsize=14, fontweight='bold')
        st.pyplot(fig)

st.markdown("---")

# Visualization 2: Time Patterns
st.subheader("⏰ Pertanyaan 2: Pola Penyewaan Berdasarkan Waktu")

tab4, tab5, tab6 = st.tabs(["Pola per Jam", "Pola per Hari", "Trend Bulanan"])

with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        hourly_avg = filtered_hour_df.groupby('hr')[['casual', 'registered', 'cnt']].mean()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(hourly_avg.index, hourly_avg['registered'], marker='o', 
               label='Registered', color='#72BCD4', linewidth=2)
        ax.plot(hourly_avg.index, hourly_avg['casual'], marker='s', 
               label='Casual', color='#FFA07A', linewidth=2)
        ax.fill_between(hourly_avg.index, hourly_avg['registered'], alpha=0.3, color='#72BCD4')
        ax.fill_between(hourly_avg.index, hourly_avg['casual'], alpha=0.3, color='#FFA07A')
        ax.set_title('Pola Penyewaan per Jam', fontsize=14, fontweight='bold')
        ax.set_xlabel('Jam')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_xticks(range(0, 24))
        ax.legend()
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **Insight:**
        - **Jam Puncak:** 08:00 (pagi) dan 17:00-18:00 (sore)
        - **Registered** menunjukkan pola commuter (bimodal)
        - **Casual** lebih aktif di siang hari (11:00-16:00)
        - Pola ini menunjukkan registered digunakan untuk transportasi kerja
        """)
        
        # Peak hours
        peak_hours = hourly_avg.nlargest(5, 'cnt')[['cnt', 'casual', 'registered']].round(0)
        peak_hours.columns = ['Total', 'Casual', 'Registered']
        st.markdown("**Top 5 Jam Tersibuk:**")
        st.dataframe(peak_hours)

with tab5:
    col1, col2 = st.columns(2)
    
    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        
        # Ensure the column is ordered
        filtered_df_copy = filtered_df.copy()
        filtered_df_copy['weekday_name'] = pd.Categorical(
            filtered_df_copy['weekday_name'], 
            categories=day_order, 
            ordered=True
        )
        weekday_avg = filtered_df_copy.groupby('weekday_name')[['casual', 'registered']].mean()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        x = range(len(day_order))
        width = 0.35
        ax.bar([i - width/2 for i in x], weekday_avg['registered'], width, 
              label='Registered', color='#72BCD4')
        ax.bar([i + width/2 for i in x], weekday_avg['casual'], width, 
              label='Casual', color='#FFA07A')
        ax.set_title('Pola Penyewaan per Hari', fontsize=14, fontweight='bold')
        ax.set_xlabel('Hari')
        ax.set_ylabel('Rata-rata Penyewaan')
        ax.set_xticks(x)
        ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
        ax.legend()
        st.pyplot(fig)
    
    with col2:
        st.markdown("""
        **Insight:**
        - **Casual** meningkat signifikan di weekend (Sabtu-Minggu)
        - **Registered** relatif stabil sepanjang minggu
        - Weekend cocok untuk program promosi casual users
        - Weekday fokus pada pelayanan commuter
        """)
        
        # Workingday comparison
        workday_stats = filtered_df.groupby('workingday').agg({
            'casual': 'mean',
            'registered': 'mean',
            'cnt': 'mean'
        }).round(0)
        workday_stats.index = ['Weekend/Holiday', 'Working Day']
        workday_stats.columns = ['Casual', 'Registered', 'Total']
        st.dataframe(workday_stats)

with tab6:
    monthly_trend = filtered_df.groupby(filtered_df['dteday'].dt.to_period('M'))[['cnt', 'casual', 'registered']].mean()
    monthly_trend.index = monthly_trend.index.astype(str)
    
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(range(len(monthly_trend)), monthly_trend['cnt'], marker='o', 
           color='#72BCD4', linewidth=2, label='Total')
    ax.fill_between(range(len(monthly_trend)), monthly_trend['cnt'], alpha=0.3, color='#72BCD4')
    ax.set_title('Trend Penyewaan Bulanan', fontsize=14, fontweight='bold')
    ax.set_xlabel('Periode')
    ax.set_ylabel('Rata-rata Penyewaan')
    ax.set_xticks(range(0, len(monthly_trend), max(1, len(monthly_trend)//12)))
    ax.set_xticklabels(monthly_trend.index[::max(1, len(monthly_trend)//12)], rotation=45)
    ax.grid(True, alpha=0.3)
    ax.legend()
    st.pyplot(fig)
    
    st.markdown("""
    **Insight:**
    - Terdapat **pola musiman** yang jelas dengan puncak di bulan-bulan hangat
    - **Pertumbuhan year-over-year** dari 2011 ke 2012 menunjukkan adopsi yang meningkat
    - Bulan-bulan dingin (Des-Feb) memiliki penyewaan terendah
    """)

st.markdown("---")

# Clustering Analysis
st.subheader("🔍 Analisis Lanjutan: Kategorisasi Hari Berdasarkan Penyewaan")

col1, col2 = st.columns(2)

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
    
    filtered_df_copy = filtered_df.copy()
    filtered_df_copy['rental_category'] = filtered_df_copy['cnt'].apply(categorize_rental)
    
    category_counts = filtered_df_copy['rental_category'].value_counts()
    category_order = ['Low', 'Medium', 'High', 'Very High']
    category_counts = category_counts.reindex(category_order).fillna(0)
    
    fig, ax = plt.subplots(figsize=(8, 8))
    colors = ['#FF6B6B', '#FFE66D', '#4ECDC4', '#72BCD4']
    ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%', 
          colors=colors, explode=[0.05]*4)
    ax.set_title('Distribusi Hari Berdasarkan Kategori Penyewaan', fontsize=14, fontweight='bold')
    st.pyplot(fig)

with col2:
    st.markdown("""
    **Kategori Penyewaan:**
    - 🔴 **Low:** < 2,000 penyewaan/hari
    - 🟡 **Medium:** 2,000 - 4,000 penyewaan/hari
    - 🟢 **High:** 4,000 - 6,000 penyewaan/hari
    - 🔵 **Very High:** > 6,000 penyewaan/hari
    """)
    
    category_stats = filtered_df_copy.groupby('rental_category').agg({
        'temp_actual': 'mean',
        'hum_actual': 'mean',
        'cnt': ['count', 'mean']
    }).round(1)
    category_stats.columns = ['Avg Temp (°C)', 'Avg Humidity (%)', 'Days', 'Avg Rentals']
    category_stats = category_stats.reindex(category_order)
    st.dataframe(category_stats)
    
    st.markdown("""
    **Insight:**
    - Hari dengan penyewaan **Very High** cenderung memiliki suhu lebih hangat
    - **Kelembaban rendah** berkorelasi dengan penyewaan lebih tinggi
    - Informasi ini dapat digunakan untuk prediksi dan perencanaan inventori
    """)

st.markdown("---")

# Conclusion
st.subheader("📝 Kesimpulan")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### Pertanyaan 1: Pengaruh Cuaca
    
    1. **Musim Fall** adalah waktu terbaik untuk penyewaan sepeda
    2. **Cuaca cerah** meningkatkan penyewaan hingga 2x lipat dibanding cuaca buruk
    3. **Suhu** memiliki korelasi positif kuat (r≈0.63) dengan penyewaan
    4. **Kelembaban tinggi** menurunkan minat bersepeda
    """)

with col2:
    st.markdown("""
    ### Pertanyaan 2: Pola Waktu
    
    1. **Jam puncak:** 08:00 dan 17:00-18:00 (jam commuter)
    2. **Registered users** dominan di hari kerja dengan pola bimodal
    3. **Casual users** meningkat 2x di weekend
    4. Terdapat **pertumbuhan YoY** dari 2011 ke 2012
    """)

st.markdown("---")
st.caption("Dashboard dibuat oleh Muhammad Himbar Buana | Data: Bike Sharing Dataset")
