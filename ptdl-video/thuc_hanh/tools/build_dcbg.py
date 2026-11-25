import sys
SP = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, SP + "/tools")
from kits import Dcbg, WNS

d = Dcbg()
# kits.py lấy bảng đầu tiên của mẫu (khung "Mục tiêu" 1 ô, chữ đậm); dùng bảng dữ liệu thật (Bảng 8.1) làm mẫu
import copy
from docx import Document as _D
_t = [e for e in _D(SP + "/dcbg/b8.docx").element.body.iterchildren() if e.tag == WNS + "tbl"]
d.ex["table"] = copy.deepcopy(_t[1])
P, H1, H2, CAP, TB, EX = d.para, d.h1, d.h2, d.caption, d.table, d.example


def B(t):
    d.para("•  " + t)


def SRC(t="(Nguồn: Tác giả tổng hợp)"):
    d.para(t)


def numbered(t, num_id="3"):
    d.bullet(t)
    last = list(d.body)[-2]
    n = last.find(".//" + WNS + "numId")
    if n is not None:
        n.set(WNS + "val", num_id)


d.title("BÀI 15:", "THỰC HÀNH 5: XÂY DỰNG KPIs VÀ ĐÁNH GIÁ", "HIỆU QUẢ HOẠT ĐỘNG")
P("")
P("***********")

P("Mục tiêu: Sau buổi thực hành này, người học có khả năng:")
B("Nạp bốn tệp dữ liệu bán hàng vào một mô hình dữ liệu hình sao, phát hiện và xử lý các lỗi chất lượng dữ liệu, ghi lại từng quyết định làm sạch.")
B("Xây dựng bảng đặc trưng cấp khách hàng từ dữ liệu giao dịch, chọn phép biến đổi phù hợp và phân cụm khách hàng bằng K-means.")
B("Chọn số cụm bằng cả chỉ số thống kê lẫn khả năng đặt tên kinh doanh, viết chân dung cụm và đề xuất hành động marketing cho từng cụm.")
B("Xác định nhóm người dùng dashboard theo quyết định họ phải ra, chọn KPI tương ứng và dựng một dashboard có dùng kết quả phân cụm.")
B("Lập luận được vì sao một chỉ số có sẵn trong dữ liệu vẫn nên bị loại khỏi dashboard.")
P("Chuẩn đầu ra học phần liên quan: L1 (ứng dụng kiến thức về thuật toán và thống kê vào phân tích dữ liệu, kết hợp kiến thức kinh tế, kinh doanh để đưa ra khuyến nghị chiến lược về sản phẩm, khách hàng, thị trường), mức độ vận dụng U.")
P("Kiến thức cần có trước buổi học:")
B("Bài 1, mục 1.3: quy trình CRISP-DM và từ điển chỉ số chung.")
B("Bài 2, mục 2.3: quản trị dữ liệu marketing, các nguyên tắc chính xác, toàn vẹn, nhất quán và chuẩn hoá dữ liệu.")
B("Bài 3, mục 3.2 và mô hình RFM: phân tích cụm, K-means, chọn K bằng Elbow và Silhouette, DBSCAN; ba chỉ số R, F, M.")
B("Bài 5, mục 5.2: RFM làm nền cho phân khúc theo giá trị khách hàng.")
B("Bài 9, mục 9.2 và 9.3: quy trình xây dựng KPI, nguyên tắc SMART, ba cấp KPI, các sai lầm khi chọn KPI.")
B("Bài 10, mục 10.1 và 10.2: nguyên tắc trình bày dashboard, bốn loại dashboard tác nghiệp, chiến thuật, chiến lược, phân tích.")
P("Công cụ: SPSS, Excel hoặc Power BI theo đề bài. Sinh viên quen Python có thể dùng pandas và scikit-learn cho phần làm sạch và phân cụm, sau đó nạp kết quả vào Power BI. Đề bài yêu cầu nộp kèm file code, vì vậy mọi bước làm sạch nên được ghi thành script hoặc thành các bước Power Query có thể chạy lại.")

# ------------------------------------------------------------------ 15.1
H1("15.1. Ôn tập kiến thức lý thuyết trọng tâm")
H2("15.1.1. Chất lượng dữ liệu và mô hình dữ liệu")
P("Bài 2 nêu năm thuộc tính của dữ liệu chất lượng: chính xác, đầy đủ, kịp thời, nhất quán và phù hợp với mục tiêu. Trong thực hành, năm thuộc tính này chuyển thành năm nhóm lỗi cần kiểm tra. Bảng 15.1 gắn mỗi nhóm lỗi với cách phát hiện.")
CAP("Bảng 15.1. Các nhóm lỗi dữ liệu và cách phát hiện")
TB([
    ["Nhóm lỗi", "Biểu hiện thường gặp", "Cách phát hiện"],
    ["Trùng lặp", "Cùng một dòng xuất hiện hai lần", "Đếm số dòng theo khoá chính, so với số dòng sau Remove Duplicates"],
    ["Không nhất quán", "Một giá trị viết nhiều kiểu, thừa khoảng trắng, khác chữ hoa", "Lập bảng tần số các giá trị riêng biệt của cột văn bản"],
    ["Sai kiểu dữ liệu", "Số lưu dạng chữ, có ký tự đơn vị hoặc dấu phân cách lạ", "Thử đổi kiểu sang số, đếm số ô báo lỗi"],
    ["Thiếu và mồ côi", "Ô trống, khoá ngoại không có trong bảng gốc", "Đếm ô trống; ghép bảng kiểu left anti join"],
    ["Bất thường", "Giá trị lớn gấp hàng trăm lần mức thường gặp", "Tứ phân vị và khoảng IQR theo từng nhóm hàng"],
])
SRC()
P("Mô hình dữ liệu hình sao (star schema) tách dữ liệu thành bảng sự kiện (fact) và bảng chiều (dimension). Bảng sự kiện ghi từng giao dịch, mỗi dòng là một sự kiện có số đo, ví dụ một dòng đơn hàng có số lượng và đơn giá. Bảng chiều mô tả đối tượng, mỗi dòng là một khách hàng hoặc một sản phẩm, có khoá chính duy nhất. Quan hệ chuẩn đi từ bảng chiều sang bảng sự kiện theo kiểu một-nhiều. Khi khoá phía \"một\" không duy nhất, công cụ sẽ tạo quan hệ nhiều-nhiều và phép cộng dồn có thể bị nhân đôi.")
P("Nguyên tắc ghi chép: mỗi quyết định làm sạch phải ghi rõ số dòng bị ảnh hưởng và lý do. Bài 1 gọi đây là từ điển chỉ số chung. Thiếu bản ghi này, hai người làm cùng bộ dữ liệu sẽ ra hai con số doanh thu khác nhau mà không ai giải thích được vì sao.")

