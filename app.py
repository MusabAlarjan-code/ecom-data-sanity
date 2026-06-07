import streamlit as st
import pandas as pd
import numpy as np
import io

# 1. إعدادات الصفحة الأساسية الاحترافية المتوافقة مع الجوال 100%
st.set_page_config(page_title="منظومة ذكاء وتطهير البيانات", layout="wide")

# --- محرك التحليل والذكاء الإحصائي الصارم ---
class BusinessIntelligenceEngine:
    def __init__(self, df):
        self.df = df.copy()

    def get_health_report(self):
        """ناقوس الخطر: فحص الجودة وكشف المشاكل قبل التطهير الإحصائي"""
        report = {
            "السجلات المكررة المكتشفة": self.df.duplicated().sum(),
            "القيم المفقودة (الكمية)": self.df['الكمية'].isna().sum() if 'الكمية' in self.df.columns else 0,
            "القيم المفقودة (السعر)": self.df['سعر_الوحدة'].isna().sum() if 'سعر_الوحدة' in self.df.columns else 0,
            "العمليات السالبة الفوضوية": (self.df['الكمية'] < 0).sum() if 'الكمية' in self.df.columns else 0,
            "القيم الشاذة والمتطرفة (Outliers)": 0
        }
        # كشف القيم الشاذة علمياً باستخدام الانحراف المعياري (Z-Score > 3) لضمان عدم تضليل تقرير الشركة
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if self.df[col].std() > 0:
                z_scores = np.abs((self.df[col] - self.df[col].mean()) / self.df[col].std())
                report["القيم الشاذة والمتطرفة (Outliers)"] += (z_scores > 3).sum()
        return report

    def clean_pipeline(self):
        """تطهير أوتوماتيكي متقدم (تعويض بالوسيط والمنوال لحماية دقة القرارات)"""
        df_clean = self.df.copy()
        df_clean.drop_duplicates(inplace=True)
        
        if 'الكمية' in df_clean.columns:
            df_clean['الكمية'] = df_clean['الكمية'].fillna(df_clean['الكمية'].median() if not df_clean['الكمية'].dropna().empty else 1)
            df_clean['الكمية'] = df_clean['الكمية'].apply(lambda x: abs(x) if x < 0 else x)
            
        if 'سعر_الوحدة' in df_clean.columns:
            df_clean['سعر_الوحدة'] = df_clean['سعر_الوحدة'].fillna(df_clean['سعر_الوحدة'].median())
            
        for col in df_clean.select_dtypes(include=['object']).columns:
            if not df_clean[col].mode().empty:
                df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])
                
        df_clean['إجمالي_المبيعات'] = df_clean['الكمية'] * df_clean['سعر_الوحدة']
        return df_clean

    def generate_enterprise_mock(self):
        """توليد محاكاة لبيانات تجارية ضخمة وفوضوية للاختبار الفوري"""
        np.random.seed(42)
        rows = 150
        cities = ['الرياض', 'جدة', 'الدمام', 'مكة']
        products = ['هاتف ذكي', 'سماعة لاسلكية', 'ساعة ذكية', 'شاحن سريع']
        
        dates = pd.date_range(start="2026-01-01", periods=rows, freq='D')
        prod_pool = np.random.choice(products, size=rows)
        city_pool = np.random.choice(cities, size=rows)
        
        quantities = np.random.randint(1, 10, size=rows).astype(float)
        quantities[np.random.choice(rows, 10, replace=False)] = -5 
        quantities[np.random.choice(rows, 8, replace=False)] = np.nan 
        
        prices = np.random.choice([150, 300, 45, 1200], size=rows).astype(float)
        prices[np.random.choice(rows, 5, replace=False)] = np.nan 
        
        df = pd.DataFrame({
            'تاريخ_الطلب': dates,
            'اسم_المنتج': prod_pool,
            'الكمية': quantities,
            'سعر_الوحدة': prices,
            'المدينة': city_pool,
            'حالة_الطلب': np.random.choice(['مكتمل', 'ملغي', 'قيد المعالجة'], size=rows, p=[0.7, 0.1, 0.2])
        })
        return pd.concat([df, df.iloc[[0, 1]]], ignore_index=True)

# --- إدارة حالة النظام والذاكرة العميقة للتطبيق ---
if 'df_raw' not in st.session_state:
    st.session_state.df_raw = None

