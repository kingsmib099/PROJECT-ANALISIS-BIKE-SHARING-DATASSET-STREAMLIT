import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from math import sqrt
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns
import csv

# Mengatur konfigurasi
st.set_page_config(page_title="Bicycle rental Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
# Pemanggilan file csv
df = pd.read_csv('day.csv')
# Membuat sidebar
st.sidebar.header("Filter Pilihan Disini")
mnth = st.sidebar.multiselect(
    "Pilih Bulan:",
    options=df["mnth"].unique(),        
    default=df["mnth"].unique()        
)
weathersit= st.sidebar.multiselect(
    "Pilih Cuaca:",
    options=df["weathersit"].unique(),        
    default=df["weathersit"].unique()        
)
season = st.sidebar.multiselect(
    "Pilih Musim:",
    options=df["season"].unique(),        
    default=df["season"].unique()        
)
# Menyeleksi sidebar
df_selection = df.query(
    "mnth == @mnth & weathersit == @weathersit & season == @season"
)
# Mainpage
st.title(":bar_chart: Bicycle Rent Dashboard")
st.markdown("##")

col1, col2 = st.columns(2)
with col1:
    st.header("Nama")
    st.text("Muhammad Japa Maulana")
with col2:
    st.header("Nim")
    st.text("10122483")
# informasi keseluruhan dataset
total_cnt = int(df_selection["cnt"].sum())
average_rent_by_cnt = round(df_selection["cnt"].mean(), )

st.markdown("---")

left_column, right_column = st.columns(2)
with left_column:
    st.subheader("total rent")
    st.subheader(f"Total {total_cnt:,}")
with right_column:
    st.subheader("Rata-rata rent perbulan")
    st.subheader(f"Total {average_rent_by_cnt:,}")
# rent by mnth
rent_by_mnth_line = (
    df_selection.groupby(by=["mnth"]).sum()[["cnt"]].sort_values(by="cnt")
)
fig_rent = px.bar(
    rent_by_mnth_line,
    x="cnt",
    y=rent_by_mnth_line.index,
    orientation="h",
    color_discrete_sequence=["#0099BB"] * len(rent_by_mnth_line),
    template="plotly_white"
)
fig_rent.update_layout(
    title="<b>Rent By Line</b>",
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))    
)
with st.expander("Penjelasan Keseluruhan cnt") :
        st.write('Pada grafik di ketahui pada masing masing bulan banyak penyewa sepeda, dan itu semua bisa disortir sehingga kita bisa memahami pada bulan berapakah, cuaca apakah, musim apakah, penyewa sepeda ada dan tiadanya')

fig_rent.update_layout(
    width=600,
    height=400,
)
st.plotly_chart(fig_rent)
# Menghitung RMSE antara 'temp' dan 'atemp'
rmse = sqrt(mean_squared_error(df['temp'], df['atemp']))
print(f'RMSE: {rmse}')
st.write('Nilai RMSE :',rmse)

# Membuat plot
plt.figure(figsize=(10, 6))
plt.bar(df.index - 0.2, df['temp'], 0.4, label='Prediksi', color='skyblue')
plt.bar(df.index + 0.2, df['atemp'], 0.4, label='Aktual', color='orange')
plt.xlabel('Index')
plt.ylabel('Nilai')
plt.title('Perbandingan Nilai Aktual dan Prediksi')
plt.legend()
plt.tight_layout()

# Menampilkan plot di Streamlit
with st.expander("Penjelasan RMSE"):
    st.write('Kita bisa melihat nilai aktual dan prediksi pada table di bawah ini yang mana nilai aktual dan prediksi yaitu RMSE: 0.03660265940449758 antara atribut temp dengan atemp, menunjukkan bahwa rata-rata kesalahan prediksi dari model Anda relatif kecil..')
st.pyplot(plt)
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
# Mengelompokkan data berdasarkan bulan dan menghitung total penyewaan ('cnt') per bulan
df['dteday'] = pd.to_datetime(df['dteday'])
monthly_rentals = df.groupby(df['dteday'].dt.month)['cnt'].sum()

# Visualisasi
plt.figure(figsize=(10, 6))

monthly_rentals.plot(kind='bar', color='skyblue')

plt.title('Total Penyewaan Sepeda per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penyewaan')
plt.xticks(ticks=range(len(monthly_rentals)), labels=[f'Bulan {i+1}' for i in range(len(monthly_rentals))], rotation=45)
with st.expander("Penjelasan penyewa setiap bulan") :
        st.write('Untuk penyewaan pada setiap bulan bisa dilihat sangat berbeda antara bulan 1 dengan yang lain, tetapi kita bisa melihat bahwa pada bulan-bulan tertentu terdapat konsumen yang sangat amat banyak, dan kita bisa melihat nya pada table diagram yang ada di bawah ')
st.pyplot(plt.gcf())

# Mengelompokkan data berdasarkan musim dan menghitung rata-rata penyewaan sepeda
season_rentals = df.groupby('season')['cnt'].mean()

# Visualisasi
season_labels = ['Musim Dingin', 'Musim Semi', 'Musim Panas', 'Musim Gugur']

