# Bài 5. Dữ liệu thực hành: CLV theo cohort, case NAVIO

Dữ liệu mô phỏng, hư cấu, chỉ dùng cho học tập. NAVIO giao hộp thực phẩm tươi theo tuần, thu phí hằng tháng; biên lợi nhuận gộp 40%, CAC bình quân khoảng 900.000 đ. Dữ liệu được sinh đúng theo "dữ liệu cohort thực tế" trong slide:

- Tỷ lệ rời bỏ: 25% ở tháng 1, 12% ở tháng 2 và 3, 7% ở tháng 4 đến 6, 4% từ tháng 7.
- ARPU: 450.000 đ ở tháng 1 đến 3, 560.000 đ ở tháng 4 đến 6, 680.000 đ từ tháng 7.

```
python gen_data.py      # sinh 4 file CSV (seed cố định)
python solution.py      # lời giải tham khảo
```

Thư viện: pandas, numpy.

## 1. Các file dữ liệu

**NAVIO_khach_hang.csv (9.264 dòng):** mỗi dòng một khách hàng mới.

| Cột | Ý nghĩa |
|---|---|
| ma_kh | Mã khách hàng |
| thang_gia_nhap | Tháng đăng ký gói (07/2022 đến 06/2025), tức cohort |
| kenh_thu_hut | Giới thiệu bạn bè, Google Search, Facebook/TikTok Ads, KOL/Influencer |
| thanh_pho | Hà Nội, TP.HCM |
| quy_mo_ho | 1-2 người, 3-4 người, 5+ người |

**NAVIO_giao_dich.csv (69.579 dòng):** mỗi dòng một lần thanh toán tháng.

| Cột | Ý nghĩa |
|---|---|
| ma_kh | Mã khách hàng |
| thang | Tháng thanh toán (YYYY-MM) |
| doanh_thu | Số tiền thanh toán trong tháng, đồng |

Khách đã rời bỏ thì không còn dòng nào sau tháng cuối. Khách còn thanh toán ở 06/2025 là đang hoạt động (dữ liệu bị cắt tại ngày phân tích 30/06/2025, chưa biết họ có rời đi hay không).

**NAVIO_chi_phi_kenh.csv (4 dòng):** `kenh_thu_hut`, `chi_phi_thu_hut` (tổng 36 tháng, đồng), `so_kh_moi`. CAC = chi phí / số khách mới.

**bai_tap_app_tieng_anh.csv (5 dòng):** số liệu bài tập slide 10 (ứng dụng học tiếng Anh, biên 62%, CAC 260.000 đ): `phan_khuc`, `so_kh`, `doanh_thu_kh_6_thang`, `ty_le_roi_bo_thang`.

## 2. Yêu cầu

1. Dựng ma trận retention: cohort theo hàng, tháng tuổi đời (1, 2, 3, ...) theo cột. Tính tỷ lệ rời bỏ và ARPU theo tháng tuổi đời. Chú ý loại khách chưa quan sát được tháng kế tiếp khi tính tỷ lệ rời bỏ.
2. Tái hiện cách tính của hai phòng bằng công thức rút gọn CLV = ARPU × biên / churn: phòng tài chính dùng số tháng đầu, phòng marketing dùng số của khách đã ở lại trên 6 tháng. Tính LTV:CAC cho mỗi cách.
3. Tính CLV theo cohort: cộng dồn lợi nhuận gộp thực nhận trong 24 tháng trên mỗi khách mới, dùng các cohort đã đủ 24 tháng (07/2022 đến 06/2023). Tính thêm bản chiết khấu 10%/năm, tuổi thọ kỳ vọng, tháng hoàn vốn CAC và tỷ trọng giá trị nằm từ tháng 7 trở đi.
4. Tính CLV 24 tháng và LTV:CAC theo kênh thu hút, xếp loại theo ngưỡng trong slide (dưới 1, 1 đến 3, khoảng 3, trên 5) và đề xuất phân bổ ngân sách.
5. So sánh retention tháng 2, tháng 3 giữa cohort 2024 và cohort 2025. Điều gì đã thay đổi?
6. Bài tập slide 10: ARPU tháng, CLV, LTV:CAC, phân khúc lỗ trên mỗi khách mới, tổng customer equity.

