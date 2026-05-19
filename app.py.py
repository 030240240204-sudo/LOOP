import streamlit as st
import pandas as pd
import time

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="LOOP System - Hệ Sinh Thái Tuần Hoàn AI",
    page_icon="🌿",
    layout="centered"
)

# --- CSS TÙY CHỈNH & HIỆU ỨNG LÁ RƠI (FALLING LEAVES) ---
# Sử dụng kết hợp CSS nền xanh lá đậm và hiệu ứng JavaScript tạo lá rơi tự động
st.markdown("""
    <style>
    /* Cấu hình nền xanh lá đậm toàn trang */
    .stApp {
        background-color: #0b2513 !important; /* Màu xanh rừng già đậm */
        background-image: linear-gradient(135deg, #0b2513 0%, #143d22 100%);
        color: #e8f5e9 !important;
    }

    /* Thiết kế các thẻ chứa (Card) mờ ảo tinh tế */
    .main-card {
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 25px;
    }

    /* Định dạng lại màu sắc tiêu đề và văn bản */
    h1, h2, h3, h4, p, label, .stMarkdown {
        color: #e8f5e9 !important;
    }
    
    /* Thiết kế nút bấm xanh neon sinh thái */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #2ecc71, #27ae60);
        color: white !important;
        border-radius: 30px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(46, 204, 113, 0.3);
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(46, 204, 113, 0.5);
    }

    /* Làm các ô nhập liệu sáng lên để dễ nhìn trên nền tối */
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.9) !important;
        color: #1e3a1e !important;
        border-radius: 10px;
    }
    
    /* Định dạng các tab chọn */
    .stTabs [data-baseweb="tab"] {
        color: #a5d6a7 !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #fff !important;
        border-bottom-color: #2ecc71 !important;
    }
    
    /* Hiệu ứng tạo hạt lá rơi tự động */
    @keyframes snowfall {
        0% { fill: rgba(139, 195, 74, 0.8); transform: translateY(-10px) rotate(0deg); }
        100% { fill: rgba(76, 175, 80, 0.2); transform: translateY(100vh) rotate(360deg); }
    }
    </style>
    
    <script>
    function createLeaf() {
        const leaf = document.createElement('div');
        leaf.innerHTML = '🍃';
        leaf.style.position = 'fixed';
        leaf.style.top = '-20px';
        leaf.style.left = Math.random() * 100 + 'vw';
        leaf.style.fontSize = (Math.random() * 15 + 10) + 'px';
        leaf.style.opacity = Math.random();
        leaf.style.pointerEvents = 'none';
        leaf.style.zIndex = '9999';
        
        // Tạo quỹ đạo bay ngẫu nhiên
        const duration = Math.random() * 5 + 5;
        leaf.style.transition = `transform ${duration}s linear, opacity ${duration}s linear`;
        
        document.body.appendChild(leaf);
        
        setTimeout(() => {
            leaf.style.transform = `translate(${Math.random() * 50 - 25}px, 105vh) rotate(${Math.random() * 360}deg)`;
        }, 100);
        
        setTimeout(() => {
            leaf.remove();
        }, duration * 1000);
    }
    
    // Cứ mỗi 800ms sẽ tạo thêm một chiếc lá mới rơi xuống
    setInterval(createLeaf, 800);
    </script>
""", unsafe_allow_html=True)

# --- KHỞI TẠO CƠ SỞ DỮ LIỆU GIẢ LẬP ---
if "users" not in st.session_state:
    st.session_state.users = [
        {"email": "eco@loop.vn", "name": "Đại sứ Xanh", "role": "Người dùng", "pass": "123"}
    ]
if "waste_kgs" not in st.session_state:
    st.session_state.waste_kgs = 745
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center; font-size: 3.5rem; font-weight: 800;'>🌿 LOOP SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #a5d6a7 !important; font-size: 1.2rem; margin-bottom: 2rem;'>Hệ sinh thái tuần hoàn kết hợp trí tuệ nhân tạo AI</p>", unsafe_allow_html=True)

# CHƯA ĐĂNG NHẬP
if not st.session_state.is_logged_in:
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Hành trình Xanh (Đăng nhập)", "📝 Đăng ký làm thành viên"])
    
    with tab1:
        st.write("### Đăng nhập hệ thống")
        email = st.text_input("Địa chỉ Gmail của bạn:", key="l_email", placeholder="vi-du@gmail.com")
        name = st.text_input("Họ và tên chính xác:", key="l_name")
        pwd = st.text_input("Mật khẩu:", type="password", key="l_pwd")
        role = st.selectbox("Vai trò thành viên:", ["Người dùng", "Tổ chức Doanh nghiệp", "Hệ thống tái chế"], key="l_role")
        
        if st.button("Xác nhận đăng nhập", use_container_width=True):
            user = next((u for u in st.session_state.users if u['email'].lower() == email.strip().lower() and u['pass'] == pwd), None)
            if user:
                st.session_state.is_logged_in = True
                st.session_state.user_data = user
                st.success(f"🎉 Đăng nhập thành công! Chào mừng {user['name']} đến với thế giới xanh.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Thông tin đăng nhập chưa trùng khớp, bạn kiểm tra lại nhé!")

    with tab2:
        st.write("### Tạo tài khoản mới")
        r_email = st.text_input("Nhập Gmail đăng ký (*)", key="r_email")
        r_name = st.text_input("Nhập họ tên / Tên tổ chức (*)", key="r_name")
        r_pwd = st.text_input("Thiết lập mật khẩu (*)", type="password", key="r_pwd")
        r_role = st.selectbox("Vai trò bạn tham gia (*)", ["Người dùng", "Tổ chức Doanh nghiệp", "Hệ thống tái chế"], key="r_role")
        
        if st.button("Hoàn tất quy trình đăng ký", use_container_width=True):
            if r_email and r_name and r_pwd:
                st.session_state.users.append({"email": r_email.strip(), "name": r_name.strip(), "role": r_role, "pass": r_pwd})
                st.balloons()
                st.success("🌱 Chúc mừng bạn đã đăng ký thành công! Hãy chuyển sang tab Đăng nhập.")
            else:
                st.warning("⚠️ Vui lòng không để trống các ô có dấu (*)")
    st.markdown("</div>", unsafe_allow_html=True)

