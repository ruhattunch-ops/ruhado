import streamlit as st
import pandas as pd
from io import BytesIO

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Nefroloji Asistanı Web", page_icon="🩺", layout="wide")

st.title("🩺 Nefroloji Klinik Asistanı (Web)")
st.markdown("---")

# --- OTURUM (SESSION) DURUMU ---
# Web sayfasında verilerin kaybolmaması için hafızada tutuyoruz
if 'hasta_listesi' not in st.session_state:
    st.session_state.hasta_listesi = []

# --- YAN MENÜ ---
with st.sidebar:
    st.header("Hasta Girişi")
    dosya_no = st.text_input("Protokol / Dosya No")
    # İşlem bittiğinde listeyi temizleme butonu
    if st.button("Listeyi Temizle / Yeni Gün"):
        st.session_state.hasta_listesi = []
        st.success("Liste temizlendi.")

# --- SEKMELER ---
tab1, tab2, tab3 = st.tabs(["🩸 Hematüri", "💓 Tansiyon & Dipping", "📏 Hacim (TKV)"])

# Değişkenler (Hata önleyici)
hem_sonuc = "-"
dip_yuzde = 0
dip_kat = "-"
map_val = 0
ht_tkv = 0

with tab1:
    st.subheader("Hematüri Analiz")
    c1, c2 = st.columns(2)
    epitel = c1.selectbox("Yassı Epitel", ["Seçiniz", "Bol Miktarda (Bulaş)", "Yok / Nadir"])
    eritrosit = c2.selectbox("Eritrosit", ["Seçiniz", "Var", "Yok"])
    
    if epitel == "Bol Miktarda (Bulaş)":
        st.error("🚫 Kontamine (Bulaş)")
        hem_sonuc = "Kontamine"
    elif epitel == "Yok / Nadir" and eritrosit == "Var":
        st.success("✅ Gerçek Hematüri")
        hem_sonuc = "Pozitif"
    elif eritrosit == "Yok":
        st.info("Negatif")
        hem_sonuc = "Negatif"

with tab2:
    st.subheader("Tansiyon Analiz")
    tc1, tc2, tc3, tc4 = st.columns(4)
    g_sys = tc1.number_input("Gündüz Sys", 0)
    g_dia = tc2.number_input("Gündüz Dia", 0)
    n_sys = tc3.number_input("Gece Sys", 0)
    n_dia = tc4.number_input("Gece Dia", 0)
    
    if g_sys > 0 and n_sys > 0:
        dip_yuzde = ((g_sys - n_sys) / g_sys) * 100
        map_val = (g_sys + (2*g_dia))/3
        
        if dip_yuzde < 0: dip_kat = "Reverse Dipper"
        elif dip_yuzde < 10: dip_kat = "Non-Dipper"
        else: dip_kat = "Dipper"
        st.info(f"Dipping: %{dip_yuzde:.1f} ({dip_kat})")

with tab3:
    st.subheader("Hacim Hesapla")
    vc1, vc2 = st.columns(2)
    tkv = vc1.number_input("TKV (ml)", 0)
    boy = vc2.number_input("Boy (cm)", 0)
    
    if boy > 0:
        ht_tkv = tkv / (boy/100)
        st.info(f"ht-TKV: {ht_tkv:.0f} ml/m")

# --- LİSTEYE EKLEME ---
st.markdown("---")
if st.button("➕ Bu Hastayı Listeye Ekle", type="primary"):
    if not dosya_no:
        st.warning("Dosya No giriniz!")
    else:
        yeni_kayit = {
            "Dosya_No": dosya_no,
            "Hematuri": hem_sonuc,
            "Dipping_Yuzde": round(dip_yuzde, 1),
            "Dipping_Kat": dip_kat,
            "MAP": round(map_val, 1),
            "ht_TKV": round(ht_tkv, 0)
        }
        st.session_state.hasta_listesi.append(yeni_kayit)
        st.success(f"{dosya_no} listeye eklendi.")

# --- LİSTEYİ GÖSTER VE İNDİR ---
if len(st.session_state.hasta_listesi) > 0:
    st.subheader("📋 Güncel Hasta Listesi")
    df = pd.DataFrame(st.session_state.hasta_listesi)
    st.dataframe(df)
    
    # Excel İndirme İşlemi (Bellekten)
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Veriler')
        
    st.download_button(
        label="📥 Listeyi Excel Olarak İndir",
        data=buffer.getvalue(),
        file_name="nefroloji_verileri.xlsx",
        mime="application/vnd.ms-excel"
    )