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
        """التنظيف الإحصائي للبيانات"""
        # معالجة القيم المفقودة إحصائياً
        for col in self.df.select_dtypes(include=[np.number]).columns:
            median_val = self.df[col].median()
            self.df[col] = self.df[col].fillna(median_val)
        
        # معالجة النصوص
        for col in self.df.select_dtypes(include=['object']).columns:
            if not self.df[col].mode().empty:
                mode_val = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(mode_val)
            
        self.df.drop_duplicates(inplace=True)
        return self.df

    def generate_mock_data(self):
        """توليد بيانات تجريبية (لأغراض العرض التوضيحي)"""
        rows = 150
        np.random.seed(42)
        cities = ['الرياض', 'جدة', 'الدمام', 'مكة']
        products = ['هاتف ذكي', 'سماعة لاسلكية', 'ساعة ذكية', 'شاحن سريع']
        
        data = {
            'تاريخ_الطلب': pd.date_range(start="2026-01-01", periods=rows, freq='D'),
            'اسم_المنتج': np.random.choice(products, size=rows),
            'الكمية': np.random.randint(1, 10, size=rows).astype(float),
            'سعر_الوحدة': np.random.choice([150, 300, 45, 1200], size=rows).astype(float),
            'المدينة': np.random.choice(cities, size=rows)
        }
        df = pd.DataFrame(data)
        # إدخال أخطاء متعمدة
        df.loc[np.random.choice(rows, 10), 'الكمية'] = np.nan
        return df

    def get_kpis(self):
        """حساب المؤشرات"""
        self.df['إجمالي_المبيعات'] = self.df['الكمية'] * self.df['سعر_الوحدة']
        total_revenue = self.df['إجمالي_المبيعات'].sum()
        avg_order = self.df['إجمالي_المبيعات'].mean()
        return total_revenue, avg_order

# --- 2. واجهة المستخدم الاحترافية ---
st.set_page_config(page_title="Enterprise BI", layout="wide")
st.title("🚀 نظام تحليل الأعمال المتقدم")

# القائمة الجانبية (Sidebar) للتحكم
with st.sidebar:
    st.header("إعدادات النظام")
    uploaded_file = st.file_uploader("ارفع ملف بياناتك", type=["csv", "xlsx"])
    st.divider()
    st.subheader("وضع التجربة")
    btn_mock = st.button("🔄 توليد بيانات تجريبية")

# --- 3. المنطق الأساسي ---
df_raw = None

# تحديد المصدر (ملف مرفوع أم تجربة؟)
if uploaded_file:
    df_raw = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
elif btn_mock:
    # إنشاء نسخة مؤقتة من المحرك لتوليد البيانات
    temp_engine = DataEngine(pd.DataFrame())
    df_raw = temp_engine.generate_mock_data()
    st.sidebar.success("تم تفعيل وضع التجربة!")

if df_raw is not None:
    engine = DataEngine(df_raw)
    df_clean = engine.clean_pipeline()
    
    # تقسيم الواجهة لألسنة (Tabs)
    tab1, tab2, tab3 = st.tabs(["📊 لوحة التحكم", "🛠️ تنظيف البيانات", "📥 التصدير"])

    with tab1:
        rev, avg = engine.get_kpis()
        col1, col2 = st.columns(2)
        col1.metric("إجمالي الإيرادات", f"{rev:,.2f} ر.س")
        col2.metric("متوسط الطلب", f"{avg:,.2f} ر.س")
        
        st.subheader("تحليل الأداء الجغرافي")
        st.bar_chart(engine.df.groupby('المدينة')['إجمالي_المبيعات'].sum())
        
        st.info("💡 التوصية: بناءً على البيانات، نوصي بتركيز الحملات التسويقية في المدن ذات الأداء الأعلى.")

    with tab2:
        st.write("بيانات تم تنظيفها ومعالجتها إحصائياً:")
        st.dataframe(df_clean.head(10))

    with tab3:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, index=False)
        st.download_button("📥 تحميل التقرير الاحترافي النهائي", buffer, "Cleaned_Report.xlsx")

else:
    st.warning("يرجى رفع ملف البيانات أو استخدام وضع التجربة للبدء.")
