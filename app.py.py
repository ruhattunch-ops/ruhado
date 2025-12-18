 import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Kan Takip Formu", layout="wide", page_icon="🩸")

st.markdown(
    """
    <h2 style='text-align: center; color: #b30000;'>🩸 YÜZÜNCÜ YIL ÜNİVERSİTESİ DAHİLİYE KAN TAKİP SİSTEMİ</h2>
    """, 
    unsafe_allow_html=True
)
st.markdown("---")

# --- OTURUM (SESSION) BAŞLATMA ---
# Sayfa yenilendiğinde verilerin kaybolmaması için Dataframe'leri hafızada tutuyoruz.
# Görseldeki sütun başlıklarını birebir tanımlıyoruz.

if 'data' not in st.session_state:
    st.session_state.data = {
        "Seroloji": pd.DataFrame(columns=["Tarih", "Parametre", "Değer"]),
        "Geniş_Kanlar": pd.DataFrame(columns=["Tarih", "Parametre", "Değer"]),
        "Hematoloji": pd.DataFrame(columns=["Tarih", "HGB", "HCT", "MCV", "WBC", "NEUT", "LENF", "PLT", "SEDIM", "PROK", "CRP"]),
        "Biyokimya_1": pd.DataFrame(columns=["Tarih", "ÜRE", "KRE", "GLUKOZ", "NA", "K", "CA", "FOSFOR", "MG", "AST", "ALT", "GGT", "ALP", "T BIL", "D BIL"]),
        "Biyokimya_2": pd.DataFrame(columns=["Tarih", "ALB", "GLO", "ÜRİK ASİT", "LDH", "CK", "CK-MB", "TROB", "AMİLAZ", "LİPAZ"]),
        "Koagulasyon": pd.DataFrame(columns=["Tarih", "INR", "PT", "APTT", "FİBRİNOJEN", "D-DİMER"]),
        "Kan_Gazi": pd.DataFrame(columns=["Tarih", "KG PH", "CO2", "ActHCO3", "StdHCO3", "LAC"]),
        "Idrar": pd.DataFrame(columns=["Tarih", "PH", "DANSİTE", "PROTEİN", "ERİT", "LÖK", "KETON", "GLU", "PCR", "ACR"])
    }

# --- HASTA BİLGİLERİ (ÜST KISIM) ---
with st.container():
    col1, col2, col3 = st.columns(3)
    ad_soyad = col1.text_input("HASTA ADI SOYADI", placeholder="Örn: BERAT SAMSUR")
    dosya_no = col2.text_input("DOSYA NO", placeholder="Örn: 403559")
    tarih_bugun = col3.date_input("FORM TARİHİ", datetime.now())

st.markdown("---")
st.info("💡 Tablolara veri girmek için hücrelere tıklayın. Yeni satır eklemek için tablonun altındaki '+' simgesini veya Enter tuşunu kullanın.")

# --- BÖLÜM 1: SEROLOJİ VE GENİŞ KANLAR (YAN YANA) ---
col_sol, col_sag = st.columns(2)

with col_sol:
    st.subheader("SEROLOJİ")
    # Kullanıcıya örnek parametreleri hatırlatmak için
    st.caption("Örn: HBSAG, ANTI-HBS, ANTI-HCV...")
    st.session_state.data["Seroloji"] = st.data_editor(
        st.session_state.data["Seroloji"], 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_seroloji"
    )

with col_sag:
    st.subheader("GENİŞ KANLAR")
    st.caption("Örn: HBA1C, B12, FOLAT, TSH, FERRİTİN...")
    st.session_state.data["Geniş_Kanlar"] = st.data_editor(
        st.session_state.data["Geniş_Kanlar"], 
        num_rows="dynamic", 
        use_container_width=True,
        key="editor_genis"
    )

st.markdown("---")

# --- BÖLÜM 2: HEMATOLOJİ ---
st.subheader("HEMATOLOJİ")
st.session_state.data["Hematoloji"] = st.data_editor(
    st.session_state.data["Hematoloji"], 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_hem"
)

# --- BÖLÜM 3: BİYOKİMYA 1 ---
st.subheader("BİYOKİMYA 1")
st.session_state.data["Biyokimya_1"] = st.data_editor(
    st.session_state.data["Biyokimya_1"], 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_bio1"
)

# --- BÖLÜM 4: BİYOKİMYA 2 ---
st.subheader("BİYOKİMYA 2")
st.session_state.data["Biyokimya_2"] = st.data_editor(
    st.session_state.data["Biyokimya_2"], 
    num_rows="dynamic", 
    use_container_width=True,
    key="editor_bio2"
)

st.markdown("---")

# --- BÖLÜM 5: ALT GRUPLAR (KOAGÜLASYON, KAN GAZI, İDRAR) ---
c1, c2 = st.columns(2)

with c1:
    st.subheader("KOAGÜLASYON")
    st.session_state.data["Koagulasyon"] = st.data_editor(
        st.session_state.data["Koagulasyon"], num_rows="dynamic", use_container_width=True, key="editor_koag"
    )

with c2:
    st.subheader("KAN GAZI")
    st.session_state.data["Kan_Gazi"] = st.data_editor(
        st.session_state.data["Kan_Gazi"], num_rows="dynamic", use_container_width=True, key="editor_kg"
    )

st.subheader("İDRAR")
st.session_state.data["Idrar"] = st.data_editor(
    st.session_state.data["Idrar"], num_rows="dynamic", use_container_width=True, key="editor_idrar"
)

# --- EXCEL İNDİRME İŞLEMİ ---
st.markdown("---")
st.header("💾 Kayıt ve Çıktı")

dosya_adi = f"{ad_soyad if ad_soyad else 'Hasta'}_{dosya_no if dosya_no else 'No'}_KanTakip.xlsx"

# Excel oluşturma butonu
buffer = BytesIO()
if st.button("📥 FORM EXCEL OLARAK İNDİR", type="primary"):
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        # Her kategoriyi ayrı bir sayfaya (Sheet) yazıyoruz ki karışmasın
        st.session_state.data["Seroloji"].to_excel(writer, sheet_name='Seroloji', index=False)
        st.session_state.data["Geniş_Kanlar"].to_excel(writer, sheet_name='Geniş Kanlar', index=False)
        st.session_state.data["Hematoloji"].to_excel(writer, sheet_name='Hematoloji', index=False)
        st.session_state.data["Biyokimya_1"].to_excel(writer, sheet_name='Biyokimya 1', index=False)
        st.session_state.data["Biyokimya_2"].to_excel(writer, sheet_name='Biyokimya 2', index=False)
        st.session_state.data["Koagulasyon"].to_excel(writer, sheet_name='Koagülasyon', index=False)
        st.session_state.data["Kan_Gazi"].to_excel(writer, sheet_name='Kan Gazı', index=False)
        st.session_state.data["Idrar"].to_excel(writer, sheet_name='İdrar', index=False)
        
    st.download_button(
        label="Dosyayı İndir",
        data=buffer.getvalue(),
        file_name=dosya_adi,
        mime="application/vnd.ms-excel"
    )
    st.success("Excel dosyası hazırlandı! Butona basarak indirebilirsiniz.")