# ĐÃ ĐĂNG NHẬP THÀNH CÔNG
else:
    user = st.session_state.user_data
    
    # Khối thông tin thành viên tổng quan
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.markdown(f"### 🍀 Tài khoản: **{user['name']}**")
    st.markdown(f"Vai trò hoạt động: `:green[{user['role']}]`")
    
    # Hiển thị số liệu dạng Metric của Streamlit
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Cộng đồng LOOP", value=f"{len(st.session_state.users)} Thành viên")
    with col2:
        st.metric(label="Tổng khối lượng rác đã tái sinh", value=f"{st.session_state.waste_kgs} kg")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # KHU VỰC CHỨC NĂNG PHÂN QUYỀN
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    
    if user['role'] == "Người dùng":
        st.markdown("<h3>🤖 CỔNG NHẬN DIỆN & PHÂN LOẠI RÁC THẢI BẰNG AI</h3>", unsafe_allow_html=True)
        st.write("Hệ thống AI thông minh của LOOP sẽ giúp bạn quét hình ảnh các loại rác đang có, tự động phân tích phân loại rác hữu cơ/vô cơ/tái chế và tính điểm thưởng tương ứng.")
        
        # LỰA CHỌN PHƯƠNG THỨC QUÉT ẢNH
        ai_option = st.radio("Chọn cách cung cấp hình ảnh cho AI:", ["Tải ảnh từ máy tính", "Chụp ảnh trực tiếp bằng Camera"])
        
        image_file = None
        if ai_option == "Tải ảnh từ máy tính":
            image_file = st.file_uploader("Chọn tệp ảnh rác thải của bạn (.png, .jpg, .jpeg):", type=['jpg', 'png', 'jpeg'])
        else:
            image_file = st.camera_input("Hãy đưa rác thải trước camera máy tính/điện thoại:")
            
        if image_file is not None:
            # Hiển thị ảnh xem trước
            st.image(image_file, caption="Ảnh rác thải đang chờ xử lý...", use_container_width=True)
            
            if st.button("✨ KÍCH HOẠT MÔ HÌNH AI PHÂN TÍCH"):
                with st.spinner("🤖 Trí tuệ nhân tạo AI đang quét vật thể và phân tích cấu trúc..."):
                    time.sleep(3) # Giả lập thời gian AI xử lý tính toán thuật toán sâu
                    
                    # Giả lập mảng kết quả phân tích AI thực tế trả về
                    ai_results = [
                        {"item": "Chai nhựa nước ngọt (PET)", "category": "Rác tái chế nhựa", "status": "Hợp lệ", "points": 15},
                        {"item": "Vỏ lon nước ngọt", "category": "Rác tái chế kim loại", "status": "Hợp lệ", "points": 20},
                        {"item": "Túi nilon bẩn", "category": "Rác thải còn lại", "status": "Không tính điểm", "points": 0}
                    ]
                    
                    st.success("🎯 AI quét thành công! Báo cáo kết quả phân loại nguồn rác:")
                    
                    # Hiển thị bảng chi tiết vật thể AI tìm được
                    total_points_earned = 0
                    for index, obj in enumerate(ai_results):
                        total_points_earned += obj["points"]
                        st.markdown(f"**Vật thể {index+1}:** {obj['item']} 👉 Phân loại: *{obj['category']}* | Kết quả: `+{obj['points']} điểm`")
                    
                    st.write("---")
                    st.markdown(f"#### 🎉 TỔNG ĐIỂM XANH BẠN NHẬN ĐƯỢC: `+{total_points_earned} ĐIỂM`")
                    st.balloons() # Hiệu ứng bóng bay ăn mừng tích điểm môi trường sạch đẹp
                    
    elif user['role'] == "Hệ thống tái chế":
        st.markdown("<h3>🏭 TRẠM XỬ LÝ KHỐI LƯỢNG THU GOM</h3>", unsafe_allow_html=True)
        st.write("Chức năng cập nhật khối lượng rác thu gom thực tế tại kho bãi lên hệ thống tổng.")
        weight_input = st.number_input("Nhập số kg rác vừa xử lý thành công:", min_value=1, max_value=500, value=10)
        
        if st.button("⚡ Xác nhận cập nhật số liệu"):
            st.session_state.waste_kgs += weight_input
            st.success(f"Hệ thống ghi nhận tăng thêm {weight_input}kg rác thải được tái sinh!")
            time.sleep(1)
            st.rerun()
            
    elif user['role'] == "Tổ chức Doanh nghiệp":
        st.markdown("<h3>🏢 CỔNG TÀI TRỢ & CHIẾN DỊCH XANH</h3>", unsafe_allow_html=True)
        st.write("Dành cho doanh nghiệp quản lý các chiến dịch và ngân sách bảo trợ môi trường xanh sạch đẹp.")
        st.text_input("Tên chiến dịch cộng đồng muốn phát động:")
        if st.button("📢 Công bố chiến dịch"):
            st.success("Chiến dịch mới của doanh nghiệp đã được phát động toàn hệ thống thành công!")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # NÚT ĐĂNG XUẤT ĐỂ ĐỔI TÀI KHOẢN KHÁC TEST
    if st.button("🚪 Đăng xuất khỏi hệ thống", use_container_width=True):
        st.session_state.is_logged_in = False
        st.session_state.user_data = None
        st.rerun()
