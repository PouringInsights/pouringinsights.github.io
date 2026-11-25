import sys, os
W = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, W + "/tools")
from kits import Deck

OUT = W + "/th_out/bai_13"
os.makedirs(OUT, exist_ok=True)
k = Deck()
Bl, S = k.bullets, k.section
import re
from pptx.enum.text import PP_ALIGN
from pptx.util import Emu
NUM = re.compile(r"^[≈~]?\s*[\d.,]+\s*(đ|%|tháng|dòng)?(\s*\(.*\))?$")

def Tb(title, rows, note=None):
    s = k.table(title, rows, note=note)
    gf = next(sh for sh in s.shapes if sh.has_table)
    tbl = gf.table
    n = len(rows[0])
    L = [max(len(str(r[i])) for r in rows) for i in range(n)]
    w = [max(0.12, x / sum(L)) for x in L]
    tot = sum(w); width = sum(c.width for c in tbl.columns)
    for c, x in zip(tbl.columns, w): c.width = Emu(int(width * x / tot))
    for ci in range(n):
        if all(NUM.match(str(r[ci]).strip()) for r in rows[1:]):
            for ri in range(1, len(rows)):
                for p in tbl.cell(ri, ci).text_frame.paragraphs: p.alignment = PP_ALIGN.RIGHT
    notes = [sh for sh in s.shapes if sh.has_text_frame and sh is not gf and sh.top > gf.top]
    for sh in notes:
        sh.top = Emu(gf.top + len(rows) * 457200 + 320000)
    return s

# Page jobs (one line each) are written as comments above every slide.

# 1. Mở bài: tên buổi thực hành
k.cover("Thực hành 3: Giá trị vòng đời khách hàng, dự báo rời bỏ và phân khúc tâm lý",
        "Phân tích dữ liệu Marketing – Bài 13")

# 2. Người học biết sẽ làm được gì sau buổi học
Bl("Sau buổi thực hành, sinh viên làm được năm việc", [
    "Làm sạch dữ liệu giao dịch, tính và chấm điểm RFM, gán nhãn phân khúc",
    "Tính CLV, LTV:CAC theo phân khúc và theo kênh, đưa ra khuyến nghị ngân sách",
    "Dựng bảng cohort giữ chân và đọc đúng xu hướng",
    "Dự báo rời bỏ bằng hồi quy logistic, chọn ngưỡng cắt có lập luận",
    "Chạy EFA, phân cụm theo điểm nhân tố, lập ma trận ưu tiên can thiệp",
    "CĐR L1, mức U: vận dụng thống kê và thuật toán để khuyến nghị về khách hàng",
])

# 3. Lộ trình buổi học
Bl("AGENDA", [
    "13.1  Ôn tập: RFM, CLV, cohort, logistic, EFA, K-means",
    "13.2  Tình huống EDUGO và bộ dữ liệu",
    "13.3  Hướng dẫn sáu yêu cầu của đề",
    "13.4  Lỗi thường gặp, sản phẩm nộp và tiêu chí chấm",
])

# 4. Case mở đầu: vì sao doanh thu kỳ hiện tại không đủ để quyết định ngân sách
Bl("Case EDUGO: tăng hay cắt ngân sách quảng cáo?", [
    "EDUGO bán khoá học tiếng Anh trực tuyến, khoảng 3.000 người học, doanh thu 18 tháng gần 9,5 tỷ đồng",
    "Giám đốc marketing muốn tăng gấp đôi quảng cáo vì doanh thu vẫn tăng",
    "Giám đốc tài chính phản đối vì càng chạy quảng cáo càng lỗ",
    "Cả hai chỉ nhìn doanh thu của kỳ hiện tại",
    "Thảo luận: cần con số nào để biết một người học mới có lãi hay không?",
])

# 5. Ba câu hỏi quản trị nối với sáu yêu cầu và bài lý thuyết
Tb("Ba câu hỏi quản trị, sáu yêu cầu của đề", [
    ["Câu hỏi", "Yêu cầu", "Phương pháp", "Ôn ở"],
    ["Một người học đáng giá bao nhiêu?", "1, 2, 3", "RFM, CLV, LTV:CAC, cohort", "Bài 3, Bài 5"],
    ["Ai sắp rời bỏ?", "4", "Hồi quy logistic", "Bài 5, Bài 7"],
    ["Người học ở lại vì điều gì?", "5", "EFA, Cronbach's Alpha", "Bài 6, Bài 8"],
    ["Giữ ai, giữ bằng cách nào?", "6", "K-means, ma trận ưu tiên", "Bài 3, Bài 6"],
], note="Tổng 10 điểm. Yêu cầu 2 nặng nhất với 2,5 điểm.")

