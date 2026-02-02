import streamlit as st
import os
import base64
from datetime import datetime
import time
import pandas as pd

# แก้ไขตัวสะกดตรงนี้ให้ถูกต้องแล้วครับ
try:
    from streamlit_gsheets import GSheetsConnection
except ImportError:
    st.error("ระบบกำลังติดตั้งตัวเชื่อมต่อ Google Sheets... โปรดรอสักครู่แล้ว Refresh หน้าจอครับ")

# --- 1. การตั้งค่าหน้าจอ ---
st.set_page_config(page_title="Space of Us", page_icon="💝", layout="centered")

# --- 2. ฟังก์ชันจัดการพื้นหลัง ---
def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    return ""

def set_bg_and_style(bg_file):
    bin_str = get_base64_of_bin_file(bg_file)
    if bin_str:
        st.markdown(f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            header, footer {{visibility: hidden;}}
            </style>
            """, unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 3. หน้า LOGIN ---
if not st.session_state.authenticated:
    set_bg_and_style("bg_login.png")
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        password = st.text_input("", type="password", placeholder="รหัสผ่านจ้า", key="login_v_final")
        if st.button("เข้าสู่ระบบ 🤍", key="btn_login_v_final", use_container_width=True):
            if password == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("รหัสผิดนะเจ้าอ้วน")
    st.stop()

# --- 4. จัดการสถานะเมนู ---
if 'menu' not in st.session_state:
    st.session_state.menu = None

if st.session_state.menu:
    set_bg_and_style("bg_dashboard.png")
    if st.button("🔙 กลับไปหน้าเมนู", key="back_to_main"):
        st.session_state.menu = None
        st.rerun()
    st.divider()

    # --- หน้า 365 DAYS ---
    if st.session_state.menu == "365days":
        clock_holder = st.empty()
        target = datetime(2027, 2, 14, 0, 0, 0)
        while st.session_state.menu == "365days":
            diff = target - datetime.now()
            if diff.total_seconds() <= 0:
                clock_holder.markdown("<h1 style='text-align:center;'>Happy Anniversary! 💖</h1>", unsafe_allow_html=True)
                break
            d, h, m, s = diff.days, diff.seconds//3600, (diff.seconds//60)%60, diff.seconds%60
            
            my_html = f"""
            <div style="text-align:center; background:rgba(255,255,255,0.85); padding:30px; border-radius:30px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin:auto;">
                <p style="color:#FF4B4B; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">COUNTING DOWN TO OUR DAY</p>
                <div style="font-size:40px; font-weight:bold; font-family:monospace; display:flex; justify-content:center; gap:10px; color:#007BFF;">
                    <div>{d:02d}<br><span style="font-size:10px; color:#555;">DAYS</span></div>
                    <div style="color:#CCC;">:</div>
                    <div>{h:02d}<br><span style="font-size:10px; color:#555;">HRS</span></div>
                    <div style="color:#CCC;">:</div>
                    <div>{m:02d}<br><span style="font-size:10px; color:#555;">MIN</span></div>
                    <div style="color:#CCC;">:</div>
                    <div style="color:#FF4B4B;">{s:02d}<br><span style="font-size:10px; color:#555;">SEC</span></div>
                </div>
                <div style="margin-top:20px; padding:15px; background:#F0F8FF; border-radius:15px; border:1px dashed #007BFF; color:#333; font-size:16px;">
                    "อยู่ด้วยกันมาจะครบปีแล้วนะไอ่หมูอ้วน <br> อยู่ต่อ อยู่อีก ห้ามหนี ห้ามทิ้ง รักบี๋ที่สุดๆๆ ❤️"
                </div>
            </div>
            """
            clock_holder.markdown(my_html, unsafe_allow_html=True)
            time.sleep(1)

    # --- หน้า TANG'S GIFT (เชื่อมต่อ Google Sheets) ---
    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        
        gift_sequence = [
            {"date": "2024-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"},
            {"date": "2024-05-20", "image": "gift2.jpg", "text": "ชิ้นที่ 2: ของขวัญเซอร์ไพรส์จ้า ✨"},
            {"date": "2024-08-12", "image": "gift3.jpg", "text": "ชิ้นที่ 3: คนเก่งของเค้า 💖"},
            {"date": "2024-12-25", "image": "gift4.jpg", "text": "ชิ้นที่ 4: คริสต์มาสนี้มีแค่เรา 🎄"}
        ]

        # เชื่อมต่อ Google Sheets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        def get_opened_data():
            try:
                df = conn.read(ttl=0)
                return dict(zip(df['box_id'], df['gift_index']))
            except:
                return {}

        def save_opened_data(box_id, gift_idx):
            try:
                existing_df = conn.read(ttl=0)
            except:
                existing_df = pd.DataFrame(columns=['box_id', 'gift_index'])
            new_row = pd.DataFrame([{"box_id": box_id, "gift_index": gift_idx}])
            updated_df = pd.concat([existing_df, new_row], ignore_index=True)
            conn.update(data=updated_df)

        opened_status = get_opened_data()
        today = datetime.now().date()
        cols = st.columns(2)
        box_labels = ["กล่องสีแดง 🎈", "กล่องสีฟ้า 💎", "กล่องสีทอง 🏆", "กล่องสีชมพู 🎀"]

        for i in range(4):
            box_id = f"box_{i+1}"
            with cols[i % 2]:
                if box_id in opened_status:
                    idx = int(opened_status[box_id])
                    info = gift_sequence[idx]
                    if os.path.exists(info['image']):
                        st.image(info['image'], caption=info['text'], use_container_width=True)
                    else:
                        st.success(f"🎉 {info['text']}")
                else:
                    current_count = len(opened_status)
                    if current_count < len(gift_sequence):
                        target_info = gift_sequence[current_count]
                        target_date = datetime.strptime(target_info['date'], "%Y-%m-%d").date()
                        if today >= target_date:
                            if st.button(f"🎁 {box_labels[i]}", key=f"gift_{box_id}", use_container_width=True):
                                save_opened_data(box_id, current_count)
                                st.balloons()
                                st.rerun()
                        else:
                            st.button(f"🔒 {box_labels[i]}", key=f"lock_{box_id}", disabled=True, use_container_width=True)

    else:
        st.info(f"หน้า {st.session_state.menu} กำลังรอข้อมูลครับ")

else:
    # --- 5. หน้า DASHBOARD หลัก ---
    set_bg_and_style("bg_dashboard.png")
    st.markdown("""
        <style>
        [data-testid="column"] { display: flex; flex-direction: column; align-items: center; margin-bottom: 25px; }
        [data-testid="stImage"] img { border-radius: 20px 20px 0 0; box-shadow: 0 4px 15px rgba(0,0,0,0.2); object-fit: cover; }
        .stButton > button { width: 100% !important; border-radius: 0 0 20px 20px !important; border: none !important; background: white !important; color: #333 !important; font-weight: bold; height: 45px; }
        </style>
        """, unsafe_allow_html=True)

    st.markdown("<br><h3 style='text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>ของขวัญสำหรับคนเก่ง 💖</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if os.path.exists("gift.jpg"): st.image("gift.jpg", use_container_width=True)
        if st.button("Tang's Gift", key="m1"): st.session_state.menu = "gift"; st.rerun()
        if os.path.exists("memories.jpg"): st.image("memories.jpg", use_container_width=True)
        if st.button("Memories", key="m2"): st.session_state.menu = "memories"; st.rerun()
        if os.path.exists("unseen.jpg"): st.image("unseen.jpg", use_container_width=True)
        if st.button("Unseen", key="m3"): st.session_state.menu = "unseen"; st.rerun()
    with c2:
        if os.path.exists("quiz.jpg"): st.image("quiz.jpg", use_container_width=True)
        if st.button("Quiz", key="m4"): st.session_state.menu = "quiz"; st.rerun()
        if os.path.exists("message.jpg"): st.image("message.jpg", use_container_width=True)
        if st.button("Message", key="m5"): st.session_state.menu = "message"; st.rerun()
        if os.path.exists("365days.jpg"): st.image("365days.jpg", use_container_width=True)
        if st.button("365 Days", key="m6"): st.session_state.menu = "365days"; st.rerun()
