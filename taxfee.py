import streamlit as st

# 1. ページ構成
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
    .detail-text { font-size: 14px; color: #444; line-height: 1.8; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">⚖️ 賃貸 VS 購入 シミュレーター</div>', unsafe_allow_html=True)

# --- 共通入力エリア ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("物件価格（万円）", value=5000, step=100)
        loan_amount = st.number_input("ローン借入額（万円）", value=5000, step=100)
    with col2:
        rent = st.number_input("比較用の家賃（月/円）", value=140000, step=5000)
        income = st.number_input("世帯年収（万円）", value=600, step=50)

# --- 【重要】計算ロジック ---
# 売買関連
broker_fee = (price * 0.03 + 6) * 1.1
bank_fee = loan_amount * 0.022

# 登記関連を分解（修正箇所）
reg_tax_only = price * 0.013  # 登録免許税のみ（概算1.3%）
judicial_scrivener_fee = 10.0 # 司法書士報酬（固定概算）

# 印紙税（最新の合算ロジック）
if price <= 5000:
    base_stamp = 1.0
elif price <= 10000:
    base_stamp = 3.0
else:
    base_stamp = 6.0

loan_stamp = 0.0
if loan_amount > 0:
    if loan_amount <= 5000:
        loan_stamp = 2.0
    elif loan_amount <= 10000:
        loan_stamp = 6.0
    else:
        loan_stamp = 10.0
stamp_duty = base_stamp + loan_stamp

insurance = 15.0 # 火災保険料

# 全体合計
total_buy_fee = broker_fee + reg_tax_only + judicial_scrivener_fee + bank_fee + stamp_duty + insurance
deduction_annual = min(loan_amount * 0.007, income * 0.05 + 13.5, 21.0)
monthly_repay = (loan_amount*10000*(0.005/12)*(1+0.005/12)**420)/((1+0.005/12)**420-1)

# 賃貸関連
rent_initial = (rent * 4) + (rent * 0.5) + 20000

# --- タブの定義 ---
tab1, tab2, tab3 = st.tabs(["🏠 1. 売買（購入）の詳細", "🏢 2. 賃貸（入居）の詳細", "⚖️ 3. 賃貸 VS 購入"])

# ---------------------------------------------------------
# TAB1: 売買（購入）の詳細
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 購入諸経費と減税の内訳")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<p class="result-label">概算諸経費 合計</p><p class="result-value">{total_buy_fee:.1f} 万円</p>', unsafe_allow_html=True)
        with st.expander("🔍 内訳を確認"):
            # 修正箇所：登記関連を2つに分けて表示
            st.markdown(f"""
            ・仲介手数料： {broker_fee:.1f}万円<br>
            ・融資事務手数料： {bank_fee:.1f}万円<br>
            ・登録免許税（税金）： {reg_tax_only:.1f}万円<br>
            ・司法書士報酬： {judicial_scrivener_fee:.1f}万円<br>
            ・火災保険料： {insurance:.1f}万円<br>
            ・印紙税： {stamp_duty:.1f}万円（売買{base_stamp}万 + ローン{loan_stamp}万）
            """, unsafe_allow_html=True)
    with c2:
        st.markdown(f'<p class="result-label">ローン控除（年間最大）</p><p class="result-value" style="color:#27ae60;">+{deduction_annual:.1f} 万円</p>', unsafe_allow_html=True)
    
    st.write(f"**月々のローン返済額: 約 {int(monthly_repay):,} 円**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB2: 賃貸（入居）の詳細
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 賃貸入居の初期費用内訳")
    st.markdown(f'<p class="result-label">初期費用 合計（目安）</p><p class="result-value" style="color:#d32f2f;">{rent_initial/10000:.1f} 万円</p>', unsafe_allow_html=True)
    with st.expander("🔍 内訳を確認"):
        st.write(f"・前賃料・敷金・礼金・仲介料（4ヶ月）: {rent*4/10000:.1f}万円")
        st.write(f"・保証会社初回・火災保険他: { (rent*0.5 + 20000)/10000:.1f}万円")
    
    st.write(f"**月々の支払額: 約 {int(rent+10000):,} 円**（管理費込）")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB3: 賃貸 VS 購入
# ---------------------------------------------------------
with tab3:
    st.write("### 35年間の支出合計を比較")
    buy_35_total = ((monthly_repay + 35000) * 12 * 35 / 10000) + total_buy_fee - (deduction_annual * 13)
    rent_35_total = ((rent + 10000) * 12 * 35 / 10000) + (rent * 17.5 / 10000)
    
    col_a, col_b = st.columns(2)
    col_a.metric("🏠 購入の35年総支出", f"{int(buy_35_total):,}万円")
    col_b.metric("🏢 賃貸の35年総支出", f"{int(rent_35_total):,}万円")
    
    diff = int(abs(buy_35_total - rent_35_total))
    
    if buy_35_total < rent_35_total:
        st.success(f"💡 購入の方が {diff:,}万円 お得です。さらに資産が残ります。")
    else:
        st.warning(f"💡 賃貸の方が {diff:,}万円 支出を抑えられます。")

st.info("※本数値は概算です。正確な資金計画は担当者へご相談ください。")