S("13.1.  Ôn tập kiến thức lý thuyết trọng tâm")

# 7. RFM: định nghĩa và cách chấm điểm
Bl("RFM: ba con số từ dữ liệu hoá đơn", [
    "R: số ngày từ lần mua gần nhất tới ngày phân tích 30/06/2025",
    "F: số đơn hợp lệ. M: tổng giá trị đơn hợp lệ",
    "Chấm điểm 1 đến 5 theo ngũ phân vị; R nhỏ nhất được 5 điểm",
    "F trùng giá trị nhiều: xếp hạng trước, rồi mới cắt nhóm bằng qcut",
    "Quy tắc gán nhãn do nhóm tự viết, phải phủ hết mọi tổ hợp điểm",
])

# 8. CLV rút gọn và quy đổi churn
Bl("CLV rút gọn: tử số và mẫu số phải cùng kỳ", [
    "CLV = ARPU tháng × biên lợi nhuận gộp ÷ tỷ lệ rời bỏ tháng",
    "Đề cho nhãn rời bỏ theo quý, ARPU tính theo tháng",
    "Quy đổi: tỷ lệ rời bỏ tháng = 1 − (1 − tỷ lệ rời bỏ quý)^(1/3)",
    "Giả định ẩn: ARPU và tỷ lệ rời bỏ không đổi, không chiết khấu",
    "Customer equity = tổng (số khách × CLV) qua các phân khúc",
])

# 9. Ví dụ số: dùng sai tỷ lệ quý làm CLV thấp ba lần
Tb("Dùng thẳng tỷ lệ quý làm CLV thấp gần ba lần", [
    ["Bước", "Quy về tháng (đúng)", "Dùng tỷ lệ quý (sai)"],
    ["Lợi nhuận gộp/tháng", "204.000 đ", "204.000 đ"],
    ["Mẫu số", "0,0717", "0,20"],
    ["Số tháng kỳ vọng", "14,0 tháng", "5 tháng"],
    ["CLV", "2.846.000 đ", "1.020.000 đ"],
    ["LTV:CAC (CAC 600.000 đ)", "4,74", "1,70"],
], note="Ví dụ minh hoạ: ARPU 300.000 đ/tháng, biên 68%, rời bỏ quý 20%.")

# 10. Ngưỡng LTV:CAC
Tb("LTV:CAC cho biết mỗi đồng thu hút khách mang về bao nhiêu", [
    ["LTV:CAC", "Ý nghĩa", "Hành động"],
    ["Dưới 1", "Mỗi khách mới làm doanh nghiệp lỗ", "Dừng mở rộng kênh, sửa sản phẩm hoặc giá"],
    ["1 đến 3", "Có lãi nhưng mỏng", "Giảm CAC hoặc tăng giữ chân"],
    ["Khoảng 3", "Ngưỡng lành mạnh", "Duy trì và tối ưu dần"],
    ["Trên 5", "Có thể đang đầu tư quá ít", "Cân nhắc tăng ngân sách kênh đó"],
], note="Nguồn: Bài 5, mục 5.1.3.")

# 11. Cohort: hai điểm kỹ thuật
Bl("Cohort: hai điểm kỹ thuật quyết định kết luận", [
    "Mỗi hàng là một cohort theo quý gia nhập, mỗi cột là tháng thứ k",
    "Tháng thứ k = số ngày từ ngày gia nhập chia 30, lấy phần nguyên",
    "Tháng lịch xếp sai: gia nhập 29/03, mua 03/04 bị tính là tháng 1",
    "Ô chưa quan sát đủ để trống, không ghi 0%",
    "Ghi 0% làm đường cohort mới lao dốc giả và đảo ngược kết luận",
])

