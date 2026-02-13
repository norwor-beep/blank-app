import streamlit as st
import os
import base64
from datetime import datetime
import time

import streamlit.components.v1 as components

# --- (ลบฟังก์ชัน play_bg_music เดิมที่แสดงตรงกลางออกแล้ว) ---

# 2. การตั้งค่าหน้าจอ
st.set_page_config(page_title="คู่รักคู่แค้นคู่คี่", page_icon="💝", layout="centered")

# --- ระบบจัดการไฟล์สถานะ ---
def get_saved_status():
    if os.path.exists("status.txt"):
        try:
            with open("status.txt", "r") as f:
                lines = f.readlines()
                return [line.split(',')[0] for line in lines if ',' in line]
        except: return []
    return []

def save_status(box_id, gift_idx):
    with open("status.txt", "a") as f:
        f.write(f"{box_id},{gift_idx}\n")

# --- ฟังก์ชันจัดการรูปและปุ่ม ---
def render_clickable_box(img_path, box_id, label, disabled=False):
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            data = f.read()
            encoded = base64.b64encode(data).decode()
        opacity = "1.0" if not disabled else "0.4"
        cursor = "pointer" if not disabled else "not-allowed"
        html = f"""<div style="text-align: center; margin-bottom: 10px;">
                <img src="data:image/png;base64,{encoded}" style="width: 140px; cursor: {cursor}; opacity: {opacity}; transition: 0.2s;" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1.0)'">
            </div>"""
        st.markdown(html, unsafe_allow_html=True)
        if not disabled:
            if st.button(f"เลือก {label}", key=f"btn_{box_id}", use_container_width=True): return True
    else: return st.button(f"📦 {label}", key=f"btn_{box_id}", use_container_width=True, disabled=disabled)
    return False

def get_base64_of_bin_file(bin_file):
    if os.path.exists(bin_file):
        with open(bin_file, 'rb') as f: data = f.read()
        return base64.b64encode(data).decode()
    return ""

