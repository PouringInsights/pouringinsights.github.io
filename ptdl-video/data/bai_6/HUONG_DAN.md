# Bài 6. Dữ liệu thực hành: EFA và phân khúc theo tâm lý học, case MỘC AN

Dữ liệu mô phỏng, hư cấu, chỉ dùng cho học tập. MỘC AN là thương hiệu thời trang nội địa. Lần này bảng hỏi được thiết kế lại: ngoài chất lượng, giá và trải nghiệm cửa hàng, có thêm câu hỏi đo thương hiệu (thứ mà bảng hỏi cũ chưa từng đo) và phong cách thiết kế.

```
python gen_data.py      # sinh dữ liệu (seed cố định)
python solution.py      # lời giải tham khảo
```

Thư viện: pandas, numpy, factor_analyzer, scikit-learn, statsmodels. `solution.py` có đoạn bọc tương thích để factor_analyzer 0.5.1 chạy được với scikit-learn 1.8 trở lên.

## 1. Các file dữ liệu

**MOCAN_khaosat.csv (420 dòng, 34 cột):** mỗi dòng một khách hàng.

- `ma_dv`: mã đáp viên.
- 23 biến quan sát thang Likert 1 đến 5 (1 = hoàn toàn không đồng ý, 5 = hoàn toàn đồng ý): CL1 đến CL5, GT1 đến GT5, TN1 đến TN5, TH1 đến TH4, PC1 đến PC4. Nội dung từng câu xem trong MOCAN_bien_quan_sat.csv. Tiền tố chỉ là mã câu hỏi theo bảng hỏi, không phải kết quả EFA.
- YD1 đến YD3: ý định mua lại (Likert 1 đến 5). Không đưa vào EFA; dùng để nối sang Bài 7.
- Nhân khẩu học và hành vi: `gioi_tinh`, `nhom_tuoi`, `thu_nhap`, `kenh_mua_chinh` (Cửa hàng, Website/App MỘC AN, Sàn TMĐT), `thanh_pho`, `so_lan_mua_12t`, `chi_tieu_12t_nghin`.

**MOCAN_bien_quan_sat.csv (26 dòng):** `ma_bien`, `noi_dung` (câu hỏi), `vai_tro` (EFA hoặc biến kết quả).

**_dap_an_phan_khuc_an.csv (420 dòng):** nhãn phân khúc thật đã cài khi sinh dữ liệu. Chỉ dành cho giảng viên đối chiếu, không phát cho sinh viên.

## 2. Yêu cầu

Làm đủ sáu bước EFA như slide 6.2 rồi nối sang phân cụm:

1. Kiểm tra điều kiện: KMO (≥ 0,6, lý tưởng > 0,8) và kiểm định Bartlett (p < 0,05).
2. Trích nhân tố bằng PCA.
3. Chọn số nhân tố bằng eigenvalue > 1 và Scree Plot.
4. Xoay Varimax.
5. Lọc biến: communality ≥ 0,5; hệ số tải ≥ 0,5; không tải trên 0,4 lên nhân tố thứ hai. Loại biến vi phạm, chạy lại EFA, so sánh phương sai tích luỹ trước và sau.
6. Đặt tên nhân tố theo nội dung các biến (không theo tên đặt sẵn trong kế hoạch) và kiểm tra Cronbach's Alpha (> 0,7).
7. Tính điểm nhân tố, chạy K-means (K từ 2 đến 8, chọn bằng Elbow và Silhouette), đặt tên phân khúc theo động cơ, rồi đối chiếu với tuổi, thu nhập, kênh mua và chi tiêu để biết tìm mỗi phân khúc ở đâu.
8. (Nối sang Bài 7) Hồi quy ý định mua lại lên điểm nhân tố: phương sai giải thích của một nhân tố có phải là tầm quan trọng của nó không?

## 3. Kết quả tham khảo (solution.py)

**Điều kiện:** KMO = 0,875; Bartlett Chi² = 3.674, p < 0,001.

**Số nhân tố:** eigenvalue 4,97; 3,84; 3,03; 1,18; 1,04; 0,80; ... nên giữ **5 nhân tố**.

**Lần chạy đầu (23 biến):** phương sai tích luỹ 61,1%. Hai biến bị loại:

