import streamlit as st
import os
import base64
from datetime import datetime
import time
import pandas as pd

# 1. ตั้งค่าหน้าจอและหน้าตาแอป
st.set_page_config(page_title="Space of Us", page_icon="💝", layout="centered")

try:
    from streamlit_gsheets import GSheetsConnection
except ImportError:
    st.error("กำลังเตรียมระบบ... กรุณารอสักครู่ครับ")

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

# 2. ส่วนของหน้า LOGIN
if not st.session_state.authenticated:
    set_bg_and_style("bg_login.png")
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        password = st.text_input("", type="password", placeholder="รหัสผ่านจ้า", key="login_final")
        if st.button("เข้าสู่ระบบ 🤍", use_container_width=True):
            if password == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("รหัสผิดนะเจ้าอ้วน")
    st.stop()

# 3. จัดการเมนูหลัก
if 'menu' not in st.session_state:
    st.session_state.menu = None

if st.session_state.menu:
    set_bg_and_style("bg_dashboard.png")
    if st.button("🔙 กลับไปหน้าเมนู"):
        st.session_state.menu = None
        st.rerun()
    st.divider()

    # --- เมนู TANG'S GIFT (ส่วนที่เชื่อมต่อ Google Sheets) ---
    if st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        
        # รายการของขวัญ
        gift_sequence = [
            {"date": "2024-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"},
            {"date": "2024-05-20", "image": "gift2.jpg", "text": "ชิ้นที่ 2: ของขวัญเซอร์ไพรส์จ้า ✨"},
            {"date": "2024-08-12", "image": "gift3.jpg", "text": "ชิ้นที่ 3: คนเก่งของเค้า 💖"},
            {"date": "2024-12-25", "image": "gift4.jpg", "text": "ชิ้นที่ 4: คริสต์มาสนี้มีแค่เรา 🎄"}
        ]

        # เชื่อมต่อกับ Google Sheets แผ่นงานชื่อ GiftStatus
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        def get_opened_data():
            try:
                # อ่านข้อมูลจาก Google Sheets (Worksheet: GiftStatus)
                df = conn.read(worksheet="GiftStatus", ttl=0)
                return dict(zip(df['box_id'], df['gift_index']))
            except Exception:
                return {}

        def save_opened_data(box_id, gift_idx):
            try:
                # ดึงข้อมูลเดิมมาอัปเดต
                existing_df = conn.read(worksheet="GiftStatus", ttl=0)
                new_row = pd.DataFrame([{"box_id": box_id, "gift_index": gift_idx}])
                if existing_df is not None:
                    updated_df = pd.concat([existing_df, new_row], ignore_index=True)
                else:
                    updated_df = new_row
                
                # บันทึกกลับไปยัง Google Sheets
                conn.update(worksheet="GiftStatus", data=updated_df)
                st.balloons()
                st.success("บันทึกความทรงจำเรียบร้อยแล้ว!")
                time.sleep(1)
            except Exception as e:
                st.error(f"บันทึกไม่สำเร็จ: {e}")

        opened_status = get_opened_data()
        today = datetime.now().date()
        cols = st.columns(2)
        box_labels = ["กล่องสีแดง 🎈", "กล่องสีฟ้า 💎", "กล่องสีทอง 🏆", "กล่องสีชมพู 🎀"]

        for i in range(4):
            b_id = f"box_{i+1}"
            with cols[i % 2]:
                if b_id in opened_status:
                    idx = int(opened_status[b_id])
                    info = gift_sequence[idx]
                    if os.path.exists(info['image']):
                        st.image(info['image'], caption=info['text'], use_container_width=True)
                    else:
                        st.success(f"🎉 {info['text']}")
                else:
                    opened_count = len(opened_status)
                    if opened_count < len(gift_sequence):
                        g_info = gift_sequence[opened_count]
                        g_date = datetime.strptime(g_info['date'], "%Y-%m-%d").date()
                        if today >= g_date:
                            if st.button(f"🎁 {box_labels[i]}", key=f"btn_{b_id}", use_container_width=True):
                                save_opened_data(b_id, opened_count)
                                st.rerun()
                        else:
                            st.button(f"🔒 {box_labels[i]}", disabled=True, use_container_width=True)

    # --- เมนู 365 DAYS ---
    elif st.session_state.menu == "365days":
        target = datetime(2027, 2, 14, 0, 0, 0)
        diff = target - datetime.now()
        d, h, m, s = diff.days, diff.seconds//3600, (diff.seconds//60)%60, diff.seconds%60
        st.metric("Counting down to our day", f"{d} Days {h:02d}:{m:02d}:{s:02d}")

else:
    # หน้า DASHBOARD หลัก
    set_bg_and_style("bg_dashboard.png")
    st.markdown("<h3 style='text-align: center; color: white;'>ของขวัญสำหรับคนเก่ง 💖</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Tang's Gift"): st.session_state.menu = "gift"; st.rerun()
    with c2:
        if st.button("365 Days"): st.session_state.menu = "365days"; st.rerun()
