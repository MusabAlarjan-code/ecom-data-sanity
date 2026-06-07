import streamlit as st
import pandas as pd
import numpy as np
import io

# إعدادات الصفحة
st.set_page_config(page_title="Enterprise BI", layout="wide")

# --- محرك التحليل والذكاء (The Brain) ---
class DataEngine:
    def __init__(self, df):
        self.df = df.copy()

    def get_health_report(self):
        """تحليل جودة البيانات (الناقوس)"""
        report = {
            "التكرارات": self.df.duplicated().sum(),
            "قيم_مفقودة": self.df.isnull().sum().sum(),
            "قيم_شاذة": 0 
        }
        # كشف القيم الشاذة (Outliers) - منطق علمي
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            z_scores = np.abs((self.df[col] - self.df[col].mean()) / (self.df[col].std() + 1e-6))
            report["قيم_شاذة"] += (z_scores > 3).sum()
        return report

    def clean_pipeline(self):
        """تنظيف احترافي مع إحصاءات الوسيط والمنوال"""
        for col in self.df.select_dtypes(include=[np.number]).columns:
            self.df[col] = self.df[col].fillna(self.df[col].median())
        for col in self.df.select_dtypes(include=['object']).columns:
            if not self.df[col].mode().empty:
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
        self.df.drop_duplicates(inplace=True)
        return self.df

    def generate_mock_data(self):
        rows = 150
        np.random.seed(42)
        df = pd.DataFrame({
            'تاريخ_الطلب': pd.date_range(start="2026-01-01", periods=rows, freq='D'),
            'اسم_المنتج': np.random.choice(['هاتف', 'سماعة', 'ساعة', 'شاحن'], size=rows),
            'الكمية': np.random.randint(1, 10, size=rows).astype(float),
            'سعر_الوحدة': np.random.choice([150, 300, 45, 1200], size=rows).astype(float),
            'المدينة': np.random.choice(['الرياض', 'جدة', 'الدمام', 'مكة'], size=rows)
        })
        df.loc[np.random.choice(rows, 10), 'الكمية'] = np.nan
        return df

# --- منطق الواجهة ---
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None

if st.session_state.df_raw is None:
    st.markdown("<h1 style='text-align: center;'>🚀 نظام تحليل الأعمال المتقدم</h1>", unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        uploaded_file = st.file_uploader("قم برفع ملف البيانات", type=["csv", "xlsx"])
        if st.button("🔄 تجربة بيانات وهمية", use_container_width=True):
            st.session_state.df_raw = DataEngine(pd.DataFrame()).generate_mock_data()
            st.rerun()
        if uploaded_file:
            st.session_state.df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
            st.rerun()

else:
    engine = DataEngine(st.session_state.df_raw)
    health = engine.get_health_report()
    df_clean = engine.clean_pipeline()
    
    # الـ Sidebar الاحترافية
    with st.sidebar:
        st.subheader("⚠️ ناقوس جودة البيانات")
        for k, v in health.items():
            st.write(f"- {k}: {v}")
        
        st.divider()
        # التصدير الذكي
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, sheet_name='البيانات_النظيفة', index=False)
            pd.DataFrame([health]).to_excel(writer, sheet_name='تقرير_الجودة', index=False)
        st.download_button("📥 تحميل التقرير الكامل", buffer, "Cleaned_Report.xlsx")
        
        if st.button("🏠 العودة للرئيسية"):
            st.session_state.df_raw = None
            st.rerun()

    # لوحة التحكم
    st.title("📊 لوحة تحكم الأداء")
    tab1, tab2 = st.tabs(["📊 التحليل المالي", "🛠️ البيانات المطهوة"])
    
    with tab1:
        rev = (df_clean['الكمية'] * df_clean['سعر_الوحدة']).sum()
        st.metric("إجمالي المبيعات", f"{rev:,.2f} ر.س")
        st.bar_chart(df_clean.groupby('المدينة')['سعر_الوحدة'].sum())
    
    with tab2:
        st.dataframe(df_clean)
