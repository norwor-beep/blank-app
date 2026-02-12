import streamlit as st
import os
import base64
from datetime import datetime
import time

# --- วางฟังก์ชันเล่นเพลงไว้ตรงนี้ครับ ---
def play_bg_music():
    music_file = "bg_music.mp3"
    if os.path.exists(music_file):
        with open(music_file, "rb") as f:
            data = f.read()
            base64_audio = base64.b64encode(data).decode()
            audio_html = f"""
                <audio autoplay loop id="bg-audio">
                    <source src="data:audio/mp3;base64,{{base64_audio}}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)
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
    
    # --- เพิ่ม 2 บรรทัดนี้ลงไปตรงนี้ครับ ---
    if st.session_state.menu != "unseen":
        play_bg_music()

    if st.button("🔙 กลับไปหน้าเมนู"): 
        st.session_state.menu = None; st.rerun()
    st.divider()
    
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

    # --- หน้า TANG'S GIFT (คืนชีพ 4 กล่อง) ---
    elif st.session_state.menu == "gift":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎁 Tang's Gift</h2>", unsafe_allow_html=True)
        
        # 1. บี๋ตั้งค่าของขวัญทั้ง 4 ชิ้นตรงนี้เลยจ้า
        gift_sequence = [
            {"date": "2024-02-14", "image": "gift1.jpg", "text": "ชิ้นที่ 1: รักบี๋ที่สุดในโลก! ❤️"},
            {"date": "2024-05-20", "image": "gift2.jpg", "text": "ชิ้นที่ 2: ของขวัญเซอร์ไพรส์จ้า ✨"},
            {"date": "2024-08-12", "image": "gift3.jpg", "text": "ชิ้นที่ 3: คนเก่งของเค้า 💖"},
            {"date": "2024-12-25", "image": "gift4.jpg", "text": "ชิ้นที่ 4: คริสต์มาสนี้มีแค่เรา 🎄"}
        ]
        
        opened_boxes = get_saved_status()
        today = datetime.now().date()
        cols = st.columns(2)
        single_box_img = "box.png" # ไฟล์รูปกล่องของขวัญ (ก่อนเปิด)
        
        # สร้างกล่อง 4 กล่อง
        box_ids = ["box_1", "box_2", "box_3", "box_4"]
        
        for i, b_id in enumerate(box_ids):
            with cols[i % 2]:
                # ถ้าเคยเปิดกล่องนี้ไปแล้ว (มีชื่อใน status.txt)
                if b_id in opened_boxes:
                    gift_idx = opened_boxes.index(b_id)
                    if gift_idx < len(gift_sequence):
                        info = gift_sequence[gift_idx]
                        st.success(f"🎉 {info['text']}")
                        if os.path.exists(info['image']):
                            st.image(info['image'], use_container_width=True)
                        else:
                            st.info(f"(รออัปโหลดรูป {info['image']})")
                
                # ถ้ายังไม่ได้เปิด
                else:
                    # เช็คว่าลำดับของขวัญที่จะเปิดถัดไปคือชิ้นที่เท่าไหร่
                    next_to_open_idx = len(opened_boxes)
                    
                    # ถ้าลำดับนี้ตรงกับกล่องที่กำลังสร้าง (เพื่อให้เปิดทีละกล่องตามลำดับ)
                    if i == next_to_open_idx and i < len(gift_sequence):
                        g_info = gift_sequence[i]
                        g_date = datetime.strptime(g_info['date'], "%Y-%m-%d").date()
                        
                        # ถ้าถึงวันที่กำหนดแล้ว
                        if today >= g_date:
                            if render_clickable_box(single_box_img, b_id, f"เปิดกล่องที่ {i+1}"):
                                save_status(b_id, i)
                                st.balloons()
                                st.rerun()
                        else:
                            render_clickable_box(single_box_img, b_id, "🔒", disabled=True)
                            st.caption(f"รอก่อนนะจ๊ะ เปิดได้วันที่: {g_date}")
                    else:
                        # กล่องที่ยังไม่ถึงคิวเปิด หรือเกินจำนวนของขวัญที่มี
                        render_clickable_box(single_box_img, b_id, "🔒", disabled=True)

    # --- หน้า QUIZ (อัปเกรดให้อ่านง่ายขึ้น) ---
    elif st.session_state.menu == "quiz":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🧩 Challenge My Love</h2>", unsafe_allow_html=True)
        
        questions = [
            {"q": "1. เราเริ่มคุยกันตั้งแต่เดือนไหน?", "a": ["กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"], "ans": "มีนาคม"},
            {"q": "2. หนังเรื่องแรกที่เราดูด้วยกันในโรงคือเรื่องอะไร?", "a": ["F1", "Jurassic World Rebirth", "Superman", "Zootopia"], "ans": "F1"},
            {"q": "3. ตุ๊กตาตัวแรกที่เธอซื้อให้เค้าเป็นสัตว์อะไร?", "a": ["หมา", "จิ้งจอก", "กระต่าย", "เป็ด"], "ans": "เป็ด"},
            {"q": "4. ข้อใดต่อไปนี้ไม่ใช่ของขวัญที่เธอเคยซื้อให้เค้า?", "a": ["กระเป๋า", "สร้อยคอ", "ต่างหู", "สร้อยข้อมือ"], "ans": "สร้อยคอ"},
            {"q": "5. ของขวัญชิ้นแรกที่เค้าให้เธอคืออะไร?", "a": ["ดอกไม้", "ตุ๊กตา", "เสื้อ", "สร้อยข้อมือ"], "ans": "เสื้อ"}
        ]

        if 'q_idx' not in st.session_state:
            st.session_state.q_idx = 0
        
        if st.session_state.q_idx < len(questions):
            curr = questions[st.session_state.q_idx]
            
            # แสดง Progress Bar
            st.progress((st.session_state.q_idx) / len(questions))
            
            # --- กล่องพื้นหลังสำหรับคำถาม ---
            st.markdown(f"""
                <div style="background-color: rgba(255, 255, 255, 0.85); 
                            padding: 20px; 
                            border-radius: 15px; 
                            border-left: 8px solid #FF4B4B;
                            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
                            margin-bottom: 20px;">
                    <h3 style="color: #333; margin: 0;">{curr['q']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # --- กล่องพื้นหลังสำหรับตัวเลือก (Radio) ---
            st.markdown('<div style="background-color: rgba(255, 255, 255, 0.7); padding: 15px; border-radius: 15px; margin-bottom: 10px;">', unsafe_allow_html=True)
            ans = st.radio("เลือกคำตอบที่ถูกต้องที่สุด:", curr['a'], key=f"q_{st.session_state.q_idx}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            if st.button("ยืนยันคำตอบ 🚀", use_container_width=True):
                if ans == curr['ans']:
                    st.success("เก่งมากกกก ถูกต้องครับ! ❤️")
                    time.sleep(1)
                    st.session_state.q_idx += 1
                    st.rerun()
                else:
                    st.error("ผิดนะเจ้าอ้วน! ลองนึกดูดีๆ ซิ")
        else:
            # เมื่อตอบถูกครบทุกข้อ (ผลลัพธ์สุดท้าย)
            st.balloons()
            st.markdown("""
                <div style="text-align:center; background:rgba(255,255,255,0.9); padding:30px; border-radius:20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
                    <h2 style='color:#FF4B4B;'>🎉 ยินดีด้วยครับบี๋!</h2>
                    <h3 style="color:#444;">บี๋ตอบถูกหมดเลย เก่งที่สุดในโลก!</h3>
                    <p style="color:#666;">ขอบคุณที่ใส่ใจทุกรายละเอียดของเรานะ รักบี๋มากๆ เลย ❤️</p>
                </div>
            """, unsafe_allow_html=True)
            
            if os.path.exists("couple_prize.png"):
                st.image("couple_prize.png", use_container_width=True, caption="รางวัลของคนเก่ง ✨")
            
            if st.button("เริ่มเล่นใหม่"):
                st.session_state.q_idx = 0
                st.rerun()

    # --- หน้า MEMORIES (Canva Fix) ---
    elif st.session_state.menu == "memories":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>📸 Our Memories</h2>", unsafe_allow_html=True)
        canva_embed_code = """<div style="position: relative; width: 100%; height: 0; padding-top: 77.2727%; padding-bottom: 0; box-shadow: 0 2px 8px 0 rgba(63,69,81,0.16); margin-top: 1.6em; margin-bottom: 0.9em; overflow: hidden; border-radius: 8px; will-change: transform;">
          <iframe loading="lazy" style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; border: none; padding: 0;margin: 0;"
            src="https://www.canva.com/design/DAHAR3m9VbM/dsooFGHFyMQRKRMogfab0A/view?embed" allowfullscreen="allowfullscreen" allow="fullscreen">
          </iframe>
        </div>"""
        st.components.v1.html(canva_embed_code, height=600, scrolling=True)

    # --- หน้า UNSEEN (YouTube Fix) ---
    elif st.session_state.menu == "unseen":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>🎥 Unseen Video</h2>", unsafe_allow_html=True)
        video_url = "https://www.youtube.com/watch?v=0ZzMBohT9-I" 
        st.video(video_url)
        st.markdown("<p style='text-align:center;'>วิดีโอลับที่มีแค่เราสองคนที่รู้... 🤫💖</p>", unsafe_allow_html=True)

    # --- หน้า MESSAGE (รูปจดหมายใหญ่ๆ) ---
    elif st.session_state.menu == "message":
        st.markdown("<h2 style='text-align:center; color:#FF4B4B;'>💌 My Message</h2>", unsafe_allow_html=True)
        # บี๋ทำรูปจดหมายแล้วตั้งชื่อว่า letter.png (หรือ .jpg) แล้วอัปโหลดลง GitHub นะจ๊ะ
        letter_img = "letter.jpg"
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
    # --- เพิ่มบรรทัดนี้ลงไปตรงนี้ครับ ---
    play_bg_music() 
    
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
