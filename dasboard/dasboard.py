import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def main():
    st.title("Analisis Bike Sharing")

    menu = ["Beranda", "TOTAL ORDER TAHUN 2011", "RECORD BULAN TERENDAH", "RECORD BULAN TERTINGGI","RECORD JANUARI"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Beranda":
        st.header("Selamat Datang di Aplikasi Analisis Bike Sharing")
        st.write("""
            Informasi Kumpulan Data:
            Sistem berbagi sepeda adalah generasi baru dari persewaan sepeda tradisional di mana seluruh proses mulai dari keanggotaan, penyewaan, dan pengembalian menjadi otomatis. Melalui sistem ini, pengguna dapat dengan mudah menyewa sepeda dari posisi tertentu dan kembali lagi ke posisi lain. Saat ini, terdapat lebih dari 500 program berbagi sepeda di seluruh dunia yang mencakup lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran pentingnya dalam masalah lalu lintas, lingkungan, dan kesehatan.

            Terlepas dari penerapan sistem bike sharing di dunia nyata yang menarik, karakteristik data yang dihasilkan oleh sistem ini menjadikannya menarik untuk penelitian. Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, posisi keberangkatan, dan kedatangan dicatat secara eksplisit dalam sistem ini. Fitur ini mengubah sistem bike sharing menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas dalam kota. Oleh karena itu, diharapkan sebagian besar peristiwa penting di kota dapat dideteksi melalui pemantauan data ini.

            Informasi Atribut:
            Hour.csv dan day.csv memiliki kolom berikut, kecuali hr yang tidak tersedia di day.csv
        """)
    
    elif choice == "TOTAL ORDER TAHUN 2011":
        st.header("TOTAL ORDER TAHUN 2011")
        # Load data
        @st.cache
        def load_data():
            hour_data = pd.read_csv("hour.csv")
            return hour_data.copy()  # Membuat salinan DataFrame
        
        # Function untuk memproses data
        def process_data(data):
            # Filter data untuk tahun 2011
            data['dteday'] = pd.to_datetime(data['dteday'])
            data_2011 = data[data['dteday'].dt.year == 2011]
        
            # Hitung jumlah record order tiap bulan
            monthly_orders = data_2011.groupby(data_2011['dteday'].dt.month)['instant'].count().reset_index()
            monthly_orders.columns = ['Bulan', 'Jumlah Pesanan']
            return monthly_orders
        
        # Function untuk membuat plot
        def plot_chart(data):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(data['Bulan'], data['Jumlah Pesanan'], color='skyblue')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Jumlah Pesanan')
            ax.set_title('Jumlah Pesanan Tiap Bulan pada Tahun 2011')
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
        
        # Fungsi utama
        def main():
            # Judul halaman
            st.title("Analisis Record Order Tiap Bulan Tahun 2011")
        
            # Memuat data
            data = load_data()
        
            # Memproses data
            monthly_orders = process_data(data)
        
            # Membuat plot
            plot_chart(monthly_orders)
        
            # Detail
            st.header("Rincian Detail:")
            st.write("""
            - **Bulan**: Januari - Desember
            - **Jumlah Pesanan**: Jumlah record order pada bulan tersebut
            """)
        
        if __name__ == "__main__":
            main()

    
    elif choice == "RECORD BULAN TERENDAH":
        st.header("RECORD BULAN TERENDAH")     
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
    
        # Function untuk membuat pie chart
        def plot_pie_chart(labels, sizes):
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
    
        # Fungsi utama
        def main():
            # Judul halaman
            st.title("Bulan dengan Jumlah Pesanan Terendah")
    
            # Memuat data
            data = load_data()
    
            # Memproses data untuk setiap tahun
            monthly_orders_2011 = process_data(data, 2011)
            monthly_orders_2012 = process_data(data, 2012)
    
            # Mencari bulan dengan pesanan terendah untuk setiap tahun
            min_orders_2011 = monthly_orders_2011.loc[monthly_orders_2011['Jumlah Pesanan'].idxmin()]
            min_orders_2012 = monthly_orders_2012.loc[monthly_orders_2012['Jumlah Pesanan'].idxmin()]
    
            # Membuat pie chart untuk setiap tahun
            st.header("Grafik Jumlah Pesanan Terendah Tiap Tahun")
            st.subheader("Tahun 2011")
            plot_pie_chart([f'Bulan {min_orders_2011["Bulan"]}'], [min_orders_2011['Jumlah Pesanan']])
            st.write(f"Jumlah pesanan terendah pada tahun 2011: {min_orders_2011['Jumlah Pesanan']}")
    
            st.subheader("Tahun 2012")
            plot_pie_chart([f'Bulan {min_orders_2012["Bulan"]}'], [min_orders_2012['Jumlah Pesanan']])
            st.write(f"Jumlah pesanan terendah pada tahun 2012: {min_orders_2012['Jumlah Pesanan']}")
    
        if __name__ == "__main__":
            main()
        
    elif choice == "RECORD BULAN TERTINGGI":
        st.header("RECORD BULAM TERTINGGI")
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
        
        # Fungsi utama
        def main():
            # Judul halaman
            st.title("Perbandingan Jumlah Pesanan antara Tahun 2011 dan 2012")
        
            # Memuat data
            data = load_data()
        
            # Memproses data untuk setiap tahun
            monthly_orders_2011 = process_data(data, 2011)
            monthly_orders_2012 = process_data(data, 2012)
        
            # Menghitung bulan dengan pesanan terbanyak untuk setiap tahun
            max_orders_2011 = monthly_orders_2011.loc[monthly_orders_2011['Jumlah Pesanan'].idxmax()]
            max_orders_2012 = monthly_orders_2012.loc[monthly_orders_2012['Jumlah Pesanan'].idxmax()]
        
            # Membuat bar chart untuk setiap tahun
            st.header("Grafik Jumlah Pesanan Tiap Bulan")
            st.subheader("Tahun 2011")
            plot_bar_chart(monthly_orders_2011, 2011)
        
            st.subheader("Tahun 2012")
            plot_bar_chart(monthly_orders_2012, 2012)
        
            # Menampilkan deskripsi untuk setiap tahun
            st.header("Deskripsi Data Terbanyak")
            st.write("Tahun 2011:")
            st.write(f"Bulan dengan pesanan terbanyak: Bulan {max_orders_2011['Bulan']}, Jumlah Pesanan: {max_orders_2011['Jumlah Pesanan']}")
            st.write("Tahun 2012:")
            st.write(f"Bulan dengan pesanan terbanyak: Bulan {max_orders_2012['Bulan']}, Jumlah Pesanan: {max_orders_2012['Jumlah Pesanan']}")
        
        if __name__ == "__main__":
            main()

        
        
    elif choice == "RECORD JANUARI":
        st.header("RECORD JANUARI")
        # Load data
        @st.cache
        def load_data():
            hour_data = pd.read_csv("hour.csv")
            hour_data['dteday'] = pd.to_datetime(hour_data['dteday'])
            return hour_data
        
        # Function to process data
        def process_data(data, year):
            # Filter data untuk tahun tertentu
            data_year = data[data['dteday'].dt.year == year]
        
            # Hitung jumlah record order tiap bulan
            monthly_orders = data_year.groupby(data_year['dteday'].dt.month)['instant'].count().reset_index()
            monthly_orders.columns = ['Bulan', 'Jumlah Pesanan']
            return monthly_orders
        
        # Function to plot chart
        def plot_chart(data):
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.plot(data['Bulan'], data['Jumlah Pesanan'], marker='o', linestyle='-', color='skyblue')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Jumlah Pesanan')
            ax.set_title('Jumlah Pesanan Tiap Bulan')
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
        
        # Function to get information about the first month of a specific year
        def get_first_month_info(data, year):
            # Filter data for January of the specified year
            jan_data = data[(data['dteday'].dt.year == year) & (data['dteday'].dt.month == 1)]
            
            # Get total number of orders in January
            total_orders = len(jan_data)
            
            # Get detailed information
            first_day = jan_data['dteday'].min().strftime('%Y-%m-%d')
            last_day = jan_data['dteday'].max().strftime('%Y-%m-%d')
            total_days = (jan_data['dteday'].max() - jan_data['dteday'].min()).days + 1
            
            return total_orders, first_day, last_day, total_days
        
        # Main function
        def main():
            # Page title
            st.title("Analisis Record Order Tiap Bulan")
        
            # Load data
            data = load_data()
        
            # Sidebar for selecting year
            year = st.sidebar.selectbox("Pilih Tahun", sorted(data['dteday'].dt.year.unique()))
        
            # Process data
            monthly_orders = process_data(data, year)
        
            # Plot chart
            plot_chart(monthly_orders)
        
            # Detail
            st.header("Rincian Detail:")
            st.write("""
            - **Bulan**: Januari - Desember
            - **Jumlah Pesanan**: Jumlah record order pada bulan tersebut
            """)
            
            # Information about the first month of the selected year
            st.header(f"Informasi Bulan Pertama Tahun {year}")
            total_orders, first_day, last_day, total_days = get_first_month_info(data, year)
            st.write(f"""
            - **Total Pesanan Bulan Pertama Tahun {year}**: {total_orders}
            - **Tanggal Pertama Pesanan**: {first_day}
            - **Tanggal Terakhir Pesanan**: {last_day}
            - **Total Hari dengan Pesanan**: {total_days} hari
            """)
        
        if __name__ == "__main__":
            main()




if __name__ == "__main__":
    main()
