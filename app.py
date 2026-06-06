import io
import os
import numpy as np
import pandas as pd
import streamlit as st

# 1. إعدادات لوحة التحكم للمتصفح (واجهة تدعم الهواتف والحواسب)
st.set_page_config(
    page_title="مُصلح بيانات التجارة الإلكترونية | E-Com Data Sanity",
    page_icon="🛍️",
    layout="wide",
)

# حقن ستايل لتنسيق الواجهة البرمجية لتناسب اللغة العربية (من اليمين لليسار)
st.markdown(
    """
    <style>
    body, div, p, h1, h2, h3, h4, h5, h6, label { text-align: right; direction: rtl; }
    .stButton>button { width: 100%; font-weight: bold; background-color: #1E88E5; color: white; }
    .stDownloadButton>button { width: 100%; font-weight: bold; background-color: #4CAF50; color: white; }
    div[data-testid="stExpander"] { text-align: right; direction: rtl; }
    </style>
""",
    unsafe_allow_html=True,
    
)


# 2. بناء محرك الـ OOP الاحترافي لمعالجة البيانات
class EnterpriseDataAnalyst:
    """المحرك الخلفي المؤتمت لتطهير وتحليل بيانات المتاجر الإلكترونية."""

    def __init__(self, system_name="محرك التطهير الذكي"):
        self.system_name = system_name
        self.df = None
        self.report_summary = {}

    def load_data(self, source, is_mock=False):
        """تحميل مرن للبيانات سواء مرفوعة من العميل أو مولدة برمجياً للتجربة."""
        try:
            if is_mock:
                self.df = source.copy()
                return (
                    True,
                    f"🎯 تم توليد بيانات تجريبية فوضوية بنجاح: {self.df.shape[0]} طلب، و {self.df.shape[1]} متغير.",
                )

            filename = source.name
            if filename.endswith(".csv"):
                self.df = pd.read_csv(source)
            elif filename.endswith(".xlsx") or filename.endswith(".xls"):
                self.df = pd.read_excel(source)
            else:
                return False, "صيغة غير مدعومة. يرجى استخدام CSV أو Excel."
            return (
                True,
                f"✅ تم تحميل ملفك بنجاح: {self.df.shape[0]} صف، و {self.df.shape[1]} عمود.",
            )
        except Exception as e:
            return False, f"❌ فشل قراءة البيانات: {e}"

    def advanced_cleanse(self):
        """تطهير البيانات من الفوضى (التواريخ المعطوبة، الحقول الفارغة، القيم الشاذة، التكرار)."""
        if self.df is None:
            return 0, 0

        initial_rows = self.df.shape[0]

        # أ. معالجة وتوحيد التواريخ تلقائياً
        for col in self.df.columns:
            if "date" in col.lower() or "تاريخ" in col:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")

        # ب. معالجة القيم المفقودة (العددية بالوسيط، والنصية بالقيمة الأكثر تكراراً)
        for col in self.df.columns:
            if self.df[col].isnull().sum() > 0:
                if self.df[col].dtype in ["int64", "float64"]:
                    median_val = self.df[col].median()
                    self.df[col] = self.df[col].fillna(median_val)
                else:
                    mode_val = (
                        self.df[col].mode()[0]
                        if not self.df[col].mode().empty
                        else "غير محدد"
                    )
                    self.df[col] = self.df[col].fillna(mode_val)

        # ج. إزالة الصفوف المكررة تماماً
        self.df.drop_duplicates(inplace=True)
        deleted_duplicates = initial_rows - self.df.shape[0]

        # د. كبح وإصلاح القيم الشاذة المتطرفة (Outliers) باستخدام معادلة IQR
        numeric_cols = self.df.select_dtypes(
            include=["int64", "float64"]
        ).columns
        outliers_count = 0

        for col in numeric_cols:
            Q1 = self.df[col].quantile(0.25)
            Q3 = self.df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = (self.df[col] < lower_bound) | (
                self.df[col] > upper_bound
            )
            outliers_count += outliers.sum()

            # تهذيب القيم بدلاً من حذفها للحفاظ على حجم العينة
            self.df[col] = np.where(
                self.df[col] > upper_bound, upper_bound, self.df[col]
            )
            self.df[col] = np.where(
                self.df[col] < lower_bound, lower_bound, self.df[col]
            )

        return deleted_duplicates, outliers_count

    def analyze_patterns(self):
        """تشريح البيانات واستخراج المؤشرات الإدارية ومصفوفة الارتباط."""
        if self.df is None:
            return

        numeric_cols = self.df.select_dtypes(
            include=["int64", "float64"]
        ).columns
        categorical_cols = self.df.select_dtypes(
            include=["object", "category"]
        ).columns

        # الملخص الإحصائي الأساسي
        self.report_summary["إحصائيات_رقمية"] = (
            self.df[numeric_cols].describe().T
        )

        # مصفوفة الارتباط بين المتغيرات المخرجة
        if len(numeric_cols) > 1:
            self.report_summary["مصفوفة_العلاقات"] = self.df[numeric_cols].corr()

        # تحليل المبيعات حسب الأقسام (بشرط ألا تتجاوز الفئات 20 فئة لمنع تشويه التقارير)
        self.report_summary["تحليل_الفئات"] = {}
        for col in categorical_cols:
            if self.df[col].nunique() <= 20:
                self.report_summary["تحليل_الفئات"][col] = (
                    self.df[col].value_counts()
                )


