import streamlit as st

# 1. ページ構成（タイトルを「賃貸 VS 購入」に設定）
st.set_page_config(page_title="賃貸 VS 購入", layout="wide")

# デザイン調整
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; }
    
    .main-header { 
        color: #2c3e50; font-size: 24px; font-weight: bold; 
        text-align: center; border-bottom: 3px solid #e74c3c;
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .calc-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .result-label { font-size: 14px; color: #7f8c8d; }
    .result-value { font-size: 24px; font-weight: bold; color: #e74c3c; }
    .detail-text { font-size: 14px; color: #444; line-height: 1.8; }
    </style>
""", unsafe_allow_html=True)

# アプリのメインタイトル
st.markdown('<div class="main-header">⚖️ 賃貸 VS 購入 シミュレーター</div>', unsafe_allow_html=True)

# --- 共通入力エリア ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("物件価格（万円）", value=4500, step=100)
        loan_amount = st.number_input("ローン借入額（万円）", value=4500, step=100)
    with col2:
        rent = st.number_input("比較用の家賃（月/円）", value=140000, step=5000)
        income = st.number_input("世帯年収（万円）", value=600, step=50)

# --- タブ分け ---
tab1, tab2, tab3 = st.tabs(["⚖️ 賃貸 VS 購入", "🏠 売買（購入）の詳細", "🏢 賃貸（入居）の詳細"])

# --- 計算ロジック ---
# 売買
broker_fee = (price * 0.03 + 6) * 1.1        # 仲介手数料
reg_tax = price * 0.015                     # 登録免許税(概算)
judicial_scrivener = 10.0                   # 司法書士報酬
bank_fee = loan_amount * 0.022              # 融資事務手数料
stamp_duty = 2.0                            # 印紙代
insurance = 15.0                            # 火災保険(概算)
total_buy_fee = broker_fee + reg_tax + judicial_scrivener + bank_fee + stamp_duty + insurance

# ローン控除・返済額
deduction_annual = min(loan_amount * 0.007, income * 0.05 + 13.5, 21.0)
monthly_repay = (loan_amount*10000*(0.005/12)*(1+0.005/12)**420)/((1+0.005/12)**420-1)

# 賃貸
rent_initial = (rent * 4) + (rent * 0.5) + 2.0

# ---------------------------------------------------------
# TAB1: 賃貸 VS 購入（メイン比較）
# ---------------------------------------------------------
with tab1:
    st.write("### 35年間の支出合計を比較")
    # 購入35年総額：(返済+維持費3.5万)×35年 + 諸経費 - 控除13年
    buy_35_total = ((monthly_repay + 35000) * 12 * 35 / 10000) + total_buy_fee - (deduction_annual * 13)
    # 賃貸35年総額：(家賃+管理1万)×35年 + 更新料17.5回
    rent_35_total = ((rent + 10000) * 12 * 35 / 10000) + (rent * 17.5 / 10000)
    
    col_a, col_b = st.columns(2)
    col_a.metric("🏠 購入の場合の総支出", f"{int(buy_35_total)}万円")
    col_b.metric("🏢 賃貸の場合の総支出", f"{int(rent_35_total)}万円")
    
    diff = int(abs(buy_35_total - rent_35_total))
    
    if buy_35_total < rent_35_total:
        st.markdown(f"""
        <div class="comparison-box" style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; border: 1px solid #2e7d32; text-align: center;">
            <h4 style="color: #1b5e20;">💡 購入の方が {diff}万円 お得です</h4>
            <p style="color: #1b5e20;">完済後は住居費が大幅に減り、手元に「資産」が残ります。</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="comparison-box" style="background-color: #fff3e0; padding: 20px; border-radius: 10px; border: 1px solid #ef6c00; text-align: center;">
            <h4 style="color: #e65100;">💡 賃貸の方が {diff}万円 支出を抑えられます</h4>
            <p style="color: #e65100;">ただし、将来にわたって家賃が発生し続け、資産形成にはなりません。</p>
        </div>
        """, unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB2: 売買（購入）の詳細
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 購入諸経費と減税の内訳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<p class="result-label">概算諸経費（合計）</p><p class="result-value">{total_buy_fee:.1f} 万円</p>', unsafe_allow_html=True)
        with st.expander("🔍 内訳を確認"):
            st.markdown(f"""
            ・仲介手数料： {broker_fee:.1f}万円<br>
            ・融資手数料： {bank_fee:.1f}万円<br>
            ・登記・保険他： {reg_tax + judicial_scrivener + insurance + stamp_duty:.1f}万円
            """, unsafe_allow_html=True)
    with c2:
        st.markdown(f'<p class="result-label">ローン控除（年間最大）</p><p class="result-value" style="color:#27ae60;">+{deduction_annual:.1f} 万円</p>', unsafe_allow_html=True)
    st.write(f"**月々のローン返済額: 約 {int(monthly_repay/1000):,} 万円**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB
