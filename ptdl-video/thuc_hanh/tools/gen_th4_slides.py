import sys, os
W = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, f"{W}/tools")
from kits import Deck

OUT = f"{W}/th_out/bai_14"
k = Deck()

# Page jobs (một việc mỗi slide)
# 1 Bìa: tên bài
k.cover("Thực hành 4: Phân tích sản phẩm và chiến lược giá", "Phân tích dữ liệu Marketing, Bài 14")
# 2 CĐR: gắn buổi học với chuẩn đầu ra L1
k.table("CHUẨN ĐẦU RA VÀ MỤC TIÊU BÀI HỌC",
        [["Mã CĐR", "Nội dung chuẩn đầu ra của học phần", "Mức độ"],
         ["L1", "Ứng dụng kiến thức về thuật toán và thống kê vào phân tích dữ liệu, kết hợp kiến thức kinh tế, kinh doanh để đưa ra khuyến nghị về sản phẩm, khách hàng, nghiên cứu thị trường", "U"]],
        note="Buổi thực hành vận dụng Bài 3, 4, 5, 7 và 10 trên một bộ dữ liệu doanh nghiệp.")
# 3 Mục tiêu: năm việc sinh viên làm được sau buổi
k.bullets("Sau buổi học, sinh viên làm được năm việc", [
    "Đánh giá danh mục bằng Pareto, lợi nhuận gộp và vai trò cửa ngõ của từng gói",
    "Ước lượng part-worth, tầm quan trọng và WTP từ dữ liệu conjoint",
    "Xác định khoảng giá bằng Van Westendorp, mức giá tối đa doanh thu bằng Gabor-Granger",
    "Ước lượng độ co giãn từ dữ liệu bán hàng và tách ảnh hưởng mùa vụ",
    "Đánh giá lãi lỗ khuyến mãi bằng độ co giãn hoà vốn",
])
# 4 Agenda
k.bullets("AGENDA", [
    "14.1.  Ôn tập: danh mục, conjoint, khảo sát giá, co giãn, hoà vốn",
    "14.2.  Tình huống MOVA và sáu tệp dữ liệu",
    "14.3.  Phần 1: Phân tích danh mục sản phẩm",
    "14.4.  Phần 2: Conjoint cho MOVA Fit Premium",
    "14.5.  Phần 3: Phân tích giá và khuyến mãi",
    "14.6.  Phần 4: Khuyến nghị, quy trình, tiêu chí chấm",
])
# 5 Case mở đầu: ba câu hỏi của Ban giám đốc
k.bullets("CASE MỞ ĐẦU: Ba câu hỏi của Ban giám đốc MOVA", [
    "MOVA (doanh nghiệp hư cấu) có ứng dụng MOVA Fit và 14 câu lạc bộ, bán 17 gói dịch vụ",
    "Câu 1: cắt năm gói doanh thu thấp nhất, trong đó có gói APP01, có hợp lý không?",
    "Câu 2: MOVA Fit Premium có huấn luyện viên AI nên gồm gì, giá bao nhiêu, có bắt cam kết năm không?",
    "Câu 3: đợt giảm 35% gói Năm mỗi tháng 1 bán rất nhiều đơn. Chương trình có lãi không?",
    "Thảo luận: con số nào trong báo cáo hiện tại có thể đang đánh lừa Ban giám đốc?",
])
# 6 Thông tin chung: thời lượng và thang điểm
# ---------------- 14.1
k.section("14.1.  Ôn tập kiến thức lý thuyết trọng tâm")
# 8 Danh mục: doanh thu không phải đóng góp
k.table("Doanh thu cao chưa chắc đóng góp lợi nhuận cao", [
    ["Thước đo", "Cách tính", "Trả lời câu hỏi"],
    ["Tỷ trọng doanh thu", "Doanh thu gói ÷ tổng doanh thu", "Gói nào mang nhiều tiền nhất?"],
    ["Biên lợi nhuận gộp", "(Doanh thu − chi phí biến đổi) ÷ doanh thu", "Mỗi đồng doanh thu để lại bao nhiêu?"],
    ["Chi tiêu của nhóm khách vào bằng gói", "Tổng chi tiêu của khách có gói đầu tiên là gói đó", "Gói này dẫn khách tới đâu?"],
], note="Quy tắc 80/20 là quan sát thực nghiệm, không phải quy luật (Bài 3, mục 3.1.1; Bài 5, mục 5.1).")
# 9 Conjoint: từ hệ số tới tầm quan trọng
k.bullets("Conjoint: hệ số biến giả là part-worth so với mức tham chiếu", [
    "Thuộc tính k mức cần k − 1 biến giả; đủ k biến sẽ gây đa cộng tuyến hoàn hảo",
    "Part-worth (giá trị bộ phận) của mức tham chiếu bằng 0",
    "Biên độ = part-worth lớn nhất − nhỏ nhất trong một thuộc tính",
    "Tầm quan trọng (%) = biên độ ÷ tổng biên độ × 100",
    "Chênh lệch nhỏ hơn sai số chuẩn thì không xếp hạng hai thuộc tính",
    "Nguồn: Bài 4, mục 4.2; Bài 7, mục 7.3.2",
])
# 10 WTP và logit, ví dụ minh hoạ
k.table("Quy hữu dụng ra tiền: ví dụ minh hoạ", [
    ["Bước", "Công thức", "Ví dụ minh hoạ"],
    ["Kiểm tra tuyến tính", "So hai mức giảm hữu dụng liên tiếp", "1,0 và 1,1: gần tuyến tính"],
    ["Giá trị 1 đơn vị hữu dụng", "Chênh giá hai mức ngoài ÷ biên độ giá", "100.000 ÷ 2,1 ≈ 47.600 đ"],
    ["WTP một tính năng", "Hệ số × giá trị 1 đơn vị", "0,8 × 47.600 ≈ 38.100 đ"],
    ["Thị phần ưu tiên", "exp(U_i) ÷ Σ exp(U)", "U = 2,0; 2,5; 3,0 → 18,6%; 30,7%; 50,6%"],
], note="Hệ số là điểm hấp dẫn, không phải tiền. Thị phần ưu tiên chỉ dùng để xếp hạng.")
# 11 Van Westendorp và Gabor-Granger
k.table("Van Westendorp cho khoảng giá, Gabor-Granger cho đỉnh doanh thu", [
    ["Điểm", "Giao của hai đường", "Ý nghĩa"],
    ["PMC", "Quá rẻ × Đắt", "Giới hạn dưới"],
    ["OPP", "Quá rẻ × Quá đắt", "Giá tham khảo, ít người từ chối nhất"],
    ["IPP", "Rẻ × Đắt", "Số người thấy rẻ bằng số người thấy đắt"],
    ["PME", "Rẻ × Quá đắt", "Giới hạn trên"],
    ["Gabor-Granger", "Giá × tỷ lệ chấp nhận", "Đỉnh doanh thu nằm quanh |E| = 1"],
], note="Phiếu hợp lệ: Quá rẻ < Rẻ < Đắt < Quá đắt. Hai đường Rẻ và Quá rẻ cộng dồn giảm.")
# 12 Co giãn và biến bỏ sót
k.bullets("Bỏ sót mùa vụ làm độ co giãn bị phóng đại", [
    "Hồi quy log-log: hệ số của ln(Giá) là độ co giãn (Bài 7, mục 7.3.2)",
    "Giảm giá sâu đúng mùa cao điểm: mức tăng do mùa vụ bị gán cho giá",
    "Cách xử lý: thêm biến giả mùa vụ hoặc sự kiện (Bài 7, mục 7.2.1)",
    "Kiểm chứng độc lập: so cùng tháng ở hai năm có mức giảm khác nhau",
    "Độ co giãn cung (arc) giữa hai điểm: %ΔQ ÷ %ΔP, tính theo điểm giữa",
])
# 13 Hoà vốn khuyến mãi
k.table("Khuyến mãi chỉ có lãi khi |E| vượt ngưỡng hoà vốn", [
    ["Đại lượng", "Công thức", "Ví dụ minh hoạ: P = 1 triệu, C = 400 nghìn, d = 20%"],
    ["Hệ số sản lượng", "k = (1 − d)^(−|E|)", "|E| = 1,2 → k ≈ 1,307"],
    ["Doanh thu thay đổi", "k × (1 − d) − 1", "+4,6%"],
    ["Lợi nhuận gộp thay đổi", "k × [P(1 − d) − C] ÷ (P − C) − 1", "−12,9%"],
    ["|E| hoà vốn", "ln[(P − C) ÷ (P(1 − d) − C)] ÷ ln[1 ÷ (1 − d)]", "≈ 1,82"],
    ["Xấp xỉ khi d nhỏ", "1 ÷ biên lợi nhuận gộp", "1 ÷ 0,6 ≈ 1,67"],
], note="Doanh thu tăng không có nghĩa lợi nhuận tăng.")