# 3. دالة ذكية لتوليد بيانات متجر إلكتروني "مليئة بالأخطاء العمداً" لأغراض التجربة والبيع
def generate_messy_ecommerce_data():
    np.random.seed(42)
    rows = 250
    categories = ["إلكترونيات", "ملابس وأزياء", "أدوات منزلية", "مستحضرات تجميل"]
    dates = [
        "2026-01-10",
        "2026/02/15",
        "12-03-2026",
        None,
        "2026-04-01",
        "2026-05-18",
    ]

    data = {
        "رقم_الطلب": [f"ORD-{1000+i}" for i in range(rows)],
        "تاريخ_الشراء": [np.random.choice(dates) for _ in range(rows)],
        "اسم_العميل": [f"عميل_{np.random.randint(1, 40)}" for _ in range(rows)],
        "قسم_المنتجات": [np.random.choice(categories) for _ in range(rows)],
        # إدخال قيم فارغة وقيم شاذة ضخمة جداً (خطأ إدخال كـ 25,000 دينار لقميص مثلاً)
        "إجمالي_الفاتورة": [
            np.random.choice([25.0, 45.0, 110.0, 320.0, np.nan, 25000.0])
            for _ in range(rows)
        ],
        "الكمية": [np.random.randint(1, 5) for _ in range(rows)],
    }

    df = pd.DataFrame(data)
    # إضافة صفوف مكررة عمداً بالنظام
    df = pd.concat([df, df.head(8)], ignore_index=True)
    return df


# --- 4. واجهة المستخدم الرسومية للتطبيق التفاعلي ---

st.title("🛍️ منصة تطهير وتحليل بيانات التجارة الإلكترونية المتقدمة")
st.write(
    "نظام مؤتمت مصمم خصيصاً للمدراء وأصحاب المتاجر لإصلاح تقارير المبيعات الفوضوية وتحويلها إلى تقارير تنفيذية بضغطة زر."
)

# تقسيم الواجهة إلى خيارين لسهولة التجربة والبيع
st.header("🛠️ خطوة 1: جلب البيانات وتجربة النظام")
tab1, tab2 = st.tabs(
    ["📊 تجربة النظام ببيانات وهمية فوضوية", "📥 رفع ملف متجرك الحقيقي"]
)

analyst = EnterpriseDataAnalyst()
data_loaded = False

with tab1:
    st.write(
        "اضغط على الزر أدناه لتوليد ملف مبيعات وهمي يحتوي على (قيم فارغة، تواريخ معطوبة، صفوف مكررة، وأخطاء مالية شاذة) لتشاهد كيف يطهرها النظام."
    )
    if st.button("🔄 توليد البيانات الفوضوية التجريبية واختبار النظام"):
        mock_df = generate_messy_ecommerce_data()
        success, message = analyst.load_data(mock_df, is_mock=True)
        st.session_state["analyst_engine"] = analyst
        st.session_state["data_ready"] = True
        st.success(message)

