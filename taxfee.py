import streamlit as st

# 1. ページ構成
st.set_page_config(page_title="不動産資金計画ツール", layout="wide")

# デザイン調整（メニュー非表示・スマホ最適化）
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding-top: 1rem; }
    
    .main-header { 
        color: #2c3e50; font-size: 22px; font-weight: bold; 
        text-align: center; border-bottom: 2px solid #3498db;
        padding-bottom: 10px; margin-bottom: 20px;
    }
    .calc-card {
        background-color: #ffffff; padding: 20px; border-radius: 12px;
        border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .result-label { font-size: 14px; color: #7f8c8d; }
    .result-value { font-size: 24px; font-weight: bold; color: #2980b9; }
    .comparison-box {
        padding: 20px; border-radius: 10px; text-align: center;
        margin-top: 15px; font-weight: bold;
    }
    .buy-win { background-color: #e8f5e9; border: 1px solid #2e7d32; color: #1b5e20; }
    .rent-win { background-color: #fff3e0; border: 1px solid #ef6c00; color: #e65100; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💰 資金計画シミュレーター</div>', unsafe_allow_html=True)

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
tab1, tab2, tab3 = st.tabs(["🏠 売買（購入）", "🏢 賃貸（入居）", "⚖️ 賃貸 VS 購入"])

# --- 計算ロジック（全タブ共通） ---
# 売買：諸経費
broker_fee = (price * 0.03 + 6) * 1.1
reg_fee = price * 0.02
bank_fee = loan_amount * 0.022
total_buy_fee = broker_fee + reg_fee + bank_fee + 20
# ローン控除
deduction_annual = min(loan_amount * 0.007, income * 0.05 + 13.5, 21.0)
# 月々返済（金利0.5% 35年想定）
monthly_repay = (loan_amount*10000*(0.005/12)*(1+0.005/12)**420)/((1+0.005/12)**420-1)

# 賃貸：初期費用
rent_initial = (rent * 4) + (rent * 0.5) + 2.0 # 敷1礼1仲1前1 + 保証 + 保険

# ---------------------------------------------------------
# TAB1: 売買
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 購入時に必要な現金と控除")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<p class="result-label">概算諸経費</p><p class="result-value">{total_buy_fee:.1f} 万円</p>', unsafe_allow_html=True)
        st.caption("内訳: 仲介手数料, 登記費用, 融資事務手数料")
    with c2:
        st.markdown(f'<p class="result-label">ローン控除（年間最大）</p><p class="result-value" style="color:#27ae60;">+{deduction_annual:.1f} 万円</p>', unsafe_allow_html=True)
        st.caption("所得税・住民税から還付される目安")
    st.write(f"**月々のローン返済額: 約 {int(monthly_repay/1000):,} 万円**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB2: 賃貸
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 賃貸入居時の初期費用")
    st.markdown(f'<p class="result-label">入居初期費用（目安）</p><p class="result-value" style="color:#d32f2f;">{rent_initial/10000:.1f} 万円</p>', unsafe_allow_html=True)
    st.write(f"**月々の支払額: {int((rent+10000)/1000):,} 万円**（管理費込）")
    st.caption("※敷金1・礼金1・仲介1・前家賃1・保証会社・火災保険を想定")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB3: 賃貸 VS 購入
# ---------------------------------------------------------
with tab3:
    st.write("### 35年間のトータルコスト比較")
    # 購入35年総額：(返済+維持費3.5万)×35年 + 諸経費 - 控除13年
    buy_35_total = ((monthly_repay + 35000) * 12 * 35 / 10000) + total_buy_fee - (deduction_annual * 13)
    # 賃貸35年総額：(家賃+管理1万)×35年 + 更新料17.5回
    rent_35_total = ((rent + 10000) * 12 * 35 / 10000) + (rent * 17.5 / 10000)
    
    col_a, col_b = st.columns(2)
    col_a.metric("🏠 購入の場合の支出", f"{int(buy_35_total)}万円")
    col_b.metric("🏢 賃貸の場合の支出", f"{int(rent_35_total)}万円")
    
    diff = int(abs(buy_35_total - rent_35_total))
    
    if buy_35_total < rent_35_total:
        st.markdown(f'<div class="comparison-box buy-win">💡 購入の方が {diff}万円 お得！<br>さらに完済後は資産価値のある「家」が手元に残ります。</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="comparison-box rent-win">💡 賃貸の方が {diff}万円 支出少<br>ただし35年後も家賃支払いは続き、資産は残りません。</div>', unsafe_allow_html=True)

st.info("※本ツールは概算です。詳細な資金計画は必ず見積もりをご依頼ください。")
