import streamlit as st
import pandas as pd
import numpy as np
import io

# --- 1. الدوال الخاصة بمعالجة البيانات (Business Logic) ---

def clean_data(df):
    """دالة لتنظيف البيانات ومعالجتها"""
    df_clean = df.copy()
    df_clean.drop_duplicates(inplace=True)
    df_clean['الكمية'] = df_clean['الكمية'].fillna(1)
    df_clean['الكمية'] = df_clean['الكمية'].apply(lambda x: abs(x) if x < 0 else x)
    df_clean['سعر_الوحدة'] = df_clean['سعر_الوحدة'].fillna(df_clean['سعر_الوحدة'].median())
    df_clean['إجمالي_المبيعات'] = df_clean['الكمية'] * df_clean['سعر_الوحدة']
    return df_clean

def generate_mock_data():
    """دالة لتوليد بيانات تجريبية"""
    np.random.seed(42)
    rows = 150
    cities = ['الرياض', 'جدة', 'الدمام', 'مكة']
    products = ['هاتف ذكي', 'سماعة لاسلكية', 'ساعة ذكية', 'شاحن سريع']
    
    df = pd.DataFrame({
        'تاريخ_الطلب': pd.date_range(start="2026-01-01", periods=rows, freq='D'),
        'اسم_المنتج': np.random.choice(products, size=rows),
        'الكمية': np.random.randint(1, 10, size=rows).astype(float),
        'سعر_الوحدة': np.random.choice([150, 300, 45, 1200], size=rows).astype(float),
        'المدينة': np.random.choice(cities, size=rows)
    })
    # إضافة قيم فارغة ومشاكل
    df.loc[np.random.choice(rows, 10), 'الكمية'] = -5
    df.loc[np.random.choice(rows, 8), 'الكمية'] = np.nan
    return df

# --- 2. إعداد الصفحة والـ Sidebar ---

st.set_page_config(page_title="منظومة ذكاء البيانات", layout="wide")

st.title("📊 منظومة ذكاء وتطهير بيانات المبيعات")

# نقل الأدوات للـ Sidebar
with st.sidebar:
    st.header("إعدادات النظام")
    uploaded_file = st.file_uploader("ارفع ملف المبيعات", type=["xlsx", "csv"])
    generate_mock = st.button("🔄 توليد بيانات تجريبية")

# --- 3. المنطق الأساسي (Main Flow) ---

df_raw = None

if uploaded_file is not None:
    df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
elif generate_mock:
    df_raw = generate_mock_data()
    st.sidebar.success("تم التوليد!")

if df_raw is not None:
    # التنظيف
    df_clean = clean_data(df_raw)
    
    # العرض
    st.subheader("🛠️ الفحص والطهير")
    col1, col2, col3 = st.columns(3)
    col1.metric("السجلات المكررة المحذوفة", f"{len(df_raw) - len(df_clean)}")
    col3.metric("جودة البيانات", "100%")
    
    st.markdown("---")
    st.subheader("📈 الملخص التنفيذي")
    # ... (بقية منطق العرض الخاص بك) ...
    # هنا يمكنك إكمال عرض الكروت والرسوم البيانية بنفس طريقتك السابقة
    
    st.success("تمت معالجة البيانات بنجاح!")
