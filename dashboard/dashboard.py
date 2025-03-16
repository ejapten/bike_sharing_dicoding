import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import os


# Untuk Header
def show_header():
    st.markdown(
        "<h1 style='text-align: center; font-size: 40px;'>Dashboard Analisis Penyewaan Sepeda 🚲</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<h2 style='text-align: center; font-size: 24px;'>Eksplorasi Pola dalam Penyewaan Sepeda</h2>",
        unsafe_allow_html=True,
    )


show_header()
st.markdown("---")
st.markdown("---")

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
bike_day_path = os.path.join(data_dir, "bike_day_clean.csv")
bike_hour_path = os.path.join(data_dir, "bike_hour_clean.csv")


bike_day = pd.read_csv(bike_day_path)
bike_hour = pd.read_csv(bike_hour_path)

# Fungsi untuk Insight


# 1. Menampilkan Seluruh Total penyewa
def total_penyewa_day(bike_day):
    casual_rental = bike_day["casual"].sum()
    registered_rental = bike_day["registered"].sum()
    total_rental = bike_day["cnt"].sum()

    return {
        "casual": casual_rental,
        "registered": registered_rental,
        "total": total_rental,
    }


# 2. Menampilkan total penyewa terhadap bulan


def penyewaan_per_bulan(bike_day):

    # Pastikan urutan bulan yang benar
    urutan_bulan = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    # Ubah kolom 'mnth' menjadi kategori dengan urutan yang benar
    bike_day["mnth"] = pd.Categorical(
        bike_day["mnth"], categories=urutan_bulan, ordered=True
    )

    # Grouping berdasarkan bulan
    hasil_bulan = bike_day.groupby("mnth", as_index=False)["cnt"].sum()

    return hasil_bulan


# 3. Fungsi pada seluruh musim
def penyewaan_per_musim(bike_day):
    return bike_day.groupby("season", as_index=False)["cnt"].sum()


# 4. Fungsi pada jumlah pengunjung berdasarkan hari libur
def penyewaan_per_holiday(bike_day):
    return bike_day.groupby("holiday", as_index=False)["cnt"].sum()


# 5. Fungsi pada Jumlah pengunjung berdasarkan hari
def penyewaan_per_hari(bike_hour):
    hasil_hari = (
        bike_hour.groupby("weekday", as_index=False)["cnt"]
        .sum()
        .rename(columns={"cnt": "total_penyewa"})
        .sort_values("total_penyewa", ascending=False)
    )
    return hasil_hari


# 6. Fungsi Jumlah pengunjung berdasarkan kategori waktu
def penyewaan_per_kategori_waktu(bike_hour):
    hasil_kategori_waktu = (
        bike_hour.groupby("time_category", as_index=False)["cnt"]
        .sum()
        .rename(columns={"cnt": "total_penyewa"})
        .sort_values("total_penyewa", ascending=False)
    )
    return hasil_kategori_waktu


# ----------------------Visualisasi Data----------------------#
# 1. Menampilkan Seluruh Total penyewa
st.subheader("Total Penyewaan Sepedah ")

penyewa_day = total_penyewa_day(bike_day)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Penyewa yang Tidak Terdaftar", value=penyewa_day["casual"])

with col2:
    st.metric("Total Penyewa yang Terdaftar", value=penyewa_day["registered"])

with col3:
    st.metric("Total Seluruh Penyewa", value=penyewa_day["total"])

# Buat data untuk visualisasi
casual = penyewa_day["casual"]
registered = penyewa_day["registered"]
total = penyewa_day["total"]

kategori = ["Tidak Terdaftar", "Terdaftar", "Total Penyewa"]
jumlah_penyewaan = [casual, registered, total]
# grafik
fig, ax = plt.subplots(figsize=(6, 4))
ax.plot()
ax.bar(kategori, jumlah_penyewaan, color=["red", "blue", "green"])
ax.set_title("Jumlah Penyewaan Sepeda (2011-2012)")
ax.set_xlabel("Kategori Penyewa")
ax.set_ylabel("Jumlah Penyewaan")
ax.grid(axis="y")
st.pyplot(fig)

st.info(
    "Jumlah penyewa sepeda yang sudah mendaftar jauh lebih banyak daripada yang belum mendaftar sebagai member. Jumlah penyewa pada 2011 adalah 1233103 dan pada 2012 adalah 2049676. Hal tersebut mengalami kenaikan dalam kurun 1 tahun"
)

st.markdown("---")

# 2. Visualisasi total bulanan
hasil_bulan = penyewaan_per_bulan(bike_day)
st.subheader("Penyewaan Sepeda per Bulan")


