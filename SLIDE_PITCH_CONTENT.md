# NỘI DUNG 6 TRANG SLIDE THUYẾT TRÌNH (DEMO-SLIDES) & KỊCH BẢN PITCH
**Dự án:** Grounded Tutor — Trợ giảng AI "Biết-mình-không-biết"  
**Nhóm:** y0sh1da · Lớp 3A · Phòng E403  
**Thời lượng:** 5 phút thuyết trình + 5 phút Q&A  
**Quy chuẩn bắt buộc:** Mỗi slide đều có số liệu / quote kiểm chứng được; mỗi thành viên trong nhóm trình bày ít nhất 1 phần.

---

## 📑 TRANG 1 · USER & JOB (45 GIÂY)
> **Người trình bày:** Đặng Hữu Cương (Đội trưởng)

* **Tiêu đề Slide:** GROUNDED TUTOR — TRỢ GIẢNG AI "BIẾT-MÌNH-KHÔNG-BIẾT"
* **User & Bối cảnh:** Sinh viên VLearn đang tự học theo tài liệu slide bài giảng môn kỹ thuật (Data Engineering).
* **Core JTBD:** *"Hiểu đúng và nhanh chóng các khái niệm kỹ thuật trong bài giảng để hoàn thành bài tập mà không bị hiểu sai kiến thức học thuật."*
* **Con số nỗi đau thực tế (Mining từ dữ liệu K4):**
  * Khảo sát chatlog K4: **84%** lượt trao đổi gặp tình trạng AI trả lời không có căn cứ hoặc trả lời mơ hồ khi thiếu cơ chế grounding.
  * **5 Bằng chứng Turn ID thực tế:** `T10293` (AI tự bịa so sánh), `T10316` (AI đoán mò câu hỏi cụt), `T10303` (AI bịa deadline bài tập), `T10296` (AI chỉ dẫn ngoài lề), `T10298` (Người học hỏi "cái này là sao" thì AI trả lời sai trọng tâm).
* **Lời nói (Speaker Script):**  
  *"Kính thưa Ban giám khảo và các bạn. Khi sinh viên tự học qua slide, nỗi sợ lớn nhất không phải là không có câu trả lời, mà là nhận được một câu trả lời sai nhưng nghe rất thuyết phục từ AI. Dữ liệu từ khoá K4 cho thấy có tới 84% trường hợp sinh viên hoang mang vì AI chém gió ngoài lề hoặc bịa đặt trích dẫn. Đó là lý do nhóm y0sh1da xây dựng Grounded Tutor — một trợ giảng AI triệt để tuân thủ nguyên tắc: Biết mình không biết."*

---

## 📑 TRANG 2 · VÌ SAO CHỌN TÍNH NĂNG NÀY (45 GIÂY)
> **Người trình bày:** Đặng Hữu Cương

* **Tiêu đề Slide:** BÀI TOÁN CÓ CHI PHÍ SAI SÓT (COST OF ERROR) CAO NHẤT
* **Bảng so sánh 3 ứng viên:**
  1. *A1. Grounded Tutor (Biết mình không biết):* 100% sinh viên gặp, tần suất 5-10 lần/buổi. **Cost of error: RẤT CAO** (hiểu sai kiến thức cốt lõi, trượt môn, sai đồ án). -> **CHỌN**.
  2. *A2. Quiz Generator (Tự sinh trắc nghiệm):* Tần suất thấp (chỉ dùng lúc thi), câu hỏi dở thì bỏ qua. Cost of error: Thấp. -> **LOẠI**.
  3. *A3. Auto-Summarizer (Tóm tắt bài học):* Tính năng thụ động, không giải quyết được khi học viên bị tắc ở 1 thuật ngữ cụ thể. -> **LOẠI**.
* **Định vị khác biệt với thị trường:**
  * *Coursera Coach:* Trả lời theo kiến thức internet chung chung, không có trích dẫn câu gốc.
  * *Khanmigo:* Luôn hỏi gợi mở lòng vòng ngay cả khi sinh viên chỉ cần xác thực một sự thật từ slide.
  * *Grounded Tutor:* Đủ bằng chứng thì trả lời trực diện kèm trích dẫn nguyên văn; chỉ hỏi lại khi câu hỏi thực sự mơ hồ; ngoài bài thì kiên quyết từ chối.
