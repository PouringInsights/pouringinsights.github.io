# Bài 4. Dữ liệu thực hành: nhận thức, Conjoint và định giá

Dữ liệu mô phỏng, hư cấu, chỉ dùng cho học tập. Bám theo các ví dụ trong slide: bản đồ MDS sáu thương hiệu nước giải khát có ga, hồi quy thuộc tính lên ý định mua, Conjoint chuỗi cà phê (slide ẩn 18 đến 27) và Van Westendorp.

```
python gen_data.py      # sinh 6 file CSV (seed cố định)
python solution.py      # lời giải tham khảo
```

Thư viện: pandas, numpy, scikit-learn, scipy, statsmodels.

## 1. Các file dữ liệu

| File | Số dòng | Một dòng là |
|---|---|---|
| b4_mds_khaosat.csv | 2.250 | 1 đáp viên chấm 1 cặp thương hiệu (150 người × 15 cặp) |
| b4_danhgia_thuonghieu.csv | 900 | 1 đáp viên chấm 1 thương hiệu trên 2 thuộc tính (150 × 6) |
| b4_hoiquy_nuocngot.csv | 400 | 1 đáp viên |
| b4_conjoint_profiles.csv | 9 | 1 tổ hợp trong thiết kế trực giao L9 |
| b4_conjoint_khaosat.csv | 1.800 | 1 lượt chấm điểm (200 đáp viên × 9 tổ hợp) |
| b4_vanwestendorp.csv | 320 | 1 đáp viên |

**b4_mds_khaosat.csv:** `dap_vien`, `thuong_hieu_1`, `thuong_hieu_2`, `muc_giong_nhau` (1 = hoàn toàn khác, 9 = gần như giống hệt). Sáu thương hiệu: Coca-Cola, Pepsi, Sprite, 7Up, Fanta, Mirinda.

**b4_danhgia_thuonghieu.csv:** `dap_vien`, `thuong_hieu`, `vi_cola_dam`, `cao_cap` (thang 1 đến 7). Dùng để dựng bản đồ theo thuộc tính và so với bản đồ MDS.

**b4_hoiquy_nuocngot.csv:** điểm đánh giá thang 1 đến 7 của `hinh_anh_thuong_hieu`, `vi_va_do_ga`, `san_co_tai_diem_ban`, `cam_nhan_gia_cao` (càng cao càng thấy đắt), `thiet_ke_bao_bi`, `khuyen_mai_diem_ban`; biến phụ thuộc `y_dinh_mua` (1 đến 7); thêm `tuoi`, `gioi_tinh`.

**b4_conjoint_profiles.csv:** `to_hop`, `nguon_goc` (Ethiopia, Colombia, Việt Nam), `bao_bi` (Hộp cao cấp, Túi giấy, Hộp nhựa), `gia` (45.000, 60.000, 75.000 đ/ly).

**b4_conjoint_khaosat.csv:** `dap_vien`, `to_hop`, `nguon_goc`, `bao_bi`, `gia`, `diem` (1 đến 9). Đúng cấu trúc bảng minh hoạ ở slide 21.

**b4_vanwestendorp.csv:** bốn câu giá cho một ly cà phê, đơn vị đồng: `qua_re` (rẻ đến mức nghi ngờ chất lượng), `re` (rẻ nhưng vẫn mua), `dat` (đắt nhưng vẫn mua), `qua_dat` (đắt đến mức không mua); thêm `thu_nhap_trieu_thang`, `tan_suat_uong_tuan`.

## 2. Yêu cầu

1. **MDS:** tính ma trận độ khác biệt trung bình (9 trừ mức giống nhau), dựng bản đồ 2 chiều, báo cáo Stress, tự đặt tên hai trục, chỉ ra các cặp cạnh tranh trực tiếp và khoảng trống. Dựng thêm bản đồ theo thuộc tính và cho biết hai bản đồ có cùng cấu trúc không.
2. **Hồi quy:** chuẩn hoá biến, hồi quy ý định mua lên sáu thuộc tính, xếp hạng hệ số beta, chỉ ra biến không có ý nghĩa thống kê. Hình ảnh thương hiệu mạnh hơn vị bao nhiêu lần?
3. **Conjoint:** mã hoá biến giả (mức tham chiếu: Việt Nam, Hộp nhựa, 75.000 đ), ước lượng part-worth bằng hồi quy bội, quy về mức thấp nhất bằng 0 và trừ trung bình trong từng thuộc tính; tính tầm quan trọng tương đối từ khoảng dao động; quy đổi utility ra tiền và tính WTP cho hạt Ethiopia, hộp cao cấp; mô phỏng thị phần logit cho một cấu hình của mình so với ba đối thủ, rồi tính lợi nhuận chứ không dừng ở thị phần.
4. **Van Westendorp:** vẽ bốn đường tích luỹ, tìm PMC, PME, OPP, IPP và vùng giá chấp nhận được. Đối chiếu với kết quả Conjoint.

