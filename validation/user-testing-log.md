# NHẬT KÝ THỬ NGHIỆM NGƯỜI DÙNG (USER TESTING LOG)
**Dự án:** Grounded Tutor — Trợ giảng AI "Biết-mình-không-biết" (Track A1)  
**Nhóm:** y0sh1da · Lớp 3A · Phòng E403  
**Mục tiêu:** Kiểm thử thực tế trải nghiệm người học theo quy chuẩn R6 (+8 điểm rubric) với 2 Willing Users đã đăng ký từ CP1, phát hiện điểm gãy trong tương tác và cải tiến sản phẩm trước vòng thuyết trình CP6.

---

## 📋 1. THIẾT KẾ PHIÊN TEST (THEO QUY CHUẨN 5 NHỊP)
* **Phương pháp:** Giao nhiệm vụ dựa trên kết quả đầu ra (Outcome-based Task), người quan sát giữ im lặng và ghi nhận hành vi thật (không giải thích hay hướng dẫn thao tác).
* **5 Nhịp thực hiện (10 phút/người):**
  1. *Comfort (~1'):* Trấn an người dùng ("Đánh giá sản phẩm, không đánh giá bạn").
  2. *Context (~1'):* Hỏi về trải nghiệm học slide môn Data Engineering gần nhất.
  3. *Task (~1'):* Người dùng tự cầm chuột sử dụng Grounded Tutor để tra cứu một khái niệm vướng mắc trên slide.
  4. *Observe (~5'):* Quan sát hành vi (chỗ dừng lại, thao tác gõ, phản ứng khi thấy nhãn A/B/C).
  5. *Hỏi sau khi dùng (~2'):* Ghi lại quote nguyên văn cảm nhận, độ tin cậy và câu hỏi Disappointment (Sean Ellis).

---

## 👥 2. BẢNG NHẬT KÝ KIỂM THỬ THỰC TẾ (2 WILLING USERS NGOÀI NHÓM)

| STT | Người thử | Vai trò / Đặc điểm | Nhiệm vụ giao (Task) | Hành vi quan sát được (Observe) | Quote nguyên văn của người dùng | Đánh giá & Quyết định xử lý |
|:---:|---|---|---|---|---|---|
| **1** | **Thân Tiến Đạt**<br>*(MSSV: 2A202603023)* | Sinh viên K4, học lực Khá, thường tự đọc slide trước giờ học | Đọc slide 12 và tra cứu: "Data Lake là gì?", sau đó thử hỏi câu hỏi ngoài bài | Nhập câu hỏi rất nhanh, mắt nhìn ngay vào khung trích dẫn **Citation** màu xanh lá. Dừng lại đọc kỹ đoạn trích dẫn nguyên văn trước khi đọc câu trả lời. Sau đó thử hỏi một câu ngoài bài và thấy bot hiện **Badge C (Từ chối)**. | *"Hay ở chỗ nó chỉ rõ nguồn ở Slide 12 và chép đúng câu trong slide ra. Bình thường hỏi ChatGPT nó hay chém gió lan man sang Hadoop với Spark mà mình chưa học tới. Còn câu hỏi ngoài bài thì nó từ chối thẳng thắn, không chém bừa."* | **Thành công (Case A & Case C)**.<br>Người dùng xác nhận tính năng trích dẫn nguyên văn giúp tạo niềm tin tuyệt đối vào kiến thức học thuật. |
| **2** | **Vũ Gia Khải**<br>*(MSSV: 2A202602786)* | Sinh viên K4, thích hỏi vắn tắt, hay dùng câu hỏi cụt | Dùng từ ngữ tự nhiên để hỏi sâu hơn về nội dung vừa đọc trên slide | Ban đầu chỉ gõ đúng 4 chữ: *"cái này là gì?"*. Khi thấy hệ thống không trả lời ngay mà hiện **Badge B (HỎI LÀM RÕ)** kèm câu hỏi ngược lại, bạn hơi bất ngờ nhưng sau đó gõ lại câu hỏi chi tiết hơn. | *"Ủa lúc đầu mình gõ 'cái này là gì', nó không đoán bừa mà hỏi lại mình muốn hỏi về Data Lake hay kho lưu trữ thô. Như vậy rất chuẩn, chứ đoán mò lỡ mình hỏi cái khác thì sao."* | **Thành công (Case B)**.<br>Chứng minh giá trị cốt lõi: "Biết mình không biết". Đã kịp thời sửa prompt ở v0.4 để nhận diện triệt để đại từ mơ hồ. |

---

## 📊 3. ĐO LƯỜNG ĐỘ THIẾT YẾU (SEAN ELLIS DISAPPOINTMENT SCORE)
Sau buổi thử nghiệm, cả 2 bạn được hỏi câu hỏi chuẩn Product-Market Fit:  
*"Nếu từ ngày mai bạn không được sử dụng Grounded Tutor khi học bài giảng nữa, bạn sẽ cảm thấy thế nào?"*
* **Rất tiếc (Very Disappointed):** 2/2 người (**100%** — vượt xa ngưỡng chuẩn 40% của Sean Ellis).
* **Hơi tiếc (Somewhat Disappointed):** 0/2 người (**0%**).
* **Không sao (Not Disappointed):** 0/2 người (**0%**).

---

## 🎯 4. TỔNG HỢP 4 DÒNG KẾT LUẬN (THEO CHUẨN §4.2 CỦA BTC)

1. **Chủ đề lặp nhiều nhất:**
   Cả 2 bạn đều đánh giá cao nhất sự **minh bạch và trung thực** (luôn có trích dẫn nguyên văn và không bịa đặt), nhưng đều phản ánh về **độ trễ phản hồi** (mất khoảng 10-12 giây cho mỗi lượt gọi do mô hình `gpt-5-nano` phân tích sâu).
2. **Thay đổi đã làm ngay trước vòng demo (Đã cập nhật vào Changelog §9 của `spec.md`):**
   Đưa quy tắc nhận diện đại từ mơ hồ (*"cái này"*, *"nó"*, *"cái ấy"*) lên mức **Ưu tiên số 1 (Priority 1)** trong System Prompt. Khi gặp các từ này mà không chỉ đích danh khái niệm, hệ thống bắt buộc vào **Case B (Hỏi làm rõ)** chứ không được tự suy diễn sang Case A.
3. **Giữ nguyên có lý do:**
   Giữ nguyên nguyên tắc kiểm định nghiêm ngặt: **100% trích dẫn phải xuất hiện nguyên văn trong slide context** (nếu lệch 1 chữ backend guardrail sẽ từ chối và kích hoạt retry lượt 2). Không nới lỏng quy tắc này để đảm bảo uy tín học thuật.
4. **Đưa vào Backlog cho tương lai (Trình bày ở Slide 6):**
   Xây dựng cơ chế **Semantic Caching** đối với các câu hỏi phổ biến để trả lời ngay lập tức (<1 giây) và tính năng **tự động bóc tách tài liệu bài giảng từ file PDF/PPTX** thay vì phải dán ngữ cảnh thủ công.
