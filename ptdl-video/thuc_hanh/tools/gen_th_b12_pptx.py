"""Slides Bài 12 = Thực hành 2 (LUMI). Dàn ý: mỗi slide một việc (page job) ghi ở comment."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th_b12_lib import K

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{W}/th_out/bai_12"
k = K()

# 1 job: nhận diện buổi học
k.cover("Thực hành 2: Phân khúc khách hàng và nhóm hoá danh mục sản phẩm", "Phân tích dữ liệu Marketing – Bài 12")
# 2 job: buổi học phục vụ CĐR nào
k.table("Chuẩn đầu ra của buổi thực hành", [
    ["Mã CĐR", "Nội dung chuẩn đầu ra của học phần", "Mức độ"],
    ["L1", "Ứng dụng thuật toán và thống kê vào phân tích dữ liệu, kết hợp kiến thức kinh doanh để đưa ra khuyến nghị về sản phẩm, khách hàng, thị trường", "U2"],
], widths=[1,6,1])
# 3 job: sau buổi học làm được gì
k.bullets("Mục tiêu: sau buổi này, sinh viên tự làm được", [
    "Làm sạch dữ liệu, xử lý ngoại lệ, chuẩn hoá biến trước khi phân cụm",
    "Phân khúc 3.000 khách hàng bằng K-means, chọn K có căn cứ",
    "Gom 16 nhóm sản phẩm thành họ bằng Hierarchical Clustering",
    "Đọc Elbow, Silhouette, dendrogram và biểu đồ k-distance",
    "Viết khuyến nghị có phép tính tài chính và chỉ số theo dõi",
])
# 4 job: lộ trình buổi học
k.bullets("AGENDA", [
    "12.1.  Ôn tập lý thuyết: IQR, chuẩn hoá, K-means, Hierarchical, DBSCAN",
    "12.2.  Tình huống LUMI và ba tệp dữ liệu",
    "12.3.  Yêu cầu 1: chuẩn bị dữ liệu khách hàng",
    "12.4.  Yêu cầu 2: phân khúc khách hàng bằng K-means",
    "12.5.  Yêu cầu 3: nhóm hoá danh mục bằng Hierarchical",
    "12.6.  Vùng giao hàng và Yêu cầu 4: so sánh, khuyến nghị",
])
# 5 job: case mở đầu, đặt vấn đề
k.bullets("Case mở đầu: LUMI chăm sóc 3.000 thành viên theo một cách duy nhất", [
    "Mỗi tháng một tin khuyến mại giống nhau, mỗi quý một voucher 15% giống nhau",
    "Tỷ lệ phản hồi chiến dịch giảm từ 24% xuống 19%",
    "Chi phí chăm sóc tăng 28%, doanh thu thành viên chỉ tăng 6%",
    "Chi phí giao chặng cuối tăng 41%, số đơn chỉ tăng 12%",
    "Thảo luận: LUMI đang chi sai chỗ nào?",
])

# ---- 12.1
k.section("12.1.  Ôn tập kiến thức lý thuyết trọng tâm")
# 7 job: quy trình 7 bước
k.bullets("Phân cụm là một quy trình bảy bước, không phải một lệnh chạy", [
    "1-2. Xác định câu hỏi kinh doanh, chọn biến đầu vào",
    "3-4. Kiểm tra chất lượng dữ liệu, xử lý điểm ngoại lệ",
    "5. Chuẩn hoá biến để mọi biến đóng góp ngang nhau",
    "6. Chọn thuật toán và tham số, kiểm tra bằng chỉ số và đồ thị",
    "7. Lập chân dung, đặt tên, kiểm tra ổn định, viết khuyến nghị",
])
# 8 job: công thức IQR
k.bullets("Ngoại lệ cực trị: vượt Q3 + 3·IQR (Tukey, 1977)", [
    "IQR = Q3 − Q1, khoảng chứa 50% quan sát ở giữa",
    "Ngoại lệ nhẹ: vượt Q3 + 1,5·IQR",
    "Ngoại lệ cực trị: vượt Q3 + 3·IQR, ngưỡng đề bài yêu cầu",
    "Dựa trên thứ hạng, ít bị giá trị cực đoan kéo lệch",
    "Ví dụ minh hoạ: Q1 = 1,2 tr, Q3 = 3,8 tr, ngưỡng 11,6 tr",
])
# 9 job: vì sao chuẩn hoá
k.table("Không chuẩn hoá, Monetary quyết định mọi khoảng cách", [
    ["Cặp khách (ví dụ minh hoạ)", "Khoảng cách thô", "Khoảng cách z-score"],
    ["A (10 ngày, 12 lần, 8,0 tr) và B (200 ngày, 2 lần, 8,2 tr)", "≈ 200.000", "≈ 3,11"],
    ["A và C (12 ngày, 11 lần, 6,0 tr)", "≈ 2.000.000", "≈ 0,28"],
], widths=[5,2,2], note="z = (x − trung bình) / độ lệch chuẩn. Sau chuẩn hoá, A gần C, đúng với hành vi mua.")
# 10 job: chọn K
k.bullets("Chọn K bằng Elbow và Silhouette, đọc kèm quy mô cụm", [
    "Inertia luôn giảm khi K tăng: tìm điểm gãy, không tìm giá trị nhỏ nhất",
    "Silhouette s(i) = [b(i) − a(i)] / max{a(i), b(i)}, từ −1 đến 1",
    "Trên 0,70 mạnh; 0,51 đến 0,70 hợp lý; 0,26 đến 0,50 yếu (Kaufman và Rousseeuw, 1990)",
    "Silhouette cao vẫn có thể đi kèm cụm chỉ vài chục khách",
    "Luôn đặt n_init=10 và random_state cố định",
])
# 11 job: linkage
k.table("Phương pháp liên kết quyết định hình dạng dendrogram", [
    ["Liên kết", "Khoảng cách giữa hai cụm", "Kết quả điển hình"],
    ["Single", "Cặp điểm gần nhất", "Hiện tượng chuỗi, cụm một phần tử"],
    ["Complete", "Cặp điểm xa nhất", "Cụm gọn, nhạy với ngoại lệ"],
    ["Average", "Trung bình mọi cặp điểm", "Trung gian"],
    ["Ward", "Mức tăng tổng bình phương nội cụm", "Cụm cân đối, cần khoảng cách Euclidean"],
], widths=[1,2,2], note="R: dùng hclust(..., method = \"ward.D2\"). Cắt cây ở khoảng trống dọc dài nhất.")
# 12 job: so sánh 3 phương pháp
k.table("Mỗi tệp dữ liệu LUMI cần một phương pháp riêng", [
    ["Tiêu chí", "K-means", "Hierarchical", "DBSCAN"],
    ["Định nghĩa cụm", "Gần một tâm", "Nhánh của cây", "Vùng mật độ cao"],
    ["Tham số", "K", "Linkage, ngưỡng cắt", "ε, MinPts"],
    ["Điểm ngoại lệ", "Bị ép vào cụm", "Bị ép vào cụm", "Tách thành nhiễu −1"],
    ["Quy mô", "Rất lớn", "Dưới vài nghìn", "Trung bình, lớn"],
    ["Tệp LUMI", "3.000 khách", "16 nhóm SP", "1.140 điểm giao"],
])

# ---- 12.2
k.section("12.2.  Tình huống LUMI và dữ liệu")
# 14 job: ba tệp
k.table("Ba tệp dữ liệu, kỳ 01/04/2025 đến 31/03/2026", [
    ["Tệp", "Số dòng", "Dùng cho"],
    ["LUMI_khach_hang.csv", "3.000", "Yêu cầu 1, 2: K-means"],
    ["LUMI_nhom_san_pham.csv", "16", "Yêu cầu 3: Hierarchical"],
    ["LUMI_diem_giao_hang.csv", "1.140", "Vùng giao hàng, Yêu cầu 4"],
], widths=[3,1,3], note="Ngày phân tích quy ước: 31/03/2026. Dữ liệu khách hàng chưa làm sạch. Đọc bằng pandas, encoding=\"utf-8-sig\".")
# 15 job: biến khách hàng
k.table("RFM là biến đầu vào, các biến khác để mô tả cụm", [
    ["Vai trò", "Cột", "Đơn vị"],
    ["R: Recency", "SoNgayTuLanMuaGanNhat", "ngày"],
    ["F: Frequency", "SoLanMua_12T", "lần"],
    ["M: Monetary", "TongChiTieu_12T", "đồng"],
    ["Mô tả cụm", "GiaTriDonTrungBinh, SoPhienApp_30Ngay", "đồng, phiên"],
    ["Mô tả cụm", "SoLanDungVoucher, TyLeMuaOnline, PhanHoiChienDich", "lần, tỷ lệ, 0/1"],
], widths=[1.2,3,1.2])

# ---- 12.3
k.section("12.3.  Yêu cầu 1: Chuẩn bị dữ liệu khách hàng (2,0 điểm)")
# 17 job: câu a, b
k.bullets("Câu a, b: kiểm tra chất lượng và tìm ngoại lệ", [
    "df.duplicated().sum(), df[\"MaKH\"].duplicated().sum(), df.isna().sum()",
    "Cột suy ra được từ cột khác: tính lại, không xoá dòng",
    "Cột không suy ra được: điền trung vị hoặc xoá, nêu lý do",
    "Vẽ histogram ba biến R, F, M trên một hình",
    "Báo cáo ba con số: số khách vượt ngưỡng, % số khách, % doanh thu",
])
# 18 job: câu c, d
k.bullets("Câu c, d: tách ngoại lệ trước, chuẩn hoá sau", [
    "Giữ, xoá hay tách riêng: lập luận kỹ thuật và kinh doanh",
    "So % số khách với % doanh thu của nhóm vượt ngưỡng",
    "Fit StandardScaler sau khi đã tách ngoại lệ",
    "Chạy K = 4 trên dữ liệu thô và chuẩn hoá: báo silhouette và quy mô cụm",
    "Ghi rõ câu d chạy trên tệp nào",
])

# ---- 12.4
k.section("12.4.  Yêu cầu 2: Phân khúc khách hàng bằng K-means (2,5 điểm)")
# 20 job: chọn K + ổn định
k.bullets("Câu a, b, e: chọn K từ 2 đến 8 và kiểm tra ổn định", [
    "KMeans(n_clusters=k, n_init=10, random_state=42), lưu inertia_ và silhouette",
    "Vẽ hai đường Elbow và Silhouette theo K",
    "Hai tiêu chí lệch nhau: nêu tiêu chí ưu tiên và lý do",
    "Ổn định: chạy lại với ít nhất 5 random_state, báo khoảng dao động silhouette",
    "So sánh theo quy mô cụm, không theo số thứ tự nhãn",
])
# 21 job: chân dung + tên
k.table("Câu c, d: bảng chân dung trên giá trị gốc, tên theo hành vi", [
    ["Chỉ số", "Phân khúc 1", "Phân khúc 2", "…", "Nhóm tách riêng"],
    ["Số khách, % số khách", "", "", "", ""],
    ["Recency, số lần mua, chi tiêu TB", "", "", "", ""],
    ["Giá trị đơn TB, số phiên app TB", "", "", "", ""],
    ["% mua online, % phản hồi", "", "", "", ""],
    ["Tỷ trọng doanh thu", "", "", "", ""],
], widths=[3,1.3,1.3,0.5,1.5], note="Tên tốt nói khách làm gì và nên được đối xử thế nào. Không đặt tên Cụm 1, Cụm 2.")

# ---- 12.5
k.section("12.5.  Yêu cầu 3: Nhóm hoá danh mục bằng Hierarchical (2,0 điểm)")
# 23 job: dendrogram
k.bullets("Câu a, b, c: 16 quan sát, đọc dendrogram bằng mắt", [
    "Lý do: n nhỏ, chưa biết số họ, cần thấy quan hệ lồng nhau",
    "Chuẩn hoá 6 thuộc tính, nếu không giá bán quyết định cả cây",
    "linkage(Xs, method=m) với single, complete, ward; fcluster(Z, t=4, criterion=\"maxclust\")",
    "Mỗi phương pháp: silhouette khi cắt 4 cụm và quy mô cụm",
    "Vẽ ngưỡng cắt bằng axhline, liệt kê và đặt tên từng họ",
])
# 24 job: chính sách
k.bullets("Câu d: chính sách khuyến mại phải trích dẫn thuộc tính của họ", [
    "Biên gộp cao: chịu được ưu đãi, chưa chắc cần giảm giá",
    "Tỷ lệ mua kèm voucher cao: khách đã quen chờ khuyến mại",
    "Trả hàng nhiều: giảm trả hàng trước khi đẩy doanh số",
    "Mua lại thường xuyên: gói định kỳ hoặc combo",
    "Ví dụ minh hoạ: biên gộp 20%, voucher 15%, còn khoảng 5 điểm %",
])

# ---- 12.6
k.section("12.6.  Vùng giao hàng và Yêu cầu 4: So sánh, khuyến nghị (1,5 điểm)")
# 26 job: DBSCAN
k.bullets("DBSCAN trên toạ độ: haversine và biểu đồ k-distance", [
    "Không chuẩn hoá z-score cho toạ độ; đổi sang radian",
    "MinPts khoảng 4 cho dữ liệu 2 chiều, tăng khi nhiều nhiễu",
    "k-distance: NearestNeighbors(n_neighbors=MinPts, metric=\"haversine\"), chọn ε ở điểm bẻ gập",
    "DBSCAN(eps=km/6371, min_samples=MinPts, metric=\"haversine\")",
    "Đối chứng K-means cùng số vùng: điểm rải rác bị ép vào vùng nào?",
])
# 27 job: khuyến nghị tài chính
k.table("Khuyến nghị có hành động, đối tượng, phép tính, chỉ số", [
    ["Hạng mục (ví dụ minh hoạ)", "Phép tính", "Kết quả"],
    ["Tiết kiệm tin nhắn", "800 × (12 − 4) × 2.500 đ", "16,0 tr/năm"],
    ["Lợi nhuận gộp tăng", "800 × 3% × 400.000 đ × 34%", "3,3 tr"],
    ["Tổng tác động", "16,0 + 3,3", "≈ 19,3 tr/năm"],
], widths=[2,3,1.5], note="Chỉ số theo dõi: tỷ lệ mua lần hai trong 60 ngày, tỷ lệ huỷ nhận tin. Giữ nhóm đối chứng (Bài 9, Bài 10).")
# 28 job: quy trình thực hiện
k.bullets("Quy trình thực hiện trong buổi", [
    "Bước 1: kiểm tra dữ liệu, tách ngoại lệ (Yêu cầu 1)",
    "Bước 2: chuẩn hoá RFM, chọn K, lập chân dung (Yêu cầu 2)",
    "Bước 3: dendrogram 16 nhóm sản phẩm, đặt tên họ (Yêu cầu 3)",
    "Bước 4: DBSCAN điểm giao hàng, đối chứng K-means",
    "Bước 5: bảng so sánh và hai khuyến nghị (Yêu cầu 4)",
    "Bước 6: chạy lại mã từ đầu, nộp báo cáo",
])
# 29 job: lỗi thường gặp
k.table("Lỗi thường gặp và cách tránh", [
    ["Lỗi", "Hệ quả", "Cách tránh"],
    ["Không chuẩn hoá", "Cụm chỉ theo chi tiêu hoặc giá", "StandardScaler trước khi chạy"],
    ["Xoá ngoại lệ không bình luận", "Mất nhóm doanh thu lớn", "Tách riêng, phân tích riêng"],
    ["Chỉ báo silhouette", "Bỏ sót cụm vài chục khách", "Báo kèm quy mô cụm"],
    ["Bỏ n_init, random_state", "Kết quả không lặp lại", "n_init=10, SEED cố định"],
    ["Khuyến nghị chung chung", "Mất điểm câu 4b", "Có phép tính và chỉ số"],
])
# 30 job: nộp và chấm
k.table("Sản phẩm nộp và tiêu chí chấm", [
    ["Yêu cầu", "Điểm", "Tiêu chí chính"],
    ["1. Chuẩn bị dữ liệu", "2,0", "Xử lý có lý do, 3·IQR, minh chứng chuẩn hoá"],
    ["2. K-means", "2,5", "Biện luận K, chân dung đủ chỉ số, tên, ổn định"],
    ["3. Hierarchical", "2,0", "Ba linkage, ngưỡng cắt, họ có tên, chính sách"],
    ["4. So sánh, khuyến nghị", "1,5", "Dẫn chứng từ bài, hai khuyến nghị có phép tính"],
], widths=[2,0.8,5], note="Nộp cuối buổi: báo cáo Word hoặc PDF và tệp mã chạy lại được. Tổng theo đề: 8,0 điểm.")
# 31 job: tóm tắt
k.bullets("Tóm tắt", [
    "Khách hàng: tách ngoại lệ 3·IQR, chuẩn hoá, K-means, chọn K bằng Elbow và Silhouette",
    "Sản phẩm: 16 quan sát, Hierarchical với Ward, cắt cây ở khoảng trống lớn nhất",
    "Điểm giao: DBSCAN, haversine, k-distance, tách nhiễu",
    "Chỉ số kỹ thuật luôn đọc cùng quy mô cụm và tên kinh doanh",
    "Khuyến nghị: đối tượng, phép tính, chỉ số theo dõi",
])
# 32 job: câu hỏi thảo luận
k.bullets("Câu hỏi thảo luận", [
    "Silhouette 0,76 nhưng hai cụm chỉ vài chục khách: mô hình tốt hay không?",
    "Nhóm vượt ngưỡng 3·IQR là ai? Kiểm chứng bằng dữ liệu nào?",
    "Vì sao không dùng K-means cho 16 nhóm sản phẩm?",
    "Voucher 15% đồng loạt ảnh hưởng thế nào tới biên lợi nhuận của từng họ?",
    "Điểm trung chuyển đáng mở khi lợi ích lớn hơn chi phí bao nhiêu?",
])
k.save(f"{OUT}/Bai 12_Thuc hanh 2_Slides.pptx")
print("slides", len(k.prs.slides))