H2("15.1.2. Phân tích cụm và K-means")
P("Phân tích cụm là kỹ thuật học không giám sát. Thuật toán tự chia đối tượng thành nhóm sao cho các đối tượng trong cùng nhóm giống nhau và các nhóm khác nhau rõ. Mức giống nhau được đo bằng khoảng cách, thường là khoảng cách Euclid.")
P("K-means định nghĩa một cụm là tập các điểm gần một tâm cụm (centroid) hơn mọi tâm khác. Thuật toán tối thiểu hoá inertia, còn gọi là WCSS, tức tổng bình phương khoảng cách từ mỗi điểm đến tâm cụm của nó:")
P("WCSS = Σₖ Σ_{x ∈ Cₖ} ‖x − μₖ‖²")
P("trong đó μₖ là trung bình các điểm thuộc cụm k. Từ định nghĩa này suy ra ba hệ quả mà buổi thực hành sẽ gặp:")
B("K-means dùng trung bình nên nhạy với giá trị cực đoan. Một khách hàng có doanh thu gấp trăm lần người khác sẽ kéo tâm cụm về phía mình.")
B("K-means dùng khoảng cách nên nhạy với đơn vị đo. Biến tính bằng USD sẽ lấn át biến tính bằng số đơn nếu không chuẩn hoá.")
B("Tâm khởi tạo ngẫu nhiên nên mỗi lần chạy có thể ra kết quả khác. Cần đặt n_init từ 10 trở lên và cố định random_state.")
P("Chuẩn hoá z-score đưa mọi biến về trung bình 0, độ lệch chuẩn 1:")
P("z = (x − x̄) / s")
P("Với biến lệch phải mạnh như doanh thu hay số đơn, nên lấy log trước khi chuẩn hoá. Dùng log(1 + x) để xử lý giá trị 0. Phép log nén khoảng cách ở phía giá trị lớn, nhờ đó khách hàng lớn vẫn đứng riêng nhưng không lấn át toàn bộ phép đo khoảng cách.")
EX("Ví dụ 15.1. Tác dụng của phép log lên biến lệch phải")
P("Bốn khách hàng có tổng doanh thu lần lượt 5, 20, 80 và 2.000 nghìn USD (số liệu tự đặt). Trên thang gốc, khách lớn nhất cách khách nhỏ nhất 1.995 đơn vị, trong khi ba khách đầu chỉ cách nhau tối đa 75 đơn vị. Sau khi chuẩn hoá, ba khách đầu gần như trùng nhau và mọi khác biệt về khoảng cách đến từ khách thứ tư. Lấy log cơ số 10, bốn giá trị thành 0,70; 1,30; 1,90 và 3,30. Khoảng cách giữa các khách đều đặn hơn, khách thứ tư vẫn xa nhất nhưng ba khách đầu đã tách được khỏi nhau.")

H2("15.1.3. Chọn số cụm: Elbow và Silhouette")
P("Inertia luôn giảm khi K tăng, vì vậy không thể chọn K bằng cách lấy inertia nhỏ nhất. Phương pháp Elbow vẽ inertia theo K và chọn điểm mà đường cong gãy rõ nhất. Điểm gãy thường không rõ trên dữ liệu thật, nên cần thêm chỉ số Silhouette.")
P("Với mỗi điểm i, gọi a(i) là khoảng cách trung bình từ i đến các điểm cùng cụm và b(i) là khoảng cách trung bình nhỏ nhất từ i đến các điểm của một cụm khác. Hệ số Silhouette của điểm i là (Rousseeuw, 1987):")
P("s(i) = [b(i) − a(i)] / max{a(i), b(i)}")
P("s(i) nằm trong khoảng từ −1 đến 1. Giá trị gần 1 nghĩa là điểm nằm gọn trong cụm của nó. Giá trị gần 0 nghĩa là điểm nằm trên ranh giới hai cụm. Giá trị âm gợi ý điểm bị gán nhầm cụm. Silhouette của cả lời giải là trung bình s(i) trên mọi điểm. Kaufman và Rousseeuw (1990) đề xuất thang đọc ở Bảng 15.2.")
CAP("Bảng 15.2. Thang đọc hệ số Silhouette trung bình")
TB([
    ["Silhouette trung bình", "Cách đọc"],
    ["0,71 đến 1,00", "Cấu trúc cụm mạnh"],
    ["0,51 đến 0,70", "Cấu trúc cụm hợp lý"],
    ["0,26 đến 0,50", "Cấu trúc yếu, có thể do dữ liệu tạo ra; cần kiểm tra thêm"],
    ["0,25 trở xuống", "Không có cấu trúc cụm đáng kể"],
])
SRC("(Nguồn: Kaufman và Rousseeuw, 1990)")
EX("Ví dụ 15.2. Tính Silhouette bằng tay")
P("Bốn điểm trên một trục số: cụm A gồm 1 và 2, cụm B gồm 6 và 8 (số liệu tự đặt). Với điểm 1: a = 1, b = (5 + 7)/2 = 6, s = (6 − 1)/6 = 0,83. Với điểm 2: a = 1, b = (4 + 6)/2 = 5, s = 0,80. Với điểm 6: a = 2, b = (5 + 4)/2 = 4,5, s = 2,5/4,5 = 0,56. Với điểm 8: a = 2, b = (7 + 6)/2 = 6,5, s = 4,5/6,5 = 0,69. Silhouette trung bình bằng 0,72. Cụm B kém chặt hơn cụm A vì hai điểm của nó cách nhau 2 đơn vị.")
P("Bài 3 đã nhấn mạnh: chỉ số đo mức tách bạch hình học, không đo mức hữu ích. Một lời giải có Silhouette cao hơn vẫn có thể bị loại nếu không đặt được tên kinh doanh cho các cụm, hoặc nếu doanh nghiệp không đủ nguồn lực phục vụ từng cụm theo cách khác nhau. Quyết định K cuối cùng là quyết định kinh doanh có căn cứ thống kê.")
P("DBSCAN (Ester và cộng sự, 1996) định nghĩa cụm là vùng có mật độ cao, với hai tham số ε và MinPts. Thuật toán gán nhãn −1 cho điểm nhiễu, tức điểm không thuộc cụm nào. K-means thì ép mọi điểm vào một cụm. Trong bài này DBSCAN là bước kiểm tra phụ, không bắt buộc: nó cho biết khách hàng nào có hành vi quá khác thường để gom vào bất kỳ nhóm nào. Điểm nhiễu không đồng nghĩa với dữ liệu bẩn. Nhiều khi đó là khách hàng thật cần một chính sách chăm sóc riêng.")

