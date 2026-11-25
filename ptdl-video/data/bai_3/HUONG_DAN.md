# Bài 3. Bài tập về nhà: chuỗi mỹ phẩm LUMI

Dữ liệu mô phỏng, hư cấu, chỉ dùng cho học tập. LUMI có 24 cửa hàng tại Hà Nội và 3.000 khách hàng thành viên. Ban giám đốc cần biết: khách hàng chia thành mấy nhóm, 16 nhóm sản phẩm gom thành mấy họ, đơn online tập trung ở khu vực nào.

Chạy lại dữ liệu và lời giải:

```
python gen_data.py      # sinh 3 file CSV (seed cố định, chạy lại cho kết quả y hệt)
python solution.py      # lời giải tham khảo
```

Thư viện: pandas, numpy, scikit-learn, scipy.

## 1. Các file dữ liệu

### LUMI_khach_hang.csv (3.000 dòng)

Một dòng là một khách hàng thành viên. Ngày phân tích 30/06/2025, kỳ phân tích 12 tháng (01/07/2024 đến 30/06/2025).

| Cột | Ý nghĩa |
|---|---|
| ma_kh | Mã khách hàng |
| cua_hang | Cửa hàng đăng ký (CH01 đến CH24) |
| gioi_tinh, tuoi | Giới tính, tuổi |
| ngay_dang_ky | Ngày đăng ký thành viên |
| ngay_mua_gan_nhat | Ngày của hoá đơn gần nhất (dùng tính R) |
| so_don_12t | Số hoá đơn trong 12 tháng (F) |
| tong_chi_tieu_12t | Tổng giá trị hoá đơn trong 12 tháng, đồng (M) |
| so_lan_doi_tra | Số lần đổi trả trong 12 tháng |
| so_phien_app_thang | Số phiên dùng app trung bình mỗi tháng |
| ty_le_mua_online | Tỷ lệ đơn mua online (0 đến 1) |
| so_nhom_sp_da_mua | Số nhóm sản phẩm khác nhau đã mua (trên 16) |

Tệp có lỗi cài sẵn để làm sạch: dòng trùng lặp, dòng thiếu ngày mua hoặc chi tiêu, ngày mua sau ngày phân tích, chi tiêu âm, tài khoản mua sỉ có F và M cực lớn, và giá trị thiếu ở `tuoi`, `so_phien_app_thang`.

### LUMI_nhom_san_pham.csv (16 dòng)

| Cột | Ý nghĩa |
|---|---|
| ma_nhom, ten_nhom | Mã và tên nhóm sản phẩm |
| gia_ban_tb_nghin | Giá bán trung bình, nghìn đồng |
| bien_loi_nhuan_gop | Biên lợi nhuận gộp (0 đến 1) |
| chu_ky_mua_lai_ngay | Số ngày trung bình giữa hai lần mua lại |
| ty_le_don_co_khuyen_mai | Tỷ lệ đơn có áp khuyến mãi |
| ty_le_mua_online | Tỷ lệ doanh số online |
| tuoi_tb_khach | Tuổi trung bình người mua |
| tang_truong_doanh_thu_yoy | Tăng trưởng doanh thu so với cùng kỳ |
| so_sku | Số mã hàng đang bán |
| doanh_thu_12t_ty | Doanh thu 12 tháng, tỷ đồng (để mô tả, không bắt buộc đưa vào phân cụm) |

### LUMI_diem_giao_hang.csv (1.140 dòng)

| Cột | Ý nghĩa |
|---|---|
| ma_don | Mã đơn online |
| lat, lon | Vĩ độ, kinh độ điểm giao (nội thành Hà Nội) |
| quan | Quận của điểm giao |
| gia_tri_don | Giá trị đơn, đồng |
| thoi_gian_dat | Thời điểm đặt (04/2025 đến 06/2025) |

## 2. Yêu cầu

1. Làm sạch LUMI_khach_hang.csv: xử lý trùng lặp, giá trị thiếu, dòng sai logic và ngoại lệ. Ghi rõ mỗi bước bỏ bao nhiêu dòng và vì sao.
2. Tính R, F, M; chấm điểm ngũ phân vị và gán nhãn phân khúc RFM. Sau đó chuẩn hoá (log cho F, M rồi z-score) và chạy K-means với K từ 2 đến 8, chọn K bằng Elbow kết hợp Silhouette (n_init ≥ 10, cố định random_state). Đặt tên và mô tả chân dung từng cụm.
3. Chuẩn hoá 8 thuộc tính của 16 nhóm sản phẩm, chạy Hierarchical Clustering liên kết Ward, vẽ dendrogram, chọn ngưỡng cắt và đặt tên các họ sản phẩm.
4. Chạy DBSCAN trên toạ độ điểm giao (khoảng cách haversine, giữ nguyên toạ độ). Chọn ε bằng biểu đồ k-distance, MinPts gợi ý 12. Nêu số vùng mật độ cao, số điểm nhiễu, so sánh với K-means K = 6 trên cùng dữ liệu.
5. So sánh ba phương pháp (cụm được định nghĩa thế nào, xử lý ngoại lệ ra sao, kết quả dùng được vào việc gì) và viết khuyến nghị có ước tính tác động bằng con số.

Bài tập nhỏ đi kèm (slide 12): chấm RFM cho 5 khách KH01 đến KH05 theo ngưỡng ngũ phân vị của chính tệp LUMI.

