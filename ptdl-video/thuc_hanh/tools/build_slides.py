import sys
SP = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, SP + "/tools")
from kits import Deck

k = Deck()
from pptx.util import Inches
_orig_table = k.table


def _table(title, rows, note=None):
    sl = _orig_table(title, rows, note=note)
    if note:
        tsh = next(sh for sh in sl.shapes if sh.has_table)
        nsh = [sh for sh in sl.shapes if sh.has_text_frame and sh.text_frame.text.strip() == note][0]
        nsh.top = int(tsh.top + len(rows) * Inches(0.52) + Inches(0.3))
    return sl


k.table = _table
k.cover("Thực hành 5: Xây dựng KPIs và đánh giá hiệu quả hoạt động",
        "Phân tích dữ liệu Marketing, Bài 15",
        ["Giảng viên: Nguyễn Bình Minh An", "Khoa Kinh doanh số, Trường Kinh tế - Đại học Công nghiệp Hà Nội"])

k.bullets("Mục tiêu buổi thực hành và chuẩn đầu ra", [
    "Dựng mô hình dữ liệu hình sao từ 4 tệp bán hàng, làm sạch và ghi nhật ký từng quyết định",
    "Tạo bảng đặc trưng cấp khách hàng và phân cụm bằng K-means",
    "Chọn số cụm bằng chỉ số thống kê và khả năng đặt tên kinh doanh",
    "Gắn mỗi nhóm người dùng dashboard với quyết định, tần suất và KPI",
    "Dựng dashboard có dùng kết quả phân cụm, lập luận chỉ số bị loại",
    "CĐR L1, mức vận dụng U: kết hợp thuật toán, thống kê và kiến thức kinh doanh",
])

k.bullets("AGENDA", [
    "15.1.  Ôn tập: chất lượng dữ liệu, K-means, Silhouette, KPI, dashboard",
    "15.2.  Tình huống Trường Thịnh và bộ dữ liệu",
    "15.3.  Phần 1: nạp dữ liệu, làm sạch, dựng mô hình",
    "15.4.  Phần 2: phân cụm khách hàng",
    "15.5.  Phần 3: thiết kế dashboard",
    "15.6.  Quy trình, lỗi thường gặp, sản phẩm nộp",
])

k.bullets("CASE MỞ ĐẦU: Trường Thịnh chăm sóc 180 khách theo cùng một cách", [
    "Nhà máy gỗ ở Bình Dương bán cho 180 khách doanh nghiệp trong và ngoài nước",
    "Nhân viên giỏi dồn sức cho khách đơn to nhưng thất thường",
    "Khách đặt đều đặn gần như bị bỏ mặc",
    "Chỉ có file Excel doanh thu theo tháng, dữ liệu do nhiều người nhập",
    "Thảo luận 1: doanh thu thật của công ty là bao nhiêu?",
    "Thảo luận 2: 180 khách chia mấy nhóm, ai cần nhìn kết quả để quyết định gì?",
])

