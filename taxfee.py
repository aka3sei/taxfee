import streamlit as st

# --- ページ全体のデザイン調整 ---
st.markdown("""
    <style>
    .calc-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 20px;
    }
    .result-label { font-size: 14px; color: #666; }
    .result-value { font-size: 22px; font-weight: bold; color: #1a73e8; }
    .red-value { color: #d32f2f; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💰 資金計画シミュレーション</div>', unsafe_allow_html=True)

# 賃貸と売買を切り替えるタブ
tab1, tab2 = st.tabs(["🏠 売買（購入）", "🏢 賃貸（入居）"])

# ---------------------------------------------------------
# TAB1: 売買シミュレーション
# ---------------------------------------------------------
with tab1:
    st.subheader("物件購入の総額・減税計算")
    c1, c2 = st.columns(2)
    with c1:
        buy_price = st.number_input("物件価格（万円）", value=4000, step=100, key="buy_p")
        loan_amt = st.number_input("ローン借入額（万円）", value=3800, step=100)
    with c2:
        income = st.number_input("世帯年収（万円）", value=600, step=50, key="inc_b")
        period = st.selectbox("借入期間（年）", [35, 30, 25, 20], index=0)

    # 計算ロジック（売買）
    brokerage = (buy_price * 0.03 + 6) * 1.1  # 仲介手数料
    registration = buy_price * 0.02           # 登記費用・印紙
    bank_fee = 5.5 + (loan_amt * 0.022)       # 融資手数料（2.2%想定）
    buy_total_costs = brokerage + registration + bank_fee + 20 # 諸経費合計
    
    # 住宅ローン控除
    deduction = min(loan_amt * 0.007, 21.0) # 最大21万（中古）想定

    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    res_c1, res_c2 = st.columns(2)
    with res_c1:
        st.markdown('<p class="result-label">概算諸経費（現金準備）</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-value">{buy_total_costs:.1f} 万円</p>', unsafe_allow_html=True)
    with res_c2:
        st.markdown('<p class="result-label">ローン控除（年間最大）</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-value" style="color:#2e7d32;">+{deduction:.1f} 万円/年</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB2: 賃貸シミュレーション
# ---------------------------------------------------------
with tab2:
    st.subheader("賃貸入居の初期費用・更新料")
    c1, c2 = st.columns(2)
    with c1:
        rent = st.number_input("月額家賃（円）", value=120000, step=5000)
        management_fee = st.number_input("管理費・共益費（円）", value=8000, step=1000)
    with c2:
        shikikin = st.slider("敷金（ヶ月）", 0, 2, 1)
        reikin = st.slider("礼金（ヶ月）", 0, 2, 1)

    # 計算ロジック（賃貸）
    rent_brokerage = rent * 1.1               # 仲介手数料1ヶ月+税
    guarantee_fee = (rent + management_fee) * 0.5 # 保証会社（初回50%）
    insurance = 2.0                            # 火災保険
    rent_initial_total = (rent * shikikin) + (rent * reikin) + rent_brokerage + guarantee_fee + insurance + (rent/30*15) # 前家賃15日計算
    
    # 2年間の総コスト（更新料込）
    two_year_cost = ((rent + management_fee) * 24) + rent_initial_total + rent # 更新料1ヶ月込

    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    res_c3, res_c4 = st.columns(2)
    with res_c3:
        st.markdown('<p class="result-label">入居初期費用（目安）</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-value red-value">{rent_initial_total/10000:.1f} 万円</p>', unsafe_allow_html=True)
    with res_c4:
        st.markdown('<p class="result-label">2年間の総支払額</p>', unsafe_allow_html=True)
        st.markdown(f'<p class="result-value">{two_year_cost/10000:.1f} 万円</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.info("💡 「売買」は資産が残りますが、「賃貸」は掛け捨てとなります。この差を比較してご提案ください。")