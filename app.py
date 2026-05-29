import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up clean web page configuration
st.set_page_config(page_title="US Mortgage Underwriting Hub", layout="wide")

st.title("📋 US Mortgage Underwriting & Condo Project Review Hub")
st.write("An automated evaluation system using custom credit tiers, debt risk brackets, and property criteria.")

# --- NEW: PARAMETERS DOCUMENTATION EXPANDER ---
with st.expander("📋 View Underwriting Evaluation Rules & Parameters"):
    st.markdown("""
    ### 🎯 Core Underwriting & Risk Evaluation Brackets

    #### 1. Credit Score Tiers
    * **Excellent (800 - 900):** Instant Approval / Best Deals 🟢
    * **Very Good (740 - 799):** Low Risk / Fast Approval 🟢
    * **Good (670 - 739):** Standard Risk / Standard Rates 🟡
    * **Fair (580 - 669):** High Risk / Strict Review 🟠
    * **Poor (Below 580):** Severe Risk / Auto-Reject 🔴

    #### 2. Debt-to-Income (DTI) Brackets
    * **Excellent (Below 30.00%):** Low Debt Risk 🟢
    * **Good (30.01% - 36.00%):** Manageable Debt 🟡
    * **High Risk (36.01% - 43.00%):** Borderline Strain 🟠
    * **Critical Danger (Over 43.00%):** Too Much Debt / Auto-Reject 🔴

    #### 3. Condo Project Review Matrix
    * **PASSED:** HOA Reserves $\ge$ 10% **AND** No Active Litigation 🟢
    * **REJECTED:** HOA Reserves < 10% 🔴
    * **REJECTED:** Dangerous Active Litigation Present 🔴
    * **REJECTED:** Low Reserves & Active Lawsuit Combined 🔴
    """)

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🕹️ Simulation Configurations")
total_profiles = st.sidebar.slider("Number of Sample Profiles to Generate", 10, 200, 100, step=10)
lawsuit_rate = st.sidebar.slider("Condo Active Litigation Probability (%)", 0, 50, 12, step=1) / 100.0

# Generate Locked Random Data Matrix
np.random.seed(42)
loan_ids = list(range(5001, 5001 + total_profiles))
borrowers = [f"Client_Name_{i}" for i in range(1, total_profiles + 1)]
credit_scores = np.random.randint(300, 901, size=total_profiles) 
gross_income = np.random.randint(15000, 40000, size=total_profiles) 
monthly_debts = np.random.randint(4000, 16000, size=total_profiles)
condo_names = [f"Luxury Plaza Block {i}" for i in range(1, total_profiles + 1)]
hoa_budgets = np.random.randint(100000, 300000, size=total_profiles)
hoa_reserves = [int(b * np.random.uniform(0.06, 0.15)) for b in hoa_budgets]
active_litigation = np.random.choice([True, False], size=total_profiles, p=[lawsuit_rate, 1 - lawsuit_rate])

row_based_records = []

# --- RUN PROCESSING ENGINE ---
for i in range(total_profiles):
    # 1. Credit Score Tier Logic Rules
    score = credit_scores[i]
    if 800 <= score <= 900:
        score_tier = "Excellent (Instant Approval / Best Deals) 🟢"
        credit_status_ok = True
    elif 740 <= score <= 799:
        score_tier = "Very Good (Low Risk / Fast Approval) 🟢"
        credit_status_ok = True
    elif 670 <= score <= 739:
        score_tier = "Good (Standard Risk / Standard Rates) 🟡"
        credit_status_ok = True
    elif 580 <= score <= 669:
        score_tier = "Fair (High Risk / Strict Review) 🟠"
        credit_status_ok = True  
    else:
        score_tier = "Poor (Severe Risk / Auto-Reject) 🔴"
        credit_status_ok = False 

    # 2. Calculated DTI % & DTI Bracket Logic Rules
    dti_calc = (monthly_debts[i] / gross_income[i]) * 100
    if dti_calc < 30.00:
        dti_bracket = "Excellent (Low Debt Risk) 🟢"
        dti_status_ok = True
    elif 30.01 <= dti_calc <= 36.00:
        dti_bracket = "Good (Manageable Debt) 🟡"
        dti_status_ok = True
    elif 36.01 <= dti_calc <= 43.00:
        dti_bracket = "High Risk (Borderline Strain) 🟠"
        dti_status_ok = True
    else:
        dti_bracket = "Critical Danger (Too Much Debt) 🔴"
        dti_status_ok = False 

    # 3. Calculated HOA Reserve % & Property Verdict Logic Rules
    reserve_pct_calc = (hoa_reserves[i] / hoa_budgets[i]) * 100
    condo_has_lawsuit = active_litigation[i]
    
    if reserve_pct_calc >= 10.00 and not condo_has_lawsuit:
        banks_verdict = "PASSED: Condo Project Approved 🟢"
        condo_status_ok = True
    elif reserve_pct_calc < 10.00 and not condo_has_lawsuit:
        banks_verdict = "REJECTED: HOA Reserves Under 10% 🔴"
        condo_status_ok = False
    elif reserve_pct_calc >= 10.00 and condo_has_lawsuit:
        banks_verdict = "REJECTED: Dangerous Active Litigation 🔴"
        condo_status_ok = False
    else:
        banks_verdict = "REJECTED: Low Reserves & Active Lawsuit 🔴"
        condo_status_ok = False

    calculated_loan_amount = gross_income[i] * 12 * 4

    # 4. Final Underwriting Audit Logic Integration
    if credit_status_ok and dti_status_ok and condo_status_ok:
        final_decision = "APPROVED"
        denial_reason = "Clear to Close"
    else:
        final_decision = "DENIED"
        errors = []
        if not credit_status_ok:
            errors.append("Auto-Reject Credit Score")
        if not dti_status_ok:
            errors.append("Over-Leveraged Debt Limit")
        if not condo_status_ok:
            errors.append("Property Checklist Failure")
        denial_reason = " | ".join(errors)
        
    row_based_records.append({
        "Loan ID": loan_ids[i],
        "Borrower Name": borrowers[i],
        "Credit Score": score,
        "Credit Score Tier": score_tier,
        "Gross Monthly Income": f"${gross_income[i]:,}",
        "Total Monthly Debts": f"${monthly_debts[i]:,}",
        "Calculated DTI %": f"{dti_calc:.2f}%",
        "DTI Bracket": dti_bracket,  
        "Condo Project Name": condo_names[i],
        "Total HOA Budget": f"${hoa_budgets[i]:,}",
        "HOA Reserve Savings": f"${hoa_reserves[i]:,}",
        "Calculated HOA Reserve %": f"{reserve_pct_calc:.2f}%",
        "🛑 The Bank's Verdict": banks_verdict,  
        "Active Lawsuit Status": "YES" if active_litigation[i] else "NO",
        "Loan Amount": f"${calculated_loan_amount:,}",  
        "Final Decision": final_decision,
        "Audit Findings": denial_reason
    })

# Convert to tracking table data frame
final_df = pd.DataFrame(row_based_records).sort_values(by="Credit Score", ascending=False)

# --- STAGE 3: VISUAL PIE GRAPHICS LAYER ---
st.subheader("📊 Visual Compliance Distribution Overview")
verdict_counts = final_df["🛑 The Bank's Verdict"].value_counts()
decision_counts = final_df["Final Decision"].value_counts()

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.pie(verdict_counts, labels=verdict_counts.index, autopct='%1.1f%%', startangle=140, colors=['#4f81bd', '#c0504d', '#9bbb59', '#8064a2'], wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
    ax1.set_title("Condo Property Verdict Distribution", fontsize=10, weight='bold')
    st.pyplot(fig1)

with col2:
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    ax2.pie(decision_counts, labels=decision_counts.index, autopct='%1.1f%%', startangle=90, colors=['#36648b', '#95a5a6'], wedgeprops={'edgecolor': 'white', 'linewidth': 1.2})
    ax2.set_title("Final Underwriting Loan Decisions", fontsize=10, weight='bold')
    st.pyplot(fig2)

# --- STAGE 4: DETAILED APPROVED CLIENTS REPORT TABLE ---
st.subheader("🏆 Summary Report: Approved Clients (Clear to Close)")
approved_df = final_df[final_df["Final Decision"] == "APPROVED"]

target_columns = ["Borrower Name", "Loan Amount", "Credit Score", "Credit Score Tier", "Calculated DTI %", "DTI Bracket", "Calculated HOA Reserve %", "🛑 The Bank's Verdict"]
display_approved = approved_df[target_columns].sort_values(by="Borrower Name").reset_index(drop=True)

st.write(f"Total Matches Clear to Close: **{len(display_approved)}** profiles out of **{total_profiles}** generated.")
st.dataframe(display_approved, use_container_width=True)

# --- STAGE 5: EXPORT FULL PIPELINE AS CSV ---
st.subheader("📥 Download Complete Master Audit Pipeline")
st.write(f"Click below to download the complete data sheet containing all {total_profiles} profiles.")

csv_data = final_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Master Data Sheet (CSV)",
    data=csv_data,
    file_name="Underwriting_Dashboard_Report.csv",
    mime="text/csv"
)