# 15.1
k.section("15.1.  Ôn tập kiến thức lý thuyết trọng tâm")
k.table("Mỗi phần của đề dựa trên một bài lý thuyết đã học", [
    ["Phần của đề", "Kiến thức cần dùng", "Bài, mục"],
    ["1. Làm sạch, mô hình", "Chất lượng dữ liệu, từ điển chỉ số", "Bài 2 mục 2.3; Bài 1 mục 1.3"],
    ["2.1 Đặc trưng", "R, F, M; ngày và kỳ phân tích cố định", "Bài 3; Bài 5 mục 5.2"],
    ["2.2 Phân cụm", "K-means, chuẩn hoá, Elbow, Silhouette, DBSCAN", "Bài 3 mục 3.2"],
    ["3.1 Người dùng", "Ba cấp KPI, SMART, quy trình xây KPI", "Bài 9 mục 9.2, 9.3"],
    ["3.2, 3.3 Dashboard", "Bốn loại dashboard, nguyên tắc trình bày", "Bài 10 mục 10.1, 10.2"],
])
k.table("Năm nhóm lỗi dữ liệu và cách phát hiện", [
    ["Nhóm lỗi", "Cách phát hiện"],
    ["Trùng lặp", "Đếm dòng theo khoá chính trước và sau Remove Duplicates"],
    ["Không nhất quán", "Bảng tần số giá trị riêng biệt của cột văn bản"],
    ["Sai kiểu dữ liệu", "Đổi sang kiểu số, đếm ô báo lỗi"],
    ["Thiếu, khoá mồ côi", "Đếm ô trống; ghép kiểu Left Anti"],
    ["Bất thường", "Q3 + 1,5 × IQR theo từng sản phẩm hoặc đơn vị tính"],
], note="Mỗi quyết định ghi số dòng bị ảnh hưởng và lý do (Bài 2, nguyên tắc chính xác và toàn vẹn).")
k.bullets("K-means nhạy với đơn vị đo và giá trị cực đoan", [
    "K-means tối thiểu hoá WCSS, tổng bình phương khoảng cách từ điểm đến tâm cụm",
    "Tâm cụm là trung bình, nên một khách cực lớn kéo lệch cả cụm",
    "Biến lệch phải như doanh thu, số đơn: lấy log(1 + x) trước",
    "Sau đó chuẩn hoá z = (x − trung bình) / độ lệch chuẩn",
    "Đặt n_init ≥ 10 và cố định random_state để chạy lại ra cùng kết quả",
])
k.table("Silhouette: đo mức tách bạch, không đo mức hữu ích", [
    ["Silhouette trung bình", "Cách đọc (Kaufman và Rousseeuw, 1990)"],
    ["0,71 đến 1,00", "Cấu trúc cụm mạnh"],
    ["0,51 đến 0,70", "Cấu trúc hợp lý"],
    ["0,26 đến 0,50", "Cấu trúc yếu, cần kiểm tra thêm"],
    ["0,25 trở xuống", "Không có cấu trúc đáng kể"],
], note="s(i) = [b(i) − a(i)] / max{a(i), b(i)}. Chọn K khi mọi cụm đặt được tên kinh doanh; chỉ số cao nhất chưa đủ.")
k.table("Bốn loại dashboard khác nhau ở người dùng và tần suất quyết định", [
    ["Loại", "Người dùng", "Tần suất", "Câu hỏi điển hình"],
    ["Tác nghiệp", "Nhân viên tuyến đầu", "Hằng ngày", "Hôm nay làm gì?"],
    ["Chiến thuật", "Quản lý cấp trung", "Tuần, tháng", "Ưu tiên nguồn lực vào đâu?"],
    ["Chiến lược", "Ban lãnh đạo", "Quý, năm", "Có đạt mục tiêu năm không?"],
    ["Phân tích", "Nhà phân tích", "Theo nhu cầu", "Vì sao chỉ số thay đổi?"],
], note="Nguồn: Bài 10, mục 10.2. KPI theo SMART (Bài 9); mỗi dashboard 5 đến 10 chỉ số, mỗi số có mốc so sánh.")
# 15.2
k.section("15.2.  Tình huống và dữ liệu")
k.table("Bốn tệp dữ liệu, 18 tháng, ngày phân tích 31/10/2026", [
    ["Tệp", "Vai trò", "Số dòng", "Khoá"],
    ["01_KhachHang.csv", "Bảng chiều khách hàng", "180", "MaKH"],
    ["02_SanPham.csv", "Bảng chiều sản phẩm", "56", "MaSP"],
    ["03_DonHang.csv", "Sự kiện: dòng đơn hàng", "8.537", "MaDonHang + MaSP"],
    ["04_KhieuNai.csv", "Sự kiện: khiếu nại", "176", "MaKhieuNai"],
], note="Một đơn có nhiều dòng sản phẩm. Bảng khiếu nại không có MaKH, phải đi qua mã đơn hàng. Dữ liệu mô phỏng, doanh nghiệp hư cấu.")