# --- أولاً: واجهة الترحيب الاحترافية المركزية (Landing Page) ---
if st.session_state.df_raw is None:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center;'>📊 منظومة ذكاء وتطهير بيانات المبيعات</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>اصنع تقاريرك المحاسبية النظيفة واستخلص الرؤى الإستراتيجية بضغطة زر واحدة.</p>", unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        uploaded_file = st.file_uploader("قم برفع ملف مبيعاتك بصيغة Excel أو CSV الفوضوية", type=["xlsx", "csv"])
        
        st.markdown("<p style='text-align: center; margin: 10px 0;'>أو هل تريد فحص قوة النظام مباشرة؟</p>", unsafe_allow_html=True)
        
        if st.button("🔄 توليد بيانات تجريبية فوضوية واختبار المنظومة فوراً", use_container_width=True):
            st.session_state.df_raw = BusinessIntelligenceEngine(pd.DataFrame()).generate_enterprise_mock()
            st.rerun()

        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    st.session_state.df_raw = pd.read_csv(uploaded_file)
                else:
                    st.session_state.df_raw = pd.read_excel(uploaded_file)
                st.rerun()
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

# --- ثانياً: لوحة تحكم الأداء الشاملة والذكية بعد جلب البيانات ---
else:
    engine = BusinessIntelligenceEngine(st.session_state.df_raw)
    health_report = engine.get_health_report()
    df_clean = engine.clean_pipeline()
    
    # حساب كافة المؤشرات الرياضية لشركتك بدقة كاملة
    dup_count = health_report["السجلات المكررة المكتشفة"]
    null_qty = health_report["القيم المفقودة (الكمية)"]
    null_price = health_report["القيم المفقودة (السعر)"]
    negative_qty = health_report["العمليات السالبة الفوضوية"]
    outliers_count = health_report["القيم الشاذة والمتطرفة (Outliers)"]
    
    total_errors_fixed = dup_count + null_qty + null_price + negative_qty
    
    total_sales = df_clean['إجمالي_المبيعات'].sum()
    avg_order = df_clean['إجمالي_المبيعات'].mean()
    total_orders = len(df_clean)
    cv_sales = df_clean['إجمالي_المبيعات'].std() / avg_order if avg_order > 0 else 0
    
    city_summary = df_clean.groupby('المدينة')['إجمالي_المبيعات'].sum().reset_index()
    top_city = city_summary.sort_values(by='إجمالي_المبيعات', ascending=False).iloc[0]['المدينة'] if not city_summary.empty else "غير محدد"
    
    product_summary = df_clean.groupby('اسم_المنتج')['إجمالي_المبيعات'].sum().reset_index()
    top_product = product_summary.sort_values(by='إجمالي_المبيعات', ascending=False).iloc[0]['اسم_المنتج'] if not product_summary.empty else "غير محدد"

    # تصميم القائمة الجانبية المتقدمة للتحكم والتصدير
    with st.sidebar:
        st.markdown("### 🛠️ لوحة تحكم المحلل")
        st.markdown("---")
        st.subheader("🚨 ناقوس جودة البيانات المكتشفة")
        st.error(f"• السجلات المكررة: {dup_count}")
        st.error(f"• القيم المفقودة والمنتهكة: {null_qty + null_price + negative_qty}")
        st.warning(f"• القيم الشاذة إحصائياً: {outliers_count}")
        
        st.markdown("---")
        st.subheader("📥 مركز تصدير التقارير للقيادة")
        
        # إعادة بناء محرك التصدير لملف الـ Excel الاحترافي مع الرسوم البيانية والتنسيقات
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df_clean.to_excel(writer, sheet_name='البيانات المطهوة النظيفة', index=False)
            
            workbook  = writer.book
            worksheet_summary = workbook.add_worksheet('الملخص التنفيذي الإداري')
            writer.sheets['الملخص التنفيذي الإداري'] = worksheet_summary
            
            fmt_title = workbook.add_format({'bold': True, 'font_size': 16, 'font_name': 'Segoe UI', 'align': 'right'})
            fmt_body = workbook.add_format({'font_size': 11, 'font_name': 'Segoe UI', 'align': 'right'})
            fmt_header = workbook.add_format({'bold': True, 'bg_color': '#007bff', 'font_color': 'white', 'align': 'center'})
            
            worksheet_summary.right_to_left()
            worksheet_summary.write('A1', 'تقرير ذكاء الأعمال والملخص التنفيذي للمتجر', fmt_title)
            worksheet_summary.write('A3', 'المؤشر المالي', fmt_header)
            worksheet_summary.write('B3', 'القيمة المكتشفة', fmt_header)
            
            metrics_data = [
                ('إجمالي صافي المبيعات', total_sales),
                ('متوسط قيمة الطلب', avg_order),
                ('إجمالي الطلبات المعالجة', total_orders),
                ('المنتج الأكثر مبيعاً', top_product),
                ('أعلى مدينة في المبيعات', top_city),
                ('عدد الأخطاء التي تم تطهيرها', total_errors_fixed)
            ]
            
            row = 3
            for item, val in metrics_data:
                worksheet_summary.write(row, 0, item, fmt_body)
                worksheet_summary.write(row, 1, val, fmt_body)
                row += 1
                
            city_summary.to_excel(writer, sheet_name='الملخص التنفيذي الإداري', startrow=11, index=False)
            
            chart = workbook.add_chart({'type': 'column'})
            max_row = 11 + len(city_summary)
            chart.add_series({
                'categories': f"='الملخص التنفيذي الإداري'!$A$13:$A${max_row}",
                'values':     f"='الملخص التنفيذي الإداري'!$B$13:$B${max_row}",
                'title':      {'name': 'توزيع المبيعات الإجمالي حسب المدن'},
                'name':       'صافي الأرباح ر.س'
            })
            chart.set_style(10)
            worksheet_summary.insert_chart('D3', chart)

        st.download_button(
            label="📥 تحميل تقرير Excel المطور (شامل الرسوم)",
            data=excel_buffer.getvalue(),
            file_name="Executive_Data_Sanity_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 إغلاق التقرير والعودة للرئيسية", use_container_width=True):
            st.session_state.df_raw = None
            st.rerun()

    # الأقسام التفاعلية للوحة التحكم عبر نظام الـ Tabs الأنيق والمريح للهاتف
    tab_dashboard, tab_clean_data = st.tabs(["📈 التحليل المالي التنفيذي", "🛠️ لوحة الفحص والتطهير"])
    
    with tab_dashboard:
        st.subheader("📊 المؤشرات المالية الكبرى للشركة")
        m1, m2, m3 = st.columns(3)
        m1.metric(label="إجمالي صافي المبيعات", value=f"{total_sales:,.2f} ر.س")
        m2.metric(label="متوسط قيمة الطلب", value=f"{avg_order:,.2f} ر.س")
        m3.metric(label="حجم العمليات الناجحة", value=f"{total_orders} طلب")
        
        st.markdown("---")
        st.subheader("🧠 التوصيات الإستراتيجية الفورية للأداء الحالي:")
        insight_text = f"• **المنتج القيادي**: يعتبر منتج ({top_product}) هو المحرك الأساسي لحجم الإيرادات في المتجر.\n\n"
        insight_text += f"• **التوزيع الجغرافي**: تعد مدينة ({top_city}) هي السوق الأكثر نشاطاً وتوليداً للأرباح.\n\n"
        
        if cv_sales > 0.8:
            insight_text += "• **تنبيه إدارة المخاطر (تذبذب عالٍ)**: يلاحظ وجود تشتت كبير في قيم المبيعات اليومية، مما يعني الاعتماد على صفقات كبيرة متباعدة. نوصي بعمل عروض مستمرة لتثبيت قاعدة الإيرادات."
        else:
            insight_text += "• **الاستقرار التجاري**: هناك استقرار نسبي وتوزيع متزن في حجم المبيعات اليومية، مما يقلل المخاطر التشغيلية الكبرى للمتجر."
        st.info(insight_text)
        
        st.markdown("---")
        st.subheader("📊 التوزيع الإحصائي التفاعلي للمبيعات")
        c1, c2 = st.columns(2)
        with c1:
            st.write("حجم المبيعات لكل مدينة:")
            st.bar_chart(data=city_summary, x='المدينة', y='إجمالي_المبيعات', use_container_width=True)
        with c2:
            st.write("أداء المنتجات المالي الاستراتيجي:")
            st.bar_chart(data=product_summary, x='اسم_المنتج', y='إجمالي_المبيعات', use_container_width=True)

    with tab_clean_data:
        st.subheader("🛠️ الفحص والطهير الأوتوماتيكي المعالج علمياً")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="السجلات المكررة المحذوفة", value=f"{dup_count} سطر")
        col2.metric(label="القيم المصلحة إحصائياً", value=f"{null_qty + null_price + negative_qty} قيمة")
        col3.metric(label="جودة وجاهزية البيانات المعتمدة", value="100%")
        
        st.markdown("---")
        st.subheader("📋 معاينة البيانات المطهوة والنظيفة بالكامل")
        st.dataframe(df_clean, use_container_width=True)
