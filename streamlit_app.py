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
                # คืนค่าเป็น List ของ box_id ที่เคยเปิดไปแล้ว
                return [line.split(',')[0] for line in lines if ',' in line]
        except: return []
    return []

def save_status(box_id, gift_idx):
    with open("status.txt", "a") as f:
        f.write(f"{box_id},{gift_idx}\n")

# --- ฟังก์ชันจัดการพื้นหลัง ---
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

    # --- หน้า 365 DAYS ---
    if st.session_state.menu == "365days":
        clock_holder = st.empty()
        target = datetime(2027, 2, 14, 0, 0, 0)
        while st.session_state.menu == "365days":
            diff = target - datetime.now()
            d, h, m, s = diff.days, diff.seconds//3600, (diff.seconds//60)%60, diff.seconds%60
            my_html = f"""<div style="text-align:center; background:rgba(255,255,255,0.85); padding:30px; border-radius:30px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin:auto;">
                <p style="color:#FF4B4B; font-weight:bold; letter-spacing:1px; margin-bottom:15px;">COUNTING DOWN TO OUR DAY</p>
                <div style="font-size:40px; font-weight:bold; font-family:monospace; display:flex; justify-content:center; gap:10px; color:#007BFF;">
                    <div>{d:02d}<br><span style="font-size:10px; color:#555;">DAYS</span></div><div style="color:#CCC;">:</div>
                    <div>{h:02d}<br><span style="font-size:10px; color:#555;">HRS</span></div><div style="color:#CCC;">:</div>
                    <div>{m:02d}<br><span style="font-size:10px; color:#555;">MIN</span></div><div style="color:#CCC;">:</div>
                    <div style="color:#FF4B4B;">{s:02d}<br><span style="font-size:10px; color:#555;">SEC</span></div>
                </div></div>"""
            clock_holder.markdown(my_html, unsafe_allow_html=True)
            time.sleep(1)

    # --- หน้า TANG'S GIFT (ระบบสุ่มกล่อง แต่รันของขวัญตามลำดับ) ---
    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        
        # ลำดับของขวัญที่บี๋ตั้งไว้
        gift_sequence = [
            {"date": "2026-02-3", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"},
            {"date": "2026-05-20", "image": "gift2.jpg", "text": "ชิ้นที่ 2: ของขวัญเซอร์ไพรส์จ้า ✨"},
            {"date": "2026-08-12", "image": "gift3.jpg", "text": "ชิ้นที่ 3: คนเก่งของเค้า 💖"},
            {"date": "2026-12-25", "image": "gift4.jpg", "text": "ชิ้นที่ 4: คริสต์มาสนี้มีแค่เรา 🎄"}
        ]
        
        # ดึงว่ามีกล่องไหนถูกเปิดไปบ้างแล้ว
        opened_boxes = get_saved_status() # คืนค่าเป็น list เช่น ['box_1', 'box_3']
        today = datetime.now().date()
        
        cols = st.columns(2)
        box_ids = ["box_1", "box_2", "box_3", "box_4"]
        box_labels = ["กล่องสีแดง 🎈", "กล่องสีฟ้า 💎", "กล่องสีทอง 🏆", "กล่องสีชมพู 🎀"]
        
        # วนลูปสร้าง 4 กล่อง
        for i, b_id in enumerate(box_ids):
            with cols[i % 2]:
                if b_id in opened_boxes:
                    # ถ้ากล่องนี้เคยถูกกดเปิดไปแล้ว ให้หาว่ามันคือลำดับที่เท่าไหร่ในไฟล์
                    gift_idx = opened_boxes.index(b_id)
                    info = gift_sequence[gift_idx]
                    st.success(f"🎉 {info['text']}")
                    if os.path.exists(info['image']):
                        st.image(info['image'], use_container_width=True)
                else:
                    # กล่องยังไม่ถูกเปิด ให้เช็คว่า "ชิ้นถัดไป" ถึงวันเปิดหรือยัง
                    next_gift_idx = len(opened_boxes)
                    if next_gift_idx < len(gift_sequence):
                        g_info = gift_sequence[next_gift_idx]
                        g_date = datetime.strptime(g_info['date'], "%Y-%m-%d").date()
                        
                        if today >= g_date:
                            if st.button(f"🎁 {box_labels[i]}", key=f"g_{b_id}", use_container_width=True):
                                save_status(b_id, next_gift_idx)
                                st.balloons()
                                st.rerun()
                        else:
                            st.button(f"🔒 {box_labels[i]}", key=f"l_{b_id}", disabled=True, use_container_width=True)
                    else:
                        # กรณีเปิดครบหมดทุกชิ้นแล้วแต่ยังมีกล่องเหลือ
                        st.button(f"📦 {box_labels[i]} (ว่างเปล่า)", disabled=True, use_container_width=True)

    else:
        st.info(f"หน้า {st.session_state.menu} กำลังสร้างอยู่นะครับ")

else:
    # 4. หน้า DASHBOARD หลัก
    set_bg_and_style("bg_dashboard.png")
    st.markdown("<br><h3 style='text-align: center; color: white;'>Our Special Space 💖</h3>", unsafe_allow_html=True)
    
    menu_items = [
        {"id": "quiz", "label": "🧩 Quiz", "img": "quiz.jpg"},
        {"id": "365days", "label": "📅 365 Days", "img": "365days.jpg"},
        {"id": "memories", "label": "📸 Memories", "img": "memories.jpg"},
        {"id": "message", "label": "💌 Message", "img": "message.jpg"},
        {"id": "gift", "label": "🎁 Tang's Gift", "img": "gift.jpg"},
        {"id": "unseen", "label": "🎥 Unseen", "img": "unseen.jpg"}
    ]
    
    cols = st.columns(2)
    for i, item in enumerate(menu_items):
        with cols[i % 2]:
            if os.path.exists(item['img']):
                st.image(item['img'], use_container_width=True)
            if st.button(item['label'], key=f"m_{item['id']}", use_container_width=True):
                st.session_state.menu = item['id']
                st.rerun()
