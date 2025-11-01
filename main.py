## V1 code
# import streamlit as st
# from prediction_helper import predict
#
# st.title("Lauki Finance: Credit Risk Modeling")
#
# row1 = st.columns(3)
# row2 = st.columns(3)
# row3 = st.columns(3)
# row4 = st.columns(3)
#
# with row1[0]:
#     age = st.number_input('Age', min_value=18, max_value=100, step=1)
# with row1[1]:
#     income = st.number_input('Income', min_value=0, value=1200000)
# with row1[2]:
#     loan_amount = st.number_input('Loan Amount', min_value=0, value=2560000)
#
# #Calclate loan to income ratio and and display it
# loan_to_income_ratio = loan_amount / income if income > 0 else 0
# with row2[0]:
#     st.text("Loan to Income Ratio:")
#     st.text(f"{loan_to_income_ratio:.2f}") #Display a text field
#
# #Assign inputs to the remaining controls
# with row2[1]:
#     loan_tenure_months = st.number_input('Loan Tenure (months)', min_value=0, step=1, value=36)
# with row2[2]:
#     avg_dpd_per_delinquency = st.number_input('Avg DPD', min_value=0, value=20)
#
# with row3[0]:
#     delinquency_ratio = st.number_input('Delinquency Ratio', min_value=0, max_value=100, step=1, value=30)
# with row3[1]:
#     credit_utilization_ratio = st.number_input('Credit Utilization Ratio', min_value=0, max_value=100, step=1, value=30)
# with row3[2]:
#     num_open_accounts = st.number_input('Open Loan Accounts', min_value=1, max_value=4, step=1, value=2)
#
# with row4[0]:
#     residence_type = st.selectbox('Residence Type', ['Owned', 'Rented', 'Mortgage'])
# with row4[1]:
#     loan_purpose = st.selectbox('Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
# with row4[2]:
#     loan_type = st.selectbox('Loan Type', ['Unsecured', 'Secured'])
#
# if st.button("Calculate Risk"):
#     probability, credit_score, rating = predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency, delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type, loan_purpose, loan_type)
#     # Display the results
#     st.write(f"Deafult Probability: {probability:.2%}")
#     st.write(f"Credit Score: {credit_score}")
#     st.write(f"Rating: {rating}")

def format_in_indian_style(number):
    try:
        number = float(number)
        if number >= 1e7:
            return f"₹ {number / 1e7:.2f} Cr"
        elif number >= 1e5:
            return f"₹ {number / 1e5:.2f} L"
        else:
            return f"₹ {number:,.0f}"
    except:
        return "₹ 0"


def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    c.setFillColorRGB(0.0, 0.27, 0.65)
    c.rect(0, height - 80, width, 80, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(180, height - 55, "FinEdge Bank - Credit Risk Report")

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 120, "🧾 Borrower & Loan Details")
    c.setFont("Helvetica", 12)

    details = [
        ("Age", f"{age} years"),
        ("Income", format_in_indian_style(income)),
        ("Loan Amount", format_in_indian_style(loan_amount)),
        ("Tenure", f"{loan_tenure_months} months"),
        ("Loan Purpose", loan_purpose),
        ("Loan Type", loan_type),
        ("Residence Type", residence_type),
        ("Open Accounts", num_open_accounts),
        ("Delinquency Ratio", f"{delinquency_ratio}%"),
        ("Credit Utilization", f"{credit_utilization_ratio}%"),
        ("Avg DPD", f"{avg_dpd_per_delinquency} days"),
        ("Loan-to-Income Ratio", f"{loan_to_income_ratio:.2f}")
    ]

    y = height - 150
    for label, value in details:
        c.drawString(70, y, f"• {label}: {value}")
        y -= 20

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y, "📊 Credit Risk Summary")
    y -= 40

    cards = [
        ("Default Probability", f"{probability:.2%}", colors.whitesmoke),
        ("Credit Score", str(credit_score), colors.whitesmoke),
        ("Risk Rating", rating, colors.whitesmoke)
    ]

    x = 70
    for title, value, bg in cards:
        c.setFillColor(bg)
        c.roundRect(x, y, 150, 60, 8, fill=True)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(x + 75, y + 40, title)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(x + 75, y + 20, value)
        x += 160

    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawString(50, 50, "Made with ❤️ by Raj Lakshmi | FinEdge Analytics © 2025")

    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()
    return pdf_data


# V2 : Improved UI Code