# 12. Đánh giá mô hình phân loại
Tb("Bốn chỉ số đánh giá mô hình rời bỏ", [
    ["Chỉ số", "Công thức", "Trả lời câu hỏi"],
    ["Precision", "TP ÷ (TP + FP)", "Người bị cảnh báo có thật sự rời bỏ?"],
    ["Recall", "TP ÷ (TP + FN)", "Bắt được bao nhiêu người rời bỏ?"],
    ["Accuracy", "(TP + TN) ÷ tổng", "So với mô hình \"không ai rời bỏ\""],
    ["AUC", "Diện tích dưới ROC", "Xếp hạng rủi ro tốt đến đâu"],
], note="AUC 0,7 đến 0,8 chấp nhận được, 0,8 đến 0,9 tốt (Bài 7, mục 7.4.3).")

# 13. EFA: ngưỡng từng bước
Tb("EFA sáu bước: ngưỡng phải đạt", [
    ["Bước", "Chỉ số", "Ngưỡng"],
    ["Điều kiện", "KMO; Bartlett", "KMO ≥ 0,6; p < 0,05"],
    ["Số nhân tố", "Eigenvalue; Scree Plot", "Eigenvalue > 1; điểm gãy"],
    ["Xoay", "Varimax", "Theo yêu cầu đề"],
    ["Lọc biến", "Communality; hệ số tải", "≥ 0,5; không tải > 0,4 lên nhân tố thứ hai"],
    ["Kết quả", "Phương sai tích luỹ", "≥ 50%"],
    ["Độ tin cậy", "Cronbach's Alpha", "> 0,7 cho từng nhân tố"],
], note="Nguồn: Bài 6, mục 6.2; Hair và cộng sự (2019).")

# 14. K-means trên điểm nhân tố và ma trận ưu tiên
Bl("Phân cụm tâm lý và ma trận ưu tiên", [
    "K-means dùng khoảng cách, nên đầu vào phải cùng thang đo",
    "Silhouette s(i) = (b − a) ÷ max(a, b), từ −1 đến 1; chọn K cao nhất",
    "Dùng điểm nhân tố: không đếm trùng câu hỏi tương quan, đã chuẩn hoá",
    "Giá trị có thể mất = tổng CLV × xác suất rời bỏ trong mỗi ô",
    "Ưu tiên theo giá trị có thể mất, không theo xác suất rời bỏ",
])

S("13.2.  Tình huống EDUGO và bộ dữ liệu")

# 16. Các tệp dữ liệu
Tb("Bốn tệp dữ liệu nối với nhau qua MaKH", [
    ["Tệp", "Quy mô", "Nội dung", "Yêu cầu"],
    ["EDUGO_khach_hang", "3.000 dòng", "Hồ sơ, kênh, CAC, hành vi 30 ngày, nhãn rời bỏ", "1, 2, 4, 6"],
    ["EDUGO_giao_dich", "12.975 dòng", "Mã đơn, ngày mua, gói, giá trị, kênh mua", "1, 2, 3"],
    ["EDUGO_khao_sat", "600 dòng", "17 câu Likert 1 đến 5 về động cơ học", "5, 6"],
    ["EDUGO_tu_dien_bien", "17 dòng", "Nội dung câu Q01 đến Q17", "5"],
], note="Dữ liệu mô phỏng. Có lỗi cài sẵn; đề không nêu vị trí, nhóm phải tự phát hiện.")

# 17. Giả định đề cho trước
Tb("Giả định đề cho trước", [
    ["Giả định", "Giá trị"],
    ["Ngày phân tích", "30/06/2025"],
    ["Kỳ giao dịch", "01/01/2024 đến 30/06/2025, 18 tháng"],
    ["Biên lợi nhuận gộp", "68%"],
    ["Rời bỏ", "Không có giao dịch trong quý III/2025 (cột RoiBo_Quy3)"],
    ["Ngưỡng LTV:CAC", "Dưới 1 là lỗ; khoảng 3 là lành mạnh"],
])

S("13.3.  Hướng dẫn thực hiện sáu yêu cầu")

# 19. Quy trình tổng
Tb("Quy trình thực hiện", [
    ["Bước", "Việc chính", "Đầu ra dùng cho"],
    ["1. Làm sạch, RFM", "Nhật ký lỗi; bảng R, F, M", "Yêu cầu 2, 3, 4"],
    ["2. Unit economics", "CLV, LTV:CAC theo phân khúc và kênh", "Yêu cầu 6"],
    ["3. Cohort", "Ma trận giữ chân đã che ô", "Kết luận xu hướng"],
    ["4. Mô hình rời bỏ", "Xác suất rời bỏ từng người", "Yêu cầu 6"],
    ["5. EFA", "Nhân tố có tên, Alpha", "Yêu cầu 6"],
    ["6. Ghép", "Cụm, ma trận bốn ô, ba thông điệp", "Báo cáo cuối"],
])

