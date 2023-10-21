import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# load data
main_data_df = pd.read_csv("https://raw.githubusercontent.com/RikoYan/ds-p/main/main_data.csv")

# membuat fungsi total pengguna harian
def create_total_pengguna_df(df):
    total_pengguna_df = df.resample(rule='D', on='dteday').agg({
        "cnt" : "sum"
    })
    total_pengguna_df = total_pengguna_df.reset_index()
    total_pengguna_df.rename(columns={
        "cnt": "total"
    }, inplace=True)

    return total_pengguna_df


datetime_columns = ["dteday"]
main_data_df.sort_values(by="dteday", inplace=True)
main_data_df.reset_index(inplace=True)

for column in datetime_columns:
    main_data_df[column] = pd.to_datetime(main_data_df[column])

min_date = main_data_df["dteday"].min()
max_date = main_data_df["dteday"].max()

# tampilan sidebar
with st.sidebar:
    # Menambahkan logo
    st.image("https://github.com/RikoYan/ds-p/blob/main/vecteezy_bike-bicycle-line-icon-vector-illustration-logo_.jpg?raw=true")

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date, 
        max_value=max_date, 
        value=[min_date, max_date]
    )

main_df = main_data_df[(main_data_df["dteday"] >= str(start_date)) &
                       (main_data_df["dteday"] <= str(end_date))]

# Membuat dataframe baru dan grouping untuk visualisasi
total_pengguna_df = create_total_pengguna_df(main_df)

only_2011_df = main_data_df[(main_data_df['dteday'] > "2011-01-01") & (main_data_df['dteday'] < "2011-12-31")]
only_2012_df = main_data_df[(main_data_df['dteday'] > "2012-01-01") & (main_data_df['dteday'] < "2012-12-31")]
 
season_11_sum_df = only_2011_df.groupby(by='nameseason').agg({
    'season':"unique",
    'cnt':"sum"
})
season_11_sum_df = season_11_sum_df.reset_index() #revisi

season_12_sum_df = only_2012_df.groupby(by='nameseason').agg({
    'season':"unique",
    'cnt':"sum"
})
season_12_sum_df = season_12_sum_df.reset_index() #revisi

hw_mean_df = main_data_df.groupby(['weekdesc']).agg({
    'casual':"mean",
    'registered':"mean"
})
hw_mean_df = hw_mean_df.reset_index() #revisi


# grafik total pengguna harian
st.header('Bike-Sharing rental :bike:')
st.subheader('Total Pengguna Harian')

fig, ax = plt.subplots(figsize=(16,8))
ax.plot(
    total_pengguna_df["dteday"],
    total_pengguna_df["total"],
    marker='o',
    linewidth=2,
    color="#40E0D0"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)

# grafik season
st.subheader("jumlah pengguna keseluruhan berdasarkan season tahun 2011 dan 2012")

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#B2BEB5", "#B2BEB5", "#40E0D0", "#B2BEB5"]
 
sns.barplot(x="nameseason", y="cnt", data=season_11_sum_df.sort_values(by="season", ascending=True), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("tahun 2011", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(x="nameseason", y="cnt", data=season_12_sum_df.sort_values(by="season", ascending=True), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("tahun 2012", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)
 
st.pyplot(fig)


with st.expander("Penjelasan"):
    st.write(
        """karena jumlah pengguna casual tiap tahun dan jumlah pengguna registered tiap tahun cenderung sama
        agar lebih ringkas dalam visualisasi data maka dapat diwakilkan dengan total jumlah pengguna tiap season
        per tahun. dapat di simpulkan bahwa terdapat kenaikan signifikan dari season springer ke season summer dan
        puncaknya di season fall kemudian jumlah pengguna turun di season winter dan pengguna paling sedikit di 
        season springer atau awal tahun."""
    )

# grafik weekend, workingday, dan holiday.
st.subheader("Perbandingan rata-rata pengguna terhadap weekend, working day, dan holiday")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))

    colors = ["#40E0D0", "#B2BEB5", "#B2BEB5"]
 
    sns.barplot(
        y="casual", 
        x="weekdesc",
        data=hw_mean_df.sort_values(by="casual", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("pengguna casual", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="registered", 
        x="weekdesc",
        data=hw_mean_df.sort_values(by="registered", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("pengguna registered", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

