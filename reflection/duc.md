# BẢN REFLECTION CÁ NHÂN — HACKATHON AI K4
**Học viên:** Nguyễn Minh Đức · **MSSV:** 2A202602783 · **Lớp:** 3A · **Phòng:** E403  
**Vai trò:** Backend & AI Engine Lead  

---

### 1. Đóng góp cụ thể của tôi trong dự án
* Thiết kế và xây dựng toàn bộ hệ thống Backend API bằng FastAPI, triển khai endpoint `POST /api/chat`.
* Tích hợp mô hình OpenAI `gpt-5-nano` sử dụng Structured Outputs với Pydantic schema chặt chẽ.
* Lập trình bộ bảo vệ Deterministic Guardrail độc lập để kiểm chứng chuỗi ký tự (`exact_quote in slide_context`), tự động kích hoạt cơ chế retry lượt 2 nếu LLM vi phạm.
* Xây dựng hệ thống ghi log chi tiết phục vụ đo kiểm tại `eval.log`.

### 2. Sự cố kỹ thuật / Quyết định sản phẩm khó khăn nhất
* Sự cố: Gặp lỗi CORS và timeout khi kết nối giữa Frontend và Backend do xung đột port và cấu hình credentials mode.
* Cách giải quyết: Cấu hình lại `allow_origin_regex=r".*"` trên FastAPI CORS Middleware và chuyển đổi sang SDK OpenAI mới với cơ chế bắt lỗi an toàn.

### 3. Bài học lớn nhất rút ra sau 48 giờ
* Không bao giờ được tin tưởng 100% vào output tự nhiên của LLM trong các ứng dụng mang tính học thuật. Sự kết hợp giữa khả năng suy luận của LLM và tính tất định (deterministic) của mã nguồn backend là chìa khóa duy nhất để triệt tiêu ảo giác.