# ---------------- 14.2
k.section("14.2.  Tình huống MOVA và dữ liệu")
k.table("Sáu tệp dữ liệu, kỳ 11/2024 đến 10/2026", [
    ["Tệp", "Số dòng", "Một dòng là", "Dùng cho"],
    ["01_DanhMucGoi", "17", "Một gói dịch vụ", "Phần 1, 3"],
    ["02_KhachHang", "10.500", "Một khách hàng", "Phần 1"],
    ["03_GiaoDich", "22.778", "Một giao dịch", "Phần 1, 3"],
    ["04_TheConjoint", "12", "Một thẻ sản phẩm giả định", "Phần 2"],
    ["05_ChamDiemConjoint", "3.840", "Một lượt chấm 1 đến 10", "Phần 2"],
    ["06_KhaoSatGia", "320", "Một đáp viên khảo sát giá", "Phần 2, 3"],
])
# ---------------- 14.3
k.section("14.3.  Phần 1: Phân tích danh mục sản phẩm")
k.bullets("Câu 1.1 đến 1.3: từ Pareto doanh thu tới lợi nhuận gộp", [
    "PivotTable: MaGoi ở Rows, Sum GiaBan_VND và Count MaGiaoDich ở Values",
    "Thêm tỷ trọng, luỹ kế; đếm số gói tới mốc 80% rồi chia cho 17",
    "Lợi nhuận gộp = Tổng giá bán − Số giao dịch × ChiPhiPhucVu_CaGoi_VND",
    "Xếp hạng lại bằng RANK.EQ; tìm ba gói tụt hạng nhiều nhất và điểm chung",
    "Theo nhóm: cộng doanh thu, cộng lợi nhuận rồi mới chia",
    "Doanh thu dùng GiaBan_VND; kết quả là lợi nhuận gộp, chưa trừ chi phí cố định",
])
k.bullets("Câu 1.4: kiểm tra vai trò cửa ngõ trước khi cắt gói App", [
    "Tra nhóm của GoiDauTien sang bảng khách hàng",
    "Đánh dấu khách từng mua CMB12 bằng COUNTIFS trên bảng giao dịch",
    "Tính tỷ lệ khách vào bằng App ở nhóm có và không có CMB12",
    "Cộng chi tiêu của khách vào bằng App, so với tổng doanh thu công ty",
    "So ba con số với doanh thu của riêng nhóm App rồi mới kết luận",
    "Nếu giữ gói, đề xuất cách khác để gọn danh mục",
])

