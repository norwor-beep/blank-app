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
                return [line.split(',')[0] for line in lines if ',' in line]
        except: return []
    return []

def save_status(box_id, gift_idx):
    with open("status.txt", "a") as f:
        with open("status.txt", "a") as f: f.write(f"{box_id},{gift_idx}\n")

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

# 2. หน้า LOGIN
if not st.session_state.authenticated:
    set_bg_and_style("bg_login.png")
    st.markdown('<div style="height: 150px;"></div>', unsafe_allow_html=True)
    col_l, col_mid, col_r = st.columns([1, 2, 1])
    with col_mid:
        password = st.text_input("", type="password", placeholder="รหัสผ่านจ้า", key="login_pass")
        if st.button("เข้าสู่ระบบ 🤍", use_container_width=True):
            if password == "1234": st.session_state.authenticated = True; st.rerun()
            else: st.error("รหัสผิดนะเจ้าอ้วน")
    st.stop()

# 3. จัดการเมนู
if 'menu' not in st.session_state: st.session_state.menu = None

if st.session_state.menu:
    set_bg_and_style("bg_dashboard.png")
    if st.button("🔙 กลับไปหน้าเมนู"): st.session_state.menu = None; st.rerun()
    st.divider()

    # --- หน้า 365 DAYS ---
    if st.session_state.menu == "365days":
        clock_holder = st.empty()
        target = datetime(2027, 2, 14, 0, 0, 0)
        while st.session_state.menu == "365days":
            diff = target - datetime.now()
            d, h, m, s = diff.days, diff.seconds//3600, (diff.seconds//60)%60, diff.seconds%60
            my_html = f"""<div style="text-align:center; background:rgba(255,255,255,0.85); padding:30px; border-radius:30px; box-shadow:0 10px 25px rgba(0,0,0,0.1); margin:auto;">
                <p style="color:#FF4B4B; font-weight:bold; margin-bottom:15px;">COUNTING DOWN TO OUR DAY</p>
                <div style="font-size:40px; font-weight:bold; color:#007BFF; display:flex; justify-content:center; gap:10px;">
                    <div>{d:02d}<br><span style="font-size:10px; color:#555;">DAYS</span></div>:
                    <div>{h:02d}<br><span style="font-size:10px; color:#555;">HRS</span></div>:
                    <div>{m:02d}<br><span style="font-size:10px; color:#555;">MIN</span></div>:
                    <div style="color:#FF4B4B;">{s:02d}<br><span style="font-size:10px; color:#555;">SEC</span></div>
                </div></div>"""
            clock_holder.markdown(my_html, unsafe_allow_html=True); time.sleep(1)

    # --- หน้า TANG'S GIFT ---
    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        gift_sequence = [{"date": "2024-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"}] # บี๋เพิ่มได้อีก
        opened_boxes = get_saved_status()
        today = datetime.now().date()
        cols = st.columns(2)
        single_box_img = "box.png"
        for i in range(4):
            b_id = f"box_{i+1}"
            with cols[i % 2]:
                if b_id in opened_boxes:
                    gift_idx = opened_boxes.index(b_id)
                    st.success(gift_sequence[gift_idx]['text'])
                    if os.path.exists(gift_sequence[gift_idx]['image']): st.image(gift_sequence[gift_idx]['image'])
                else:
                    count = len(opened_boxes)
                    if count < len(gift_sequence):
                        g_date = datetime.strptime(gift_sequence[count]['date'], "%Y-%m-%d").date()
                        if today >= g_date:
                            if render_clickable_box(single_box_img, b_id, f"กล่องที่ {i+1}"):
                                save_status(b_id, count); st.balloons(); st.rerun()
                        else: render_clickable_box(single_box_img, b_id, "🔒", disabled=True)

    # --- หน้า QUIZ (ทายใจเวอร์ชั่นอัปเดตคำถาม 5 ข้อ) ---
    elif st.session_state.menu == "quiz":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🧩 Challenge My Love</h2>", unsafe_allow_html=True)
        
        # รายการคำถามที่บี๋ให้มา
        questions = [
            {
                "q": "1. เราเริ่มคุยกันตั้งแต่เดือนไหน?",
                "a": ["กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"],
                "ans": "มีนาคม"
            },
            {
                "q": "2. หนังเรื่องแรกที่เราดูด้วยกันในโรงคือเรื่องอะไร?",
                "a": ["F1", "Jurassic World Rebirth", "Superman", "Zootopia"],
                "ans": "F1"
            },
            {
                "q": "3. ตุ๊กตาตัวแรกที่เธอซื้อให้เค้าเป็นสัตว์อะไร?",
                "a": ["หมา", "จิ้งจอก", "กระต่าย", "เป็ด"],
                "ans": "เป็ด"
            },
            {
                "q": "4. ข้อใดต่อไปนี้ไม่ใช่ของขวัญที่เธอเคยซื้อให้เค้า?",
                "a": ["กระเป๋า", "สร้อยคอ", "ต่างหู", "สร้อยข้อมือ"],
                "ans": "สร้อยคอ"
            },
            {
                "q": "5. ของขวัญชิ้นแรกที่เค้าให้เธอคืออะไร?",
                "a": ["ดอกไม้", "ตุ๊กตา", "เสื้อ", "สร้อยข้อมือ"],
                "ans": "เสื้อ"
            }
        ]

        if 'q_idx' not in st.session_state:
            st.session_state.q_idx = 0
        
        if st.session_state.q_idx < len(questions):
            curr = questions[st.session_state.q_idx]
            
            # แสดง Progress Bar (ความคืบหน้า)
            progress = (st.session_state.q_idx) / len(questions)
            st.progress(progress)
            
            st.markdown(f"### {curr['q']}")
            
            # ตัวเลือกคำตอบ
            ans = st.radio("เลือกคำตอบที่ถูกต้องที่สุด:", curr['a'], key=f"q_{st.session_state.q_idx}")
            
            if st.button("ยืนยันคำตอบ 🚀", use_container_width=True):
                if ans == curr['ans']:
                    st.success("เก่งมากกกก ถูกต้องครับ! ❤️")
                    time.sleep(1)
                    st.session_state.q_idx += 1
                    st.rerun()
                else:
                    st.error("ผิดนะเจ้าอ้วน! ลองนึกดูดีๆ ซิ")
        else:
            # เมื่อตอบถูกครบทุกข้อ
            st.balloons()
            st.markdown("""
                <div style='text-align:center; background:rgba(255,255,255,0.9); padding:30px; border-radius:20px;'>
                    <h2 style='color:#FF4B4B;'>🎉 ยินดีด้วยครับบี๋!</h2>
                    <h3>บี๋ตอบถูกหมดเลย เก่งที่สุดในโลก!</h3>
                    <p>ขอบคุณที่ใส่ใจทุกรายละเอียดของเรานะ รักบี๋มากๆ เลย ❤️</p>
                </div>
            """, unsafe_allow_html=True)
            
            # ถ้ามีรูปรางวัลก็โชว์ตรงนี้จ้า
            if os.path.exists("couple_prize.png"):
                st.image("couple_prize.png", use_container_width=True, caption="ของรางวัลสำหรับคนเก่ง ✨")
            
            if st.button("เริ่มเล่นใหม่"):
                st.session_state.q_idx = 0
                st.rerun()

    # --- หน้า MEMORIES (ฝัง Canva) ---
    elif st.session_state.menu == "memories":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>📸 Our Memories</h2>", unsafe_allow_html=True)
        canva_embed_code = """https://www.canva.com/design/DAHAR3m9VbM/2CtCdb7FIbKo9zBg-4Es4g/edit?utm_content=DAHAR3m9VbM&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton"""
        if "canva" in canva_embed_code.lower():
            st.components.v1.html(canva_embed_code, height=500, scrolling=True)
        else:
            st.info("รอจดหมายรักจาก Canva ของบี๋อยู่นะจ๊ะ! ❤️")

    # --- หน้า UNSEEN (YouTube) ---
    elif st.session_state.menu == "unseen":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎥 Unseen Video</h2>", unsafe_allow_html=True)
        video_url = "https://youtube.com/shorts/0ZzMBohT9-I?si=T6-IG8xCBgJVSgHn" 
        st.video(video_url)
        st.markdown("<p style='text-align:center;'>วิดีโอลับที่มีแค่เราสองคนที่รู้... 🤫💖</p>", unsafe_allow_html=True)

    # --- หน้า MESSAGE (รูปจดหมายใหญ่ๆ) ---
    elif st.session_state.menu == "message":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>💌 My Message</h2>", unsafe_allow_html=True)
        # บี๋ทำรูปจดหมายแล้วตั้งชื่อว่า letter.png (หรือ .jpg) แล้วอัปโหลดลง GitHub นะจ๊ะ
        letter_img = "letter.png"
        if os.path.exists(letter_img):
            st.image(letter_img, use_container_width=True)
            st.markdown("<p style='text-align:center; color:#555;'>จดหมายฉบับนี้... เขียนให้คนเก่งของเค้านะ ❤️</p>", unsafe_allow_html=True)
        else:
            st.warning("บี๋อย่าลืมอัปโหลดรูปจดหมายชื่อ 'letter.png' ลงใน GitHub นะจ๊ะ รูปถึงจะขึ้น!")

    else:
        st.info(f"หน้า {st.session_state.menu} กำลังเตรียมเซอร์ไพรส์จ้า!")

else:
    # 4. หน้า DASHBOARD
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
            if st.button(item['label'], key=item['id'], use_container_width=True): st.session_state.menu = item['id']; st.rerun()