plt.figure(figsize=(10, 6))

season_rentals.plot(kind='bar', color='lightgreen')

plt.title('Rata-Rata Penyewaan Sepeda per Musim')
plt.xlabel('Musim')
plt.ylabel('Rata-Rata Jumlah Penyewaan')
plt.xticks(ticks=range(len(season_rentals)), labels=season_labels, rotation=45)

with st.expander("Penjelasan Geoanalisyst pada tahun 2011") :
        st.write('Disini kita mengambil dari atribut season yaitu musim, yang mana pada 1 tahun terdapat 4 musim yaitu musim dingin, musim semi, musim panas dan musim gugur. Lalu pada masing-masing musim terdapat banyak penyewa diantara 4 musim tersebut, dan ini bisa kita lihat pada tabel diagram di bawah ')
st.pyplot(plt.gcf())

# Menjumlahkan record rent perbulan
sns.set(style="whitegrid")
data = pd.read_csv('day.csv')  

records_per_month = data.groupby('mnth')['cnt'].count()

plt.figure(figsize=(8,6))

plt.bar(records_per_month.index, records_per_month.values)
plt.title('Jumlah Record per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Record')

with st.expander("Record rent per bulan") :
        st.write('jadi, kita dapat menentukan bulan manakah yang memiliki jumlah record tertinggi dengan menggunakan kode Python pada Jupyter Notebook. Selain itu, kita juga dapat membuat diagram batang jumlah record per bulan dengan menggunakan Pandas dan Matplotlib pada Jupyter Notebook. dan menghasil kan jumlah record tertinggi pada 2011-1-1. ')
st.pyplot(plt)

#MENAMPILKAN DATA DALAM BENTUK GRAFIK
data['dteday'] = pd.to_datetime(data['dteday'])

bulan_pertama = data[data['dteday'].dt.strftime('%Y-%m').str.startswith
                ('2011-01')]

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

sns.lineplot(x='dteday', y='cnt', data=bulan_pertama, marker='o', color='green')

plt.title('Grafik Data Bulan Pertama')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah cnt')
plt.xticks(rotation=50)

with st.expander("Record rent per bulan") :
        st.write('kode ini mengekstraksi data dari file CSV day.csv dan menggambarkannya dalam grafik batang berdasarkan jumlah per hari pada bulan pertama 2011')
st.pyplot(plt)

# Mengonversi kolom "dteday" ke dalam tipe data datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Membuat filter untuk tahun 2012
filter_2012 = (data['dteday'] >= '2012-01-01') & (data['dteday'] <= '2012-12-31')

# Mengambil data untuk tahun 2012 dan kolom "registered"
registered_2012 = data.loc[filter_2012, ['dteday', 'registered']]

# Memilih data untuk tahun 2012
data_2012 = data.loc[filter_2012, ['dteday', 'registered']]

# Menambahkan kolom bulan untuk mengelompokkan berdasarkan bulan
data_2012['month'] = data_2012['dteday'].dt.month

# Mengelompokkan berdasarkan kolom bulan dan menjumlahkan nilai "registered" untuk setiap grup
total_registrasi_perbulan = data_2012.groupby('month').agg({'registered': 'sum'})

sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Plot batang berdasarkan 'dteday' dan 'registered'
sns.barplot( x ='month', y ='registered', hue = 'month' ,data=total_registrasi_perbulan, legend=False)

plt.title('Jumlah registerasi tahun 2012')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Registrasi')

with st.expander("Registered pada tahun 2012") :
        st.write('Kesimpulannya adalah kita diminta untuk memberikan informasi terkait data frame tersebut yaitu berapa jumlah pengguna yang terdaftar perbulannya selama tahun 2012.')
st.pyplot(plt)

# Ubah kolom tanggal menjadi tipe data datetime
data['dteday'] = pd.to_datetime(data['dteday'])

# Filter data untuk bulan Februari tahun 2012
bulan_kedua = data[data['dteday'].dt.strftime('%Y-%m').str.startswith('2012-02')]

# Atur gaya plot menggunakan seaborn
sns.set(style="whitegrid")

# Buat plot menggunakan seaborn
plt.figure(figsize=(10, 6))
sns.lineplot(x='dteday', y='cnt', data=bulan_pertama, marker='o', color='purple')

# Judul dan label sumbu
plt.title('Grafik Data Bulan February 2012')
plt.xlabel('Tanggal')
plt.ylabel('Jumlah cnt')
plt.xticks(rotation=50)

with st.expander("Tampilan Grafik") :
        st.write('setelah di lihat dalam grafik dan persentase piechart, record terendah pada bulan Februari 2012 adalah: 1529 dengan persentase pie chart 1.5%, jatuh pada tanggal 2012-02-12')

# Tampilkan streamlit
st.pyplot(plt)

# Memfilter untuk data season 1 saja yang muncul
df_s1 = df[df['season'] == 1]

# Menghitung jumlah workingday pada data season 1
sum_wokrdays_s1 = df_s1['workingday'].sum()

# Menampilkan hasil data
st.write("Jumlah working day pada season 1 adalah %s" %  sum_wokrdays_s1)
