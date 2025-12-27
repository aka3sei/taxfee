import streamlit as st

# 1. ページ構成
st.set_page_config(page_title="不動産資金計画ツール", layout="wide")

# デザイン調整
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
    .detail-text { font-size: 14px; color: #444; line-height: 1.8; }
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
# TAB1: 売買
# ---------------------------------------------------------
with tab1:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 購入時に必要な現金と控除")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<p class="result-label">概算諸経費 合計</p><p class="result-value">{total_buy_fee:.1f} 万円</p>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<p class="result-label">ローン控除（年間最大）</p><p class="result-value" style="color:#27ae60;">+{deduction_annual:.1f} 万円</p>', unsafe_allow_html=True)

    # 【新機能】詳細内訳を表示するアコーディオン
    with st.expander("🔍 諸経費の内訳を確認する"):
        st.markdown(f"""
        <div class="detail-text">
        ・仲介手数料（3%+6万+税）： <b>{broker_fee:.1f} 万円</b><br>
        ・融資事務手数料（2.2%）： <b>{bank_fee:.1f} 万円</b><br>
        ・登記費用（税+報酬概算）： <b>{reg_tax + judicial_scrivener:.1f} 万円</b><br>
        ・火災保険料（概算）： <b>{insurance:.1f} 万円</b><br>
        ・印紙代・その他： <b>約 {stamp_duty:.1f} 万円</b>
        </div>
        """, unsafe_allow_html=True)
        st.caption("※登記費用は物件の評価額により変動します。")
    
    st.write(f"**月々のローン返済額: 約 {int(monthly_repay/1000):,} 万円**")
    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# TAB2・TAB3（中身は前回のまま）
# ---------------------------------------------------------
with tab2:
    st.markdown('<div class="calc-card">', unsafe_allow_html=True)
    st.write("### 賃貸入居時の初期費用")
    st.markdown(f'<p class="result-label">入居初期費用（目安）</p><p class="result-value" style="color:#d32f2f;">{rent_initial/10000:.1f} 万円</p>', unsafe_allow_html=True)
    with st.expander("🔍 初期費用の内訳"):
        st.write(f"・前家賃・敷金・礼金・仲介料（4ヶ月分）: {rent*4/10000:.1f}万円")
        st.write(f"・保証会社初回費用（0.5ヶ月分）: {rent*0.5/10000:.1f}万円")
        st.write(f"・火災保険・その他: 2.0万円")
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.write("### 35年間のトータルコスト比較")
    buy_35_total = ((monthly_repay + 35000) * 12 * 35 / 10000) + total_buy_fee - (deduction_annual * 13)
    rent_35_total = ((rent + 10000) * 12 * 35 / 10000) + (rent * 17.5 / 10000)
    col_a, col_b = st.columns(2)
    col_a.metric("🏠 購入の場合", f"{int(buy_35_total)}万円")
    col_b.metric("🏢 賃貸の場合", f"{int(rent_35_total)}万円")
    diff = int(abs(buy_35_total - rent_35_total))
    if buy_35_total < rent_35_total:
        st.success(f"💡 購入の方が {diff}万円 お得！")
    else:
        st.warning(f"💡 賃貸の方が {diff}万円 支出少")