## 3. Kết quả tham khảo (solution.py)

**Làm sạch:** 3.000 dòng, bỏ 30 dòng trùng, 26 dòng thiếu R hoặc M, 20 dòng sai logic, 25 tài khoản mua sỉ (IQR trên log F và log M; ngưỡng trên khoảng 77 đơn và 48 triệu đồng). Điền trung vị cho 87 giá trị thiếu ở `tuoi` và 58 ở `so_phien_app_thang`. Còn **2.899 khách**.

**K-means trên R, log F, log M:**

| K | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Silhouette | 0,602 | 0,670 | **0,686** | 0,655 | 0,503 |

Inertia gãy rõ ở K = 4 (2.980, 1.070, 606, 482). Chọn K = 4:

| Cụm | Số KH | R tb (ngày) | F tb | M tb (triệu đ) | Phiên app/tháng | Tỷ trọng doanh thu |
|---|---|---|---|---|---|---|
| VIP | 319 | 9 | 23,9 | 13,1 | 14,0 | 39,6% |
| Thường xuyên | 885 | 32 | 11,1 | 5,0 | 7,8 | 41,6% |
| Thỉnh thoảng | 1.172 | 95 | 4,0 | 1,4 | 2,9 | 16,0% |
| Ngủ đông | 523 | 264 | 1,9 | 0,6 | 0,9 | 2,8% |

11% số khách (VIP) tạo khoảng 40% doanh thu.

**RFM ngũ phân vị:** vì R, F, M tương quan mạnh nên nhóm Champions (R, F, M đều ≥ 4) khá lớn: 1.066 khách, 75,6% doanh thu; Hibernating/Lost 872 khách; At Risk 197 khách, doanh thu 12 tháng 0,36 tỷ đồng. Đây là điểm để thảo luận: ngưỡng do người đặt, còn K-means tách VIP khỏi Thường xuyên rõ hơn.

**Bài tập slide 12** (theo ngưỡng của tệp LUMI): KH01 = 5-5-5 Champions; KH02 = 4-3-5; KH03 = 1-3-4 At Risk; KH04 = 5-1-1 Khách mới; KH05 = 1-2-3.

**Ward, 16 nhóm sản phẩm:** hệ số cophenetic 0,943. Chiều cao hợp nhất nhảy từ 2,5 lên 6,3 nên cắt ở 4 họ (Silhouette 0,592, cao nhất trong 2 đến 6 họ):

- Chăm sóc da cơ bản, mua lặp lại: Sữa rửa mặt, Toner, Tẩy trang, Kem chống nắng, Mặt nạ giấy (tăng trưởng 18%/năm).
- Đặc trị, cao cấp: Serum, Kem dưỡng chống lão hoá, Nước hoa (giá trung bình khoảng 845 nghìn, biên 56%, mua lại sau khoảng 4 tháng).
- Trang điểm: Son, Kem nền, Phấn phủ, Mascara, Phấn má (nhiều SKU, online cao).
- Cơ thể và tóc: Sữa tắm, Dưỡng thể, Dầu gội (giá thấp, biên 29%, phụ thuộc khuyến mãi).

**DBSCAN (ε = 500 m, MinPts = 12):** 6 vùng mật độ cao (Cầu Giấy 212 đơn, Thanh Xuân 196, Hai Bà Trưng 172, Hoàn Kiếm 159, Tây Hồ 141, Long Biên 119) và **141 điểm nhiễu (12,4%)**. Biểu đồ k-distance gãy quanh phân vị 88% (khoảng 250 m lên 870 m), khớp với tỷ lệ nhiễu.

So với K-means K = 6: Silhouette K-means 0,638 cao hơn DBSCAN khi coi nhiễu là một nhóm (0,568). Nhưng khoảng cách xa nhất giữa hai đơn trong cùng một vùng của K-means là 5 đến 9 km, còn của DBSCAN chỉ 1,6 đến 4,1 km. Chỉ số kỹ thuật cao hơn chưa chắc là kết quả dùng được hơn.

**Gợi ý khuyến nghị:** giữ VIP bằng chương trình đặc quyền (40% doanh thu); kéo lại 20% nhóm At Risk giữ được khoảng 0,07 tỷ đồng/năm; đặt điểm gom hàng hoặc tuyến xe riêng cho 6 vùng; 141 đơn lẻ giao qua đối tác vận chuyển ngoài.

## 4. Giả định khi dựng dữ liệu

- Slide không nêu cấu trúc cột. Các cột hành vi (app, online, đổi trả, số nhóm sản phẩm) và 8 thuộc tính sản phẩm là do người soạn đặt.
- Quy mô 4 cụm, tỷ trọng doanh thu, 6 vùng giao hàng, 141 điểm nhiễu, ε khoảng 500 m và MinPts = 12 lấy theo hình minh hoạ trong slide. Các vùng được dựng dọc trục đường (chữ L Xuân Thủy và Trần Duy Hưng, vòng cung quanh Hồ Gươm, Minh Khai, Xuân Diệu, Nguyễn Trãi, Nguyễn Văn Cừ) để có hình dạng không cầu.
- Tệp khách hàng chỉ có dữ liệu tổng hợp R, F, M cho từng khách, không có bảng hoá đơn chi tiết, để giữ đúng 3 file như slide.
