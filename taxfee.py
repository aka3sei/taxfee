import streamlit as st

# 1. ページ構成（スマホ最適化）
st.set_page_config(page_title="不動産資金計画ツール", layout="wide")

# デザイン調整（3本線・ヘッダー非表示、カード型デザイン）
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
    .calc-section {
        background-color: #ffffff; padding: 15px; border-radius: 12px;
        border: 1px solid #e0e0e0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .label { font-size: 13px; color: #7f8c8d; }
    .value { font-size: 20px; font-weight: bold; color: #2980b9; }
    .diff-box {
        padding: 15px; border-radius: 10px; text-align: center;
        font-weight: bold; margin-top: 10px;
    }
    .buy-color { background-color: #ebf5fb; border-left: 5px solid #3498db; }
    .rent-color { background-color: #fef9e7; border-left: 5px solid #f1c40f; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💰 資金計画・比較シミュレーター</div>', unsafe_allow_html=True)

# --- 入力セクション（ここですべての基本を決める） ---
with st.expander("📝 物件・条件を入力する", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        price = st.number_input("物件価格（万円）", value=4500, step=100)
        income = st.number_input("世帯年収（万円）", value=600, step=50)
    with col2:
        rent = st.number_input("比較用の家賃（月/円）", value=140000, step=5000)
        interest = st.number_input("住宅ローン金利（％）", value=0.5, step=0.1)

# --- 計算ロジック ---
# ① 売買の諸費用
broker_fee = (price * 0.03 + 6) * 1.1
reg_fee = price * 0.02
bank_fee = price * 0.022
total_buy_fee = broker_fee + reg_fee + bank_fee + 20 # その他保険等

# ② 住宅ローン控除（簡易計算：借入0.7% vs 納税額）
deduction_annual = min(price * 0.007, income * 0.05 + 13.5, 21.0)

# ③ 比較（35年総支出）
# 購入：(返済+維持費)×35年 + 諸経費 - 控除
monthly_repay = (price*10000*(interest/12/100)*(1+interest/12/100)**420)/((1+interest/12/100)**420-1)
buy_35yr = ((monthly_repay + 35000) * 12 * 35 / 10000) + total_buy_fee - (deduction_annual * 13)
# 賃貸：(家賃+共益費)×35年 + 更新料
rent_35yr = ((rent + 10000) * 12 * 35 / 10000) + (rent * 17 / 10000)

# --- 表示セクション ---

# 1. 売買（購入）の詳細
st.markdown('<div class="calc-section buy-color">', unsafe_allow_html=True)
st.write("🏠 **【購入】諸費用と減税**")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<p class="label">初期諸費用</p><p class="value">{total_buy_fee:.1f}万</p>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<p class="label">月々返済</p><p class="value">{int(monthly_repay/1000):,}万</p>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<p class="label">ローン控除/年</p><p class="value" style="color:#27ae60;">+{deduction_annual:.1f}万</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# 2. 比較（借りる VS 買う）
st.write("⚖️ **35年間のトータル支出比較**")
col_buy, col_rent = st.columns(2)
col_buy.metric("「買う」総支出", f"{int(buy_35yr)}万円")
col_rent.metric("「借りる」総支出", f"{int(rent_35yr)}万円")

diff = int(abs(buy_35yr - rent_35yr))
if buy_35yr < rent_35yr:
    st.success(f"💡 購入の方が {diff}万円 お得です。さらに完済後は資産が残ります。")
else:
    st.warning(f"💡 賃貸の方が {diff}万円 支出が抑えられます。ただし資産は残りません。")

# 3. 減税・税金についての補足
with st.expander("ℹ️ 税金・減税の計算根拠"):
    st.write(f"・**仲介手数料**: {broker_fee:.1f}万円（上限額）")
    st.write(f"・**住宅ローン控除**: 年間最大{deduction_annual:.1f}万円を13年間想定")
    st.write(f"・**固定資産税/修繕**: 年間約42万円（月3.5万）を維持費として加算")

st.caption("※本計算は概算です。正確な資金計画は必ず詳細見積もりを依頼してください。")
