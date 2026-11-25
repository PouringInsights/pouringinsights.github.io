# Brief: ĐCBG + slide cho bài thực hành (Bài 12–15), học phần Phân tích dữ liệu Marketing (BM6110, HaUI)

Học phần có 10 bài lý thuyết (Bài 1–10) và 5 buổi thực hành, đánh số Bài 11–15 = Thực hành 1–5.
Mỗi bài thực hành cần: (1) **Đề cương bài giảng (ĐCBG)** dạng docx, (2) **slide** pptx, đúng FORMAT của Bài 1–10,
nhưng NỘI DUNG là hướng dẫn thực hành cho sinh viên + ôn lại kiến thức lý thuyết liên quan đã học ở các bài trước.

## Nguồn (đọc trước khi viết)
- Đề bài và Đáp án của buổi thực hành: đọc bằng tool Google Drive `mcp__Google_Drive__read_file_content`
  (nạp schema bằng ToolSearch "select:mcp__Google_Drive__read_file_content,mcp__Google_Drive__search_files").
  - Thực hành 2 (→ Bài 12): Đề 1p8bsK_gckbc9UUM_vm4trcAIqSjRp6uI, Đáp án 1SBbSmtcsjQl4fb2fk_51ThytAN3ZV40m, dữ liệu LUMI (folder 1dF2jGxYKWGaERTQExIPVqrkNK3NEBq39)
  - Thực hành 3 (→ Bài 13): Đề 1v7s_W47sNmcJSsUE4KNYeDomYyqC2tEH, Đáp án 156XfBFKHOmA_mairUhqHitbBmLLvOil0, dữ liệu EDUGO (folder 1d6FuVKDGgPlEZ7w2SIcBVyLDj0Jac5yw; có EDUGO_tu_dien_bien_khao_sat.csv)
  - Thực hành 4 (→ Bài 14): Đề 1lEihOHKiohL_zc_TOvGbISym_wYt_Ig7, Đáp án 1rkichr4AFSFead4BdgMrACDVI-4XtVrR, dữ liệu MOVA (folder 1DXy9l0UDKzzoIQKFeVjEaf_1ZP8qqlwY)
  - Thực hành 5 (→ Bài 15): Đề 1t3LXiRjIqrOLlIltrh07k4KJiUAuFyVn, Đáp án 1mDxN25qf9MbzOnZhBvbJ3hhot66QwT5M, dữ liệu (folder 1RDcvdPpcc5vQK7y83KFaDAFTBTyO4ESy)
- Lý thuyết đã học (để trích dẫn và ôn lại): chữ trên slide các bài ở thư mục này: b1_slides.txt, b3_slides.txt … b8_slides.txt, b10_slides.txt;
  ĐCBG mẫu (docx) tại ../dcbg/b8.docx, b7.docx, b1.docx (đọc bằng python-docx để học cấu trúc và giọng văn).
  Bài 2, 9, 10 chỉ có pdf: tìm trên Drive nếu cần (search_files title contains 'Bài 9').

## Format bắt buộc (dùng bộ kit, KHÔNG tự dựng từ đầu)
`import sys; sys.path.insert(0, "<scratchpad>/tools"); from kits import Dcbg, Deck` (đọc docstring trong ../tools/kits.py).
Dùng python của venv: `<scratchpad>/vn311/bin/python` (có python-docx, python-pptx).

### ĐCBG (docx) – bám cấu trúc ĐCBG Bài 8:
- `d.title("BÀI N:", "THỰC HÀNH k: <TÊN CHỦ ĐỀ>")`
- Mở đầu: mục tiêu học tập (h2 hoặc bullet), chuẩn đầu ra, kiến thức cần có (liệt kê bài lý thuyết liên quan, ví dụ "Bài 3, mục 3.2").
- N.1 Ôn tập kiến thức lý thuyết trọng tâm (tóm tắt có hệ thống các khái niệm, công thức, ngưỡng, giả định cần dùng; bảng so sánh khi phù hợp).
- N.2 Tình huống và dữ liệu (bối cảnh doanh nghiệp, mô tả từng tệp, bảng mô tả cột, lưu ý chất lượng dữ liệu).
- N.3 … N.x Hướng dẫn từng yêu cầu của đề: mục đích, phương pháp, các bước làm (Python/R/SPSS: tên hàm, tham số quan trọng), cách đọc kết quả, cạm bẫy thường gặp, sản phẩm cần nộp.
  KHÔNG chép đáp án/kết quả số cuối cùng từ file Đáp án (file đó chỉ dành cho giảng viên). Được dùng ví dụ minh hoạ nhỏ với số liệu tự đặt.
- Ví dụ minh hoạ có đánh số (`d.example("Ví dụ N.1. …")`), bảng có `caption("Bảng N.1. …")`.
- Tiêu chí đánh giá / thang điểm (bảng, khớp thang điểm trong đề).
- `plain_heading("Tóm tắt bài học")`, `plain_heading("CÂU HỎI ÔN TẬP")` (5–8 câu tự luận ngắn), `plain_heading("TÀI LIỆU THAM KHẢO")` (giáo trình/bài báo chuẩn: Hair et al., Malhotra, scikit-learn docs, … chỉ ghi nguồn có thật).
- Độ dài: 12–20 trang A4 (≈ 5.000–8.000 từ).

### Slide (pptx) – 22–32 slide, khuôn HaUI của Bài 8:
- `k.cover(...)`, slide mục tiêu/CĐR (bullets), AGENDA (bullets), case mở đầu, mỗi mục lớn có `k.section("N.1.  …")`,
  nội dung bằng `k.bullets` (≤ 7 ý, mỗi ý ≤ 25 từ) và `k.table` (≤ 6 cột, ≤ 8 hàng), slide "Quy trình thực hiện",
  "Lỗi thường gặp", "Sản phẩm nộp & tiêu chí chấm", "Tóm tắt", "Câu hỏi thảo luận".
- Không chép nguyên văn đoạn dài từ ĐCBG; slide ngắn gọn.

## Văn phong (unslop)
Câu ngắn, chủ ngữ rõ; không sáo rỗng ("vô cùng quan trọng", "then chốt", "toàn diện", "bối cảnh ngày nay"); không gạch ngang dài thay dấu phẩy;
thuật ngữ tiếng Anh giữ nguyên khi phổ biến (K-means, Silhouette, CLV…) kèm giải thích tiếng Việt lần đầu. Mọi công thức/ngưỡng phải đúng theo nguồn chuẩn (tra web khi không chắc).

## Đầu ra (thư mục `<scratchpad>/th_out/bai_N/`)
- `Bai N_Thuc hanh k_ĐCBG.docx`, `Bai N_Thuc hanh k_Slides.pptx`
- Render kiểm: `soffice --headless --convert-to pdf --outdir <dir>` cho TỪNG file (outdir riêng để không trùng tên),
  rồi xem ảnh vài trang/slide (pymupdf có trong venv) để chắc không tràn chữ, không slide trống, bảng không vỡ. Sửa đến khi sạch.
- Báo cáo ngắn: số trang ĐCBG, số slide, các bài lý thuyết đã liên kết, chỗ đề bài/đáp án mơ hồ hoặc sai (nếu có).