# 20. Yêu cầu 1: danh mục kiểm tra
Bl("Yêu cầu 1: rà lỗi trước khi tính bất cứ thứ gì", [
    "Đơn trùng: duplicated trên MaDonHang, so với trùng toàn dòng",
    "Giá trị bất thường: lọc GiaTri ≤ 0, quyết định loại hay trừ vào M",
    "Logic ngày: NgayGiaNhap so với ngày mua đầu tiên của cùng MaKH",
    "Giá trị thiếu: isna().sum() trên cả ba tệp; điền trung vị, không xoá dòng",
    "Ghi nhật ký: cách phát hiện, số bản ghi, cách xử lý, lý do",
])

# 21. Yêu cầu 1: tính RFM
Bl("Yêu cầu 1: tính R, F, M bằng groupby", [
    "Đọc ngày với format='%d/%m/%Y', không để pandas tự đoán",
    "groupby('MaKH'): max(NgayMua), nunique(MaDonHang), sum(GiaTri)",
    "R = 30/06/2025 trừ lần mua cuối, tính bằng ngày",
    "Người không còn giao dịch hợp lệ: nêu rõ quy ước gán hoặc loại",
    "Thống kê mô tả: báo cả trung bình và trung vị vì F, M lệch phải",
])

# 22. Yêu cầu 2
Bl("Yêu cầu 2: bảng unit economics", [
    "Rời bỏ quý = trung bình RoiBo_Quy3 trong nhóm; quy về tháng",
    "ARPU tháng: M chia số tháng gắn bó; nêu rõ mẫu số đã chọn",
    "CLV = ARPU × 0,68 ÷ rời bỏ tháng; LTV:CAC = CLV ÷ CAC trung bình",
    "Phân khúc LTV:CAC dưới 1: nói rõ hệ quả lỗ trên mỗi khách mới",
    "Theo kênh: tách chênh lệch do CLV và do CAC rồi mới khuyến nghị",
])

# 23. Yêu cầu 3
Bl("Yêu cầu 3: cohort theo quý gia nhập", [
    "Cohort = NgayGiaNhap đã sửa, to_period('Q')",
    "Thang = (NgayMua − NgayGiaNhap).days // 30",
    "Tỷ lệ = số MaKH khác nhau có giao dịch ÷ cỡ cohort",
    "Che ô khi ngày cuối quý + (k + 1) × 30 ngày vượt 30/06/2025",
    "So các cohort tại cùng mốc tháng, nêu chênh lệch bằng điểm phần trăm",
])

# 24. Yêu cầu 4: dựng mô hình
Bl("Yêu cầu 4: dựng mô hình rời bỏ", [
    "Đầu vào: năm biến hành vi và R, F, M; mục tiêu RoiBo_Quy3",
    "train_test_split 70/30, stratify=y, ghi random_state",
    "StandardScaler fit trên tập huấn luyện, rồi mới transform tập kiểm tra",
    "LogisticRegression; báo AUC, ROC, ma trận nhầm lẫn trên tập kiểm tra",
    "Ba biến mạnh nhất theo |hệ số chuẩn hoá|, diễn giải dấu theo kinh doanh",
])

# 25. Yêu cầu 4: ngưỡng là quyết định kinh doanh (ví dụ minh hoạ)
Tb("Ngưỡng cắt là quyết định kinh doanh", [
    ["Ngưỡng", "Số bị cảnh báo", "Precision", "Recall", "Hợp với"],
    ["Thấp", "Nhiều", "Thấp", "Cao", "Ưu đãi rẻ: thông báo đẩy"],
    ["Trung bình", "Vừa", "Vừa", "Vừa", "Email kèm mã"],
    ["Cao", "Ít", "Cao", "Thấp", "Ưu đãi đắt: gọi điện, tặng tháng học"],
], note="Báo ít nhất năm ngưỡng. So accuracy với mô hình \"không ai rời bỏ\" = 1 − tỷ lệ rời bỏ.")

# 26. Yêu cầu 5
Bl("Yêu cầu 5: EFA trên 17 câu khảo sát", [
    "Điền giá trị thiếu trước; chạy KMO và Bartlett",
    "Python: factor_analyzer, method='principal', rotation='varimax'",
    "SPSS: Analyze > Dimension Reduction > Factor, ẩn hệ số dưới 0,3",
    "Lọc biến theo cả communality và cross-loading; loại từng biến, chạy lại",
    "Đặt tên theo nội dung biến tải mạnh; Alpha cho từng nhân tố",
])