- GT5 "Giá hợp lý so với chất lượng nhận được": tải chéo 0,50 lên Độ bền và 0,46 lên Giá trị kinh tế. Giống X4 trong case: khách xếp câu này vào "đáng đồng tiền", không vào "rẻ".
- TN5 "Thanh toán nhanh, ít phải xếp hàng": communality 0,45 < 0,5.

**Lần chạy lại (21 biến):** KMO = 0,869; phương sai tích luỹ tăng lên **63,6%**; mọi biến tải ≥ 0,69 lên đúng một nhân tố, communality ≥ 0,53.

| Nhân tố | Biến | Cronbach's Alpha |
|---|---|---|
| Độ bền sản phẩm | CL1 đến CL5 | 0,824 |
| Giá trị kinh tế | GT1 đến GT4 | 0,807 |
| Trải nghiệm cửa hàng | TN1 đến TN4 | 0,789 |
| Hình ảnh thương hiệu | TH1 đến TH4 | 0,826 |
| Phong cách thiết kế | PC1 đến PC4 | 0,838 |

Thứ tự NT1 đến NT5 trong bảng hệ số tải có thể khác bảng trên; đặt tên theo biến tải mạnh, không theo số thứ tự.

**K-means trên 5 điểm nhân tố:** Silhouette 0,168 / 0,211 / **0,254** / 0,239 / 0,238 với K = 2 đến 6, cao nhất ở K = 4. Silhouette khoảng 0,25 là mức thường gặp với dữ liệu thái độ (cấu trúc có nhưng các nhóm chồng lấn một phần).

| Phân khúc | Số người | Nhân tố nổi trội (điểm tb) | Đặc điểm nhân khẩu học, hành vi |
|---|---|---|---|
| Săn ưu đãi | 124 | Giá trị kinh tế +1,03 | 77% dưới 35 tuổi; 43% thu nhập dưới 10 triệu; 48% mua trên sàn TMĐT; mua nhiều lần nhất (5,4 lần/năm) |
| Thực dụng, chuộng độ bền | 103 | Độ bền +1,16 | Thiên về 35 đến 44 tuổi; chi tiêu khoảng 2,3 triệu/năm |
| Ưa thương hiệu và phong cách | 99 | Thương hiệu +1,04, Phong cách +0,88 | 53% từ 25 đến 34 tuổi; chỉ 4% thu nhập dưới 10 triệu; 42% mua qua website/app; chi tiêu cao nhất (3,1 triệu/năm) |
| Cần trải nghiệm tại cửa hàng | 94 | Trải nghiệm +1,28 | 58% từ 35 tuổi trở lên; 68% mua tại cửa hàng |

Đối chiếu với nhãn ẩn (chỉ giảng viên): Adjusted Rand Index = 0,865.

**Hồi quy ý định mua lại lên điểm nhân tố (R² = 0,41):** beta chuẩn hoá Hình ảnh thương hiệu 0,37; Độ bền 0,34; Trải nghiệm 0,30; Phong cách 0,22; Giá trị kinh tế 0,15. Nhân tố Giá trị kinh tế giải thích khoảng 12% phương sai các câu hỏi nhưng lại là đòn bẩy yếu nhất của ý định mua lại: phương sai giải thích không phải tầm quan trọng.

Ngưỡng dùng trong lời giải: KMO theo Kaiser (1974); hệ số tải, communality, tải chéo theo Hair và cộng sự (2019); Alpha > 0,7 theo Nunnally (1978); eigenvalue > 1 theo Kaiser.

## 4. Giả định khi dựng dữ liệu

- Slide chỉ có bảng 9 biến của MỘC AN (3 nhân tố) và nói tới "16 biến" ở phần phân cụm. Bộ 23 biến và 5 nhân tố (Độ bền, Giá trị kinh tế, Trải nghiệm cửa hàng, Hình ảnh thương hiệu, Phong cách thiết kế) do người soạn mở rộng: giữ nguyên ba nhân tố thật trong lời giải case, thêm Thương hiệu (vì case chỉ ra bảng hỏi chưa đo thương hiệu) và Phong cách (ví dụ "khẳng định phong cách" trong lời giảng slide 13).
- Bốn phân khúc ẩn và mức liên hệ với nhân khẩu học là giả định; slide chỉ nêu "bốn phân khúc theo động cơ" và hai nhóm "nhạy cảm giá", "ưa thương hiệu".
- Cỡ mẫu 420 lấy theo case.
