import streamlit as st
import os
import base64
from datetime import datetime
import time

# 1. การตั้งค่าหน้าจอ
st.set_page_config(page_title="Space of Us", page_icon="💝", layout="centered")

# --- ระบบบันทึกข้อมูลแบบไฟล์ (Status.txt) ---
def get_saved_status():
    if os.path.exists("status.txt"):
        try:
            with open("status.txt", "r") as f:
                lines = f.readlines()
                return {line.split(',')[0]: line.split(',')[1].strip() for line in lines if ',' in line}
        except: return {}
    return {}

def save_status(box_id, gift_idx):
    with open("status.txt", "a") as f:
        f.write(f"{box_id},{gift_idx}\n")

# --- ฟังก์ชันจัดการพื้นหลังและสไตล์ ---
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

# 2. หน้า LOGIN
if not st.session_state.authenticated:
    set_bg_and_style("bg_login.png")
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        password = st.text_input("", type="password", placeholder="รหัสผ่านจ้า", key="login_pass")
        if st.button("เข้าสู่ระบบ 🤍", use_container_width=True):
            if password == "1234":
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("รหัสผิดนะเจ้าอ้วน")
    st.stop()

# 3. จัดการสถานะเมนู
if 'menu' not in st.session_state:
    st.session_state.menu = None

if st.session_state.menu:
    set_bg_and_style("bg_dashboard.png")
    if st.button("🔙 กลับไปหน้าเมนู"):
        st.session_state.menu = None
        st.rerun()
    st.divider()

    # --- หน้า 365 DAYS (นาฬิกาดีไซน์เดิม) ---
    if st.session_state.menu == "365days":
        clock_holder = st.empty()
        target = datetime(2027, 2, 14, 0, 0, 0)
        while st.session_state.menu == "365days":
            diff = target - datetime.now()
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
            </div>
            """
            clock_holder.markdown(my_html, unsafe_allow_html=True)
            time.sleep(1)

    # --- หน้า TANG'S GIFT (ระบบบันทึกแบบไฟล์) ---
    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        # บี๋แก้วันที่เปิดกล่องตรงนี้จ้า
        gift_sequence = [
            {"date": "2024-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"},
            {"date": "2024-05-20", "image": "gift2.jpg", "text": "ชิ้นที่ 2: ของขวัญเซอร์ไพรส์จ้า ✨"},
            {"date": "2024-08-12", "image": "gift3.jpg", "text": "ชิ้นที่ 3: คนเก่งของเค้า 💖"},
            {"date": "2024-12-25", "image": "gift4.jpg", "text": "ชิ้นที่ 4: คริสต์มาสนี้มีแค่เรา 🎄"}
        ]
        opened_status = get_saved_status()
        today = datetime.now().date()
        cols = st.columns(2)
        box_labels = ["กล่องสีแดง 🎈", "กล่องสีฟ้า 💎", "กล่องสีทอง 🏆", "กล่องสีชมพู 🎀"]
        
        for i in range(4):
            b_id = f"box_{i+1}"
            with cols[i % 2]:
                if b_id in opened_status:
                    idx = int(opened_status[b_id])
                    info = gift_sequence[idx]
                    st.success(f"🎉 {info['text']}")
                    if os.path.exists(info['image']):
                        st.image(info['image'], use_container_width=True)
                else:
                    count = len(opened_status)
                    if count < len(gift_sequence):
                        g_date = datetime.strptime(gift_sequence[count]['date'], "%Y-%m-%d").date()
                        if today >= g_date:
                            if st.button(f"🎁 {box_labels[i]}", key=f"g_{b_id}", use_container_width=True):
                                save_status(b_id, count)
                                st.balloons()
                                st.rerun()
                        else:
                            st.button(f"🔒 {box_labels[i]}", key=f"l_{b_id}", disabled=True, use_container_width=True)

    else:
        st.info(f"หน้า {st.session_state.menu} อยู่ในขั้นตอนการผลิตจ้าา")

else:
    # 4. หน้า DASHBOARD หลัก (6 ปุ่ม + โชว์รูปภาพ)
    set_bg_and_style("bg_dashboard.png")
    st.markdown("<br><h3 style='text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);'>Our Special Space 💖</h3>", unsafe_allow_html=True)
    
    menu_items = [
        {"id": "365days", "label": "📅 365 Days", "img": "365days.jpg"},
        {"id": "gift", "label": "🎁 Tang's Gift", "img": "gift.jpg"},
        {"id": "memories", "label": "📸 Memories", "img": "memories.jpg"},
        {"id": "unseen", "label": "🎥 Unseen", "img": "unseen.jpg"},
        {"id": "quiz", "label": "🧩 Quiz", "img": "quiz.jpg"},
        {"id": "message", "label": "💌 Message", "img": "message.jpg"}
    ]
    
    cols = st.columns(2)
    for i, item in enumerate(menu_items):
        with cols[i % 2]:
            if os.path.exists(item['img']):
                st.image(item['img'], use_container_width=True)
            if st.button(item['label'], key=f"m_{item['id']}", use_container_width=True):
                st.session_state.menu = item['id']
                st.rerun()