* **Lời nói (Speaker Script):**  
  *"Nhóm đã cân nhắc 3 hướng tính năng, và quyết định chọn Grounded Tutor vì đây là bài toán có chi phí sai sót cao nhất. Nếu AI sinh một câu hỏi trắc nghiệm dở, bạn có thể bỏ qua. Nhưng nếu AI dạy sai một định nghĩa kỹ thuật, sinh viên sẽ mang kiến thức sai đó đi thi và làm đồ án. Với Grounded Tutor, chúng tôi chấp nhận nói 'Tôi không biết' thay vì trả lời sai."*

---

## 📑 TRANG 3 · THIẾT KẾ GIẢI PHÁP & LIVE DEMO (2 PHÚT)
> **Người trình bày:** Trần Đức Lộc (Thao tác Demo) & Nguyễn Minh Đức (Giải thích Kỹ thuật)

* **Tiêu đề Slide:** KIẾN TRÚC 3 NHÁNH & BỘ BẢO VỆ DETERMINISTIC GUARDRAIL
* **Lát cắt 1 câu:**  
  *"Khi sinh viên đặt câu hỏi về slide trên VLearn, hệ thống phân loại chính xác vào 1 trong 3 nhánh: Trả lời có trích dẫn chuẩn / Hỏi lại để làm rõ / Từ chối có hướng dẫn, đảm bảo 100% câu trả lời có căn cứ."*
* **Mức tự động hóa:** Conditional Automation (Chỉ tự động khi đủ bằng chứng; hạ mức tự động hóa để hỏi lại hoặc từ chối khi rủi ro cao).
* **Áp dụng 4 nguyên tắc HAX/PAIR:**
  * *G1 (Năng lực rõ ràng):* Hiển thị trạng thái kết nối và 3 nút câu hỏi mẫu.
  * *G2 (Độ tin cậy trực quan):* 3 Badge màu (Xanh Case A, Vàng cam Case B, Đỏ Case C).
  * *G10 (Minh chứng trích dẫn):* Khung Citation hiện số slide và exact quote 100%.
  * *G11 (Lý do hành vi):* Giải thích vì sao cần làm rõ câu hỏi kèm gợi ý tiếp theo.
* **Kịch bản Live Demo (Lộc thao tác trực tiếp trên màn hình):**
  * *Demo 1 (Case A chuẩn):* Bấm *"Data Lake là gì?"* -> Hệ thống trả lời và hiện khung Citation trích dẫn nguyên văn từ Slide 12.
  * *Demo 2 (Case B - Chỗ khó):* Bấm *"Cái này là gì?"* -> AI không đoán mò, kích hoạt Case B yêu cầu người học làm rõ đối tượng.
  * *Demo 3 (Case C - Ngoài phạm vi):* Gõ *"Hạn nộp bài tập tuần này?"* -> Hệ thống từ chối lịch sự và hướng dẫn kiểm tra LMS.
* **Lời nói của Đức (Backend):**  
  *"Về mặt kỹ thuật, chúng tôi không phó mặc cho LLM. Phía sau OpenAI gpt-5-nano là một bộ lọc Deterministic Guardrail viết bằng Python. Nếu trích dẫn của LLM không khớp 100% từng ký tự trong slide context, Guardrail sẽ lập tức chặn lại và ép mô hình re-evaluate lần 2. Điều này triệt tiêu hoàn toàn lỗi Citation Fabrication."*

---

## 📑 TRANG 4 · KẾT QUẢ ĐO KIỂM & QUALITY BAR (45 GIÂY)
> **Người trình bày:** Đặng Hữu Cương

* **Tiêu đề Slide:** ĐO LƯỜNG ĐỊNH LƯỢNG TRÊN GOLDEN SET (20 TEST CASES)
* **Quality Bar (Đã khóa tại CP4 - 21:00 17/9):**
  > **"Pass >= 85% trên Golden Set 20 case, và Tỷ lệ bịa đặt trích dẫn (Citation Fabrication) = 0%."**
* **Kết quả các lượt chạy:**
  * *Lượt 1 (Baseline):* Đạt **90%** (18/20 case), 0 lỗi bịa trích dẫn. Vướng 2 case mơ hồ bị nhận diện nhầm sang Case A.
  * *Lượt 2 (Sau khi tinh chỉnh prompt):* Đạt **95%** (19/20 case), **0 lỗi bịa trích dẫn**.
* **Độ phủ 4 lớp chỗ khó trong Golden Set:**
  * Lớp 1 (Ảo giác trích dẫn): 5/5 pass (100%).
  * Lớp 2 (Suy diễn quá đà): 5/5 pass (100%).
  * Lớp 3 (Đại từ mơ hồ): 4/5 pass (80% -> 100% ở Lượt 2).
  * Lớp 4 (Ngoài phạm vi / Jailbreak): 5/5 pass (100%).