H2("15.1.4. KPI và dashboard")
P("Bài 9 định nghĩa KPI là thước đo định lượng mức độ đạt mục tiêu. Một KPI tốt đáp ứng SMART: cụ thể, đo được, khả thi, gắn với mục tiêu, có thời hạn. KPI chia thành ba cấp. KPI chiến lược đo kết quả tổng thể như doanh thu, thị phần, CLV. KPI chiến thuật đo kết quả trung gian như tỷ lệ giữ chân, tỷ lệ chuyển đổi. KPI vận hành đo hoạt động hằng ngày. KPI cấp dưới phải đóng góp vào KPI cấp trên.")
P("Bài 10 phân bốn loại dashboard theo người dùng và tần suất quyết định (Bảng 15.3). Cách chọn loại dashboard đi ngược từ quyết định: trước hết hỏi người dùng phải quyết định gì, bao lâu một lần, rồi mới chọn KPI và biểu đồ.")
CAP("Bảng 15.3. Bốn loại dashboard theo Bài 10")
TB([
    ["Loại", "Mục tiêu", "Người dùng", "Tần suất"],
    ["Tác nghiệp", "Theo dõi chỉ số vận hành, hành động ngay", "Nhân viên tuyến đầu, quản lý vận hành", "Hằng ngày"],
    ["Chiến thuật", "Nối chiến lược với vận hành, quyết định ngắn hạn", "Quản lý cấp trung", "Hằng tuần, hằng tháng"],
    ["Chiến lược", "Theo dõi chỉ số dài hạn so với mục tiêu năm", "Ban lãnh đạo", "Hằng quý, hằng năm"],
    ["Phân tích", "Đào sâu dữ liệu lịch sử, tìm nguyên nhân, dự báo", "Nhà phân tích, quản lý muốn đào sâu", "Theo nhu cầu"],
])
SRC("(Nguồn: Tổng hợp từ Bài 10)")
P("Bảy nguyên tắc trình bày của Bài 10 cần áp dụng trực tiếp trong Phần 3: rõ mục tiêu, đơn giản, phân cấp thông tin từ tổng quát xuống chi tiết, nhất quán màu và định dạng, có tương tác lọc, có ngữ cảnh so sánh, dữ liệu chính xác và cập nhật. Bài 9 bổ sung một cảnh báo: quá nhiều KPI làm loãng sự chú ý. Một dashboard nên giữ khoảng 5 đến 10 chỉ số trọng yếu.")

# ------------------------------------------------------------------ 15.2
H1("15.2. Tình huống và dữ liệu")
H2("15.2.1. Doanh nghiệp Trường Thịnh")
P("Công ty Cổ phần Chế biến gỗ Trường Thịnh có nhà máy tại Bình Dương. Công ty sản xuất đồ gỗ ngoài trời, nội thất phòng ngủ, tủ bếp, ván ép công nghiệp và viên nén gỗ, bán cho 180 khách hàng doanh nghiệp. Khách gồm nhà nhập khẩu ở Hoa Kỳ, Nhật Bản, châu Âu, chuỗi bán lẻ nội thất trong nước, nhà thầu thi công nội thất dự án và một mạng lưới đại lý nhỏ.")
P("Hai năm gần đây, khách châu Âu siết yêu cầu về chứng chỉ FSC và truy xuất nguồn gốc gỗ. Khách nội địa nhạy cảm về giá, đặt đơn nhỏ nhưng dày. Đội kinh doanh chăm sóc mọi khách theo cùng một cách: nhân viên giỏi dành phần lớn thời gian cho khách đặt đơn to nhưng thất thường, nhóm khách đều đặn gần như bị bỏ mặc. Công ty chưa từng phân nhóm khách hàng bằng dữ liệu và chỉ có file Excel doanh thu theo tháng.")
P("Trường Thịnh là doanh nghiệp hư cấu. Toàn bộ số liệu là dữ liệu mô phỏng phục vụ giảng dạy, không được trích dẫn như phát hiện về ngành gỗ Việt Nam.")
P("Câu hỏi quản trị của buổi thực hành có ba tầng. Tầng một: doanh thu thật của công ty là bao nhiêu sau khi dữ liệu được làm sạch. Tầng hai: 180 khách hàng chia thành mấy nhóm hành vi, mỗi nhóm cần cách chăm sóc nào. Tầng ba: ai trong công ty cần nhìn kết quả này, nhìn bằng dashboard nào, để ra quyết định gì.")

H2("15.2.2. Bộ dữ liệu")
P("Dữ liệu gồm 18 tháng giao dịch trích từ hệ thống bán hàng, ngày phân tích quy ước là 31/10/2026. Bảng 15.4 mô tả bốn tệp. Tên tệp trong thư mục dữ liệu ngắn hơn tên ghi trong đề bài, ví dụ 01_KhachHang.csv tương ứng với 01_DimKhachHang.csv; nội dung là một.")
CAP("Bảng 15.4. Bốn tệp dữ liệu của Trường Thịnh")
TB([
    ["Tệp", "Vai trò", "Số dòng", "Khoá"],
    ["01_KhachHang.csv", "Bảng chiều khách hàng", "180", "MaKH"],
    ["02_SanPham.csv", "Bảng chiều sản phẩm", "56", "MaSP"],
    ["03_DonHang.csv", "Bảng sự kiện dòng đơn hàng", "8.537", "MaDonHang + MaSP"],
    ["04_KhieuNai.csv", "Bảng sự kiện khiếu nại", "176", "MaKhieuNai"],
])
SRC("(Nguồn: Đề bài Thực hành 5)")
CAP("Bảng 15.5. Các cột chính và lưu ý khi đọc")
TB([
    ["Tệp", "Cột", "Lưu ý"],
    ["KhachHang", "QuocGia, KenhBanHang, LoaiHinhKH", "Văn bản do nhiều người nhập, viết nhiều kiểu"],
    ["KhachHang", "NamBatDauHopTac, MaNhanVienPhuTrach", "Dùng để tính thâm niên và phân bổ nhân sự"],
    ["SanPham", "NhomSanPham, LoaiGo, ChungChiFSC", "Sáu nhóm sản phẩm, cột FSC nhận Có hoặc Không"],
    ["SanPham", "DonViTinh, GiaNiemYet_USD", "Bốn đơn vị: Bộ, Cái, Tấm, Tấn; không cộng số lượng khác đơn vị"],
    ["DonHang", "NgayDatHang, NgayGiaoHang, TrangThai", "Ô ngày giao trống phải đọc cùng cột trạng thái"],
    ["DonHang", "SoLuong, DonGia_USD, ChietKhau_Pct", "Chiết khấu lưu dạng tỷ lệ thập phân, ví dụ 0,1 là 10%"],
    ["KhieuNai", "MaDonHang, LoaiKhieuNai, MucDo, ChiPhiXuLy_USD", "Nối với khách hàng qua mã đơn hàng"],
])
SRC()
P("Hai điểm cấu trúc cần nhận ra ngay khi mở dữ liệu. Thứ nhất, một đơn hàng có thể gồm nhiều dòng sản phẩm, vì vậy MaDonHang không duy nhất trong bảng đơn hàng. Khoá đúng của một dòng là cặp (MaDonHang, MaSP). Thứ hai, bảng khiếu nại không có MaKH. Muốn đếm khiếu nại theo khách hàng, phải đi qua mã đơn hàng để tìm khách. Hai điểm này quyết định cách dựng mô hình ở Phần 1.")