# 15.3
k.section("15.3.  Phần 1: Nạp dữ liệu, làm sạch và dựng mô hình")
k.bullets("Mô hình hình sao cần khoá duy nhất ở phía bảng chiều", [
    "Nối DimKhachHang và DimSanPham với FactDonHang theo quan hệ một-nhiều",
    "MaDonHang không duy nhất trong FactDonHang vì một đơn có nhiều dòng",
    "Tạo DimDonHang gồm cặp (MaDonHang, MaKH) đã bỏ trùng, nối với FactKhieuNai",
    "Nối thẳng hai bảng sự kiện tạo quan hệ nhiều-nhiều, khiếu nại bị đếm lặp",
    "Python: pandas.merge(..., validate=\"many_to_one\") báo lỗi khi khoá không duy nhất",
])
k.table("Sáu bước làm sạch, làm đúng thứ tự", [
    ["Bước", "Việc cần làm", "Công cụ Power Query"],
    ["1. Hồ sơ dữ liệu", "Đếm dòng, ô trống, giá trị riêng biệt", "Column quality, Column profile"],
    ["2. Văn bản", "Gộp biến thể quốc gia, loại hình khách", "Trim, Clean, bảng ánh xạ"],
    ["3. Kiểu dữ liệu", "Bỏ đuôi \" USD\", xác định vai trò dấu phẩy", "Replace Values, Change Type"],
    ["4. Trùng lặp", "Khoá dòng là (MaDonHang, MaSP)", "Remove Duplicates"],
    ["5. Thiếu, mồ côi", "Đọc ô trống cùng TrangThai trước khi xoá", "Merge Queries, Left Anti"],
    ["6. Bất thường", "IQR theo từng sản phẩm, xem từng dòng", "Group By, cột điều kiện"],
])
k.bullets("Ô trống chưa chắc là lỗi, số lượng lớn chưa chắc là thật", [
    "Ngày giao trống: kiểm tra trạng thái đơn trước khi xoá dòng",
    "Không so số lượng chung toàn bảng vì có 4 đơn vị: Bộ, Cái, Tấm, Tấn",
    "Ví dụ minh hoạ: số lượng 2, 3, 3, 4, 5, 6, 400; ngưỡng IQR là 9,25",
    "Kiểm chứng: so tổng doanh thu trước và sau khi xử lý từng nhóm dòng",
    "Ghi mọi thay đổi vào nhật ký: bảng, lỗi, cách phát hiện, số dòng, lý do",
])
k.table("Doanh thu tính theo từng dòng rồi mới cộng", [
    ["Cách tính", "Ví dụ minh hoạ: 10 sản phẩm, 200 USD, chiết khấu 0,1", "Kết quả"],
    ["Đúng: 0,1 là 10%", "10 × 200 × (1 − 0,1)", "1.800 USD"],
    ["Sai: hiểu 0,1 là 0,1%", "10 × 200 × (1 − 0,001)", "1.998 USD"],
], note="DAX: SUMX(FactDonHang, [SoLuong] * [DonGia_USD] * (1 - [ChietKhau_Pct])). Số khiếu nại: ghép trái từ bảng khách hàng, khách không có khiếu nại nhận 0.")

