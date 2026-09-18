# HƯỚNG DẪN HÀNH ĐỘNG DÀNH CHO NHÓM Y0SH1DA (CP5 & CP6)
**Dành cho:** Đặng Hữu Cương (Lead) · Nguyễn Minh Đức (Backend) · Trần Đức Lộc (Frontend)  
**Thời gian:** Ngày 18/9/2026 (Chung kết Hackathon)

---

## 🚨 PHẦN 1: MỐC CP5 (HẠN CHÓT: 13:00 HÔM NAY — CỰC KỲ GẤP)

### Việc 1: Xuất file `demo-slides.pdf` (Cương phụ trách)
1. Mở file `SLIDE_PITCH_CONTENT.md` trong repo.
2. Copy nguyên văn nội dung của 6 slide vào Canva hoặc PowerPoint (chọn template phong cách tối giản, công nghệ, nền sáng hoặc tối).
3. Đảm bảo đúng **6 trang**, mỗi trang có đầy đủ số liệu và trích dẫn.
4. Xuất ra định dạng PDF với tên file chính xác: **`demo-slides.pdf`**.
5. Đặt file này ngay tại thư mục gốc của repo GitHub và push lên main.

### Việc 2: Quay video demo dự phòng 1-2 phút (Lộc phụ trách)
1. Mở giao diện `codebase/fronten/index.html` trên trình duyệt.
2. Đảm bảo backend đang chạy (`python -m uvicorn app.main:app --port 8001 --reload`).
3. Dùng phần mềm quay màn hình (OBS, Windows Game Bar `Win + G`, hoặc CapCut):
   * Thao tác lần lượt:
     - Case A: Bấm nút *"Data Lake là gì?"* -> Thấy ra câu trả lời có thẻ Citation xanh lá.
     - Case B: Bấm nút *"Cái này là gì?"* -> Thấy hiện Badge B vàng cam hỏi lại người học.
     - Case C: Gõ *"Hôm nay nộp bài tập gì?"* -> Thấy hiện Badge C đỏ từ chối lịch sự.
4. Đẩy video lên Google Drive, bật quyền **Bất kỳ ai có liên kết đều xem được**. Gửi link cho Cương để nộp form.

### Việc 3: Nộp Form CP5 trước 13:00 (Cương nộp)
* Điền mã học viên đội trưởng: `2A202602572`
* Đính kèm link file `demo-slides.pdf` trên GitHub và link video dự phòng trên Google Drive.

---

## 🎤 PHẦN 2: MỐC CP6 · THUYẾT TRÌNH TẠI PHÒNG E403 (17:30 HÔM NAY)

### 1. Phân vai thuyết trình 5 phút (Bắt buộc cả 3 cùng nói):
* **00:00 - 01:30 (Cương):** Mở đầu Slide 1 (Nỗi đau & Evidence 84%) + Slide 2 (Vì sao chọn A1 theo Cost of Error).
* **01:30 - 03:30 (Lộc & Đức):** Slide 3 Live Demo:
  * Lộc trực tiếp cầm chuột thao tác màn hình (chạy 1 case A chuẩn + 1 case B chỗ khó).
  * Đức đứng cạnh giải thích cơ chế Backend: OpenAI Structured Outputs + Deterministic Guardrail chặn ảo giác.
* **03:30 - 04:30 (Cương):** Slide 4 (Quality Bar 85% và kết quả đo 95%) + Slide 5 (Feedback từ 2 Willing Users Đạt & Khải).
* **04:30 - 05:00 (Cả nhóm):** Slide 6 (Bài học lớn nhất & Lời cảm ơn).

### 2. Chuẩn bị cho 5 phút Q&A & "Thẻ Giám Khảo":
* **Thẻ giám khảo (Chạy case lạ tại chỗ):**
  - Giám khảo sẽ đưa 1 câu hỏi bất kỳ. Nếu là câu hỏi ngoài bài -> Hệ thống sẽ vào Case C. Nếu câu hỏi cụt -> Vào Case B. Nếu có trong slide -> Vào Case A. Nhóm cứ bình tĩnh gõ vào web, Guardrail sẽ xử lý chính xác.
* **Câu hỏi về Kỹ thuật:** Đức trả lời (nhấn mạnh vào Pydantic validation và Guardrail kiểm tra chuỗi).
* **Câu hỏi về UX/UI:** Lộc trả lời (nhấn mạnh vào 4 nguyên tắc HAX/PAIR và 3 màu sắc trực quan).
* **Câu hỏi về Sản phẩm/Bài toán:** Cương trả lời (nhấn mạnh vào Cost of Error và khảo sát chatlog K4).