# ---------------- 14.4
k.section("14.4.  Phần 2: Conjoint cho MOVA Fit Premium")
k.table("Câu 2.1: năm biến giả cho bốn thuộc tính", [
    ["Thuộc tính", "Số mức", "Biến giả", "Mức tham chiếu gợi ý"],
    ["Thời hạn cam kết", "2", "CamKetNam", "1 tháng"],
    ["Phạm vi phòng tập", "2", "ToanHeThong", "1 cơ sở"],
    ["Huấn luyện viên AI", "2", "CoAI", "Không"],
    ["Giá mỗi tháng", "3", "Gia690, Gia890", "490.000 đ"],
], note="Ghép tệp 05 với 04 theo MaThe trước. Chọn mức tham chiếu khác vẫn đúng nếu diễn giải nhất quán.")
k.bullets("Câu 2.2 và 2.3: hồi quy rồi tính tầm quan trọng", [
    "Excel: Data Analysis, Regression; năm cột X phải nằm liền nhau",
    "SPSS: Analyze, Regression, Linear; đọc cột B và R Square",
    "Python: smf.ols('DiemHapDan ~ CamKetNam + ToanHeThong + CoAI + Gia690 + Gia890')",
    "Kiểm tra dấu từng hệ số; hệ số trái dấu thường do gán sai biến giả",
    "Tầm quan trọng tính từ biên độ, có tính mức tham chiếu bằng 0",
])
k.bullets("Câu 2.4 và 2.5: quy ra tiền, rồi tách theo thu nhập", [
    "Bước bắt buộc: so hai mức giảm hữu dụng của giá; lệch nhiều thì dừng",
    "WTP cho AI và cho toàn hệ thống = hệ số × giá trị 1 đơn vị",
    "Mức giảm để bù cam kết năm = |hệ số cam kết| × giá trị 1 đơn vị",
    "So mức đó với mức giảm 35% gói Năm, quy về đồng mỗi tháng",
    "Câu 2.5: Split File theo thu nhập từ 20 triệu; so WTP của AI giữa hai nhóm",
])