# ------------------------------------------------------------------ 15.3
H1("15.3. Hướng dẫn Phần 1: Nạp dữ liệu, làm sạch và dựng mô hình")
H2("15.3.1. Yêu cầu 1.1: Nạp dữ liệu và dựng mô hình dữ liệu")
P("Mục đích: đưa bốn tệp vào một mô hình mà mọi phép tính sau này đều chạy đúng, không bị nhân đôi.")
P("Các bước trong Power BI:")
B("Get Data, chọn Text/CSV, nạp từng tệp. Kiểm tra mã hoá UTF-8 để tên tiếng Việt hiển thị đúng. Mở Transform Data để làm việc trong Power Query.")
B("Đổi tên bảng theo vai trò: DimKhachHang, DimSanPham, FactDonHang, FactKhieuNai.")
B("Tạo thêm bảng DimDonHang gồm các cặp (MaDonHang, MaKH) duy nhất: tham chiếu FactDonHang, giữ hai cột, Remove Duplicates. Bảng này có khoá MaDonHang duy nhất.")
B("Trong Model view, nối DimKhachHang[MaKH] với FactDonHang[MaKH], DimSanPham[MaSP] với FactDonHang[MaSP], DimDonHang[MaDonHang] với FactKhieuNai[MaDonHang]. Cả ba quan hệ phải là một-nhiều, lọc một chiều.")
B("Tạo bảng ngày (Date table) bằng CALENDAR từ 01/05/2025 đến 31/10/2026, đánh dấu Mark as date table, nối với NgayDatHang.")
P("Trong Python, mô hình tương đương là các phép merge có kiểm tra: dùng pandas.merge với tham số validate=\"many_to_one\" khi ghép bảng sự kiện với bảng chiều. Nếu khoá bên phải không duy nhất, pandas báo lỗi ngay thay vì âm thầm nhân dòng.")
P("Cạm bẫy: nối trực tiếp FactKhieuNai với FactDonHang qua MaDonHang. Power BI sẽ tạo quan hệ nhiều-nhiều. Một khiếu nại của đơn có ba dòng sản phẩm sẽ bị đếm ba lần khi cộng theo khách hàng.")
P("Sản phẩm cần nộp: ảnh chụp Model view có đủ bảng và quan hệ, kèm một câu giải thích vì sao cần bảng DimDonHang hoặc giải pháp thay thế tương đương.")

H2("15.3.2. Yêu cầu 1.2: Làm sạch và chuẩn hoá dữ liệu")
P("Mục đích: biến dữ liệu do nhiều người nhập thành một nguồn duy nhất mà mọi phòng ban tính ra cùng một con số. Quy trình đề xuất gồm sáu bước, làm theo đúng thứ tự vì bước sau dựa vào kết quả bước trước.")
P("Bước 1. Lập hồ sơ dữ liệu (data profiling). Trong Power Query, bật View, Column quality, Column distribution và Column profile, chọn chế độ profiling trên toàn bộ dữ liệu thay vì 1.000 dòng đầu. Trong Python, dùng df.info(), df.isna().sum(), df[col].value_counts(dropna=False). Ghi lại số dòng ban đầu của từng bảng.")
P("Bước 2. Chuẩn hoá văn bản. Với QuocGia và LoaiHinhKH, áp dụng Trim để bỏ khoảng trắng đầu cuối, Clean để bỏ ký tự điều khiển, rồi đưa về một kiểu chữ thống nhất. Sau đó lập bảng tần số giá trị riêng biệt. Các biến thể như viết không dấu, viết hoa toàn bộ, viết tắt hay viết tiếng Anh của cùng một quốc gia cần được gộp bằng bảng ánh xạ (mapping table) hai cột: giá trị gốc và giá trị chuẩn. Bảng ánh xạ tốt hơn chuỗi Replace Values vì người khác đọc được và bổ sung được.")
P("Bước 3. Sửa kiểu dữ liệu. DonGia_USD có dòng kèm đuôi \" USD\" và có dấu phẩy. Trước khi thay, phải xác định dấu phẩy là phân cách hàng nghìn hay phân cách thập phân bằng cách xem vài giá trị cụ thể và so với GiaNiemYet_USD của cùng sản phẩm. SoLuong có khoảng trắng thừa. Sau khi thay ký tự, đổi kiểu sang Decimal Number và Whole Number, rồi đếm số ô báo Error. Số ô lỗi phải bằng 0 trước khi đi tiếp.")
P("Bước 4. Xử lý trùng lặp. Xác định khoá dòng là (MaDonHang, MaSP), sau đó chọn hai cột này và Remove Duplicates. Nên kiểm tra thêm: các dòng trùng có giống hệt nhau ở mọi cột không. Nếu trùng khoá nhưng khác số lượng, đó là vấn đề nghiệp vụ cần hỏi lại chứ không tự xoá.")
P("Bước 5. Xử lý thiếu và khoá mồ côi. Đếm ô trống ở từng cột. Với mỗi cột có ô trống, hỏi: ô trống này là lỗi hay là thông tin? Ví dụ, ngày giao trống có thể chỉ đơn chưa giao. Đối chiếu với TrangThai trước khi quyết định xoá. Với khoá mồ côi, dùng Merge Queries kiểu Left Anti để liệt kê dòng ở bảng sự kiện không tìm thấy khoá trong bảng chiều. Có hai cách xử lý chấp nhận được: loại dòng, hoặc giữ lại với nhãn \"Không xác định\" nếu giải thích được vì sao giữ.")
P("Bước 6. Tìm giá trị bất thường. Bốn đơn vị tính khác nhau nên không so số lượng chung toàn bảng. Tính tứ phân vị của SoLuong theo từng MaSP hoặc từng DonViTinh, đánh dấu dòng vượt Q3 + 1,5 × IQR (quy tắc Tukey), rồi xem từng dòng bị đánh dấu. Một dòng có số lượng gấp vài trăm lần mức thường gặp của chính sản phẩm đó gần như chắc chắn là lỗi nhập liệu. Cách kiểm chứng nhanh: tính tổng doanh thu trước và sau khi xử lý các dòng này. Nếu vài dòng làm doanh thu thay đổi hàng chục phần trăm, đó là dấu hiệu cần xử lý.")
EX("Ví dụ 15.3. Phát hiện số lượng bất thường bằng IQR")
P("Một sản phẩm tính theo Cái có bảy dòng với số lượng 2, 3, 3, 4, 5, 6, 400 (số liệu tự đặt). Theo cách tính QUARTILE.INC của Excel, Q1 = 3, Q3 = 5,5, IQR = 2,5. Ngưỡng trên là 5,5 + 1,5 × 2,5 = 9,25. Dòng 400 vượt ngưỡng 43 lần. Nếu đơn giá là 300 USD, dòng này đóng góp 120.000 USD, trong khi sáu dòng còn lại cộng lại chỉ 6.900 USD. Một dòng sai làm tổng doanh thu của sản phẩm phồng gần 18 lần.")
CAP("Bảng 15.6. Mẫu nhật ký làm sạch cần nộp")
TB([
    ["TT", "Bảng", "Lỗi phát hiện", "Cách phát hiện", "Số dòng", "Cách xử lý và lý do"],
    ["1", "FactDonHang", "...", "...", "...", "..."],
    ["2", "DimKhachHang", "...", "...", "...", "..."],
    ["3", "FactKhieuNai", "...", "...", "...", "..."],
])
SRC()
P("Cạm bẫy thường gặp ở yêu cầu 1.2:")
B("Xoá mọi dòng có ô trống. Cách này nhanh nhưng có thể xoá luôn những đơn hợp lệ.")
B("Chỉ sửa bốn loại lỗi được nêu sẵn trong dữ liệu mà không tự kiểm tra giá trị bất thường.")
B("Thay dấu phẩy trước khi biết nó là dấu gì, khiến 1,5 thành 15.")
B("Không ghi số dòng trước và sau từng bước, nên không chứng minh được kết quả.")

