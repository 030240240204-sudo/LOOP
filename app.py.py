import streamlit as st
import pandas as pd
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="LOOP System - Hệ Sinh Thái Tuần Hoàn AI",
    page_icon="🌿",
    layout="centered"
)

# --- CSS THUẦN TÚY: NỀN XANH ĐẬM & HIỆU ỨNG LÁ RƠI CHUẨN ĐIỆN THOẠI ---
st.markdown("""
    <style>
    /* Nền xanh rừng già đậm */
    .stApp {
        background-color: #0b2513 !important;
        background-image: linear-gradient(135deg, #0b2513 0%, #143d22 100%);
        color: #e8f5e9 !important;
    }

    /* Thẻ chứa (Card) mờ ảo sang trọng */
    .main-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 25px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
    }

    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #e8f5e9 !important;
    }
    
    /* Nút bấm xanh neon */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        color: white !important;
        border-radius: 25px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }

    /* Đảm bảo ô nhập liệu dễ nhìn */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #1e3a1e !important;
    }

    /* --- HIỆU ỨNG LÁ RƠI BẰNG CSS KHÔNG BỊ ĐIỆN THOẠI CHẶN --- */
    .leaves {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 999; overflow: hidden;
    }
    .leaf {
        position: absolute; display: block; list-style: none;
        width: 20px; height: 20px; background: transparent;
        animation: animate 20s linear infinite; bottom: -150px;
    }
    .leaf:nth-child(1){ left: 25%; width: 20px; height: 20px; animation-delay: 0s; animation-duration: 12s; }
    .leaf:nth-child(2){ left: 10%; width: 25px; height: 25px; animation-delay: 2s; animation-duration: 15s; }
    .leaf:nth-child(3){ left: 70%; width: 15px; height: 15px; animation-delay: 4s; }
    .leaf:nth-child(4){ left: 40%; width: 20px; height: 20px; animation-delay: 0s; animation-duration: 18s; }
    .leaf:nth-child(5){ left: 65%; width: 22px; height: 22px; animation-delay: 0s; }
    .leaf:nth-child(6){ left: 85%; width: 18px; height: 18px; animation-delay: 5s; }

    @keyframes animate {
        0%{ transform: translateY(-100px) rotate(0deg); opacity: 1; }
        100%{ transform: translateY(100vh) rotate(360deg); opacity: 0; }
    }
    </style>
    
    <div class="leaves">
        <div class="leaf">🍃</div><div class="leaf">🍃</div><div class="leaf">🍃</div>
        <div class="leaf">🌿</div><div class="leaf">🍃</div><div class="leaf">🌿</div>
    </div>
""", unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if "users" not in st.session_state:
    st.session_state.users = [{"email": "eco@loop.vn", "name": "Đại sứ Xanh", "role": "Người dùng", "pass": "123"}]
if "waste_kgs" not in st.session_state:
    st.session_state.waste_kgs = 745
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; font-weight: 800;'>🌿 LOOP SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a5d6a7 !important;'>Hệ sinh thái tuần hoàn kết hợp trí tuệ nhân tạo AI</p>", unsafe_allow_html=True)

# CHƯA ĐĂNG NHẬP
if not st.session_state.is_logged_in:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Đăng nhập", "📝 Đăng ký"])
    
    with tab1:
        email = st.text_input("Gmail của bạn:", key="l_email", placeholder="eco@loop.vn")
        name = st.text_input("Họ và tên:", key="l_name")
        pwd = st.text_input("Mật khẩu:", type="password", key="l_pwd")
        role = st.selectbox("Vai trò:", ["Người dùng", "Tổ chức Doanh nghiệp", "Hệ thống tái chế"], key="l_role")
        
        if st.button("Xác nhận đăng nhập", use_container_width=True):
            user = next((u for u in st.session_state.users if u['email'].lower() == email.strip().lower() and u['pass'] == pwd), None)
            if user:
                st.session_state.is_logged_in = True
                st.session_state.user_data = user
                st.success(f"🎉 Chào mừng {user['name']}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("❌ Kiểm tra lại thông tin đăng nhập (Thử Email: eco@loop.vn | MK: 123)")

    with tab2:
        r_email = st.text_input("Nhập Gmail đăng ký:", key="r_email")
        r_name = st.text_input("Nhập họ tên:", key="r_name")
        r_pwd = st.text_input("Thiết lập mật khẩu:", type="password", key="r_pwd")
        r_role = st.selectbox("Vai trò tham gia:", ["Người dùng", "Tổ chức Doanh nghiệp", "Hệ thống tái chế"], key="r_role")
        if st.button("Hoàn tất đăng ký", use_container_width=True):
            if r_email and r_name and r_pwd:
                st.session_state.users.append({"email": r_email.strip(), "name": r_name.strip(), "role": r_role, "pass": r_pwd})
                st.success("🌱 Đăng ký xong! Hãy quay lại tab Đăng nhập.")
    st.markdown("</div>", unsafe_allow_html=True)

# ĐÃ ĐĂNG NHẬP
else:
    user = st.session_state.user_data
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown(f"### 🍀 Tài khoản: **{user['name']}**")
    
    col1, col2 = st.columns(2)
    with col1: st.metric(label="Thành viên", value=f"{len(st.session_state.users)}")
    with col2: st.metric(label="Rác tái sinh", value=f"{st.session_state.waste_kgs} kg")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    if user['role'] == "Người dùng":
        st.markdown("<h3>🤖 AI PHÂN LOẠI RÁC THẢI</h3>", unsafe_allow_html=True)
        ai_option = st.radio("Chọn camera hoặc tải ảnh:", ["Tải ảnh từ máy", "Chụp ảnh trực tiếp"])
        
        image_file = st.file_uploader("Chọn tệp ảnh:", type=['jpg', 'png', 'jpeg']) if ai_option == "Tải ảnh từ máy" else st.camera_input("Quét rác trước camera:")
            
        if image_file is not None:
            st.image(image_file, caption="Ảnh đang chờ xử lý...", use_container_width=True)
            if st.button("✨ KÍCH HOẠT AI PHÂN TÍCH"):
                with st.spinner("🤖 AI đang tính toán..."):
                    time.sleep(2)
                    st.success("🎯 Kết quả phân loại:")
                    st.markdown("- **Chai nhựa (PET)** 👉 *Rác tái chế* | `+15 điểm`")
                    st.markdown("- **Vỏ lon ngọt** 👉 *Rác tái chế* | `+20 điểm`")
                    st.balloons()
                    
    elif user['role'] == "Hệ thống tái chế":
        weight_input = st.number_input("Nhập số kg rác:", min_value=1, value=10)
        if st.button("⚡ Cập nhật số liệu"):
            st.session_state.waste_kgs += weight_input
            st.success("Đã cập nhật!")
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    
    if st.button("🚪 Đăng xuất", use_container_width=True):
        st.session_state.is_logged_in = False
        st.rerun()
