import streamlit as st
import pandas as pd
import os
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import seaborn as sns


# Mencari Modal Kerja
def Modal(aktiva, hutang):
    modal = aktiva - hutang
    return modal

#mencari Nilai Pasar Equitas
def NPE(harga, jumlah) :
    npe = harga * jumlah
    return npe

# Fungsi altman z-score
def Altman(modal,laba,ebit,npe,aset,liabil) :
    
    #Bobot variable
    x1 = 6.56
    x2 = 3.26
    x3 = 6.72
    x4 = 1.05
    
    score = x1*(modal/aset) + x2*(laba/aset) + x3*(ebit/aset) + x4*(npe/liabil)
    return score

def main():
    menu = option_menu(None, ["Home", "Visualisasi",  "Dataset", 'About'], 
        icons=['house', 'graph-up', "database", 'exclamation-circle'], 
        menu_icon="cast", default_index=0, orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "#fafafa"},
            "icon": {"color": "orange", "font-size": "25px"}, 
            "nav-link": {"font-size": "15px", "text-align": "left", "margin":"5px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "green"},
        }
    )
    
    if menu == "Home":
        st.title("Prediksi kebangkrutan")
        col1,col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Perusahaan")
            Aktiva = st.number_input("Aktiva lancar",format="%d",step=1)
            Hutang = st.number_input("Hutang Lancar",step=1)
            Laba_Ditahan = st.number_input("Laba Ditahan",step=1)
            Ebit = st.number_input("Penghasilan sebelum pajak",step=1)
        
        with col2:
            tahun = st.number_input("Laporan keuangan Tahun:",step=1)
            Harga_Saham = st.number_input("Harga Saham",step=1)
            Jumlah_Saham = st.number_input("Jumlah Sahan",step=1)
            Total_Aset = st.number_input("Total Aset",step=1)
            Total_Liabilities = st.number_input("Total Liabilitass",step=1)
            
        submit_button = st.button(label='Analisis')
        if submit_button : 
            
            #mencari score altman
            modal = Modal(Aktiva,Hutang)
            npe = NPE(Harga_Saham,Jumlah_Saham)
            score = Altman(modal,Laba_Ditahan,Ebit,npe,Total_Aset,Total_Liabilities)
            prediksi = ""
            if score > 2.59 : 
                prediksi = "tidak bangkrut"
                st.success(prediksi)
                st.success(f"score = {score:.2f}")
            elif score < 1.09 : 
                prediksi = "bangkrut"
                st.error(prediksi)
                st.error(f"score = {score:.2f}")
            else : 
                prediksi = "grey area"
                st.warning(prediksi)
                st.warning(f"score = {score:.2f}")
            
            #simpan ke dataset
            data = {'Nama_Perusahaan':[nama],'Tahun':[tahun],'Aktiva_Lancar':[Aktiva], 'Hutang_Lancar':[Hutang],'Modal_Kerja':[modal], 'Laba_Ditahan':[Laba_Ditahan],'Laba_Sebelum_Bunga_dan_Pajak':[Ebit],'Jumlah_Saham': [Jumlah_Saham], 'Harga_Saham': [Harga_Saham],'Nilai_Pasar_Ekuitas':[npe],'Total_Aset':[Total_Aset],'Total_Liabilitas':[Total_Liabilities],'Altman_Z_Score':[score],'Prediksi':[prediksi]}
            
            df_input = pd.DataFrame(data)
            
            #Import ke csv
            if os.path.exists('database/database.csv'):
                df_base = pd.read_csv('database/database.csv')
                df_base = pd.concat([df_base, df_input])
                # merged_df = pd.concat([df,df1])
                df_base.sort_values(by=['Nama_Perusahaan', 'Tahun'], ascending=[
                                    True, True]).to_csv('database/database.csv', index=False)
                # merged_df.sort_values(by='Tahun',ascending=False).to_csv('database/database.csv', index=False)
                
    elif menu == "Visualisasi" :
        st.header("Visual")
        df_visual = pd.read_csv('database/database.csv')
        
        selected_company= st.selectbox("Pilih Perusahaan",df_visual['Nama_Perusahaan'].unique())
        
        if selected_company : 
            company_data = df_visual[df_visual['Nama_Perusahaan'] == selected_company]
            plt.figure(figsize=(10, 6))
            sns.lineplot(data=company_data, x='Tahun', y='Altman_Z_Score', marker='o')
            plt.title(f'Altman Z-Score {selected_company} per Tahun')
            plt.xlabel('Tahun')
            plt.ylabel('Altman Z-Score')
            plt.grid(True)
            st.pyplot(plt)
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Grafik Aktiva berdasarkan Tahun
                plt.figure(figsize=(10, 6))
                sns.barplot(data=company_data, x='Tahun', y='Aktiva_Lancar')
                plt.title('Aktiva Lancar PT Akasha Wira Inter per Tahun')
                plt.xlabel('Tahun')
                plt.ylabel('Aktiva Lancar')
                plt.grid(axis='y')
                st.pyplot(plt)

                # Grafik Hutang berdasarkan Tahun
                plt.figure(figsize=(10, 6))
                sns.barplot(data=company_data, x='Tahun', y='Hutang_Lancar')
                plt.title('Hutang Lancar PT Akasha Wira Inter per Tahun')
                plt.xlabel('Tahun')
                plt.ylabel('Hutang Lancar')
                plt.grid(axis='y')
                st.pyplot(plt)

            with col2:
                # Grafik Total Aset berdasarkan Tahun
                plt.figure(figsize=(10, 6))
                sns.barplot(data=company_data, x='Tahun', y='Total_Aset')
                plt.title('Total Aset PT Akasha Wira Inter per Tahun')
                plt.xlabel('Tahun')
                plt.ylabel('Total Aset')
                plt.grid(axis='y')
                st.pyplot(plt)

                # Grafik Total Liabilitas berdasarkan Tahun
                plt.figure(figsize=(10, 6))
                sns.barplot(data=company_data, x='Tahun', y='Total_Liabilitas')
                plt.title('Total Liabilitas PT Akasha Wira Inter per Tahun')
                plt.xlabel('Tahun')
                plt.ylabel('Total Liabilitas')
                plt.grid(axis='y')
                st.pyplot(plt)
            
        

    elif menu == "Dataset" :
        st.header("Dataset")
        df_set = pd.read_csv('database/database.csv')
        df_set['Tahun'] = df_set['Tahun'].astype(str)
        df_set

    elif menu == "About" :
        _, col2, _ = st.columns(3)
        with col2:
            st.header("Tentang Web", )
            
        st.markdown("  Web prediksi kebangkrutan ini menggunakan metode Altman Z score, karena metode ini memiliki lebih banyak keuntungan daripada metode prediksi kebangkrutan lainnya yang telah menggabungkan beberapa rasio yang diperlukan untuk mengevaluasi likuiditas, profitabilitas, solvabilitas dan aktivitas. Selain itu, rasio Z-Score telah mencakup evaluasi internal dan eksternal perusahaan. Berikut adalah metode altman jika ditulis secara matematis : ")
        st.markdown("Z =  6,56X1  +  3,26X2  +  6,72X3  +  1,05X4")
        st.markdown("Altman menggunakan 5 rasio keuangan, yaitu variabel X1 (Modal Kerja/Total Aset), variable X2 (Laba Ditahan/Total Aset), variabel X3 (Laba Sebelum Pajak/Total Aset), variabel X4 (Nilai Pasar Ekuitas/Total Liabilitas)")
    
if __name__ == '__main__':
	main()