* **Lời nói (Speaker Script):**  
  *"Tại CP4 tối qua, nhóm đã khóa Quality Bar ở mức 85% và cam kết 0% bịa nguồn. Kết quả chạy thực nghiệm trên bộ 20 test case phủ đủ 4 lớp rủi ro đạt 95% pass, và quan trọng nhất: tỷ lệ bịa nguồn bằng đúng 0%. Mọi câu trả lời Case A đều kiểm chứng được nguồn gốc xuất xứ từng chữ."*

---

## 📑 TRANG 5 · USER THẬT NÓI GÌ (VALIDATION R6) (45 GIÂY)
> **Người trình bày:** Cương / Lộc

* **Tiêu đề Slide:** ĐƯA RA NGƯỜI DÙNG THẬT & BÀI HỌC CẢI TIẾN
* **Thử nghiệm với 5 người dùng ngoài nhóm (2 Willing Users khai từ CP1):**
  * *Thân Tiến Đạt (Willing User 1):* *"Hay ở chỗ nó chỉ rõ nguồn ở Slide 12 và chép đúng câu trong slide ra. Bình thường hỏi ChatGPT nó hay chém gió lan man sang Hadoop với Spark mà mình chưa học tới."*
  * *Vũ Gia Khải (Willing User 2):* *"Lúc đầu mình gõ 'cái này là gì', nó không đoán bừa mà hỏi lại mình muốn hỏi về Data Lake hay kho lưu trữ thô. Như vậy rất chuẩn."*
* **Chỉ số Disappointment (Sean Ellis PMF):**  
  * **80% (4/5 bạn)** trả lời *"Rất tiếc nếu không được dùng Grounded Tutor nữa"*.
* **Một cải tiến làm ngay từ phản hồi người dùng (Changelog v0.4):**  
  * Khi người dùng hỏi *"cái này"*, bot từng đoán là Data Lake. Nhóm đã lập tức nâng mức ưu tiên nhận diện đại từ mơ hồ lên Priority 1 trong prompt để luôn ép vào Case B.
* **Lời nói (Speaker Script):**  
  *"Khi mang sản phẩm cho 5 bạn sinh viên dùng thử, chúng tôi nhận được 80% phản hồi rất tiếc nếu thiếu công cụ này. Bài học lớn nhất từ user testing là người học thường có thói quen gõ câu hỏi rất cụt lủn như 'cái này là gì'. Nếu AI tự tiện đoán, người học sẽ mất niềm tin. Nhờ đó, chúng tôi đã kịp thời tối ưu hóa bộ prompt trước khi bước vào chung kết hôm nay."*

---

## 📑 TRANG 6 · NẾU CÓ THÊM 1 TUẦN & BÀI HỌC LỚN NHẤT (30 GIÂY)
> **Người trình bày:** Cả 3 thành viên

* **Tiêu đề Slide:** ROADMAP TƯƠNG LAI & BÀI HỌC TƯ DUY SẢN PHẨM AI
* **2 Việc ưu tiên hàng đầu nếu có thêm 1 tuần (Backlog):**
  1. *Semantic Caching:* Giảm độ trễ từ 12s xuống < 1s cho các câu hỏi lặp lại của sinh viên.
  2. *Auto PDF Context Ingestion:* Tự động bóc tách slide từ file PDF/PPTX của giảng viên thành vector chunks có số trang thay vì dán thủ công.
* **Bài học lớn nhất của cả nhóm (The Biggest Takeaway):**  
  > *"Trong giáo dục, AI 'biết từ chối và biết hỏi lại' có giá trị và độ tin cậy cao hơn một AI cố trả lời mọi thứ nhưng chứa đầy ảo giác."*
* **Lời nói (Speaker Script):**  
  *"Nếu có thêm thời gian, mục tiêu số một của chúng tôi là giải quyết bài toán độ trễ bằng Semantic Caching. Nhưng bài học lớn nhất mà cả 3 chúng tôi học được qua 48 giờ vừa qua: Giá trị của một sản phẩm AI không nằm ở việc nó nói được bao nhiêu thứ hoa mỹ, mà nằm ở dũng cảm nói 'Tôi không biết' để bảo vệ sự chính xác cho người học. Xin cảm ơn Ban giám khảo!"*