# bentuk visualisasi data dalam line chart
def visualisasi_penyewaan(hasil_bulan):
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.lineplot(
        data=hasil_bulan,
        x="mnth",
        y="cnt",
        marker="o",
        linewidth=2,
        color="g",
        ax=ax,
    )
    ax.set_title("Penyewaan Sepeda per Bulan 2011-2012")
    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


visualisasi_penyewaan(hasil_bulan)

st.info(
    "Secara keseluruhan total penyewaan sepeda mengalami kenaikan dimulai dari bulan februari hingga september. Namun pada bulan october hingga januari mengalami penurunan. Puncak peningkatan penyewaan sepeda pada bulan juni hingga September."
)

st.markdown("---")

# 3. Visualisasi terhadapp musim
hasil_musim = penyewaan_per_musim(bike_day)
st.subheader("Penyewaan Sepeda per Musim")


# Fungsi untuk menampilkan bar chart
def visualisasi_penyewaan_musim(hasil_musim):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=hasil_musim,
        x="season",
        y="cnt",
        palette=["orange", "green", "yellow", "blue"],
    )
    ax.set_xlabel("Musim")
    ax.set_ylabel("Total Penyewa")
    ax.set_title("Penyewaan Sepeda per Musim")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)


visualisasi_penyewaan_musim(hasil_musim)
st.info(
    "Secara keseluruhan total penyewaan sepeda berdasarkan musim mengalami kenaikan pada musim Summer dan Fall. Pada musim Winter jumlah total penyewa cukup banyak dibandingkan pada musim spring."
)

st.markdown("---")
st.info("Hubungan antara penyewaan pada bulan dan musim")
col1, col2 = st.columns(2)

with col1:
    st.info(
        "Pada musim Summer dan Fall terjadi kenaikan, hal itu berkorelasi positif dengan bulan Juni hingga October, mengingat dibulan tersebut terjadi peningkatan, Lalu musim summer dan Fall juga terjadi sepanjang bulan Juni hingga November"
    )

with col2:
    st.info(
        "Pada musim Spring total penyewa jauh lebih sedikit dibandingkan musim lainnya. Hal itu cukup berkorelasi baik natara bulan Februari hingga April. Walaupun dibulan itu terjadi peningkatan, namun tidak dalam puncaknya dan masih rendah diantara bulan laiinnya. Oleh karena itu, karena spring terjadi maret-mei, total penyewaan pada bulan februari hingga april saling mempengaruhia."
    )

st.markdown("---")

# 4. Visualisasi data total penyewaan berdasarkan holiday
hasil_holiday = penyewaan_per_holiday(bike_day)
st.subheader("Penyewaan Sepeda per Holiday")


def visualisasi_penyewaan_holiday(hasil_holiday):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(
        data=hasil_holiday,
        x="holiday",
        y="cnt",
        palette=["orange", "green"],
    )
    ax.set_xlabel("Holiday or Not")
    ax.set_ylabel("Total Penyewa")
    ax.set_title("Penyewaan Sepeda per Holiday")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()
    st.pyplot(fig)


visualisasi_penyewaan_holiday(hasil_holiday)

st.info(
    "Penyewaan sepeda sering dilakukan pada not holiday atau bukan hari liburan melainkan hari kerja"
)

st.markdown("---")

# 5. Visualisasi jumlah penyewa berdasarkan hari
hasil_hari = penyewaan_per_hari(bike_hour)
st.subheader("Jumlah Penyewa Sepeda Berdasarkan Hari")


def visualisasi_penyewaan_hari(hasil_hari):
    fig, ax = plt.subplots(figsize=(8, 5))
    warna = ["skyblue", "red", "lightgreen", "yellow", "green", "gray", "black"]
    sns.barplot(data=hasil_hari, x="weekday", y="total_penyewa", palette=warna, ax=ax)
    ax.set_xlabel("Hari")
    ax.set_ylabel("Jumlah Penyewa")
    ax.set_title("Penyewaan Sepeda per Hari")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)


visualisasi_penyewaan_hari(hasil_hari)

st.info(
    "Hari yang paling sering dilakukan penyewaan sepeda adalah (urutan tertinggi sampai terendah) Jumat, Kamis, Sabtu, Jumat, Selasa, Senin, Minggu. Hasil diatas sesuai degan analisis sebelumnya bahwa hari kerja atau bukan liburan merupakan hari yang paling banyak dilakukan penyewaan."
)

st.markdown("---")

# 6.  Visualisasi kategori waktu
hasil_kategori_waktu = penyewaan_per_kategori_waktu(bike_hour)
st.subheader("Jumlah Penyewa Berdasarkan kategori waktu")