# ---------------------------------------------------------
import streamlit as st
import time
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from prediction_helper import predict

# ------------------- PAGE CONFIG -------------------
st.set_page_config(
    page_title="FinEdge | Credit Risk Intelligence Portal",
    page_icon="🏦",
    layout="wide",
)

# ------------------- STYLING -------------------
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
            font-family: 'Inter', sans-serif;
        }
        .title {
            text-align: center;
            font-size: 2.4rem;
            color: #002B5B;
            font-weight: 800;
        }
        .subtitle {
            text-align: center;
            color: #0077b6;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.3rem;
            color: #003366;
            font-weight: 600;
            margin-top: 1.5rem;
            border-left: 4px solid #0077b6;
            padding-left: 10px;
        }
        .stButton button {
            background: linear-gradient(90deg, #0072ff 0%, #00c6ff 100%);
            color: white;
            border-radius: 10px;
            height: 3rem;
            width: 100%;
            font-size: 1.1rem;
            font-weight: 600;
            transition: 0.3s;
            border: none;
        }
        .stButton button:hover {
            transform: scale(1.03);
            box-shadow: 0 4px 10px rgba(0,0,0,0.2);
        }
        .metric-card {
            background-color: black;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            text-align: center;
            transition: transform 0.3s ease-in-out, box-shadow 0.3s;
            animation: fadeInUp 0.8s ease;
        }
        .prob {background: #f8d7da;}
        .score {background: #d1e7dd;}
        .rating {background: #cfe2ff;}
        .metric-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 4px 14px rgba(0,0,0,0.1);
        }
        @keyframes fadeInUp {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.9rem;
            margin-top: 2.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ------------------- HEADER -------------------
st.markdown("""
    <style>
        @keyframes gradientShift {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .hero {
            background: linear-gradient(270deg, #004aad, #0073e6, #00b4d8);
            background-size: 600% 600%;
            animation: gradientShift 10s ease infinite;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            text-align: center;
            color: white;
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
            margin-bottom: 2rem;
        }
        .hero h1 {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .hero p {
            font-size: 1.05rem;
            opacity: 0.9;
        }
    </style>
    <div class="hero">
        <h1>💰 FinEdge Bank - Credit Risk Evaluation</h1>
        <p>AI-powered financial assessment for smarter lending decisions</p>
    </div>
""", unsafe_allow_html=True)

# ------------------- INPUT SECTIONS -------------------
st.markdown("<div class='section-header'>👤 Borrower Profile</div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    age = st.number_input('🎂 Age', min_value=18, max_value=100, step=1)
    income = st.number_input('💼 Annual Income (₹)', min_value=0, value=1200000, step=50000)
with col2:
    residence_type = st.selectbox('🏠 Residence Type', ['Owned', 'Rented', 'Mortgage'])
    num_open_accounts = st.number_input('📂 Open Loan Accounts', min_value=1, max_value=10, step=1, value=2)

st.markdown("<div class='section-header'>💰 Loan Details</div>", unsafe_allow_html=True)
col3, col4 = st.columns(2)
with col3:
    loan_amount = st.number_input('💳 Loan Amount (₹)', min_value=0, value=2560000, step=50000)
    loan_tenure_months = st.number_input('⏳ Loan Tenure (months)', min_value=0, value=36)
with col4:
    loan_purpose = st.selectbox('🎯 Loan Purpose', ['Education', 'Home', 'Auto', 'Personal'])
    loan_type = st.selectbox('🔒 Loan Type', ['Unsecured', 'Secured'])

loan_to_income_ratio = loan_amount / income if income > 0 else 0

st.markdown("<div class='section-header'>📈 Repayment & Credit Behavior</div>", unsafe_allow_html=True)

# ------------------- REPAYMENT & CREDIT BEHAVIOR -------------------
# st.markdown("<div class='section-header'>📈 Repayment & Credit Behavior</div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    avg_dpd_per_delinquency = st.number_input(
        '📅 Avg DPD per Delinquency', min_value=0, value=20, step=1
    )
with col2:
    delinquency_ratio = st.number_input(
        '⚠️ Delinquency Ratio (%)', min_value=0, max_value=100, value=30, step=1
    )
with col3:
    credit_utilization_ratio = st.number_input(
        '💳 Credit Utilization (%)', min_value=0, max_value=100, value=30, step=1
    )
# ------------------- EVALUATE BUTTON -------------------
st.markdown("<br>", unsafe_allow_html=True)
calculate = st.button("🔍 Evaluate Credit Risk")

# ------------------- PREDICTION OUTPUT -------------------
# ------------------- PREDICTION OUTPUT -------------------
if calculate:
    with st.spinner("Analyzing borrower credit profile..."):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)

    # Model Prediction Call
    probability, credit_score, rating = predict(
        age, income, loan_amount, loan_tenure_months,
        avg_dpd_per_delinquency, delinquency_ratio,
        credit_utilization_ratio, num_open_accounts,
        residence_type, loan_purpose, loan_type
    )
    progress_bar.empty()

    # Divider & Section Header
    st.markdown("---")
    st.markdown("<div class='section-header'>📊 Portfolio Risk Summary</div>", unsafe_allow_html=True)

    # 🎨 Custom CSS for Cards & Button
    st.markdown("""
    <style>
        .metrics-row {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 25px;
            margin-top: 30px;
            margin-bottom: 40px;
        }
        .metric-card {
            border-radius: 16px;
            padding: 25px 30px;
            width: 260px;
            text-align: center;
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
            transition: all 0.3s ease;
        }
        .metric-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 24px rgba(0,0,0,0.25);
        }
        .prob {background: linear-gradient(135deg, #f8d7da, #f1aeb5);}
        .score {background: linear-gradient(135deg, #d1e7dd, #a3cfbb);}
        .rating {background: linear-gradient(135deg, #cfe2ff, #9ec5fe);}
        .metric-card h3 {
            color: #1b1b1b;
            font-size: 1rem;
            margin-bottom: 8px;
        }
        .metric-card h2 {
            color: black;
            font-size: 1.6rem;
            margin: 0;
            font-weight: 800;
        }
        /* Center Download Button */
        .download-container {
            text-align: center;
            margin-top: 25px;
        }
        .download-container button {
            background: linear-gradient(90deg, #007bff, #00c6ff);
            color: white !important;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            border-radius: 10px;
            padding: 12px 28px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(0,123,255,0.3);
        }
        .download-container button:hover {
            background: linear-gradient(90deg, #0069d9, #00a2ff);
            box-shadow: 0 6px 18px rgba(0,123,255,0.45);
            transform: translateY(-2px);
        }
    </style>
    """, unsafe_allow_html=True)

    # 🧩 Combine All 3 Cards in One Row
    st.markdown(f"""
    <div class="metrics-row">
        <div class="metric-card prob">
            <h3>🔥 Default Probability</h3>
            <h2>{probability:.2%}</h2>
        </div>
        <div class="metric-card score">
            <h3>💳 Credit Score</h3>
            <h2>{credit_score}</h2>
        </div>
        <div class="metric-card rating">
            <h3>⚖️ Risk Rating</h3>
            <h2>{rating}</h2>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ✅ Success Message
    st.success("✅ Risk assessment completed successfully!")

    # 📄 Single Centered Download Button
    pdf_report = generate_pdf()
    # 📄 Stylish Centered Download Button (Glassmorphic)
    st.markdown("""
        <style>
            .download-container {
                display: flex;
                justify-content: center;
                margin-top: 30px;
            }
            .download-btn-custom button {
                background: rgba(0, 123, 255, 0.2);
                backdrop-filter: blur(10px);
                border: 2px solid rgba(255, 255, 255, 0.3);
                color: white !important;
                font-weight: 600;
                font-size: 1rem;
                border-radius: 12px;
                padding: 14px 32px;
                box-shadow: 0 4px 16px rgba(0, 123, 255, 0.3);
                transition: all 0.3s ease;
            }
            .download-btn-custom button:hover {
                background: linear-gradient(90deg, #007bff, #00c6ff);
                color: white;
                transform: translateY(-3px) scale(1.03);
                box-shadow: 0 6px 20px rgba(0, 123, 255, 0.45);
            }
        </style>
        """, unsafe_allow_html=True)

    st.markdown('<div class="download-container download-btn-custom">', unsafe_allow_html=True)
    st.download_button(
        label="📥 Download Credit Risk Report (PDF)",
        data=pdf_report,
        file_name="FinEdge_Credit_Risk_Report.pdf",
        mime="application/pdf",
    )
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------- FOOTER -------------------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<div class='footer'>© 2025 FinEdge Analytics | Developed with ❤️ by <b>Raj Lakshmi</b></div>", unsafe_allow_html=True)