## 3. Kết quả tham khảo (solution.py)

CAC bình quân (tổng chi phí / tổng khách mới) = 884.175 đ.

| Cách tính | ARPU | Churn | CLV | LTV:CAC |
|---|---|---|---|---|
| Phòng tài chính (tháng 1) | 449.442 đ | 26,2% | 685.870 đ | 0,78 |
| Phòng marketing (khách > 6 tháng) | 674.624 đ | 4,0% | 6.800.624 đ | 7,69 |
| Cohort 24 tháng (2.546 khách) | | | **2.438.762 đ** | **2,76** |
| Cohort 24 tháng, chiết khấu 10%/năm | | | 2.241.662 đ | 2,54 |

Tuổi thọ kỳ vọng trong 24 tháng: 10,1 tháng. Hoàn vốn CAC ở tháng thứ 7. Khoảng 68% giá trị 24 tháng nằm từ tháng 7 trở đi. Các con số này khớp với gợi ý trả lời trong slide (2,45 triệu đ; 2,72; 10,1 tháng; tháng 7; 67%).

**Theo kênh (CLV 24 tháng / CAC):**

| Kênh | Còn lại tháng 2 | CLV 24 tháng | CAC | LTV:CAC |
|---|---|---|---|---|
| Giới thiệu bạn bè | 82,3% | 3,39 triệu | 400 nghìn | 8,49 |
| Google Search | 76,0% | 2,59 triệu | 892 nghìn | 2,90 |
| Facebook/TikTok Ads | 71,5% | 2,12 triệu | 994 nghìn | 2,14 |
| KOL/Influencer | 68,0% | 1,94 triệu | 1,20 triệu | 1,61 |

Gợi ý: tăng ngân sách chương trình giới thiệu, giảm CAC hoặc cải thiện giữ chân ở KOL và quảng cáo mạng xã hội trước khi mở rộng.

**Cohort 2025:** retention tháng 2 / tháng 3 tăng từ 72,7% / 63,8% (cohort 2024) lên 82,4% / 76,1%. Dữ liệu được cài một thay đổi onboarding từ 01/2025 làm giảm rời bỏ ba tháng đầu.

**Bài tập slide 10:**

| Phân khúc | ARPU tháng | CLV | LTV:CAC |
|---|---|---|---|
| Champions | 460.000 | 14.260.000 | 54,85 |
| Loyal | 270.000 | 4.782.857 | 18,40 |
| Potential | 130.000 | 1.343.333 | 5,17 |
| At Risk | 190.000 | 1.070.909 | 4,12 |
| Hibernating | 50.000 | 182.353 | 0,70 |

Hibernating là phân khúc lỗ (LTV:CAC < 1). Tổng customer equity ≈ 5,445 tỷ đồng.

## 4. Giả định khi dựng dữ liệu

- Slide chỉ cho tỷ lệ rời bỏ và ARPU bình quân. Phần phân khúc theo kênh thu hút (tỷ trọng, CAC từng kênh, hệ số rời bỏ 0,7 đến 1,3) là do người soạn đặt sao cho CAC bình quân khoảng 900.000 đ.
- Quy mô cohort (khoảng 190 đến 330 khách/tháng), thời gian 07/2022 đến 06/2025 và thay đổi onboarding từ 01/2025 là giả định, để có đủ cohort 24 tháng và có một xu hướng cho phần phân tích cohort.
- Doanh thu từng khách dao động quanh ARPU theo quy mô hộ và nhiễu tháng; trung bình vẫn bám mức ARPU của slide.