# ---------------- 14.5
k.section("14.5.  Phần 3: Phân tích giá và khuyến mãi")
k.bullets("Câu 3.1 và 3.2: khoảng giá và đường cầu khảo sát", [
    "Lọc phiếu: AND(QuaRe < Re; Re < Dat; Dat < QuaDat); ghi số phiếu bị loại",
    "Lưới giá 100.000 đến 1.900.000, bước 10.000; COUNTIF \"<=\" hoặc \">=\"",
    "Điểm giao: nơi chênh lệch hai đường đổi dấu; ghi cả tỷ lệ tại điểm giao",
    "Gabor-Granger: tỷ lệ mua = AVERAGE cột GG; chỉ số doanh thu = giá × tỷ lệ",
    "Tính co giãn cung từng cặp giá liền kề; tìm nơi |E| vượt 1",
])
k.table("Câu 3.3: so hai mô hình co giãn trên 48 dòng", [
    ["Mô hình", "Biến độc lập", "Cần ghi"],
    ["Mô hình 1", "ln(Giá), biến giả CMB12", "Hệ số ln(Giá), sai số chuẩn, R²"],
    ["Mô hình 2", "Thêm biến giả tháng 1", "Hệ số mới; so với Mô hình 1"],
    ["Kiểm chứng cặp tháng", "Cùng tháng, năm 0% và năm 25%", "Trung bình, trung vị các cặp"],
], note="Chỉ xét CLB12 và CMB12. Giải thích chiều sai lệch bằng biến bỏ sót, không kết luận từ một cặp.")
k.bullets("Câu 3.4 và 3.5: khuyến mãi có lãi không, khảo sát có đáng tin không", [
    "Tính biên CMB12 khi bán đúng giá và khi giảm 35%",
    "Dùng |E| của câu 3.3 để tính thay đổi doanh thu và lợi nhuận gộp",
    "So |E| ước lượng với |E| hoà vốn đầy đủ và ngưỡng xấp xỉ 1 ÷ biên",
    "Từ sổ sách: tháng 1 gấp bao nhiêu lần tháng thường về số đơn và về lãi gộp",
    "Câu 3.5: GiaThang = GiaBan ÷ ThoiHan_Thang; lấy MAXIFS mỗi khách",
    "So tỷ lệ \"nói sẽ mua\" với tỷ lệ \"đã từng trả\" ở cùng mức giá",
])

