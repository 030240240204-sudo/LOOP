import streamlit as st
import pandas as pd
import time

# --- CẤU HÌNH TRANG ---
st.set_page_config(
    page_title="LOOP System - Môi Trường Xanh",
    page_icon="🌿",
    layout="centered"
)

# --- CSS TÙY CHỈNH (GIAO DIỆN HOA LÁ & CỎ CÂY) ---
st.markdown("""
    <style>
    /* Hình nền thiên nhiên toàn trang */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                          url('http://googleusercontent.com/image_collection/image_retrieval/8193808484771602678');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Tạo hiệu ứng kính mờ cho các khối nội dung */
    div.stButton > button:first-child {
        background-color: #2ecc71;
        color: white;
        border-radius: 20px;
        border: none;
        transition: all 0.3s ease;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #27ae60;
        transform: scale(1.05);
    }

    .main-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: white;
    }

    h1, h2, h3, p {
        color: #f1f8e9 !important;
    }
    
    .stTextInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- KHỞI TẠO DỮ LIỆU ---
if "users" not in st.session_state:
    st.session_state.users = [
        {"email": "eco@loop.vn", "name": "Đại sứ Xanh", "role": "Người dùng", "pass": "123"}
    ]
if "waste_kgs" not in st.session_state:
    st.session_state.waste_kgs = 500
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False
if "user_data" not in st.session_state:
    st.session_state.user_data = None

# --- GIAO DIỆN CHÍNH ---
st.markdown("<h1 style='text-align: center;'>🌿 LOOP SYSTEM</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Kiến tạo tương lai xanh từ hành động nhỏ hôm nay</p>", unsafe_allow_html=True)

if not st.session_state.is_logged_in:
    # Giao diện Đăng nhập / Đăng ký
    with st.container():
        st.markdown("<div class='main-card'>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🍃 Đăng nhập", "🌱 Đăng ký"])
        
        with tab1:
            email = st.text_input("Gmail", key="l_email")
            name = st.text_input("Họ và tên", key="l_name")
            pwd = st.text_input("Mật khẩu", type="password", key="l_pwd")
            role = st.selectbox("Vai trò", ["Người dùng", "Tổ chức", "Hệ thống tái chế"], key="l_role")
            
            if st.button("Bắt đầu hành trình xanh"):
                user = next((u for u in st.session_state.users if u['email'] == email and u['pass'] == pwd), None)
                if user:
                    st.session_state.is_logged_in = True
                    st.session_state.user_data = user
                    st.success("Chào mừng bạn quay lại với hệ sinh thái!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Thông tin chưa chính xác, hãy kiểm tra lại nhé!")

        with tab2:
            r_email = st.text_input("Gmail mới", key="r_email")
            r_name = st.text_input("Họ tên đầy đủ", key="r_name")
            r_pwd = st.text_input("Mật khẩu", type="password", key="r_pwd")
            r_role = st.selectbox("Bạn tham gia với tư cách", ["Người dùng", "Tổ chức", "Hệ thống tái chế"], key="r_role")
            
            if st.button("Gia nhập cộng đồng"):
                st.session_state.users.append({"email": r_email, "name": r_name, "role": r_role, "pass": r_pwd})
                st.balloons()
                st.success("Đăng ký thành công! Hãy đăng nhập để bắt đầu.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    # DASHBOARD
    user = st.session_state.user_data
    st.markdown(f"### Chào mừng bạn, {user['name']}! ✨")
    st.markdown(f"Vai trò: **{user['role']}**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cộng đồng Xanh", f"{len(st.session_state.users)} thành viên")
    with col2:
        st.metric("Rác thải đã xử lý", f"{st.session_state.waste_kgs} kg", delta="+15kg hôm nay")

    st.write("---")
    
    # Khu vực chức năng
    st.subheader("🍀 Hoạt động môi trường")
    if user['role'] == "Người dùng":
        st.info("Hôm nay bạn đã phân loại rác chưa? Hãy chụp ảnh và đổi lấy điểm thưởng nhé!")
        if st.button("📸 Quét rác thải để tích điểm"):
            with st.spinner("Đang phân tích hình ảnh..."):
                time.sleep(2)
                st.success("Phát hiện 2 chai nhựa PET! Bạn nhận được 20 điểm Xanh.")
                
    elif user['role'] == "Hệ thống tái chế":
        st.warning("Đang có 3 yêu cầu thu gom mới tại khu vực của bạn.")
        if st.button("✅ Xác nhận hoàn thành xử lý 20kg giấy"):
            st.session_state.waste_kgs += 20
            st.success("Dữ liệu hệ thống đã được cập nhật!")
            st.rerun()
# KHÔNG GIAN TÍNH NĂNG TỰ ĐỘNG THAY ĐỔI THEO PHÂN QUYỀN TRUY CẬP
    st.subheader("⚙️ Không gian chức năng riêng biệt")
    
    if user["role"] == "Người dùng cá nhân":
        st.markdown("#### 🎁 Đặc quyền cá nhân xanh")
        st.info("Hãy tích cực phân loại rác thải tại nhà (nhựa, giấy, kim loại) và mang tới trạm thu gom gần nhất để đổi lấy điểm thưởng mua sắm giá trị!")
        
        if st.button("✨ Thực hiện hành động: Đổi rác lấy 50 điểm", type="primary"):
            st.balloons() # Hiệu ứng bóng bay ăn mừng cực đẹp của Streamlit
            st.success("🎉 Bạn vừa được cộng 50 điểm LOOP! Lịch sử đã được ghi nhận vào tài khoản.")
            
    elif user["role"] == "Tổ chức Doanh nghiệp":
        st.markdown("#### 🏢 Bảng quản trị Doanh nghiệp")
        st.info("Nơi quản lý ngân sách tài trợ môi trường, phát động các chiến dịch truyền thông xanh và theo dõi chứng chỉ giảm phát thải carbon.")
        
        campaign_name = st.text_input("Tên chiến dịch bảo vệ môi trường muốn phát động:")
        if st.button("📢 Phát động chiến dịch mới trên toàn hệ thống", type="primary"):
            if campaign_name:
                st.success(f"📢 Chiến dịch **'{campaign_name}'** đã gửi lên cổng kiểm duyệt thành công!")
            else:
                st.warning("⚠️ Vui lòng nhập tên chiến dịch trước khi phát động.")
                
    elif user["role"] == "Hệ thống thu gom tái chế":
        st.markdown("#### 🏭 Điều hành trạm xử lý rác thải")
        st.info("Dành cho các chủ cơ sở tái chế. Bạn có quyền cập nhật khối lượng rác thực tế vừa xử lý thành công để ghi nhận trực tiếp lên hệ thống.")
        
        if st.button("⚡ Xác nhận đã xử lý thành công +15kg rác thải", type="primary"):
            st.session_state.waste_kgs += 15
            st.success("⚡ Dữ liệu đã truyền đi! Hệ thống tổng bộ vừa tăng thêm 15kg rác được tái chế.")
            st.rerun() # Refresh để cập nhật số liệu trên thanh Metric ngay lập tức

    st.write("---")
    if st.button("Đăng xuất"):
        st.session_state.is_logged_in = False
        st.rerun()