def set_bg_and_style(bg_file):
    bin_str = get_base64_of_bin_file(bg_file)
    if bin_str:
        st.markdown(f"""<style>
            .stApp {{ background-image: url("data:image/png;base64,{bin_str}"); background-size: cover; background-position: center; background-attachment: fixed; }}
            header, footer {{visibility: hidden;}}
            </style>""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state: st.session_state.authenticated = False

# --- หน้า LOGIN ---
if not st.session_state.authenticated:
    set_bg_and_style("bg_login.png")
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        password = st.text_input("", type="password", placeholder="รหัสผ่านจ้า", key="login_pass")
        if st.button("เข้าสู่ระบบ 🤍", use_container_width=True):
            if password == "220468": st.session_state.authenticated = True; st.rerun()
            else: st.error("กรอกรหัสใหม่ไอแกร่")
    st.stop()

# --- ส่วน Sidebar เพลง (จะแสดงในทุกหน้าหลัง Login) ---
with st.sidebar:
    st.write("### 🎧 Our Playlist")
    if os.path.exists("bg_music2.mp3"):
        st.audio("bg_music2.mp3")
        st.info("เปิดเพลงคลอไปด้วยนะบี๋ ❤️")
    else:
        st.warning("ไม่พบไฟล์ bg_music2.mp3")

# --- จัดการเมนู ---
if 'menu' not in st.session_state: st.session_state.menu = None

if st.session_state.menu:
    set_bg_and_style("bg_dashboard.png")
    
    if st.button("🔙 กลับไปหน้าเมนู"): 
        st.session_state.menu = None; st.rerun()
    st.divider()

    # --- เนื้อหาแต่ละหน้า ---
    # --- หน้า 365 DAYS ---
    if st.session_state.menu == "365days":
        clock_holder = st.empty()
        target = datetime(2026, 4, 22, 0, 0, 0)
        
        love_message = """
            <div style="margin-top:20px; padding:20px; background:rgba(240, 248, 255, 0.9); 
                        border-radius: 20px; border: 2px dashed #007BFF; 
                        color: #5D4037; font-size: 18px; text-align: center;
                        font-family: 'Tahoma', sans-serif; line-height: 1.6;">
                "อยู่ด้วยกันมาจะครบปีแล้วนะไอ่หมูอ้วน <br> 
                อยู่ต่อ อยู่อีก ห้ามหนี ห้ามทิ้ง รักบี๋ที่สุดๆๆ ❤️"
            </div>
        """

        while st.session_state.menu == "365days":
            diff = target - datetime.now()
            d = diff.days
            h = diff.seconds // 3600
            m = (diff.seconds // 60) % 60
            s = diff.seconds % 60
            
            clock_html = f"""
            <div style="text-align:center; background:rgba(255,255,255,0.85); padding:30px; border-radius:30px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin:auto;">
                <p style="color:#FF4B4B; font-weight:bold; margin-bottom:15px; letter-spacing: 2px;">COUNTING DOWN TO OUR DAY</p>
                <div style="font-size:40px; font-weight:bold; color:#007BFF; display:flex; justify-content:center; gap:10px;">
                    <div>{d:02d}<br><span style="font-size:12px; color:#555;">DAYS</span></div>:
                    <div>{h:02d}<br><span style="font-size:12px; color:#555;">HRS</span></div>:
                    <div>{m:02d}<br><span style="font-size:12px; color:#555;">MIN</span></div>:
                    <div style="color:#FF4B4B;">{s:02d}<br><span style="font-size:12px; color:#555;">SEC</span></div>
                </div>
                {love_message}
            </div>
            """
            clock_holder.markdown(clock_html, unsafe_allow_html=True)
            time.sleep(1)

    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        gift_sequence = [
            {"date": "2026-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: ชุดเซ๊ะซี่ชอบมั๊ยจ๊ะ"},
            {"date": "2026-02-22", "image": "gift2.jpg", "text": "ชิ้นที่ 2: บัตรตามใจ"},
            {"date": "2026-03-22", "image": "gift3.jpg", "text": "ชิ้นที่ 3: มาแง๊นกับพี่สิจ๊ะ"},
            {"date": "2026-04-22", "image": "gift4.jpg", "text": "ชิ้นที่ 4: รองเท้า หรือ เสื้อ ดีน๊า"}
        ]
        opened_boxes = get_saved_status()
        today = datetime.now().date()
        cols = st.columns(2)
        single_box_img = "box.png"
        box_ids = ["box_1", "box_2", "box_3", "box_4"]
        for i, b_id in enumerate(box_ids):
            with cols[i % 2]:
                if b_id in opened_boxes:
                    idx = opened_boxes.index(b_id)
                    st.success(f"🎉 {gift_sequence[idx]['text']}")
                    if os.path.exists(gift_sequence[idx]['image']): st.image(gift_sequence[idx]['image'])
                else:
                    next_idx = len(opened_boxes)
                    if i == next_idx:
                        g_date = datetime.strptime(gift_sequence[i]['date'], "%Y-%m-%d").date()
                        if today >= g_date:
                            if render_clickable_box(single_box_img, b_id, f"เปิดกล่องที่ {i+1}"):
                                save_status(b_id, i); st.balloons(); st.rerun()
                        else: render_clickable_box(single_box_img, b_id, "🔒", disabled=True)
                    else: render_clickable_box(single_box_img, b_id, "🔒", disabled=True)

    elif st.session_state.menu == "quiz":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🧩 จำได้มั้ยน้อ</h2>", unsafe_allow_html=True)
        questions = [
            {"q": "1. เราเริ่มคุยกันตั้งแต่เดือนไหน?", "a": ["กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"], "ans": "มีนาคม"},
            {"q": "2. หนังเรื่องแรกที่เราดูด้วยกันในโรงคือเรื่องอะไร?", "a": ["F1", "Jurassic World Rebirth", "Superman", "Zootopia"], "ans": "F1"},
            {"q": "3. ตุ๊กตาตัวแรกที่เธอซื้อให้เค้าเป็นสัตว์อะไร?", "a": ["หมา", "จิ้งจอก", "กระต่าย", "เป็ด"], "ans": "เป็ด"},
            {"q": "4. ข้อใดต่อไปนี้ไม่ใช่ของขวัญที่เธอเคยซื้อให้เค้า?", "a": ["กระเป๋า", "สร้อยคอ", "ต่างหู", "สร้อยข้อมือ"], "ans": "สร้อยคอ"},
            {"q": "5. ของขวัญชิ้นแรกที่เค้าให้เธอคืออะไร?", "a": ["ดอกไม้", "ตุ๊กตา", "เสื้อ", "สร้อยข้อมือ"], "ans": "เสื้อ"}
        ]

        if 'q_idx' not in st.session_state: st.session_state.q_idx = 0
        if st.session_state.q_idx < len(questions):
            curr = questions[st.session_state.q_idx]
            st.progress(st.session_state.q_idx / len(questions))
            st.markdown(f"""<div style="background-color: rgba(255, 255, 255, 0.9); padding: 20px; border-radius: 15px; border-left: 10px solid #FF4B4B; margin-bottom: 15px; text-align: center;">
                    <h3 style="color: #5D4037; margin: 0;">{curr['q']}</h3></div>""", unsafe_allow_html=True)
            st.markdown("""<style>div[data-testid="stRadio"] { background-color: rgba(255, 255, 255, 0.8) !important; padding: 20px !important; border-radius: 15px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; }
                div[data-testid="stRadio"] label p { color: #5D4037 !important; font-weight: bold !important; }</style>""", unsafe_allow_html=True)
            ans = st.radio("คำตอบ:", curr['a'], key=f"q_{st.session_state.q_idx}", label_visibility="collapsed")
            if st.button("ยืนยันคำตอบ 🚀", use_container_width=True):
                if ans == curr['ans']:
                    st.success("เห้ยยยย แอบเก่งนะ"); time.sleep(1); st.session_state.q_idx += 1; st.rerun()
                else: st.error("แหมไอแกร่ เดี๋ยวโดน ตอบใหม่!")
        else:
            st.balloons()
            st.markdown("""<div style="text-align:center; background:rgba(255,255,255,0.85); padding:40px; border-radius:30px; border: 2px solid #FF4B4B;">
                    <h2 style='color:#FF4B4B;'>🎉 เก่งมากไออ้วน</h2><h3 style="color:#5D4037;">ตอบจนถูกหมด ออกไปเอาของขวัญได้เลยสุดหล่อ</h3></div>""", unsafe_allow_html=True)
            if st.button("เริ่มเล่นใหม่"): st.session_state.q_idx = 0; st.rerun()

    elif st.session_state.menu == "memories":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>📸 Our Memories</h2>", unsafe_allow_html=True)
        canva_code = """<div style="position: relative; width: 100%; height: 0; padding-top: 77.2727%; overflow: hidden; border-radius: 8px;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none;" src="https://www.canva.com/design/DAHAR3m9VbM/dsooFGHFyMQRKRMogfab0A/view?embed" allowfullscreen></iframe></div>"""
        st.components.v1.html(canva_code, height=600, scrolling=True)

    elif st.session_state.menu == "unseen":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎥 Unseen Video</h2>", unsafe_allow_html=True)
        video_url = "https://www.youtube.com/watch?v=0ZzMBohT9-I"
        try: st.video(video_url, start_time=0)
        except: st.error("ไม่สามารถโหลดวิดีโอได้โดยตรง")
        st.markdown(f"""<div style="text-align:center; margin-top:20px; padding:15px; background:rgba(255,255,255,0.7); border-radius:15px;">
                <a href="{video_url}" target="_blank" style="text-decoration:none;"><button style="background-color:#FF0000; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer; font-weight:bold;">📺 คลิกเพื่อดูใน YouTube โดยตรง</button></a></div>""", unsafe_allow_html=True)
        
    elif st.session_state.menu == "message":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>💌 My Message</h2>", unsafe_allow_html=True)
        if os.path.exists("letter.jpg"): st.image("letter.jpg", use_container_width=True)
        else: st.warning("อย่าลืมอัปโหลด letter.jpg นะจ๊ะ")

else:
    # --- หน้า DASHBOARD ---
    set_bg_and_style("bg_dashboard.png")
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
            if os.path.exists(item['img']): st.image(item['img'])
            if st.button(item['label'], key=item['id'], use_container_width=True): 
                st.session_state.menu = item['id']
                st.rerun()