H2("15.3.3. Yêu cầu 1.3: Số khiếu nại theo khách hàng và tổng doanh thu")
P("Doanh thu của một dòng đơn hàng là số lượng nhân đơn giá sau chiết khấu:")
P("Doanh thu dòng = SoLuong × DonGia_USD × (1 − ChietKhau_Pct)")
P("Trong Power BI, viết measure bằng SUMX để tính theo từng dòng rồi mới cộng:")
P("Doanh thu = SUMX(FactDonHang, FactDonHang[SoLuong] * FactDonHang[DonGia_USD] * (1 - FactDonHang[ChietKhau_Pct]))")
P("Không viết SUM(SoLuong) × SUM(DonGia_USD), vì tích của hai tổng khác tổng của các tích. Trước khi chốt, cần quyết định đơn ở trạng thái nào được tính vào doanh thu và ghi rõ quy ước đó trên dashboard.")
EX("Ví dụ 15.4. Đọc sai cột chiết khấu")
P("Một dòng có SoLuong = 10, DonGia_USD = 200, ChietKhau_Pct = 0,1 (số liệu tự đặt). Đọc đúng 0,1 là 10%, doanh thu dòng là 10 × 200 × 0,9 = 1.800 USD. Nếu hiểu 0,1 là 0,1% theo tên cột \"Pct\", doanh thu thành 1.998 USD, lệch 11%. Tên cột không thay được việc xem dữ liệu: giá trị lớn nhất của cột là bao nhiêu sẽ cho biết thang đo thật.")
P("Số khiếu nại theo khách hàng: trong Power BI, measure COUNTROWS(FactKhieuNai) đặt cạnh DimKhachHang[MaKH] sẽ tự đi qua DimDonHang nếu mô hình dựng đúng. Trong Python, ghép FactKhieuNai với bảng (MaDonHang, MaKH) đã bỏ trùng rồi groupby(\"MaKH\").size(). Khách không có khiếu nại phải nhận giá trị 0 chứ không bị thiếu dòng, vì vậy dùng ghép trái từ bảng khách hàng và fillna(0).")
P("Sản phẩm cần nộp: tổng doanh thu toàn công ty sau làm sạch, kèm bảng đối chiếu doanh thu trước và sau từng bước xử lý chính; bảng số khiếu nại của 180 khách hàng.")

# ------------------------------------------------------------------ 15.4
H1("15.4. Hướng dẫn Phần 2: Phân cụm khách hàng")
H2("15.4.1. Yêu cầu 2.1: Bảng tổng hợp cấp khách hàng")
P("Mục đích: chuyển hơn tám nghìn dòng giao dịch thành 180 dòng, mỗi dòng một khách hàng, mỗi cột một đặc trưng mô tả hành vi. Đề yêu cầu ít nhất năm đặc trưng. Bảng 15.7 gợi ý các ứng viên. Sinh viên chọn và giải thích lựa chọn của mình.")
CAP("Bảng 15.7. Gợi ý đặc trưng cấp khách hàng")
TB([
    ["Đặc trưng", "Cách tính", "Ý nghĩa kinh doanh"],
    ["Recency", "Số ngày từ đơn gần nhất đến 31/10/2026", "Khách còn hoạt động hay đang rời đi"],
    ["Frequency", "Số MaDonHang riêng biệt trong 18 tháng", "Mức đặt hàng đều đặn"],
    ["Monetary", "Tổng doanh thu sau làm sạch", "Quy mô giá trị"],
    ["Giá trị đơn trung bình", "Monetary / Frequency", "Đơn to hay đơn nhỏ"],
    ["Độ biến động giá trị đơn", "Hệ số biến thiên = độ lệch chuẩn / trung bình giá trị đơn", "Đặt hàng ổn định hay thất thường"],
    ["Số nhóm sản phẩm", "Số NhomSanPham riêng biệt đã mua", "Độ rộng quan hệ, cơ hội bán chéo"],
    ["Tỷ lệ khiếu nại", "Số đơn có khiếu nại / Frequency", "Rủi ro chất lượng dịch vụ"],
    ["Tỷ trọng hàng FSC", "Doanh thu hàng có FSC / Monetary", "Mức nhạy với yêu cầu chứng chỉ"],
])
SRC()
P("Ba đặc trưng đầu là bộ R, F, M của Bài 3 và Bài 5. Phải cố định ngày phân tích và kỳ phân tích trước khi tính, nếu không các con số không so sánh được. Frequency đếm số đơn riêng biệt chứ không đếm số dòng, vì một đơn nhiều sản phẩm vẫn là một lần đặt hàng.")
P("Độ biến động giá trị đơn cần ít nhất hai đơn mới tính được. Khách chỉ có một đơn sẽ nhận giá trị thiếu; cần quyết định gán 0 hay loại khỏi phân cụm và ghi lý do.")
P("Trước khi phân cụm, tính ma trận tương quan giữa các đặc trưng. Hai đặc trưng tương quan trên 0,8 gần như đo cùng một thứ và sẽ được tính trọng số gấp đôi trong khoảng cách. Khi đó nên giữ đặc trưng dễ diễn giải hơn.")
P("Sản phẩm cần nộp: bảng 180 dòng, định nghĩa từng cột, thống kê mô tả gồm trung bình, trung vị, độ lệch chuẩn, giá trị nhỏ nhất và lớn nhất.")

