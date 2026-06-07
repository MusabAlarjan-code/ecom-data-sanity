import streamlit as st
import pandas as pd
import numpy as np
import io
import xlsxwriter

# --- 1. محرك معالجة البيانات (Data Science Core) ---
class DataEngine:
    def __init__(self, df):
        self.df = df.copy()

    def clean_pipeline(self):
        # معالجة القيم المفقودة إحصائياً (Imputation)
        for col in self.df.select_dtypes(include=[np.number]).columns:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)
        
        # معالجة النصوص
        for col in self.df.select_dtypes(include=['object']).columns:
            mode_val = self.df[col].mode()[0]
            self.df[col] = self.df[col].fillna(mode_val)
            
        # إزالة التكرارات
        self.df.drop_duplicates(inplace=True)
        return self.df

    def get_kpis(self):
        # حساب مؤشرات الأداء (KPIs)
        total_revenue = (self.df['الكمية'] * self.df['سعر_الوحدة']).sum()
        avg_order = (self.df['الكمية'] * self.df['سعر_الوحدة']).mean()
        return total_revenue, avg_order

# --- 2. واجهة المستخدم الاحترافية (Professional UI) ---
st.set_page_config(page_title="Enterprise BI", layout="wide")
st.title("🚀 نظام تحليل الأعمال المتقدم")

uploaded_file = st.sidebar.file_uploader("ارفع بياناتك (CSV/XLSX)", type=["csv", "xlsx"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
    engine = DataEngine(df_raw)
    df_clean = engine.clean_pipeline()
    
    # تقسيم الواجهة لألسنة (Tabs) - الاحترافية في التنقل
    tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم", "🛠️ تنظيف البيانات", "📥 التصدير"])

    with tab1:
        st.subheader("المؤشرات المالية")
        rev, avg = engine.get_kpis()
        col1, col2 = st.columns(2)
        col1.metric("إجمالي الإيرادات", f"{rev:,.2f} ر.س")
        col2.metric("متوسط الطلب", f"{avg:,.2f} ر.س")
        
        st.bar_chart(df_clean.groupby('المدينة')['إجمالي_المبيعات'].sum())
        
        st.info("💡 التوصية الاستراتيجية: بناءً على تحليل التوزيع الجغرافي، يوصى بزيادة المخزون في المناطق ذات معدل التكرار الأعلى.")

    with tab2:
        st.write("ملخص العمليات الإحصائية المطبقة:")
        st.table(df_clean.describe())

    with tab3:
        # تصدير احترافي
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, index=False)
        st.download_button("تحميل التقرير النهائي", buffer, "Cleaned_Report.xlsx")

else:
    st.warning("يرجى رفع ملف البيانات للبدء في التحليل.")