# 15.4
k.section("15.4.  Phần 2: Phân cụm khách hàng")
k.table("Bảng đặc trưng: mỗi khách một dòng, ít nhất 5 cột", [
    ["Đặc trưng", "Cách tính", "Ý nghĩa"],
    ["Recency", "Ngày từ đơn cuối đến 31/10/2026", "Còn hoạt động?"],
    ["Frequency", "Số MaDonHang riêng biệt", "Đặt đều đặn?"],
    ["Monetary", "Tổng doanh thu sau làm sạch", "Quy mô"],
    ["Độ biến động đơn", "Độ lệch chuẩn / trung bình giá trị đơn", "Ổn định hay thất thường?"],
    ["Số nhóm sản phẩm", "Số NhomSanPham đã mua", "Cơ hội bán chéo"],
    ["Tỷ lệ khiếu nại", "Đơn có khiếu nại / Frequency", "Rủi ro dịch vụ"],
], note="Kiểm tra tương quan: hai đặc trưng tương quan trên 0,8 thì giữ một.")
k.table("Cùng một quy trình trên ba công cụ", [
    ["Bước", "SPSS", "Python", "Power BI"],
    ["Chuẩn hoá", "Descriptives, Save standardized values", "StandardScaler", "Tự tạo cột z"],
    ["K-means", "Classify > K-Means Cluster", "KMeans(n_init=10, random_state=42)", "Automatically find clusters"],
    ["Chọn K", "TwoStep để xem Silhouette", "silhouette_score, K = 2..8", "Không có chỉ số"],
    ["Hồ sơ cụm", "Final Cluster Centers", "groupby(label).mean()", "Màu cụm"],
], note="Power BI chỉ phân cụm trên các trường đã kéo vào biểu đồ. Phân cụm đủ đặc trưng bằng SPSS hoặc Python, rồi nạp bảng MaKH, NhanCum vào mô hình.")
k.bullets("Chọn K bằng chỉ số, chốt K bằng tên kinh doanh", [
    "Vẽ inertia và Silhouette cho K từ 2 đến 8 trên cùng trục",
    "Giữ 2 đến 3 K ứng viên, lập hồ sơ cụm trên thang gốc",
    "Chọn K mà cụm nào cũng có tên và cách chăm sóc riêng",
    "Silhouette cao nhất chưa chắc là lời giải dùng được",
    "Mở rộng: DBSCAN tìm khách nhiễu; nhiễu có thể là khách thật cần chính sách riêng",
])
k.table("Hồ sơ cụm phải đọc được bằng ngôn ngữ kinh doanh", [
    ["Tiêu chí", "Cụm X (minh hoạ)", "Cụm Y (minh hoạ)"],
    ["Số khách", "40", "15"],
    ["Recency trung vị", "20 ngày", "210 ngày"],
    ["Số đơn trong 18 tháng", "45", "6"],
    ["Tên cụm", "Khách nội địa đặt đều", "Khách lớn đang im lặng"],
    ["Hành động", "Hợp đồng khung theo quý", "Giám đốc kinh doanh gọi trong 2 tuần"],
], note="Số liệu tự đặt, không phải kết quả của bộ dữ liệu Trường Thịnh.")

# 15.5
k.section("15.5.  Phần 3: Thiết kế dashboard")
k.table("Yêu cầu 3.1: thiết kế bắt đầu từ quyết định của người dùng", [
    ["Câu hỏi", "Minh hoạ: Trưởng phòng quản lý chất lượng"],
    ["Quyết định gì?", "Tháng này ưu tiên khắc phục lỗi nào, ở dòng sản phẩm nào"],
    ["Bao lâu một lần?", "Xem hằng tuần, chốt kế hoạch hằng tháng"],
    ["Loại dashboard?", "Chiến thuật"],
    ["KPI nào?", "Tỷ lệ đơn có khiếu nại; chi phí xử lý trên doanh thu; tỷ lệ đã giải quyết"],
], note="\"Ban lãnh đạo cần xem tổng quan\" không đạt yêu cầu vì không nêu quyết định.")
k.bullets("Yêu cầu 3.2: bố cục từ tổng quát xuống chi tiết", [
    "Hàng trên: 3 đến 5 thẻ KPI, mỗi thẻ có mốc so sánh",
    "Vùng giữa: biểu đồ trả lời câu hỏi chính của người dùng",
    "Vùng dưới: bảng chi tiết để đào sâu",
    "Kết quả phân cụm là một chiều phân tích: bộ lọc, màu, nhóm",
    "Mỗi cụm một màu cố định; màu nóng chỉ cho chỉ số chưa đạt",
])
k.bullets("Yêu cầu 3.3: bỏ chỉ số là một quyết định thiết kế", [
    "Không gắn với quyết định nào của người dùng đã chọn",
    "Trùng thông tin với chỉ số đã có",
    "Vô nghĩa khi cộng gộp, ví dụ cộng đại lượng khác đơn vị",
    "Bị vài giá trị cực đoan chi phối, dễ đọc sai",
    "Mỗi chỉ số bị loại: nêu tên, lý do, người dùng được gì khi không thấy nó",
])