H2("15.4.2. Yêu cầu 2.2: Phân cụm bằng K-means")
P("Quy trình gồm năm bước.")
P("Bước 1. Biến đổi. Xem phân phối từng đặc trưng. Biến tiền và biến đếm thường lệch phải mạnh; lấy log(1 + x) cho các biến này. Biến tỷ lệ nằm giữa 0 và 1 thường không cần log.")
P("Bước 2. Chuẩn hoá z-score cho mọi đặc trưng đưa vào mô hình.")
P("Bước 3. Chạy K-means với K từ 2 đến 8. Ghi inertia và Silhouette trung bình cho từng K, vẽ hai đường trên cùng trục hoành.")
P("Bước 4. Chọn hai hoặc ba K ứng viên. Với mỗi ứng viên, tính bảng hồ sơ cụm: số khách, trung bình từng đặc trưng trên thang gốc, cơ cấu loại hình khách hàng và kênh bán. Chọn K mà mọi cụm đều đặt được tên kinh doanh rõ ràng và mỗi cụm cần một cách chăm sóc khác.")
P("Bước 5. Đặt tên, mô tả chân dung, đề xuất hành động marketing cho từng cụm.")
CAP("Bảng 15.8. Thực hiện phân cụm trên ba công cụ")
TB([
    ["Bước", "SPSS", "Python (scikit-learn)", "Power BI"],
    ["Chuẩn hoá", "Analyze > Descriptive Statistics > Descriptives, chọn Save standardized values as variables", "StandardScaler().fit_transform(X)", "Không có sẵn; chuẩn hoá trước bằng cột tính toán"],
    ["Chạy K-means", "Analyze > Classify > K-Means Cluster, nhập biến Z, đặt số cụm, Save cluster membership", "KMeans(n_clusters=k, n_init=10, random_state=42)", "Scatter chart, ba chấm > Automatically find clusters"],
    ["Chọn K", "Chạy lại với nhiều K; dùng TwoStep Cluster để xem Silhouette", "silhouette_score(X, labels), vòng lặp K = 2..8", "Chỉ chọn số cụm, không có chỉ số"],
    ["Đọc kết quả", "Final Cluster Centers, ANOVA, Number of Cases in each Cluster", "groupby(label).mean() trên thang gốc", "Màu cụm trên biểu đồ"],
])
SRC("(Nguồn: Tác giả tổng hợp từ tài liệu IBM SPSS Statistics và scikit-learn)")
P("Lưu ý về SPSS: thủ tục K-Means Cluster không tự chuẩn hoá biến, nên phải tạo biến Z trước. Bảng ANOVA trong kết quả chỉ dùng để mô tả biến nào tách cụm mạnh. Các giá trị F và Sig. ở đây không phải kiểm định giả thuyết, vì cụm được tạo ra để tối đa khác biệt giữa các nhóm. Bản thân SPSS cảnh báo điều này ngay dưới bảng.")
P("Lưu ý về Power BI: tính năng Automatically find clusters chỉ dùng các trường đã đưa vào biểu đồ, thường là hai trường. Cách này phù hợp để thử nhanh, không thay được phân cụm trên đủ năm đến sáu đặc trưng. Kết quả phân cụm từ SPSS hoặc Python được xuất thành tệp MaKH và NhanCum rồi nạp vào Power BI như một bảng chiều mới, nối với DimKhachHang qua MaKH.")
P("Lưu ý về Python: đặt random_state cố định để người chấm chạy lại được. Silhouette tính trên dữ liệu đã chuẩn hoá, cùng không gian mà K-means dùng. Hồ sơ cụm lại nên trình bày trên thang gốc để người kinh doanh đọc được.")
P("Kiểm tra mở rộng bằng DBSCAN, không bắt buộc. Chạy DBSCAN trên cùng ma trận đã chuẩn hoá, thử ε quanh 0,8 đến 1,5 với MinPts bằng 5. Liệt kê các khách bị gán nhãn nhiễu và so với nhãn K-means của họ. Câu hỏi cần trả lời: những khách này là lỗi dữ liệu hay là nhóm hành vi thật mà K-means đã ép vào một cụm tròn?")
EX("Ví dụ 15.5. Mẫu hồ sơ cụm và đề xuất hành động")
P("Bảng 15.9 minh hoạ cách trình bày với hai cụm giả định, số liệu tự đặt, không phải kết quả của bộ dữ liệu Trường Thịnh.")
CAP("Bảng 15.9. Minh hoạ hồ sơ cụm (số liệu tự đặt)")
TB([
    ["Tiêu chí", "Cụm X", "Cụm Y"],
    ["Số khách", "40", "15"],
    ["Recency trung vị", "20 ngày", "210 ngày"],
    ["Số đơn trong 18 tháng", "45", "6"],
    ["Hệ số biến thiên giá trị đơn", "0,3", "1,4"],
    ["Tên đề xuất", "Khách nội địa đặt đều", "Khách lớn đang im lặng"],
    ["Hành động", "Hợp đồng khung theo quý, giao hàng định kỳ", "Giám đốc kinh doanh gọi trực tiếp trong 2 tuần"],
])
SRC("(Nguồn: Ví dụ minh hoạ)")
P("Tên cụm tốt nói được hành vi và gợi ra hành động. Tránh tên kỹ thuật như \"Cụm 2\" hoặc tên mơ hồ như \"Khách trung bình\". Mỗi đề xuất hành động nên có người thực hiện, thời hạn và chỉ số theo dõi, đúng tinh thần SMART của Bài 9.")
P("Cạm bẫy ở Phần 2:")
B("Đưa MaKH, năm bắt đầu hợp tác hoặc biến mã hoá danh mục dạng số vào K-means như biến liên tục.")
B("Phân cụm trên dữ liệu chưa làm sạch. Vài dòng số lượng sai sẽ tạo ra một cụm chỉ có một hai khách.")
B("Chọn K theo Silhouette cao nhất mà không xem cụm có đặt tên được không.")
B("Mô tả cụm bằng giá trị z-score. Người kinh doanh không đọc được \"Monetary = 1,2\".")
B("Kết luận khách bị DBSCAN gán nhiễu là dữ liệu bẩn và xoá đi.")
P("Sản phẩm cần nộp: biểu đồ Elbow và Silhouette, bảng so sánh các K ứng viên, bảng hồ sơ cụm, tên và mô tả từng cụm, đề xuất hành động, tệp kết quả MaKH và nhãn cụm.")