# 27. Yêu cầu 6
Bl("Yêu cầu 6: ghép giá trị với động cơ", [
    "Điểm nhân tố từ EFA cuối; KMeans K = 2 đến 6, chọn theo Silhouette",
    "Chân dung cụm theo điểm nhân tố trung bình, đặt tên theo chiều nổi bật",
    "Nối CLV, xác suất rời bỏ, cụm cho 600 người; chia bốn ô theo ngưỡng đã nêu",
    "Ô ưu tiên số một: theo giá trị có thể mất",
    "Ba thông điệp cho ba cụm đông nhất: nội dung, kênh, chi phí, chỉ số đo",
])

# 28. Lỗi thường gặp
Tb("Lỗi thường gặp", [
    ["Lỗi", "Hậu quả", "Cách tránh"],
    ["Không loại đơn trùng", "F, M tăng giả, sai phân khúc", "Kiểm tra MaDonHang trước"],
    ["Dùng rời bỏ quý làm mẫu số", "CLV thấp gần ba lần", "Quy đổi về tháng"],
    ["Tính tháng theo lịch", "Tháng 0 dưới 100%", "Số ngày chia 30"],
    ["Ghi 0% cho ô chưa quan sát", "Kết luận xu hướng ngược", "Để trống NaN"],
    ["Đánh giá trên tập huấn luyện", "AUC đẹp giả", "Chỉ báo tập kiểm tra"],
    ["Chỉ xét communality", "Sót biến tải chéo", "Xét cả cross-loading"],
    ["Cùng một mã giảm giá cho mọi cụm", "Tốn tiền, sai động cơ", "Thông điệp theo cụm"],
])

S("13.4.  Sản phẩm nộp và tiêu chí chấm")

# 30. Rubric
Tb("Sản phẩm nộp và tiêu chí chấm", [
    ["Yêu cầu", "Điểm", "Tiêu chí chính"],
    ["1. Làm sạch, RFM", "1,5", "Nhật ký lỗi đủ bốn cột; quy ước cho người không giao dịch"],
    ["2. CLV, LTV:CAC", "2,5", "Quy đổi rời bỏ đúng; giải thích LTV:CAC < 1; khuyến nghị kênh"],
    ["3. Cohort", "1,0", "Che ô chưa quan sát; kết luận có số"],
    ["4. Rời bỏ", "2,0", "AUC tập kiểm tra; năm ngưỡng; so mô hình ngây thơ"],
    ["5. EFA", "2,0", "KMO, Bartlett; lý do loại biến; tên nhân tố; Alpha"],
    ["6. Ghép", "1,0", "Silhouette; ma trận bốn ô; ba thông điệp đủ bốn phần"],
], note="Nộp: báo cáo ≤ 20 trang, mã nguồn chạy lại được, một trang tóm tắt cho ban giám đốc.")

# 31. Tóm tắt
Bl("Tóm tắt", [
    "Làm sạch dữ liệu trước; lỗi ở bước này lan sang mọi kết quả",
    "CLV cần tử số, mẫu số cùng kỳ; LTV:CAC dưới 1 là lỗ trên mỗi khách mới",
    "Cohort tính tháng theo ngày và để trống ô chưa quan sát đủ",
    "Mô hình rời bỏ đánh giá trên tập kiểm tra; ngưỡng do chi phí can thiệp quyết định",
    "EFA cho biết người học ở lại vì đâu; ma trận ưu tiên cho biết giữ ai trước",
])

# 32. Câu hỏi thảo luận
Bl("Câu hỏi thảo luận", [
    "Một kênh có CLV cao nhất nhưng LTV:CAC thấp nhất. Vì sao, và nên làm gì?",
    "Khi nào accuracy vẫn dùng được cho bài toán rời bỏ?",
    "Chi phí can thiệp 20.000 đ và 300.000 đ: chọn ngưỡng khác nhau thế nào?",
    "Vì sao gửi mã giảm giá cho nhóm học vì công việc là lãng phí?",
])

k.save(OUT + "/Bai 13_Thuc hanh 3_Slides.pptx")
print("ok", len(k.prs.slides))
