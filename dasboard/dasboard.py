import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    hour_data = pd.read_csv("hour.csv")
    hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
    return hour_data

# Function untuk memproses data untuk tahun tertentu
def process_data(data, year):
    data_year = data[data['dteday'].dt.year == year]
    monthly_orders = data_year.groupby(data_year['dteday'].dt.month)['instant'].count().reset_index()
    monthly_orders.columns = ['Bulan', 'Jumlah Pesanan']
    return monthly_orders

# Function untuk membuat bar chart
def plot_bar_chart(data, year):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(data['Bulan'], data['Jumlah Pesanan'], color='skyblue')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pesanan')
    ax.set_title(f'Jumlah Pesanan Tiap Bulan Tahun {year}')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Function untuk membuat pie chart
def plot_pie_chart(labels, sizes):
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

# Function untuk membuat line chart
def plot_line_chart(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['Bulan'], data['Jumlah Pesanan'], marker='o', linestyle='-', color='skyblue')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Jumlah Pesanan')
    ax.set_title('Jumlah Pesanan Tiap Bulan')
    ax.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(fig)

# Function untuk mendapatkan informasi tentang bulan pertama dari tahun tertentu
def get_first_month_info(data, year):
    jan_data = data[(data['dteday'].dt.year == year) & (data['dteday'].dt.month == 1)]
    total_orders = len(jan_data)
    first_day = jan_data['dteday'].min().strftime('%Y-%m-%d')
    last_day = jan_data['dteday'].max().strftime('%Y-%m-%d')
    total_days = (jan_data['dteday'].max() - jan_data['dteday'].min()).days + 1
    return total_orders, first_day, last_day, total_days

# Fungsi utama
def main():
    st.title("Analisis Bike Sharing")
    
    menu = ["Beranda", "TOTAL ORDER TAHUN 2011", "RECORD BULAN TERENDAH", "RECORD BULAN TERTINGGI", "RECORD JANUARI"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Beranda":
        st.header("Selamat Datang di Aplikasi Analisis Bike Sharing")
        st.write("""
            Informasi Kumpulan Data:
            ...
        """)
    
    elif choice == "TOTAL ORDER TAHUN 2011":
        st.header("TOTAL ORDER TAHUN 2011")
        data = load_data()
        monthly_orders = process_data(data, 2011)
        plot_bar_chart(monthly_orders, 2011)
        st.header("Rincian Detail:")
        st.write("""
            - **Bulan**: Januari - Desember
            - **Jumlah Pesanan**: Jumlah record order pada bulan tersebut
        """)
    
    elif choice == "RECORD BULAN TERENDAH":
        st.header("RECORD BULAN TERENDAH")
        data = load_data()
        monthly_orders_2011 = process_data(data, 2011)
        monthly_orders_2012 = process_data(data, 2012)
        min_orders_2011 = monthly_orders_2011.loc[monthly_orders_2011['Jumlah Pesanan'].idxmin()]
        min_orders_2012 = monthly_orders_2012.loc[monthly_orders_2012['Jumlah Pesanan'].idxmin()]
        st.header("Grafik Jumlah Pesanan Terendah Tiap Tahun")
        st.subheader("Tahun 2011")
        plot_pie_chart([f'Bulan {min_orders_2011["Bulan"]}'], [min_orders_2011['Jumlah Pesanan']])
        st.write(f"Jumlah pesanan terendah pada tahun 2011: {min_orders_2011['Jumlah Pesanan']}")
        st.subheader("Tahun 2012")
        plot_pie_chart([f'Bulan {min_orders_2012["Bulan"]}'], [min_orders_2012['Jumlah Pesanan']])
        st.write(f"Jumlah pesanan terendah pada tahun 2012: {min_orders_2012['Jumlah Pesanan']}")
    
    elif choice == "RECORD BULAN TERTINGGI":
        st.header("RECORD BULAM TERTINGGI")
        data = load_data()
        monthly_orders_2011 = process_data(data, 2011)
        monthly_orders_2012 = process_data(data, 2012)
        max_orders_2011 = monthly_orders_2011.loc[monthly_orders_2011['Jumlah Pesanan'].idxmax()]
        max_orders_2012 = monthly_orders_2012.loc[monthly_orders_2012['Jumlah Pesanan'].idxmax()]
        st.header("Grafik Jumlah Pesanan Tiap Bulan")
        st.subheader("Tahun 2011")
        plot_bar_chart(monthly_orders_2011, 2011)
        st.subheader("Tahun 2012")
        plot_bar_chart(monthly_orders_2012, 2012)
        st.header("Deskripsi Data Terbanyak")
        st.write("Tahun 2011:")
        st.write(f"Bulan dengan pesanan terbanyak: Bulan {max_orders_2011['Bulan']}, Jumlah Pesanan: {max_orders_2011['Jumlah Pesanan']}")
        st.write("Tahun 2012:")
        st.write(f"Bulan dengan pesanan terbanyak: Bulan {max_orders_2012['Bulan']}, Jumlah Pesanan: {max_orders_2012['Jumlah Pesanan']}")
    
    elif choice == "RECORD JANUARI":
        st.header("RECORD JANUARI")
        data = load_data()
        year = st.sidebar.selectbox("Pilih Tahun", sorted(data['dteday'].dt.year.unique()))
        monthly_orders = process_data(data, year)
        plot_line_chart(monthly_orders)
        st.header("Rincian Detail:")
        st.write("""
            - **Bulan**: Januari - Desember
            """)