# ------------------------------------------------------------------ 15.5
H1("15.5. Hướng dẫn Phần 3: Thiết kế dashboard")
H2("15.5.1. Yêu cầu 3.1: Xác định nhóm người dùng")
P("Mục đích: thiết kế bắt đầu từ quyết định, không bắt đầu từ dữ liệu. Với mỗi nhóm người dùng, trả lời năm câu: họ là ai, họ phải quyết định gì, bao lâu một lần, mức độ quyết định là chiến lược, chiến thuật hay tác nghiệp, cần thông tin và KPI nào để ra quyết định đó. Câu trả lời \"ban lãnh đạo cần xem tổng quan\" không đạt yêu cầu vì không nêu quyết định cụ thể.")
EX("Ví dụ 15.6. Phân tích một nhóm người dùng")
P("Bảng 15.10 minh hoạ với nhóm Trưởng phòng quản lý chất lượng, một nhóm có trong doanh nghiệp sản xuất nhưng đề bài không nêu. Sinh viên tự xác định các nhóm người dùng của Trường Thịnh theo cùng khung.")
CAP("Bảng 15.10. Khung phân tích người dùng dashboard, minh hoạ một nhóm")
TB([
    ["Câu hỏi", "Trưởng phòng quản lý chất lượng"],
    ["Quyết định", "Tháng này ưu tiên khắc phục loại lỗi nào, ở dòng sản phẩm nào"],
    ["Tần suất", "Hằng tuần xem, hằng tháng chốt kế hoạch"],
    ["Mức độ quyết định", "Chiến thuật, dashboard chiến thuật"],
    ["Thông tin cần", "Khiếu nại theo loại, mức độ, nhóm sản phẩm, cụm khách hàng; khiếu nại chưa giải quyết"],
    ["KPI", "Tỷ lệ đơn có khiếu nại, chi phí xử lý khiếu nại trên doanh thu, tỷ lệ khiếu nại đã giải quyết"],
])
SRC("(Nguồn: Ví dụ minh hoạ)")

H2("15.5.2. Yêu cầu 3.2: Dựng dashboard có dùng kết quả phân cụm")
P("Chọn một nhóm người dùng đã xác định ở 3.1 và dựng dashboard cho họ. Kết quả phân cụm phải xuất hiện như một chiều phân tích, ví dụ bộ lọc theo cụm, doanh thu theo cụm, hay danh sách khách cần liên hệ theo cụm.")
P("Bố cục theo nguyên tắc phân cấp thông tin của Bài 10:")
B("Hàng trên cùng: 3 đến 5 thẻ KPI (card), mỗi thẻ có giá trị so sánh như kỳ trước hoặc mục tiêu. Con số không có so sánh không cho biết tốt hay xấu.")
B("Vùng giữa: biểu đồ trả lời câu hỏi chính của người dùng. So sánh giữa nhóm dùng cột ngang, xu hướng theo tháng dùng đường, quan hệ hai biến dùng phân tán.")
B("Vùng dưới: bảng chi tiết cho phép đào sâu, ví dụ danh sách khách hàng có Recency tăng bất thường.")
B("Bộ lọc (slicer) cho cụm khách hàng, kênh bán, thời gian đặt ở cùng một vị trí trên mọi trang.")
B("Một bảng màu thống nhất: mỗi cụm một màu cố định trên mọi biểu đồ. Màu nóng chỉ dùng cho chỉ số chưa đạt mục tiêu.")
P("Phần diễn giải phải nói được vì sao chọn từng KPI và từng biểu đồ, gắn với quyết định của người dùng. Đề yêu cầu bài viết tối đa 4 trang Word hoặc PDF kèm ảnh dashboard, vì vậy diễn giải cần ngắn và đi thẳng vào lý do.")

H2("15.5.3. Yêu cầu 3.3: Hai chỉ số cố tình không đưa vào")
P("Mục đích: chứng minh dashboard là kết quả của lựa chọn. Một chỉ số có sẵn trong dữ liệu nên bị loại khi rơi vào một trong các trường hợp sau, đối chiếu với các sai lầm KPI của Bài 9:")
B("Không gắn với quyết định nào của người dùng đã chọn.")
B("Trùng thông tin với một chỉ số đã có, làm người xem phải đọc hai lần cùng một ý.")
B("Không có ý nghĩa khi cộng gộp, ví dụ cộng các đại lượng khác đơn vị đo.")
B("Dễ gây hiểu sai, ví dụ chỉ số bị chi phối bởi vài giá trị cực đoan.")
B("Chất lượng dữ liệu nguồn thấp, không đủ tin cậy để ra quyết định.")
P("Mỗi chỉ số bị loại cần nêu tên, lý do và người dùng mất gì, được gì khi không thấy nó. Bài làm tốt cho thấy việc bỏ chỉ số giúp người dùng tập trung vào quyết định chính.")