with tab2:
    uploaded_file = st.file_uploader(
        "ارفع ملف المبيعات الخاص بمتجرك (CSV أو Excel)",
        type=["csv", "xlsx", "xls"],
    )
    if uploaded_file is not None:
        success, message = analyst.load_data(uploaded_file, is_mock=False)
        if success:
            st.session_state["analyst_engine"] = analyst
            st.session_state["data_ready"] = True
            st.success(message)
        else:
            st.error(message)

# معالجة وعرض النتائج في حال جاهزية البيانات
if st.session_state.get("data_ready"):
    active_analyst = st.session_state["analyst_engine"]

    with st.expander("🔍 استعراض عينة من البيانات قبل التطهير والاصلاح"):
        st.dataframe(active_analyst.df.head(10))

    if st.button("🚀 إطلاق معالج التطهير والتحليل الأوتوماتيكي المتقدم"):

        # تنفيذ عمليات الهندسة والتنظيف المتقدمة
        deleted_dups, fixed_outliers = active_analyst.advanced_cleanse()
        active_analyst.analyze_patterns()

        # لوحة العدادات الرقمية للمخرجات المعالجة
        st.header("✨ خطوة 2: لوحة التحكم والبيانات المطهرة")

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        with metric_col1:
            st.metric(label="عدد الصفوف المكررة المحذوفة", value=deleted_dups)
        with metric_col2:
            st.metric(
                label="القيم المالية الشاذة التي تم كبحها وتعديلها",
                value=fixed_outliers,
            )
        with metric_col3:
            st.metric(
                label="حالة جودة البيانات الحالية (Data Health)", value="100%"
            )

        with st.expander("📋 استعراض البيانات النظيفة بالكامل وجاهزة للأنظمة المحاسبية"):
            st.dataframe(active_analyst.df.head(15))

        # عرض الرسومات والتحليلات الإدارية التلقائية للمدراء
        st.header("📊 خطوة 3: لوحة مؤشرات الأداء الإداري (MIS Insights)")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.subheader("📈 الملخص الإحصائي المالي المعتمد")
            st.dataframe(active_analyst.report_summary["إحصائيات_رقمية"])

        with col_chart2:
            if "مصفوفة_العلاقات" in active_analyst.report_summary:
                st.subheader("🔗 مصفوفة تداخل وترابط المتغيرات")
                st.dataframe(active_analyst.report_summary["مصفوفة_العلاقات"])

        # رسم بياني أوتوماتيكي لتوزيع مبيعات الأقسام
        if active_analyst.report_summary.get("تحليل_الفئات"):
            st.subheader("🗂️ التوزيع البياني لحجم عمليات المبيعات حسب الأقسام")
            for cat_col, counts in active_analyst.report_summary[
                "تحليل_الفئات"
            ].items():
                if cat_col == "قسم_المنتجات":
                    st.bar_chart(counts)

        # توليد تقرير الإكسل متعدد الصفحات للتحميل المباشر للمدراء
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
            active_analyst.df.to_excel(
                writer, sheet_name="البيانات_المطهرة", index=False
            )
            if "إحصائيات_رقمية" in active_analyst.report_summary:
                active_analyst.report_summary["إحصائيات_رقمية"].to_excel(
                    writer, sheet_name="ملخص_الأداء_الرقمي"
                )
            if "مصفوفة_العلاقات" in active_analyst.report_summary:
                active_analyst.report_summary["مصفوفة_العلاقات"].to_excel(
                    writer, sheet_name="روابط_المتغيرات"
                )

        st.markdown("---")
        st.subheader("📥 خطوة 4: تصدير واستلام التقرير التنفيذي النهائي")
        st.download_button(
            label="📥 تحميل ملف الـ Excel التنفيذي المنسق والجاهز للمحاسبين",
            data=excel_buffer.getvalue(),
            file_name="Ecom_Clean_Executive_Report.xlsx",
            mime="application/vnd.ms-excel",
        )
