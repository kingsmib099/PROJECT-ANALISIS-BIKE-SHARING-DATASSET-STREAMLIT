import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

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
    else:
        # Load data
        path = os.path.dirname(__file__)
        my_file = path+'/../alldata.csv'
        all_df = pd.read_csv(my_file)
        
        if choice == "TOTAL ORDER TAHUN 2011":
            st.header("TOTAL ORDER TAHUN 2011")
            # Memproses data
            data = all_df.copy()
            data['dteday'] = pd.to_datetime(data['dteday'])
            data_2011 = data[data['dteday'].dt.year == 2011]
            monthly_orders = data_2011.groupby(data_2011['dteday'].dt.month)['instant'].count().reset_index()
            monthly_orders.columns = ['Bulan', 'Jumlah Pesanan']
            # Membuat plot
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.bar(monthly_orders['Bulan'], monthly_orders['Jumlah Pesanan'], color='skyblue')
            ax.set_xlabel('Bulan')
            ax.set_ylabel('Jumlah Pesanan')
            ax.set_title('Jumlah Pesanan Tiap Bulan pada Tahun 2011')
            ax.grid(True, linestyle='--', alpha=0.7)
            st.pyplot(fig)
            # Detail
            st.header("Rincian Detail:")
            st.write("""
                - **Bulan**: Januari - Desember
                - **Jumlah Pesanan**: Jumlah record order pada bulan tersebut
            """)
        
        elif choice == "RECORD BULAN TERENDAH":
            st.header("RECORD BULAN TERENDAH")     
            # Memproses data
            data = all_df.copy()
            data['dteday'] = pd.to_datetime(data['dteday'])
            data_year = data[data['dteday'].dt.year.isin([2011, 2012])]
            monthly_orders = data_year.groupby([data_year['dteday'].dt.year, data_year['dteday'].dt.month])['instant'].count().reset_index()
            monthly_orders.columns = ['Tahun', 'Bulan', 'Jumlah Pesanan']
            min_orders = monthly_orders.loc[monthly_orders['Jumlah Pesanan'].idxmin()]
            # Membuat pie chart
            fig, ax = plt.subplots()
            ax.pie([min_orders['Jumlah Pesanan']], labels=[f'Bulan {min_orders["Bulan"]}'], autopct='%1.1f%%', startangle=90)
            ax.axis('equal')
            st.pyplot(fig)
            st.write(f"Jumlah pesanan terendah: {min_orders['Jumlah Pesanan']}")

if __name__ == "__main__":
    main()

    
    