# ------------------------------------------------------------------ 15.6
H1("15.6. Quy trình làm bài, sản phẩm nộp và tiêu chí đánh giá")
H2("15.6.1. Quy trình làm bài gợi ý")
CAP("Bảng 15.11. Phân bổ thời gian cho buổi thực hành")
TB([
    ["Giai đoạn", "Việc chính", "Thời lượng gợi ý"],
    ["1", "Đọc đề, xem dữ liệu, lập hồ sơ dữ liệu", "15 phút"],
    ["2", "Làm sạch, dựng mô hình, chốt doanh thu và số khiếu nại", "50 phút"],
    ["3", "Tạo bảng đặc trưng, phân cụm, đặt tên cụm", "50 phút"],
    ["4", "Phân tích người dùng, dựng dashboard, chọn chỉ số loại bỏ", "55 phút"],
    ["5", "Viết diễn giải, kiểm tra lại số liệu, đóng gói bài nộp", "20 phút"],
])
SRC()
H2("15.6.2. Sản phẩm nộp")
P("Một thư mục nén gồm: tệp .pbix; tệp code (Python, SPSS syntax hoặc các bước Power Query); tệp Word, PDF hoặc PowerPoint trả lời các câu hỏi. Nếu nộp Word hoặc PDF, tối đa 4 trang kể cả ảnh dashboard. Nhật ký làm sạch theo mẫu Bảng 15.6 có thể đặt ở phụ lục của tệp code.")
H2("15.6.3. Tiêu chí đánh giá")
P("Đề bài không công bố thang điểm chi tiết. Bảng 15.12 là thang điểm đề xuất, giảng viên điều chỉnh khi cần.")
CAP("Bảng 15.12. Thang điểm đề xuất")
TB([
    ["Yêu cầu", "Tiêu chí đạt", "Điểm"],
    ["1.1", "Mô hình hình sao đúng, quan hệ một-nhiều, không nhân đôi khiếu nại", "1,0"],
    ["1.2", "Nhật ký làm sạch đủ các nhóm lỗi, có số dòng, có lý do; phát hiện được bất thường", "1,5"],
    ["1.3", "Doanh thu tính đúng công thức, có đối chiếu trước và sau; số khiếu nại đủ 180 khách", "0,5"],
    ["2.1", "Ít nhất 5 đặc trưng có định nghĩa và lý do chọn, kiểm tra tương quan", "1,0"],
    ["2.2", "Có biến đổi và chuẩn hoá, so sánh nhiều K, tên cụm và hành động rõ ràng", "3,0"],
    ["3.1", "Mỗi nhóm người dùng gắn với quyết định cụ thể, tần suất, KPI", "1,0"],
    ["3.2", "Dashboard dùng kết quả phân cụm, bố cục phân cấp, diễn giải lựa chọn", "1,5"],
    ["3.3", "Hai chỉ số loại bỏ có lý do thuyết phục", "0,5"],
])
SRC("(Nguồn: Tác giả đề xuất)")

# ------------------------------------------------------------------ end
d.plain_heading("Tóm tắt bài học")
B("Làm sạch là bước phân tích đầu tiên, không phải việc phụ. Vài dòng sai có thể làm doanh thu lệch hàng chục phần trăm; nhật ký làm sạch là bằng chứng cho con số cuối.")
B("Mô hình hình sao đúng cần khoá duy nhất ở phía bảng chiều. Khi khoá không duy nhất, tạo bảng chiều trung gian thay vì chấp nhận quan hệ nhiều-nhiều.")
B("Bảng đặc trưng cấp khách hàng bắt đầu từ R, F, M và mở rộng bằng các đặc trưng gắn với câu hỏi kinh doanh như độ biến động đơn, khiếu nại, tỷ trọng FSC.")
B("K-means cần biến đổi log cho biến lệch, chuẩn hoá z-score, n_init từ 10 và random_state cố định.")
B("Chọn K kết hợp Elbow, Silhouette và khả năng đặt tên kinh doanh. Silhouette cao nhất chưa chắc là lời giải hữu ích nhất.")
B("Dashboard thiết kế ngược từ quyết định của người dùng. Loại bớt chỉ số là một phần của thiết kế.")

d.plain_heading("CÂU HỎI ÔN TẬP")
numbered("Vì sao quan hệ giữa bảng khiếu nại và bảng dòng đơn hàng qua MaDonHang làm sai số khiếu nại theo khách hàng? Nêu hai cách khắc phục.")
numbered("Một cột có ô trống ở 3% số dòng. Trình bày các bước anh/chị làm trước khi quyết định xoá, giữ hay điền giá trị cho các dòng này.")
numbered("Giải thích vì sao không thể phát hiện giá trị bất thường của SoLuong bằng một ngưỡng chung cho toàn bảng đơn hàng.")
numbered("Tính tay Silhouette của bốn điểm 2, 3, 9, 10 khi chia thành hai cụm {2, 3} và {9, 10}. So sánh với Ví dụ 15.2 và giải thích khác biệt.")
numbered("Vì sao nên lấy log trước khi chuẩn hoá các biến doanh thu và số đơn? Phép log có làm mất thông tin về khách hàng lớn không?")
numbered("Lời giải K = 6 có Silhouette cao hơn K = 5 nhưng hai trong sáu cụm khó đặt tên. Anh/chị chọn lời giải nào, lập luận ra sao trước ban giám đốc?")
numbered("Phân biệt dashboard chiến thuật và dashboard tác nghiệp cho cùng một công ty sản xuất. Cho ví dụ một KPI phù hợp với mỗi loại.")
numbered("Nêu ba tiêu chí để loại một chỉ số khỏi dashboard dù chỉ số đó có sẵn trong dữ liệu.")

d.plain_heading("TÀI LIỆU THAM KHẢO")
refs = [
    "Nguyễn Bình Minh An (2026). Đề cương bài giảng Phân tích dữ liệu Marketing, Bài 2, 3, 9 và 10. Khoa Kinh doanh số, Trường Kinh tế, Đại học Công nghiệp Hà Nội.",
    "Hair, J. F., Black, W. C., Babin, B. J. & Anderson, R. E. (2019). Multivariate Data Analysis (8th ed.). Cengage Learning.",
    "Kaufman, L. & Rousseeuw, P. J. (1990). Finding Groups in Data: An Introduction to Cluster Analysis. John Wiley & Sons.",
    "Rousseeuw, P. J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53-65.",
    "Ester, M., Kriegel, H.-P., Sander, J. & Xu, X. (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. Proceedings of KDD-96, 226-231.",
    "Tukey, J. W. (1977). Exploratory Data Analysis. Addison-Wesley.",
    "Jeffery, M. (2010). Data Driven Marketing: The 15 Metrics Everyone in Marketing Should Know. John Wiley & Sons.",
    "Few, S. (2013). Information Dashboard Design: Displaying Data for At-a-Glance Monitoring (2nd ed.). Analytics Press.",
    "Kimball, R. & Ross, M. (2013). The Data Warehouse Toolkit: The Definitive Guide to Dimensional Modeling (3rd ed.). John Wiley & Sons.",
    "scikit-learn developers. User Guide, mục 2.3 Clustering. https://scikit-learn.org/stable/modules/clustering.html",
    "IBM. K-Means Cluster Analysis. IBM SPSS Statistics documentation.",
    "Microsoft. Apply clustering techniques in Power BI. Microsoft Learn, Power BI documentation.",
]
for r in refs:
    numbered(r, "4")

out = SP + "/th_out/bai_15/Bai 15_Thuc hanh 5_ĐCBG.docx"
d.save(out)
from docx import Document as _D2
_doc = _D2(out)
for _p in _doc.paragraphs:
    _tx = _p.text.strip()
    if _tx.startswith(("Bảng 15.", "Ví dụ 15.", "15.")) or _tx.endswith(":") or _tx in ("Tóm tắt bài học", "CÂU HỎI ÔN TẬP", "TÀI LIỆU THAM KHẢO"):
        _p.paragraph_format.keep_with_next = True
_doc.save(out)
print("saved", out)
