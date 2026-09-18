# BẢN REFLECTION CÁ NHÂN — HACKATHON AI K4
**Học viên:** Đặng Hữu Cương · **MSSV:** 2A202602572 · **Lớp:** 3A · **Phòng:** E403  
**Vai trò:** Đội trưởng · Product Owner & Evaluation Lead  

---

### 1. Đóng góp cụ thể của tôi trong dự án
* Quản lý tiến độ toàn bộ 6 Checkpoint của nhóm y0sh1da, đảm bảo mọi deliverable nộp đúng hạn.
* Khai phá dữ liệu chatlog K4, tìm ra 5 Turn ID làm bằng chứng thực tế cho nỗi đau thông tin sai lệch.
* Trực tiếp chấp bút và hoàn thiện 100% bản AI Spec (`spec.md` từ §1 đến §9), thiết lập bộ 20 test case Golden Set và chốt Quality Bar.
* Xây dựng nội dung slide pitch 6 trang và điều phối buổi thuyết trình.

### 2. Sự cố kỹ thuật / Quyết định sản phẩm khó khăn nhất
* Sự cố: Khi test ở CP3, câu hỏi mơ hồ *"Cái này là gì?"* từng bị model suy diễn nhầm sang Case A do slide chỉ có 1 định nghĩa.
* Cách giải quyết: Tôi cùng nhóm đã phân tích nguyên nhân và quyết định đảo thứ tự ưu tiên trong System Prompt, đưa quy tắc nhận diện đại từ mơ hồ lên Priority 1. Điều này giúp hệ thống đạt 95% trên Golden Set.

### 3. Bài học lớn nhất rút ra sau 48 giờ
* Tư duy sản phẩm AI hoàn toàn khác phần mềm truyền thống: Việc đặt ra ranh giới "AI không được làm gì" và cơ chế bảo vệ (Guardrail) quan trọng hơn nhiều so với việc cố làm cho AI trả lời hoa mỹ nhưng không kiểm chứng được.