def visualisasi_penyewaan_kategori_waktu(hasil_kategori_waktu):
    fig, ax = plt.subplots(figsize=(8, 5))

    # Plot Bar Chart
    sns.barplot(
        x="time_category",
        y="total_penyewa",
        data=hasil_kategori_waktu,
        palette="pastel",
        ax=ax,
    )

    ax.set_title("Distribusi Penyewaan Sepeda Berdasarkan Kategori Waktu")
    ax.set_xlabel("Kategori Waktu")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)


visualisasi_penyewaan_kategori_waktu(hasil_kategori_waktu)

st.info(
    "Analisis selanjutnya dilakukan pengkategorian waktu yaitu berdasarkan (0-11) AM dan (12-23) PM. Dari hasil analisis tersebut bahwa kategori waktu PM paling banyak dilakukan penyewaan sepeda."
)

# 7. Visualisasi berdasarkan Cuaca
bike_day["dteday"] = pd.to_datetime(bike_day["dteday"])


def visualisasi_tren_penyewaan(bike_day):
    fig, ax = plt.subplots(figsize=(30, 6))
    sns.lineplot(
        data=bike_day, x="dteday", y="cnt", hue="weathersit", palette="tab10", ax=ax
    )

    ax.set_title("Tren Penyewaan Sepeda Berdasarkan Cuaca")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Total Penyewaan")
    ax.set_xlim([bike_day["dteday"].min(), bike_day["dteday"].max()])
    ax.xaxis.set_major_locator(
        mdates.MonthLocator(interval=2)
    )  # Menampilkan label setiap 2 bulan
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
    plt.xticks(rotation=45)
    plt.grid(True)
    ax.legend(title="Weather Situation", loc="upper center", bbox_to_anchor=(0.5, -0.2))
    st.pyplot(fig)


st.subheader("Tren Penyewaan Sepeda Berdasarkan Cuaca")
visualisasi_tren_penyewaan(bike_day)

col1, col2, col3 = st.columns(3)

with col1:
    st.info(
        "Orang-orang sering melakukan penyewaan pada cuaca cerah, berawan ringan, cuaca berawan, dan berkabut orang orang jarang sekali melakukan penyewaan sepada pada saat hujan atau salju"
    )

with col2:
    st.info(
        "Dari hasil analisis diatas, cuaca cerah dan berawan ringan biasanya terjadi mada musim Summer atau Fall, mengingat analisis sebelumnya musim summer dan fall merupakan musim dengan paling banyak dilakukan penyewaan."
    )


with col3:
    st.info(
        "Lalu pada cuaca berawan dan berkabut sering terjadi pada musim fall atau spring. Musim fall paling banyak dilakukan penyewaan, sedangkan musim spring jauh lebih sedikit dibandingkan musim lainnya. walaupun begitu, orang-orang masih tetap banyak melakukan penyewaan di cuaca berawan dan berkabut"
    )
st.markdown("---")

# 8. Visualisasi tanggal
bike_day_copy = bike_day.copy()
bike_day_copy.rename(
    columns={
        "dteday": "Tanggal",
        "season": "musim",
        "yr": "Tahun",
        "mnth": "Bulan",
        "weekday": "Hari",
        "weathersit": "cuaca",
        "casual": "Penyewa tidak Terdaftar",
        "registered": "Penyewa Terdaftar",
        "cnt": "Total Penyewa",
    },
    inplace=True,
)
bike_day_copy.drop(columns=["season_holiday"], inplace=True, errors="ignore")

min_date = bike_day_copy["Tanggal"].min()
max_date = bike_day_copy["Tanggal"].max()

st.sidebar.markdown(
    "**Silakan pilih rentang tanggal untuk mengetahui data penyewaan sepeda secara lengkap. Hasil secara otomatis, namun jika tidak  scroll ke bawah untuk melihat hasilnya**"
)

with st.sidebar:
    image_path = (
        r"C:\Pengwining\Proyek analisis data\proyek_analisis_data\data\sepeda3.jpg"
    )
    st.image(image_path, caption="Penyewaan sepeda", use_container_width=True)
    start_date = st.sidebar.date_input("Start Date", min_date)
    end_date = st.sidebar.date_input("End Date", max_date)


# Filter dataset berdasarkan rentang tanggal
filter_data = bike_day_copy[
    (bike_day_copy["Tanggal"] >= pd.Timestamp(start_date))
    & (bike_day_copy["Tanggal"] <= pd.Timestamp(end_date))
]

# Membuat visualisasi dengan Plotly
fig = px.line(
    filter_data,
    x="Tanggal",
    y="Total Penyewa",
    title="Jumlah Penyewa per Hari (2011-2012)",
    labels={"Tanggal": "Tanggal", "Total Penyewa": "Jumlah Pengunjung"},
    template="plotly_white",
)

# Menampilkan hasil di Streamlit
st.title("Analisis Jumlah Pengunjung")
st.plotly_chart(fig)
st.dataframe(filter_data)