# 15.6
k.section("15.6.  Quy trình, lỗi thường gặp và sản phẩm nộp")
k.table("Quy trình thực hiện trong buổi thực hành", [
    ["Giai đoạn", "Việc chính", "Thời lượng"],
    ["1", "Đọc đề, lập hồ sơ dữ liệu", "15 phút"],
    ["2", "Làm sạch, dựng mô hình, chốt doanh thu", "50 phút"],
    ["3", "Bảng đặc trưng, phân cụm, đặt tên cụm", "50 phút"],
    ["4", "Người dùng, dashboard, chỉ số loại bỏ", "55 phút"],
    ["5", "Viết diễn giải, kiểm tra lại, đóng gói", "20 phút"],
])
k.table("Lỗi thường gặp", [
    ["Lỗi", "Hậu quả", "Cách tránh"],
    ["Xoá mọi dòng có ô trống", "Mất đơn hợp lệ, lệch doanh thu", "Đọc ô trống cùng trạng thái"],
    ["Không tìm giá trị bất thường", "Doanh thu phồng", "IQR theo từng sản phẩm"],
    ["Quan hệ nhiều-nhiều", "Khiếu nại bị đếm lặp", "Tạo DimDonHang"],
    ["Không chuẩn hoá trước K-means", "Biến tiền quyết định cụm", "log rồi z-score"],
    ["Mô tả cụm bằng z-score", "Người kinh doanh không hiểu", "Hồ sơ trên thang gốc"],
    ["Dashboard không gắn quyết định", "Nhiều số, không ai dùng", "Đi ngược từ quyết định"],
])
k.table("Sản phẩm nộp và thang điểm đề xuất", [
    ["Yêu cầu", "Tiêu chí đạt", "Điểm"],
    ["1.1 đến 1.3", "Mô hình đúng, nhật ký làm sạch, doanh thu có đối chiếu", "3,0"],
    ["2.1", "Ít nhất 5 đặc trưng, có định nghĩa và kiểm tra tương quan", "1,0"],
    ["2.2", "Biến đổi, so sánh nhiều K, tên cụm, hành động", "3,0"],
    ["3.1", "Người dùng gắn quyết định, tần suất, KPI", "1,0"],
    ["3.2 và 3.3", "Dashboard dùng cụm, diễn giải, hai chỉ số loại bỏ", "2,0"],
], note="Nộp thư mục nén: .pbix, file code, Word, PDF hoặc PowerPoint (Word, PDF tối đa 4 trang kèm ảnh dashboard). Đề không công bố thang điểm; bảng này là đề xuất.")

k.bullets("TÓM TẮT", [
    "Làm sạch là bước phân tích đầu tiên; nhật ký là bằng chứng cho con số cuối",
    "Mô hình hình sao cần khoá duy nhất ở bảng chiều",
    "Đặc trưng bắt đầu từ R, F, M và mở rộng theo câu hỏi kinh doanh",
    "K-means cần log, z-score, n_init ≥ 10, random_state cố định",
    "Chốt K bằng chỉ số cộng khả năng đặt tên kinh doanh",
    "Dashboard đi ngược từ quyết định; bỏ chỉ số cũng là thiết kế",
])
k.bullets("Câu hỏi thảo luận", [
    "Vài dòng sai số lượng làm doanh thu lệch bao nhiêu? Làm sao chứng minh với kế toán?",
    "K = 6 có Silhouette cao hơn K = 5 nhưng khó đặt tên. Bạn chọn lời giải nào?",
    "Khách bị DBSCAN gán nhiễu: xoá, gộp hay chăm sóc riêng?",
    "Dashboard của bạn giúp người dùng quyết định điều gì vào sáng thứ Hai?",
    "Chỉ số nào bạn bỏ ra, và người dùng có nhớ nó không?",
])

out = SP + "/th_out/bai_15/Bai 15_Thuc hanh 5_Slides.pptx"
k.save(out)
print("saved", len(k.prs.slides))