# ---------------- 14.6
k.section("14.6.  Phần 4: Khuyến nghị và trình bày")
k.bullets("Câu 4.1 đến 4.3: chọn phương án theo lợi nhuận, không theo số khách", [
    "Hữu dụng phương án = hằng số + hệ số các mức có mặt",
    "Xếp bốn phương án theo thị phần, chỉ số doanh thu, chỉ số lãi gộp",
    "Nêu tiêu chí chọn và rủi ro ăn mòn gói hiện có",
    "Mỗi khuyến nghị: việc cần làm, con số căn cứ, tác động tài chính",
    "Hai hạn chế, mỗi hạn chế gắn một con số và cách khắc phục",
    "Không nhân thị phần ưu tiên với quy mô thị trường",
])
k.table("Quy trình thực hiện trong 210 phút", [
    ["Thời gian", "Việc", "Sản phẩm trung gian"],
    ["0 đến 10 phút", "Đọc bối cảnh, chia việc", "Bảng phân công"],
    ["10 đến 50 phút", "Phần 1", "Sheet 1.1 đến 1.4"],
    ["50 đến 115 phút", "Phần 2", "Biến giả, hồi quy, WTP"],
    ["115 đến 180 phút", "Phần 3", "Đồ thị VW, bảng co giãn, hoà vốn"],
    ["180 đến 210 phút", "Phần 4", "Bảng mô phỏng, tệp trình bày"],
])
k.table("Lỗi thường gặp và cách tránh", [
    ["Lỗi", "Hậu quả", "Cách tránh"],
    ["Tạo đủ k biến giả", "Hồi quy suy biến hoặc tự loại biến", "Luôn dùng k − 1"],
    ["Đọc hệ số như tiền", "Định giá tính năng quá cao", "Quy đổi qua thuộc tính giá"],
    ["Trung bình các biên", "Sai biên của nhóm", "Cộng tổng rồi mới chia"],
    ["Gộp cả 17 gói ở câu 3.3", "Lẫn chênh giá giữa các gói", "Chỉ lọc CLB12, CMB12"],
    ["Quên quy giá về tháng", "Tỷ lệ ở câu 3.5 sai", "Chia cho ThoiHan_Thang"],
    ["Nhầm chiều cộng dồn VW", "PMC lớn hơn PME", "Rẻ, Quá rẻ cộng dồn giảm"],
])
k.table("Sản phẩm nộp và tiêu chí chấm", [
    ["Phần", "Điểm", "Tiêu chí chính"],
    ["1. Danh mục", "2,0", "Kiểm tra vai trò cửa ngõ trước khi kết luận cắt gói"],
    ["2. Conjoint", "3,0", "Mã hoá đúng, kiểm tra tuyến tính trước khi quy tiền"],
    ["3. Giá", "3,0", "Tách mùa vụ khỏi giá, so với ngưỡng hoà vốn"],
    ["4. Khuyến nghị", "2,0", "Đủ việc cần làm, căn cứ số, tác động tài chính"],
], note="Nộp TH4_<Mã lớp>_Nhom<số>.xlsx, mỗi câu một sheet, giữ công thức và bảng hồi quy gốc, kèm tệp trình bày tối đa 8 trang.")
k.bullets("Tóm tắt", [
    "Doanh thu của một gói chưa đủ để cắt; xem lãi gộp và khách mà gói dẫn vào",
    "Tầm quan trọng tính từ biên độ; WTP chỉ tính khi hữu dụng của giá gần tuyến tính",
    "Trung bình WTP có thể che khác biệt giữa các phân khúc",
    "Bỏ sót mùa vụ làm độ co giãn bị phóng đại",
    "Khuyến mãi có lãi khi |E| vượt ngưỡng hoà vốn",
    "Lời khai thổi phồng tỷ lệ mua; hiệu chỉnh bằng hành vi thật",
])
k.bullets("Câu hỏi thảo luận", [
    "Gói bán nhiều giao dịch nhất của MOVA là gói nào, và điều đó gợi ý gì?",
    "Hệ số của AI có đơn vị gì? Làm sao đổi sang đồng?",
    "Tháng 1 bán gấp nhiều lần tháng thường. Lợi nhuận gộp có gấp đúng chừng đó không?",
    "Khi khảo sát và dữ liệu giao dịch mâu thuẫn, anh/chị lập kế hoạch doanh thu theo nguồn nào?",
])

k.save(f"{OUT}/Bai 14_Thuc hanh 4_Slides.pptx")
print("ok")
