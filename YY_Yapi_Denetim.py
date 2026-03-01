import streamlit as st
import pandas as pd
from datetime import datetime
from PIL import Image

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="YY YAPI DENETİM PRO-SAHA", layout="wide")

# --- KURUMSAL STİL (CSS) ---
st.markdown("""
    <style>
    .main-title { color: #1a237e; text-align: center; font-weight: bold; border-bottom: 3px solid #1a237e; padding-bottom: 10px; }
    .statik-box { background-color: #e3f2fd; padding: 20px; border-radius: 10px; border-left: 8px solid #2196f3; margin: 10px 0; }
    .mimari-box { background-color: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 8px solid #4caf50; margin: 10px 0; }
    .mekanik-box { background-color: #fffde7; padding: 20px; border-radius: 10px; border-left: 8px solid #fbc02d; margin: 10px 0; }
    .elektrik-box { background-color: #ffebee; padding: 20px; border-radius: 10px; border-left: 8px solid #f44336; margin: 10px 0; }
    .common-box { background-color: #f3e5f5; padding: 15px; border-radius: 10px; border-left: 8px solid #9c27b0; margin: 10px 0; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGO VE BAŞLIK ---
try:
    img = Image.open('YY YAPI.jpg')
    st.image(img, use_container_width=True)
except:
    st.markdown("<h1 class='main-title'>🏢 YY YAPI DENETİM LİMİTED ŞİRKETİ</h1>", unsafe_allow_html=True)

# --- YAN MENÜ (PROJE KÜNYESİ) ---
st.sidebar.header("📋 PROJE YÖNETİMİ")
proje_adi = st.sidebar.text_input("Proje Adı / Ada-Parsel", "Örn: 101 Ada 5 Parsel")
denetci = st.sidebar.text_input("Denetleyen Mühendis")
bolum_secimi = st.sidebar.selectbox("Denetim Bölümü Seçin", [
    "1. Bölüm: Radye Temel & Hazırlık",
    "2. Bölüm: Bodrum Kat (Kolon/Perde)",
    "3. Bölüm: Bodrum Kat Kiriş-Tabliye",
    "4. Bölüm: Normal Katlar",
    "5. Bölüm: Çatı & Asansör Makine Dairesi"
])

rapor_verisi = []

# --- ORTAK KONTROL MADDESİ ---
st.markdown(f'<div class="common-box">⚠️ KRİTİK KONTROL: Mevcut kat yüksekliği ve kot doğrulaması yapıldı mı?</div>', unsafe_allow_html=True)
ortak_onay = st.checkbox("Kat yüksekliği Statik/Mimari proje ile birebir tutuyor.", key="common_height")

# --- BÖLÜMLER VE KRİTERLER ---

def kriter_arayuzu(baslik, kriter_listesi, renk_sinifi, disiplin_adi):
    st.markdown(f'<div class="{renk_sinifi}"><h3>{baslik}</h3></div>', unsafe_allow_html=True)
    for i, kriter in enumerate(kriter_listesi):
        c1, c2 = st.columns([0.7, 0.3])
        res = c1.checkbox(kriter, key=f"{disiplin_adi}_{i}")
        not_alani = c2.text_input("Not", key=f"not_{disiplin_adi}_{i}")
        if res:
            rapor_verisi.append({"Bölüm": bolum_secimi, "Disiplin": disiplin_adi, "Kriter": kriter, "Durum": "Uygun", "Açıklama": not_alani})

# --- BÖLÜM 1: RADYE TEMEL ---
if "1. Bölüm" in bolum_secimi:
    kriter_arayuzu("🔵 STATİK KONTROLLER", [
        "Radye temel alt-üst donatı sayıları ve çapları (Φ) doğru mu?",
        "Bindirme mesafeleri (projede yoksa manuel) ölçüldü mü?",
        "Alt-üst ilave donatı sayıları ve yönleri doğru mu?",
        "X ve Y doğrultusundaki filiz sayıları ve konumları doğru mu?",
        "ideCAD/Prota/sta4CAD: Temel içi çiroz ve etriye detayları atıldı mı?"
    ], "statik-box", "Statik")
    
    kriter_arayuzu("🟢 MİMARİ & HAZIRLIK", [
        "İŞYERİ TESLİMİ yapıldı mı? Zemin kayalık değilse BLOKAJ serildi mi?",
        "Statik ve Mimari proje yalıtım detayları (bohçalama) uyumlu mu?",
        "Temel alt kotları doğrulanmış mı?"
    ], "mimari-box", "Mimari")

# --- BÖLÜM 2: BODRUM KAT (KOLON/PERDE) ---
elif "2. Bölüm" in bolum_secimi:
    kriter_arayuzu("🔵 STATİK KONTROLLER", [
        "Kolon orta bölgesi filiz bindirme boyları ve ÇİFT BAĞ kontrol edildi mi?",
        "Bodrum kat filiz boyları manuel ölçüldü mü?",
        "Çirozların 90° tarafı bağ teli ile bağlandı mı?",
        "Etriye kanca boyları ve 135° büküm açıları uygun mu?",
        "Yavru etriye ölçüleri ve bağlandıkları filizlerin konumu doğru mu?"
    ], "statik-box", "Statik")

# --- BÖLÜM 3: BODRUM KAT KİRİŞ-TABLİYE ---
elif "3. Bölüm" in bolum_secimi:
    kriter_arayuzu("🔵 STATİK & DÖKÜM", [
        "Kiriş ebatları ve etriye çap/uzunlukları projeye uygun mu?",
        "İlave donatı boyları ve gönyeleri doğru mu?",
        "Beton dökümü EN DERİN KİRİŞ KOTUNA göre ayarlandı mı?"
    ], "statik-box", "Statik")
    
    kriter_arayuzu("🟢 MİMARİ & KOT", [
        "Merdiven basamak sayısı ve İLK BASAMAK başlangıç noktası doğru mu?",
        "Bina girişleri ve otopark döşeme kotları METRE ATILARAK doğrulandı mı?"
    ], "mimari-box", "Mimari")

# --- BÖLÜM 4: NORMAL KATLAR ---
elif "4. Bölüm" in bolum_secimi:
    st.sidebar.number_input("Kat No", min_value=1, step=1)
    kriter_arayuzu("🔵 STATİK KONTROLLER", [
        "Kesit küçülmelerinde donatı düzeni üst kata göre ayarlandı mı?",
        "Alt ve üst kat filizleri 'yapışık/birlikte çalışır' bağlandı mı?",
        "Perde etriyeleri filizlerin içinden mi/dışından mı geçiyor?",
        "Kolon dipleri temizlendi, şakül ve gönye kontrolü yapıldı mı?"
    ], "statik-box", "Statik")
    
    kriter_arayuzu("🟢 MİMARİ & KONSOL", [
        "Balkon, Fransız balkon ve motif çıkmalar Mimari ile kıyaslandı mı?",
        "Tüm elemanlarda paspayı mesafelerine dikkat edildi mi?"
    ], "mimari-box", "Mimari")

# --- BÖLÜM 5: ÇATI & ASANSÖR ---
elif "5. Bölüm" in bolum_secimi:
    kriter_arayuzu("🔵 ASANSÖR & STATİK", [
        "Asansör kaidesinin KOTU proje ile uyumlu mu?",
        "Asansör kaidesinde HAVA BACASI bırakıldı mı?",
        "Parapetler projeye uygun (Duvar/Betonarme) ve yüksekliği doğru mu?"
    ], "statik-box", "Statik")
    
    kriter_arayuzu("🟢 MİMARİ & ÇATI", [
        "Saçak kotları mimari proje ile uyumlu mu?",
        "Çatı katı net yüksekliği ölçüldü mü?"
    ], "mimari-box", "Mimari")

# --- RAPORLAMA ---
st.divider()
if st.button("📊 YY YAPI - VERİLERİ HARMANLA VE EXCEL OLUŞTUR"):
    if rapor_verisi:
        df = pd.DataFrame(rapor_verisi)
        df['Proje'] = proje_adi
        df['Denetçi'] = denetci
        df['Firma'] = "YY YAPI DENETİM LTD. ŞTİ."
        
        file_name = f"YY_YAPI_{proje_adi}.xlsx".replace(" ", "_")
        df.to_excel(file_name, index=False)
        
        with open(file_name, "rb") as f:
            st.download_button("Excel Dosyasını İndir (YAPP360 İçin)", f, file_name=file_name)
        st.balloons()
        st.success("Rapor hazırlandı. YAPP360 sistemine aktarabilirsiniz.")
    else:
        st.error("Lütfen önce kriterleri işaretleyin!")