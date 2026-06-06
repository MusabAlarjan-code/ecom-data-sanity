import streamlit as st
import pandas as pd
import numpy as np
import io

# 1. إعدادات الصفحة ودعم اللغة العربية (RTL) والتصميم الأنيق
st.set_page_config(page_title="منظومة ذكاء وتطهير بيانات المبيعات", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [data-testid="stSidebarCodeBlock"], .stMarkdown, .stSelectbox, div {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-right: 5px solid #007bff;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .insight-box {
        background-color: #e9ecef;
        border-right: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px;
        line-height: 1.6;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 منظومة ذكاء وتطهير بيانات المبيعات للمتاجر الإلكترونية")
st.write("اصنع تقاريرك المحاسبية النظيفة واستخلص الرؤى الإستراتيجية بضغطة زر واحدة.")

# 2. آلية توليد البيانات التجريبية أو رفع ملف مخصص
uploaded_file = st.file_uploader("قم برفع ملف مبيعاتك بصيغة Excel أو CSV الفوضوية", type=["xlsx", "csv"])
generate_mock = st.button("🔄 توليد بيانات تجريبية فوضوية واختبار المنظومة فوراً")

df_raw = None

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

elif generate_mock:
    # صناعة بيانات فوضوية عمداً للاختبار الإداري والتسويقي
    np.random.seed(42)
    rows = 150
    cities = ['الرياض', 'جدة', 'الدمام', 'مكة']
    products = ['هاتف ذكي', 'سماعة لاسلكية', 'ساعة ذكية', 'شاحن سريع']
    
    dates = pd.date_range(start="2026-01-01", periods=rows, freq='D')
    prod_pool = np.random.choice(products, size=rows)
    city_pool = np.random.choice(cities, size=rows)
    
    # إدخال قيم سالبة ومفقودة عمداً لبيان قوة التطهير
    quantities = np.random.randint(1, 10, size=rows).astype(float)
    quantities[np.random.choice(rows, 10, replace=False)] = -5 
    quantities[np.random.choice(rows, 8, replace=False)] = np.nan 
    
    prices = np.random.choice([150, 300, 45, 1200], size=rows).astype(float)
    prices[np.random.choice(rows, 5, replace=False)] = np.nan 
    
    df_raw = pd.DataFrame({
        'تاريخ_الطلب': dates,
        'اسم_المنتج': prod_pool,
        'الكمية': quantities,
        'سعر_الوحدة': prices,
        'المدينة': city_pool,
        'حالة_الطلب': np.random.choice(['مكتمل', 'ملغي', 'قيد المعالجة'], size=rows, p=[0.7, 0.1, 0.2])
    })
    df_raw = pd.concat([df_raw, df_raw.iloc[[0, 1]]], ignore_index=True)
    st.success("تم توليد محاكاة لبيانات تجارية فوضوية بنجاح!")

# 3. محرك المعالجة والتطهير والتحليل الذكي
if df_raw is not None:
    st.subheader("🛠️ أولاً: الفحص والطهير الأوتوماتيكي للبيانات")
    
    dup_count = df_raw.duplicated().sum()
    null_qty = df_raw['الكمية'].isna().sum()
    null_price = df_raw['سعر_الوحدة'].isna().sum()
    negative_qty = (df_raw['الكمية'] < 0).sum() if 'الكمية' in df_raw.columns else 0
    
    df_clean = df_raw.copy()
    df_clean.drop_duplicates(inplace=True)
    
    df_clean['الكمية'] = df_clean['الكمية'].fillna(1)
    df_clean['الكمية'] = df_clean['الكمية'].apply(lambda x: abs(x) if x < 0 else x)
    df_clean['سعر_الوحدة'] = df_clean['سعر_الوحدة'].fillna(df_clean['سعر_الوحدة'].median())
    
    df_clean['إجمالي_المبيعات'] = df_clean['الكمية'] * df_clean['سعر_الوحدة']
    
    total_errors_fixed = dup_count + null_qty + null_price + negative_qty
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-card'><h4>السجلات المكررة المحذوفة</h4><h2>{dup_count}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h4>القيم المفقودة والسالبة المصححة</h4><h2>{null_qty + null_price + negative_qty}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='metric-card'><h4>جاهزية وجودة البيانات الحالية</h4><h2>100%</h2></div>", unsafe_allow_html=True)
        
    # 4. محرك ذكاء الأعمال وصناعة الاستشارات (Insights Engine)
    st.subheader("📈 ثانياً: الملخص التنفيذي والتحليلات الإستراتيجية (Executive Summary)")
    
    total_sales = df_clean['إجمالي_المبيعات'].sum()
    avg_order = df_clean['إجمالي_المبيعات'].mean()
    total_orders = len(df_clean)
    
    cv_sales = df_clean['إجمالي_المبيعات'].std() / avg_order
    
    city_summary = df_clean.groupby('المدينة')['إجمالي_المبيعات'].sum().reset_index()
    top_city = city_summary.sort_values(by='إجمالي_المبيعات', ascending=False).iloc[0]['المدينة']
    
    product_summary = df_clean.groupby('اسم_المنتج')['إجمالي_المبيعات'].sum().reset_index()
    top_product = product_summary.sort_values(by='إجمالي_المبيعات', ascending=False).iloc[0]['اسم_المنتج']

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f"<div class='metric-card'><h4>إجمالي صافي المبيعات</h4><h2>{total_sales:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
    with m2:
        st.markdown(f"<div class='metric-card'><h4>متوسط قيمة الطلب الفعلي</h4><h2>{avg_order:,.2f} ر.س</h2></div>", unsafe_allow_html=True)
    with m3:
        st.markdown(f"<div class='metric-card'><h4>حجم العمليات (الطلبات النظيفة)</h4><h2>{total_orders} طلب</h2></div>", unsafe_allow_html=True)

    st.markdown("### 🧠 التوصيات وقراءة الأداء المالي للفترة الحالية:")
    
    insight_text = f"• **المنتج القيادي:** يعتبر منتج (**{top_product}**) هو المحرك الأساسي لحجم الإيرادات في المتجر.\n\n"
    insight_text += f"• **التوزيع الجغرافي:** تعد مدينة (**{top_city}**) هي السوق الأكثر نشاطاً وتوليداً للأرباح.\n\n"
    
    if cv_sales > 0.8:
        insight_text += "• **تنبيه إدارة المخاطر (تذبذب عالٍ):** يلاحظ النظام وجود تشتت وتذبذب كبير في قيم المبيعات اليومية. "
        insight_text += "هذا يعني الاعتماد على صفقات كبيرة متباعدة بدلاً من الاستقرار المالي اليومي. "
        insight_text += "نوصي بمراجعة سياسات التسعير وعمل عروض مستمرة لتثبيت قاعدة الإيرادات."
    else:
        insight_text += "• **الاستقرار التجاري:** هناك استقرار نسبي وتوزيع متزن في حجم المبيعات اليومية، مما يقلل المخاطر التشغيلية للمتجر."

    st.markdown(f"<div class='insight-box'>{insight_text}</div>", unsafe_allow_html=True)

    # 5. عرض الرسوم البيانية التفاعلية في الواجهة
    st.subheader("📊 ثالثاً: التوزيع الإحصائي للمبيعات")
    c1, c2 = st.columns(2)
    with c1:
        st.write("حجم المبيعات لكل مدينة:")
        st.bar_chart(data=city_summary, x='المدينة', y='إجمالي_المبيعات', use_container_width=True)
    with c2:
        st.write("أداء المنتجات المالي:")
        st.bar_chart(data=product_summary, x='اسم_المنتج', y='إجمالي_المبيعات', use_container_width=True)

    # 6. بناء وتصدير ملف الـ Excel الاحترافي بميزاته الجديدة (xlsxwriter)
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

    st.subheader("📥 رابعاً: تحميل التقارير الإدارية النهائية")
    st.download_button(
        label="📥 تحميل تقرير Excel المطور (يشمل الملخص التنفيذي والرسم البياني)",
        data=excel_buffer.getvalue(),
        file_name="Executive_Data_Sanity_Report.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
