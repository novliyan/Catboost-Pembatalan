import pickle
import requests
import streamlit as st
from streamlit_lottie import st_lottie


# --- LOAD ASSETS ---
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_5h2kp8uz.json")
lottie_batal = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_vCEhKC.json")
lottie_sukses = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_uoW3t715hk.json")


# membaca model
pembatalan_model = pickle.load(open('pembatalan_model.sav', 'rb'))



# ---- Header ----

st_lottie(lottie_coding, height=300, key= "coding")

st.markdown(
    f"<h1 style='text-align: center;'>Prediksi Pembatalan Transaksi</h1>",
    unsafe_allow_html=True
)

# Membagi kolom
col1, col2 = st.columns(2)

with col1:
    # Pilihan input untuk Product_Category
    Product_Category_options = ['Gamis', 'Dresses', 'Mukena', 'Clothing Sets', 'Skirts', 'Shirts & Blouses', 'Casual Dresses']
    Product_Category_input = st.selectbox('Input Kategori Produk', Product_Category_options)
    # Konversi nilai Product_Category menjadi bilangan integer
    Product_Category_mapping = {'Gamis': 1, 'Dresses': 2, 'Mukena': 3, 'Clothing Sets': 4, 'Skirts': 5, 'Shirts & Blouses': 6, 'Casual Dresses': 7}
    Product_Category = Product_Category_mapping.get(Product_Category_input)
    
with col2:
    Variation_options = ['mustard, L', 'dusty purple, XL', 'salem', 'ungu terong', 'emerald, 40', 'silver, 44', 'silver, 42', 'mocca, 44', 'taro, 44', 'mustard, 44', 'emerald, 42']
    Variation_input = st.selectbox('Input Variasi Produk', Variation_options)

    Variation_mapping = {'mustard, L': 40, 'dusty purple, XL': 2, 'salem': 3, 'ungu terong': 4, 'emerald, 40': 5, 'silver, 44': 6, 'silver, 42':7 , 'mocca, 44': 8, 'taro, 44': 9, 'mustard, 44': 10, 'emerald, 42': 11}
    Variation = Variation_mapping.get(Variation_input)

with col1:
    province_options = ['Jawa Timur', 'Jawa Barat', 'Banten', 'Jawa Tengah', 'Kalimantan Timur', 'Sumatera Utara', 'DKI Jakarta']
    province_input = st.selectbox('Input Provinsi', province_options)

    province_mapping = {'Jawa Timur': 7, 'Jawa Barat': 2, 'Banten': 3, 'Jawa Tengah':5, 'Kalimantan Timur': 6, 'Sumatera Utara':1, 'DKI Jakarta': 4}
    Province = province_mapping.get(province_input)

with col2:
    Regency_and_City_options = ['Banyuwangi', 'Bekasi', 'Kabupaten Tangerang', 'Kabupaten Sidoarjo', 'Karawang', 'Kota Tangerang Selatan', 'Kabupaten Bogor', 'Kota Semarang', 'Kota Surabaya']
    Regency_and_City_input = st.selectbox('Input Kabupaten dan Kota', Regency_and_City_options)

    Regency_and_City_mapping = {'Banyuwangi': 366, 'Bekasi': 2, 'Kabupaten Tangerang': 3, 'Kabupaten Sidoarjo': 4, 'Karawang': 5, 'Kota Tangerang Selatan': 6, 'Kabupaten Bogor': 7, 'Kota Semarang': 7, 'Kota Surabaya': 9}
    Regency_and_City = Regency_and_City_mapping.get(Regency_and_City_input)
    
with col1:
    Payment_Method_options = ['Cash on delivery', 'DANA', 'GoPay', 'Bank Transfer', 'Akulaku', 'Cash', 'OVO', 'CCDC', 'ShopeePay']
    Payment_Method_input = st.selectbox('Input Metode Pembayaran', Payment_Method_options)

    Payment_Method_mapping = {'Cash on delivery': 1, 'DANA': 2, 'GoPay': 3, 'Bank Transfer': 4, 'Akulaku': 5, 'Cash': 6, 'OVO': 7, 'CCDC': 8, 'ShopeePay': 9}
    Payment_Method = Payment_Method_mapping.get(Payment_Method_input)

with col2:
    month_options = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni', 'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
    month_input = st.selectbox('Input Bulan', month_options)

    month_mapping = {'Januari':1, 'Februari':2, 'Maret':3, 'April':4, 'Mei':5, 'Juni':6, 'Juli':7, 'Agustus':8, 'September':9, 'Oktober':10, 'November':11, 'Desember':12}
    month = month_mapping.get(month_input)

with col1:
    Order_Refund_Amount = st.text_input ('Input Order Refund Amount')

with col2:
    SKU_Platform_Discount = st.text_input ('Input SKU Platform Discount')

with col1:
    Shipping_Fee_After_Discount = st.text_input ('Input Shipping Fee After Discount')

# code untuk prediksi
pemb_prediksi = ''

# membuat tombol untuk prediksi
if st. button('Test Prediksi Pembatalan'):
    pemb_prediction = pembatalan_model.predict([[SKU_Platform_Discount, Variation, Province, Regency_and_City, Payment_Method, Product_Category, Order_Refund_Amount, month, Shipping_Fee_After_Discount]])
    
    if (pemb_prediction[0] == 0):
        pemb_prediction = 'Produk tidak dibatalkan'
        st_lottie(lottie_sukses, height=300, key= "Sukses")
    else :
        pemb_prediction = 'Produk dibatalkan'
        st_lottie(lottie_batal, height=300, key= "Batal")
    
    st.success(pemb_prediction)