## 3. Kết quả tham khảo (solution.py)

**MDS:** cặp gần nhất là Coca-Cola và Pepsi (độ khác biệt 0,33), tiếp theo Fanta và Mirinda (0,65), Sprite và 7Up (1,37). Kruskal Stress-1 = 0,065 (mức khá theo Kruskal 1964: dưới 0,05 tốt, 0,05 đến 0,10 khá, trên 0,20 kém). Hướng và dấu của trục là tuỳ ý, nên toạ độ có thể xoay so với hình trong slide; khoảng cách tương đối thì giữ nguyên. Procrustes giữa bản đồ MDS và bản đồ thuộc tính: sai lệch 0,11, hai bản đồ cùng cấu trúc ba cặp.

**Hồi quy (n = 400, R² = 0,453), beta chuẩn hoá:** hình ảnh thương hiệu 0,43; vị và độ ga 0,28; sẵn có tại điểm bán 0,22; cảm nhận giá cao −0,19; thiết kế bao bì 0,15; khuyến mãi 0,05 (p = 0,18, không có ý nghĩa). Hình ảnh thương hiệu mạnh hơn vị khoảng 1,6 lần.

**Conjoint (R² = 0,746):**

| Thuộc tính | Part-worth (mức thấp nhất = 0) | Khoảng dao động | Tầm quan trọng |
|---|---|---|---|
| Nguồn gốc | Ethiopia 1,38 · Colombia 0,65 · Việt Nam 0 | 1,38 | 26,9% |
| Bao bì | Hộp cao cấp 1,53 · Túi giấy 0,75 · Hộp nhựa 0 | 1,53 | 29,9% |
| Giá | 45.000 đ 2,21 · 60.000 đ 1,15 · 75.000 đ 0 | 2,21 | 43,2% |

1 đơn vị utility = 30.000 / 2,21 ≈ 13.575 đ. WTP thêm cho Ethiopia so với Việt Nam ≈ 18.700 đ; hộp cao cấp so với hộp nhựa ≈ 20.800 đ. Nâng cả hai cho khoảng 39.400 đ, vượt khoảng giá đã khảo sát nên không được ngoại suy.

Mô phỏng logit (cấu hình đối thủ và giá vốn 30.000 đ/ly, quy mô 50.000 ly/tháng là giả định): ta bán Colombia, túi giấy, 60.000 đ được 27,2% thị phần, lợi nhuận gộp khoảng 409 triệu đ/tháng. Hạ xuống 45.000 đ thì thị phần lên 52,1% nhưng lợi nhuận gộp giảm còn khoảng 390 triệu đ/tháng.

**Van Westendorp (n = 320):** PMC ≈ 45.050 đ; OPP ≈ 49.050 đ; IPP ≈ 49.970 đ; PME ≈ 57.000 đ. Vùng giá chấp nhận được khoảng 45.000 đến 57.000 đ. Mức 60.000 đ trong Conjoint nằm ngoài vùng này, là điểm để thảo luận về khác biệt giữa hai phương pháp.

Quy ước giao điểm theo slide và Wikipedia: PMC = "quá rẻ" cắt "đắt"; PME = "rẻ" cắt "quá đắt"; OPP = "quá rẻ" cắt "quá đắt"; IPP = "rẻ" cắt "đắt". Một số phần mềm (ví dụ SurveyMonkey) dùng đường "không rẻ" (1 trừ "rẻ") và "không đắt"; theo cách đó PMC ≈ 37.000 đ, PME ≈ 70.000 đ. Khi nộp bài cần ghi rõ dùng quy ước nào.

## 4. Giả định khi dựng dữ liệu

- Vị trí sáu thương hiệu, part-worth (1,39 / 0,66; 1,53 / 0,72; 2,30 / 1,18), R² khoảng 0,73, các beta hồi quy và bốn mốc Van Westendorp (44.286 / 48.571 / 50.476 / 56.905 đ) lấy theo hình trong slide làm mục tiêu sinh dữ liệu. Số liệu tái tạo gần đúng, không trùng tuyệt đối do nhiễu ngẫu nhiên.
- Slide không nói Van Westendorp hỏi về sản phẩm nào; dựa vào khoảng giá 44.000 đến 57.000 đ, chọn là giá một ly cà phê của chuỗi trong ví dụ Conjoint.
- Số đáp viên MDS (150) và hồi quy (400) không có trong slide, do người soạn chọn. Cấu hình đối thủ, giá vốn và quy mô thị trường trong mô phỏng logit là giả định minh hoạ.
