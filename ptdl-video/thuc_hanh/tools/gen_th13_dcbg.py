import sys, os
W = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, W + "/tools")
from kits import Dcbg

OUT = W + "/th_out/bai_13"
os.makedirs(OUT, exist_ok=True)
d = Dcbg()
P, B, H1, H2, C, E = d.para, d.bullet, d.h1, d.h2, d.caption, d.example

import copy
from docx import Document as _D
_t = _D(W + "/dcbg/b8.docx")
_els = list(_t.element.body.iterchildren())
WNS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
_box = copy.deepcopy(_els[3]); _stars = copy.deepcopy(_els[5]); _src = copy.deepcopy(_els[19])

def _settext(p, text):
    runs = p.findall(".//" + WNS + "r")
    for r in runs[1:]: r.getparent().remove(r)
    r0 = runs[0]
    for t in r0.findall(WNS + "t"): r0.remove(t)
    t = r0.makeelement(WNS + "t", {}); t.text = text
    t.set("{http://www.w3.org/XML/1998/namespace}space", "preserve"); r0.append(t)

def objective_box(items):
    box = copy.deepcopy(_box)
    tc = box.find(".//" + WNS + "tc"); ps = tc.findall(WNS + "p")
    _settext(ps[1], "Sau buổi thực hành này, người học có khả năng:")
    proto = ps[2]
    for p in ps[2:]: tc.remove(p)
    for it in items:
        p = copy.deepcopy(proto); _settext(p, it); tc.append(p)
    d._add(box)

def T(rows, src="(Nguồn: Tác giả tổng hợp)", w=None):
    d.table(rows)
    tbl = [e for e in d.body if e.tag == WNS + "tbl"][-1]
    grid = tbl.find(WNS + "tblGrid"); cols = grid.findall(WNS + "gridCol")
    total = sum(int(c.get(WNS + "w")) for c in cols)
    n = len(cols)
    if w is None:
        L = [max(len(str(r[i])) for r in rows) for i in range(n)]
        w = [max(0.17, min(0.6, x / sum(L))) for x in L]
    tot = sum(w); ws = [int(total * x / tot) for x in w]
    for c, x in zip(cols, ws): c.set(WNS + "w", str(x))
    for tr in tbl.findall(WNS + "tr"):
        for tc, x in zip(tr.findall(WNS + "tc"), ws):
            tw = tc.find(".//" + WNS + "tcW")
            if tw is not None: tw.set(WNS + "w", str(x)); tw.set(WNS + "type", "dxa")
    SRC(src)

def _numbered(numid):
    e = copy.deepcopy(d.ex["bullet"])
    e.find(".//" + WNS + "numPr").find(WNS + "numId").set(WNS + "val", str(numid))
    return e
d.ex["bullet"] = _numbered(2)          # bullet glyph list, like the objectives box
d.ex["question"] = _numbered(3)        # numbered list used for review questions in Bài 8
d.ex["ref"] = _numbered(4)             # numbered list used for references in Bài 8
import re as _re
def Q(t): d._para("question", _re.sub(r"^\d+\. ", "", t))
def R(t): d._para("ref", t)

def stars(): d._add(copy.deepcopy(_stars))
def SRC(text="(Nguồn: Tác giả tổng hợp)"):
    p = copy.deepcopy(_src); _settext(p, text); d._add(p)

d.title("BÀI 13:", "THỰC HÀNH 3: GIÁ TRỊ VÒNG ĐỜI KHÁCH HÀNG,", "DỰ BÁO RỜI BỎ VÀ PHÂN KHÚC TÂM LÝ")

objective_box([
 "Làm sạch dữ liệu khách hàng và giao dịch, tính và chấm điểm RFM, gán nhãn phân khúc theo quy tắc nêu rõ.",
 "Lập bảng unit economics theo phân khúc và theo kênh thu hút, đưa ra khuyến nghị ngân sách dựa trên LTV:CAC.",
 "Dựng bảng cohort giữ chân, xử lý đúng các ô chưa quan sát đủ và đọc được xu hướng.",
 "Xây dựng mô hình hồi quy logistic dự báo rời bỏ và chọn ngưỡng cắt bằng lập luận kinh doanh.",
 "Thực hiện EFA đủ sáu bước, kiểm tra Cronbach's Alpha, phân cụm theo điểm nhân tố và lập ma trận ưu tiên can thiệp."])

H2("Chuẩn đầu ra")
P("Bài thực hành đóng góp vào chuẩn đầu ra L1 của học phần: ứng dụng kiến thức về thuật toán và thống kê vào phân tích dữ liệu, kết hợp kiến thức kinh tế kinh doanh để đưa ra khuyến nghị về khách hàng và ngân sách marketing cho doanh nghiệp. Mức độ yêu cầu là U (vận dụng). Sản phẩm cuối là một báo cáo trả lời được ba câu hỏi quản trị của EDUGO bằng số liệu do nhóm tự tính.")

H2("Kiến thức cần có")
P("Mục 13.1 tóm tắt các nội dung lý thuyết sẽ dùng trực tiếp trong bài.")
C("Bảng 13.1. Các bài lý thuyết liên quan tới từng yêu cầu")
T([["Yêu cầu", "Nội dung cần dùng", "Bài và mục tham chiếu"],
   ["1", "Làm sạch dữ liệu, tính R, F, M", "Bài 3, mục 3.3.2; Bài 5, mục 5.2"],
   ["2", "Chấm điểm RFM, CLV rút gọn, LTV:CAC, customer equity", "Bài 5, mục 5.1 và 5.1.3"],
   ["3", "Phân tích cohort", "Bài 5, mục 5.2"],
   ["4", "Hồi quy logistic, ma trận nhầm lẫn, ROC và AUC, ngưỡng cắt", "Bài 7, mục 7.4.1 đến 7.4.3; Bài 5, mục 5.2"],
   ["5", "EFA, KMO, Bartlett, xoay Varimax, Cronbach's Alpha", "Bài 6, mục 6.1 và 6.2; Bài 8, mục 8.1.6"],
   ["6", "K-means, Silhouette, phân khúc tâm lý, ma trận ưu tiên", "Bài 3, mục 3.2.2; Bài 6, mục 6.3; Bài 5, mục 5.2"]])
P("Công cụ: Python (pandas, scikit-learn, factor_analyzer, pingouin), R hoặc SPSS. Excel làm được Yêu cầu 1 đến 3; Yêu cầu 4 và 5 nên dùng Python, R hoặc SPSS.")

# ------------------------------------------------------------ 13.1
stars()
H1("13.1. Ôn tập kiến thức lý thuyết trọng tâm")
H2("13.1.1. RFM và chấm điểm ngũ phân vị")
P("RFM (Hughes, 1994) mô tả quan hệ giao dịch của một khách hàng bằng ba con số. Recency (R) là số ngày từ lần mua gần nhất tới ngày phân tích. Frequency (F) là số đơn hàng hợp lệ. Monetary (M) là tổng giá trị các đơn hàng hợp lệ.")
P("Mỗi chỉ số được chia thành năm nhóm theo ngũ phân vị và nhận điểm từ 1 đến 5. Chiều chấm điểm của R ngược với F và M: khách mua gần đây nhất có R nhỏ nhất và nhận 5 điểm.")
P("F thường có nhiều giá trị trùng nhau, ví dụ hàng trăm người cùng có F = 1, nên hàm cắt nhóm báo lỗi. Cách xử lý thông dụng là xếp hạng trước rồi mới cắt: pd.qcut(F.rank(method='first'), 5, labels=[1,2,3,4,5]).")
P("Mã RFM chưa phải là phân khúc. Nhóm tự viết quy tắc gán nhãn. Quy tắc nào cũng được chấp nhận nếu nêu rõ, phủ hết mọi tổ hợp điểm và áp dụng nhất quán. Các nhãn thường dùng như Champions, Loyal, At Risk, Hibernating đã giới thiệu ở Bài 5, mục 5.2.")

H2("13.1.2. CLV rút gọn, quy đổi tỷ lệ rời bỏ và LTV:CAC")
P("Giá trị vòng đời khách hàng (Customer Lifetime Value, CLV) là giá trị hiện tại của dòng lợi nhuận kỳ vọng mà một khách hàng tạo ra trong thời gian còn quan hệ với doanh nghiệp. Bài thực hành dùng công thức rút gọn đã học ở Bài 5:")
P("CLV = (ARPU tháng × biên lợi nhuận gộp) ÷ tỷ lệ rời bỏ tháng.")
P("ARPU (Average Revenue Per User) là doanh thu bình quân trên một khách hàng mỗi tháng. Phép chia cho tỷ lệ rời bỏ cho biết khách hàng kỳ vọng ở lại bao nhiêu tháng: rời bỏ 5% một tháng tương ứng 20 tháng. Công thức giả định ARPU và tỷ lệ rời bỏ không đổi, không chiết khấu dòng tiền.")
P("Tử số và mẫu số phải cùng kỳ. Dữ liệu EDUGO cho nhãn rời bỏ theo quý, còn ARPU tính theo tháng, nên tỷ lệ rời bỏ quý phải quy đổi về tháng:")
P("Tỷ lệ rời bỏ tháng = 1 − (1 − tỷ lệ rời bỏ quý)^(1/3).")
P("Nếu mỗi tháng có (1 − c) khách ở lại thì sau ba tháng còn (1 − c)³. Đặt (1 − c)³ bằng (1 − tỷ lệ rời bỏ quý) rồi giải ra c.")
E("Ví dụ 13.1. Quy đổi tỷ lệ rời bỏ trước khi tính CLV")
P("Số liệu tự đặt để minh hoạ: một phân khúc có ARPU 300.000 đồng mỗi tháng, biên lợi nhuận gộp 68%, tỷ lệ rời bỏ quý 20%, CAC trung bình 600.000 đồng.")
C("Bảng 13.2. Hai cách tính CLV cho cùng một phân khúc (ví dụ minh hoạ)")
T([["Bước", "Cách đúng: quy về tháng", "Cách sai: dùng thẳng tỷ lệ quý"],
   ["Lợi nhuận gộp mỗi tháng", "300.000 × 0,68 = 204.000 đ", "204.000 đ"],
   ["Mẫu số", "1 − 0,8^(1/3) = 0,0717", "0,20"],
   ["Số tháng kỳ vọng", "1 ÷ 0,0717 ≈ 14,0 tháng", "1 ÷ 0,20 = 5 tháng"],
   ["CLV", "≈ 2.846.000 đ", "1.020.000 đ"],
   ["LTV:CAC", "≈ 4,74", "1,70"]])
P("Cách sai cho CLV thấp hơn gần ba lần và kéo LTV:CAC từ vùng lành mạnh xuống vùng lãi mỏng.")
P("LTV:CAC bằng CLV chia cho chi phí thu hút trung bình (Customer Acquisition Cost, CAC). Bảng 13.3 nhắc lại các ngưỡng ở Bài 5, mục 5.1.3.")
C("Bảng 13.3. Đọc tỷ lệ LTV:CAC")
T([["LTV:CAC", "Ý nghĩa", "Hành động gợi ý"],
   ["Dưới 1", "Mỗi khách mới làm doanh nghiệp lỗ", "Dừng mở rộng kênh, sửa sản phẩm hoặc giá trước"],
   ["Từ 1 đến 3", "Có lãi nhưng mỏng", "Giảm CAC hoặc tăng giữ chân, chưa tăng ngân sách"],
   ["Khoảng 3", "Ngưỡng lành mạnh trong thực tiễn", "Duy trì và tối ưu dần"],
   ["Trên 5", "Rất tốt, có thể đang đầu tư quá ít vào thu hút", "Cân nhắc tăng ngân sách ở kênh đó"]])
P("Tổng giá trị khách hàng (customer equity) là tổng CLV của mọi khách hàng, bằng tổng của (số khách hàng × CLV) qua các phân khúc.")

H2("13.1.3. Phân tích cohort")
P("Cohort là nhóm khách hàng gia nhập trong cùng một khoảng thời gian. Mỗi hàng của bảng cohort là một cohort, mỗi cột là tháng thứ k kể từ khi gia nhập, mỗi ô là tỷ lệ khách còn phát sinh giao dịch ở tháng đó. Tỷ lệ rời bỏ bình quân trộn khách cũ với khách mới; bảng cohort tách hai nhóm ra nên cho thấy xu hướng.")
P("Hai điểm kỹ thuật quyết định kết quả. Thứ nhất, tháng thứ k phải tính theo khoảng cách ngày từ ngày gia nhập của từng người, không theo hiệu số tháng trên lịch. Thứ hai, cohort gia nhập gần ngày phân tích chưa được quan sát đủ số tháng. Ô chưa quan sát đủ phải để trống, không được ghi 0%.")
E("Ví dụ 13.2. Tháng lịch và tháng tính theo ngày")
P("Một người gia nhập ngày 29/03 và mua ngày 03/04. Hiệu số tháng lịch là 1, nên giao dịch bị xếp vào tháng thứ 1. Khoảng cách thực là 5 ngày; 5 chia 30 lấy phần nguyên bằng 0, nên giao dịch thuộc tháng thứ 0. Dùng tháng lịch cho cả tệp sẽ làm tỷ lệ ở tháng 0 thấp hơn 100%.")

H2("13.1.4. Hồi quy logistic và đánh giá mô hình phân loại")
P("Hồi quy logistic dùng khi biến mục tiêu là nhị phân. Mô hình ước lượng logarit của tỷ số odds: ln[p ÷ (1 − p)] = β0 + β1x1 + … + βkxk, với p là xác suất rời bỏ. Khi biến đầu vào đã chuẩn hoá, độ lớn hệ số so sánh được giữa các biến. exp(β) là tỷ số odds. Bài 7, mục 7.4.2 lưu ý: odds tăng 30% không có nghĩa là xác suất tăng 30%.")
P("Mô hình cho ra xác suất. Để ra quyết định gửi ưu đãi hay không, nhóm phải chọn ngưỡng cắt. Bảng 13.4 tóm tắt các chỉ số đánh giá.")
C("Bảng 13.4. Các chỉ số đánh giá mô hình dự báo rời bỏ")
T([["Chỉ số", "Cách tính", "Trả lời câu hỏi"],
   ["Accuracy", "(TP + TN) ÷ tổng số", "Bao nhiêu phần trăm dự báo đúng"],
   ["Precision", "TP ÷ (TP + FP)", "Trong số người bị cảnh báo, bao nhiêu người thật sự rời bỏ"],
   ["Recall", "TP ÷ (TP + FN)", "Trong số người thật sự rời bỏ, mô hình bắt được bao nhiêu"],
   ["F1", "2 × P × R ÷ (P + R)", "Cân bằng giữa precision và recall"],
   ["AUC", "Diện tích dưới đường ROC", "Mô hình xếp hạng rủi ro tốt đến đâu, không phụ thuộc ngưỡng"]])
P("Về AUC, mức 0,7 đến 0,8 được coi là chấp nhận được, 0,8 đến 0,9 là tốt (Hosmer và cộng sự, 2013). AUC bằng 0,5 nghĩa là mô hình xếp hạng không hơn tung đồng xu.")
P("Accuracy phải luôn được so với mô hình ngây thơ dự báo \"không ai rời bỏ\". Accuracy của mô hình ngây thơ bằng đúng tỷ lệ khách không rời bỏ. Ví dụ ở Bài 5 cho thấy khi tỷ lệ rời bỏ chỉ khoảng 5%, một mô hình đạt accuracy 91,2% vẫn thua mô hình ngây thơ.")
E("Ví dụ 13.3. Đọc một ma trận nhầm lẫn")
P("Số liệu tự đặt: tập kiểm tra có 1.000 người, 300 người rời bỏ thật. Tại ngưỡng 0,5, mô hình cảnh báo 300 người, trong đó 210 người rời bỏ thật. Như vậy TP = 210, FP = 90, FN = 90, TN = 610. Precision = 210 ÷ 300 = 0,70, recall = 210 ÷ 300 = 0,70, accuracy = 820 ÷ 1.000 = 0,82. Mô hình ngây thơ đạt 700 ÷ 1.000 = 0,70. Mô hình hơn mô hình ngây thơ 12 điểm phần trăm.")

H2("13.1.5. Phân tích nhân tố khám phá và độ tin cậy thang đo")
P("Phân tích nhân tố khám phá (Exploratory Factor Analysis, EFA) gom nhiều biến quan sát tương quan với nhau thành một số ít nhân tố tiềm ẩn. Động cơ học tiếng Anh không đo trực tiếp được. Bảng hỏi chỉ đo các biểu hiện của nó qua 17 câu Likert, rồi EFA suy ngược ra cấu trúc. Quy trình sáu bước ở Bài 6, mục 6.2 được tóm tắt trong Bảng 13.5.")
C("Bảng 13.5. Sáu bước EFA và ngưỡng chấp nhận")
T([["Bước", "Chỉ số kiểm tra", "Ngưỡng"],
   ["1. Kiểm tra điều kiện", "KMO; kiểm định Bartlett", "KMO ≥ 0,6, lý tưởng > 0,8; Bartlett p < 0,05"],
   ["2. Trích nhân tố", "Phương pháp trích, thường là thành phần chính", "Ghi rõ phương pháp đã dùng"],
   ["3. Chọn số nhân tố", "Eigenvalue; Scree Plot", "Eigenvalue > 1; điểm gãy của Scree Plot"],
   ["4. Xoay nhân tố", "Varimax (vuông góc) hoặc Promax (xiên)", "Đề bài yêu cầu Varimax"],
   ["5. Lọc biến", "Communality; hệ số tải; cross-loading", "Communality ≥ 0,5; tải ≥ 0,5; không tải > 0,4 lên nhân tố thứ hai"],
   ["6. Đặt tên, kiểm độ tin cậy", "Phương sai tích luỹ; Cronbach's Alpha", "Tích luỹ ≥ 50%; Alpha > 0,7"]])
P("KMO (Kaiser, 1974) so độ lớn của tương quan thông thường với tương quan riêng phần; KMO cao nghĩa là các biến chia sẻ nhiều phương sai chung. Kiểm định Bartlett kiểm tra giả thuyết ma trận tương quan là ma trận đơn vị; phải bác bỏ giả thuyết này mới chạy EFA.")
P("Communality là tỷ lệ phương sai của một biến được các nhân tố chung giải thích. Một biến có thể vượt ngưỡng communality mà vẫn phải loại vì tải chéo trên 0,4 lên hai nhân tố. Phải kiểm tra cả hai tiêu chí.")
P("Cronbach's Alpha đo độ nhất quán nội tại của các biến trong cùng một nhân tố (Cronbach, 1951): α = [k ÷ (k − 1)] × [1 − (Σσi² ÷ σt²)], với k là số biến, σi² là phương sai từng biến và σt² là phương sai của tổng điểm. Ngưỡng thường dùng là α > 0,7. Bảng kết quả nên kèm cột tương quan biến tổng hiệu chỉnh (corrected item-total correlation) và cột Alpha nếu loại biến.")

H2("13.1.6. K-means, Silhouette và phân khúc tâm lý")
P("K-means chia các quan sát thành K cụm sao cho mỗi điểm gần tâm cụm của mình hơn tâm các cụm khác (Bài 3, mục 3.2.2). Thuật toán dùng khoảng cách Euclid, nên biến đầu vào phải cùng thang đo.")
P("Chỉ số Silhouette (Rousseeuw, 1987) đo mức phù hợp của từng điểm với cụm được gán. Với điểm i, gọi a là khoảng cách trung bình tới các điểm cùng cụm và b là khoảng cách trung bình tới các điểm của cụm gần nhất khác. Khi đó s(i) = (b − a) ÷ max(a, b), nằm trong khoảng từ −1 đến 1. Silhouette trung bình càng cao thì các cụm càng tách bạch.")
P("Bài 6, mục 6.3 giải thích vì sao phân cụm trên điểm nhân tố: các biến gốc tương quan mạnh nên một chiều động cơ có bốn câu hỏi bị đếm bốn lần trong khoảng cách. Điểm nhân tố sau xoay Varimax gần như không tương quan và đã chuẩn hoá.")

H2("13.1.7. Ma trận ưu tiên can thiệp")
P("Nhóm có xác suất rời bỏ cao nhất chưa chắc đáng giữ nhất, vì CLV của họ có thể rất thấp. Thứ tự ưu tiên dựa trên giá trị có thể mất, tức tổng của (CLV × xác suất rời bỏ) trong mỗi ô.")
E("Ví dụ 13.4. So sánh hai ô ưu tiên")
P("Số liệu tự đặt: ô A có 50 khách, CLV trung bình 8 triệu đồng, xác suất rời bỏ trung bình 0,4. Ô B có 200 khách, CLV trung bình 1 triệu đồng, xác suất rời bỏ 0,6. Giá trị có thể mất ở ô A là 50 × 8 × 0,4 = 160 triệu đồng. Ở ô B là 200 × 1 × 0,6 = 120 triệu đồng. Ô A nhỏ hơn bốn lần về số người nhưng đáng ưu tiên hơn.")

# ------------------------------------------------------------ 13.2
H1("13.2. Tình huống và dữ liệu")
H2("13.2.1. Bối cảnh doanh nghiệp")
P("EDUGO là nền tảng học tiếng Anh trực tuyến hư cấu, hoạt động từ đầu năm 2024, bán gói theo tháng, quý, năm hoặc khoá luyện thi lẻ. Sau 18 tháng, công ty có khoảng 3.000 người học trả tiền và doanh thu gần 9,5 tỷ đồng. Dữ liệu là dữ liệu mô phỏng.")
P("Tháng 7/2025, giám đốc marketing muốn tăng gấp đôi ngân sách quảng cáo vì doanh thu vẫn tăng. Giám đốc tài chính phản đối vì càng chạy quảng cáo càng lỗ. Nhóm phân tích phải trả lời ba câu hỏi:")
B("Một người học mang lại bao nhiêu tiền trong suốt thời gian ở lại, và chi tối đa bao nhiêu để có được họ thì vẫn có lãi?")
B("Ai sắp rời bỏ, và trong số đó ai đáng bỏ tiền ra giữ?")
B("Người học ở lại vì điều gì, để gửi đúng thông điệp thay vì gửi cùng một mã giảm giá cho tất cả?")
P("Câu hỏi thứ nhất ứng với Yêu cầu 1 đến 3. Câu hỏi thứ hai ứng với Yêu cầu 4. Câu hỏi thứ ba ứng với Yêu cầu 5 và 6. Yêu cầu 6 ghép cả ba câu trả lời thành một kế hoạch hành động.")

H2("13.2.2. Các tệp dữ liệu")
C("Bảng 13.6. Các tệp dữ liệu EDUGO")
T([["Tệp", "Quy mô", "Nội dung", "Dùng cho"],
   ["EDUGO_khach_hang.csv", "3.000 dòng, 12 cột", "Hồ sơ người học, kênh thu hút, CAC, hành vi 30 ngày, nhãn rời bỏ quý III/2025", "Yêu cầu 1, 2, 4, 6"],
   ["EDUGO_giao_dich.csv", "12.975 dòng, 6 cột", "Từng đơn hàng: mã đơn, mã người học, ngày mua, gói, giá trị, kênh mua", "Yêu cầu 1, 2, 3"],
   ["EDUGO_khao_sat.csv", "600 dòng, 18 cột", "Mã người học và 17 câu Likert 1 đến 5 về động cơ học", "Yêu cầu 5, 6"],
   ["EDUGO_tu_dien_bien_khao_sat.csv", "17 dòng", "Nội dung đầy đủ của câu Q01 đến Q17", "Yêu cầu 5"],
   ["EDUGO_du_lieu.xlsx", "Nhiều sheet", "Bản Excel gộp các tệp trên cho nhóm làm bằng Excel", "Tất cả"]], "(Nguồn: Đề bài Thực hành 3)")
P("Ba tệp nối với nhau qua cột MaKH. Tệp khảo sát chỉ có 600 người học được chọn ngẫu nhiên, nên Yêu cầu 6 làm trên 600 người này.")
C("Bảng 13.7. Các cột của tệp EDUGO_khach_hang.csv")
T([["Cột", "Kiểu", "Ý nghĩa"],
   ["MaKH", "chuỗi", "Mã người học, khoá nối ba tệp"],
   ["NgayGiaNhap", "ngày dd/mm/yyyy", "Ngày đăng ký tài khoản"],
   ["Tinh, NhomTuoi", "chuỗi", "Tỉnh thành và nhóm tuổi"],
   ["KenhThuHut", "chuỗi", "Facebook Ads, Google Ads, TikTok, Giới thiệu bạn bè, Tìm kiếm tự nhiên"],
   ["ChiPhiThuHut", "số nguyên", "CAC của riêng người học này, đơn vị đồng"],
   ["SoLanDangNhap_30Ngay, SoBuoiHocHoanThanh_30Ngay", "số nguyên", "Số lần mở ứng dụng và số buổi học hoàn thành trong 30 ngày gần nhất"],
   ["TyLeMoEmail, SoLanLienHeCSKH", "số thực 0 đến 1; số nguyên", "Tỷ lệ mở email marketing; số lần liên hệ chăm sóc khách hàng"],
   ["DanhGiaUngDung_1_5", "số nguyên 1 đến 5", "Điểm người học chấm cho ứng dụng"],
   ["RoiBo_Quy3", "0 hoặc 1", "Biến mục tiêu: 1 nếu không có giao dịch nào từ 01/07 đến 30/09/2025"]], "(Nguồn: Đề bài Thực hành 3)")
P("Tệp giao dịch có sáu cột: MaDonHang (mã đơn, về nguyên tắc là duy nhất), MaKH, NgayMua (dd/mm/yyyy), TenGoi, GiaTri (đồng) và Kenh (App hoặc Website).")

H2("13.2.3. Các giả định cho trước")
C("Bảng 13.8. Giả định dùng chung cho mọi yêu cầu")
T([["Giả định", "Giá trị"],
   ["Ngày phân tích", "30/06/2025; mọi chỉ số R, F, M và biến hành vi tính tới ngày này"],
   ["Kỳ dữ liệu giao dịch", "01/01/2024 đến 30/06/2025, tức 18 tháng"],
   ["Biên lợi nhuận gộp", "68%"],
   ["Công thức CLV", "(ARPU tháng × biên lợi nhuận gộp) ÷ tỷ lệ rời bỏ tháng"],
   ["Quy đổi tỷ lệ rời bỏ", "Tháng = 1 − (1 − quý)^(1/3)"],
   ["Định nghĩa rời bỏ", "Không có giao dịch nào trong quý III/2025; cột RoiBo_Quy3 đã tính sẵn"],
   ["Ngưỡng LTV:CAC", "Dưới 1 là lỗ trên mỗi người học mới; khoảng 3 là lành mạnh"]], "(Nguồn: Đề bài Thực hành 3)")

H2("13.2.4. Lưu ý về chất lượng dữ liệu")
P("Dữ liệu được giao có lỗi cài sẵn, giống dữ liệu thật. Đề bài không nói lỗi nằm ở đâu. Một đơn hàng bị ghi hai lần làm F và M tăng giả và đẩy người học lên phân khúc cao hơn thực tế.")
P("Ngày ở dạng dd/mm/yyyy. Khi đọc bằng pandas phải chỉ rõ định dạng: pd.to_datetime(df['NgayMua'], format='%d/%m/%Y'). Nếu để pandas tự đoán, ngày 05/03 có thể bị hiểu thành ngày 3 tháng 5 mà không có cảnh báo.")

# ------------------------------------------------------------ 13.3
H1("13.3. Yêu cầu 1: Làm sạch dữ liệu và tính RFM")
P("Yêu cầu 1 tạo ra bảng RFM sạch cho 3.000 người học. Mọi yêu cầu từ 2 đến 4 đều dùng bảng này. Một lỗi ở đây lan sang toàn bộ báo cáo.")
H2("13.3.1. Các bước thực hiện")
P("Bước 1. Đọc dữ liệu, kiểm tra df.shape và df.dtypes, rồi rà soát chất lượng theo Bảng 13.9. Với mỗi vấn đề, ghi bốn thông tin: phát hiện bằng cách nào, bao nhiêu bản ghi bị ảnh hưởng, xử lý thế nào, vì sao chọn cách đó.")
C("Bảng 13.9. Danh mục kiểm tra chất lượng dữ liệu")
T([["Loại vấn đề", "Cách kiểm tra trong pandas", "Hướng xử lý cần cân nhắc"],
   ["Bản ghi trùng", "df.duplicated(subset='MaDonHang').sum(); so với df.duplicated().sum()", "Giữ một bản ghi; giải thích vì sao mã đơn phải duy nhất"],
   ["Giá trị bất thường", "df['GiaTri'].describe(); lọc GiaTri <= 0", "Xác định bản chất giao dịch, quyết định loại hay trừ vào M, áp dụng nhất quán"],
   ["Mâu thuẫn logic về ngày", "So NgayGiaNhap với ngày mua đầu tiên của cùng MaKH", "Sửa theo nguồn đáng tin hơn hoặc loại, nêu ảnh hưởng tới cohort"],
   ["Giá trị thiếu", "df.isna().sum() trên từng tệp, kể cả tệp khảo sát", "Điền trung vị hoặc trung vị theo nhóm; không xoá cả dòng khi chỉ thiếu một ô"],
   ["Ngày ngoài kỳ", "Lọc NgayMua ngoài 01/01/2024 đến 30/06/2025", "Loại khỏi phép tính RFM"],
   ["Khoá nối không khớp", "Tìm MaKH có trong giao dịch mà không có trong khách hàng và ngược lại", "Báo cáo số lượng và cách xử lý"]])
P("Bước 2. Tính R, F, M từ tệp giao dịch đã sạch bằng groupby:")
P("rfm = gd.groupby('MaKH').agg(LanMuaCuoi=('NgayMua','max'), F=('MaDonHang','nunique'), M=('GiaTri','sum')); rfm['R'] = (pd.Timestamp('2025-06-30') - rfm['LanMuaCuoi']).dt.days.")
P("Bước 3. Nối bảng RFM về tệp khách hàng bằng merge(how='left'). Những người học không còn giao dịch hợp lệ nào sau khi làm sạch sẽ có R, F, M bị thiếu. Nhóm phải chọn một quy ước và nói rõ. Một cách là gán F = 0, M = 0 và R bằng một giá trị lớn quy ước, ví dụ số ngày từ ngày gia nhập tới ngày phân tích hoặc một hằng số. Cách khác là loại họ khỏi phân tích và báo cáo số người bị loại cùng ảnh hưởng tới customer equity.")
P("Bước 4. Lập bảng thống kê mô tả của R, F, M bằng rfm[['R','F','M']].describe(), bổ sung trung vị và độ lệch. Nếu nhóm dùng giá trị quy ước lớn cho R, cần nói rõ thống kê mô tả có tính nhóm này hay không, vì một giá trị như 999 kéo trung bình R lên mạnh. F và M thường lệch phải, nên báo cáo cả trung bình và trung vị.")
H2("13.3.2. Cạm bẫy thường gặp")
B("Đếm F bằng count thay vì nunique trên MaDonHang khi chưa loại trùng.")
B("Xoá cả dòng khách hàng chỉ vì thiếu TyLeMoEmail, làm mất người học khỏi mọi bước sau.")
B("Để pandas tự đoán định dạng ngày.")
B("Tính R từ ngày chạy máy thay vì ngày phân tích 30/06/2025.")
P("Sản phẩm cần nộp: bảng nhật ký làm sạch theo bốn cột ở Bước 1, bảng thống kê mô tả R, F, M và một đoạn ngắn nêu quy ước cho người học không có giao dịch hợp lệ.")

# ------------------------------------------------------------ 13.4
H1("13.4. Yêu cầu 2: Phân khúc, CLV và LTV:CAC")
P("Yêu cầu 2 trả lời câu hỏi thứ nhất: mỗi nhóm người học đáng giá bao nhiêu và mỗi kênh thu hút có đáng tiền không. Đây là phần nặng điểm nhất, 2,5 điểm.")
H2("13.4.1. Chấm điểm và gán nhãn")
P("Chấm điểm R, F, M theo ngũ phân vị như mục 13.1.1. Viết quy tắc gán nhãn dưới dạng một chuỗi điều kiện kiểm tra theo thứ tự, ví dụ dùng np.select. Điều kiện đứng trước được ưu tiên, nên đặt Champions trước Loyal. Nhãn cuối cùng là nhóm còn lại để không người học nào bị bỏ sót. Báo cáo số người học trong từng phân khúc để kiểm tra không có phân khúc nào quá nhỏ.")
H2("13.4.2. Bảng unit economics theo phân khúc")
P("Bảng cần có các cột: số người học, R, F, M trung bình, ARPU tháng, tỷ lệ rời bỏ quý, tỷ lệ rời bỏ tháng, CLV, CAC trung bình và LTV:CAC. Các bước tính:")
B("Tỷ lệ rời bỏ quý của phân khúc bằng trung bình cột RoiBo_Quy3 trong phân khúc.")
B("Tỷ lệ rời bỏ tháng quy đổi theo công thức ở mục 13.1.2.")
B("ARPU tháng là doanh thu bình quân mỗi tháng. Đề bài không quy định mẫu số. Cách hợp lý là chia M của mỗi người cho số tháng người đó đã gắn bó, tức (30/06/2025 − NgayGiaNhap) ÷ 30, tối thiểu 1 tháng, rồi lấy trung bình theo phân khúc. Chia đều cho 18 tháng sẽ đánh giá thấp người mới gia nhập. Nhóm phải ghi rõ cách đã chọn.")
B("CLV = ARPU tháng × 0,68 ÷ tỷ lệ rời bỏ tháng.")
B("CAC trung bình là trung bình cột ChiPhiThuHut trong phân khúc. LTV:CAC = CLV ÷ CAC trung bình.")
P("Chỉ ra các phân khúc có LTV:CAC dưới 1 và giải thích hệ quả kinh doanh: mỗi đồng chi để thu hút một người học thuộc nhóm đó không thu hồi được trong cả vòng đời. Chỉ nêu con số mà không nói hệ quả là chưa đủ.")
H2("13.4.3. Bảng theo kênh thu hút")
P("Lặp lại phép tính với nhóm theo KenhThuHut thay vì theo phân khúc. Có hai cách tính CLV cho kênh: tính lại ARPU và tỷ lệ rời bỏ theo kênh, hoặc gán cho mỗi người học CLV của phân khúc mình rồi lấy trung bình theo kênh. Hai cách cho kết quả khác nhau; nhóm chọn một và nêu lý do.")
P("Khi đọc bảng theo kênh, tách hai thành phần của tỷ lệ: kênh khác nhau ở CLV hay ở CAC. Nếu CLV các kênh gần nhau mà CAC chênh lệch lớn, vấn đề nằm ở giá mua khách chứ không ở chất lượng khách. Khuyến nghị ngân sách cần nêu rõ kênh nào tăng, kênh nào giảm, và một mức trần CAC cụ thể cho kênh trả phí nếu cần.")
H2("13.4.4. Customer equity")
P("Customer equity bằng tổng của (số người học × CLV) qua các phân khúc. Nếu Yêu cầu 1 đã loại một số người học, phải nói con số này bỏ qua họ.")
H2("13.4.5. Cạm bẫy thường gặp")
B("Dùng tỷ lệ rời bỏ quý làm mẫu số. CLV thấp đi khoảng ba lần và mọi phân khúc trông như đang lỗ.")
B("Tính ARPU từ doanh thu theo năm rồi chia cho tỷ lệ rời bỏ tháng, lệch đơn vị.")
B("Phân khúc có tỷ lệ rời bỏ bằng 0 làm phép chia vô hạn. Phải kiểm tra và xử lý trước.")
B("Khuyến nghị tăng ngân sách chỉ vì một kênh có nhiều người học nhất.")
P("Sản phẩm cần nộp: quy tắc gán nhãn, bảng unit economics theo phân khúc, bảng theo kênh, con số customer equity và một đoạn khuyến nghị ngân sách có căn cứ từ bảng.")

# ------------------------------------------------------------ 13.5
H1("13.5. Yêu cầu 3: Phân tích cohort")
P("Yêu cầu 3 cho biết khả năng giữ chân của EDUGO đang tốt lên hay xấu đi. Bảng unit economics ở Yêu cầu 2 là ảnh chụp tại một thời điểm. Bảng cohort cho thấy xu hướng.")
H2("13.5.1. Các bước thực hiện")
P("Bước 1. Gán cohort theo quý gia nhập: kh['Cohort'] = kh['NgayGiaNhap'].dt.to_period('Q'). Dùng NgayGiaNhap đã sửa ở Yêu cầu 1.")
P("Bước 2. Nối giao dịch với ngày gia nhập và tính chỉ số tháng: gd['Thang'] = (gd['NgayMua'] - gd['NgayGiaNhap']).dt.days // 30.")
P("Bước 3. Đếm số người học khác nhau có giao dịch theo cặp (Cohort, Thang) bằng groupby(['Cohort','Thang'])['MaKH'].nunique(), rồi chia cho cỡ cohort. Dùng pivot hoặc unstack để có ma trận.")
P("Bước 4. Che các ô chưa quan sát đủ. Ô (cohort, tháng k) chỉ được tính khi người gia nhập muộn nhất trong cohort đã có đủ k + 1 tháng tính tới ngày phân tích, tức ngày cuối quý gia nhập + (k + 1) × 30 ngày ≤ 30/06/2025. Ô không đạt điều kiện để trống bằng NaN. Có thể chọn quy tắc khác, nhưng phải viết ra.")
P("Bước 5. Vẽ các đường giữ chân trên cùng một biểu đồ, mỗi đường một cohort. Matplotlib bỏ qua NaN nên các đường dừng đúng chỗ dữ liệu hết.")
H2("13.5.2. Cách đọc kết quả")
P("So sánh các cohort tại cùng một mốc tháng, ví dụ tháng thứ 3 và tháng thứ 5. Nếu cohort gia nhập sau giữ được tỷ lệ cao hơn cohort gia nhập trước ở hầu hết các mốc, giữ chân đang tốt lên. Kết luận phải dựa trên chênh lệch cụ thể, tính bằng điểm phần trăm, và nêu rõ ở bao nhiêu mốc xu hướng này lặp lại.")
H2("13.5.3. Cạm bẫy thường gặp")
B("Tính tháng theo lịch, làm tháng 0 không còn bằng 100%.")
B("Ghi 0% cho các ô chưa quan sát, làm đường của cohort mới lao dốc giả tạo và dẫn tới kết luận ngược.")
B("Chia cho số người có giao dịch ở tháng 0 thay vì cỡ cohort mà không giải thích.")
P("Sản phẩm cần nộp: ma trận cohort có ghi chú cách che ô, biểu đồ đường giữ chân và câu trả lời có căn cứ về xu hướng.")

# ------------------------------------------------------------ 13.6
H1("13.6. Yêu cầu 4: Mô hình dự báo rời bỏ")
P("Yêu cầu 4 trả lời câu hỏi thứ hai: ai sắp rời bỏ. Đầu ra quan trọng nhất là xác suất rời bỏ cho từng người học, sẽ dùng lại ở Yêu cầu 6.")
H2("13.6.1. Các bước thực hiện")
P("Bước 1. Chọn biến đầu vào: năm biến hành vi (SoLanDangNhap_30Ngay, SoBuoiHocHoanThanh_30Ngay, TyLeMoEmail, SoLanLienHeCSKH, DanhGiaUngDung_1_5) và R, F, M. Biến mục tiêu là RoiBo_Quy3. Không đưa MaKH hay NgayGiaNhap dạng ngày vào mô hình.")
P("Bước 2. Tách dữ liệu: train_test_split(X, y, test_size=0.3, stratify=y, random_state=42). Tham số stratify giữ tỷ lệ rời bỏ như nhau ở hai tập. Ghi random_state để người chấm chạy lại được.")
P("Bước 3. Chuẩn hoá: StandardScaler().fit trên tập huấn luyện, sau đó transform cả hai tập. Không fit trên toàn bộ dữ liệu, vì như vậy thông tin của tập kiểm tra rò vào mô hình.")
P("Bước 4. Huấn luyện: LogisticRegression(max_iter=1000).fit(X_train, y_train).")
P("Bước 5. Đánh giá trên tập kiểm tra: p = model.predict_proba(X_test)[:, 1]; roc_auc_score(y_test, p); confusion_matrix(y_test, p >= nguong). Vẽ đường ROC bằng RocCurveDisplay.from_predictions.")
P("Bước 6. Lập bảng đánh đổi theo ngưỡng. Với ít nhất năm ngưỡng, ví dụ 0,15; 0,20; 0,30; 0,40; 0,50, báo cáo số người bị cảnh báo, precision và recall. Thêm một cột diễn giải kinh doanh cho từng ngưỡng.")
P("Bước 7. So sánh với mô hình ngây thơ. Accuracy ngây thơ = 1 − tỷ lệ rời bỏ trong tập kiểm tra. Nhận xét chênh lệch và giải thích vì sao ở bộ dữ liệu này accuracy còn dùng được hay không, dựa vào tỷ lệ lớp thiểu số.")
P("Bước 8. Xếp hạng biến theo trị tuyệt đối của hệ số chuẩn hoá. Nêu ba biến mạnh nhất, dấu của từng hệ số và ý nghĩa kinh doanh. Có thể báo cáo thêm exp(β) để nói theo tỷ số odds. Vì R, F, M tương quan với nhau và với biến hành vi, dấu của một hệ số có thể trái trực giác. Khi đó, kiểm tra ma trận tương quan và diễn giải theo nghĩa \"khi đã kiểm soát các biến khác\".")
H2("13.6.2. Chọn ngưỡng cắt bằng lập luận kinh doanh")
P("Ngưỡng thấp bắt được nhiều người sắp rời bỏ nhưng gửi nhầm ưu đãi cho nhiều người. Ngưỡng cao tiết kiệm nhưng bỏ sót. Lựa chọn phụ thuộc chi phí một lần can thiệp và giá trị cứu được một người: thông báo đẩy rẻ cho phép ngưỡng thấp, gọi điện tư vấn hay tặng tháng học miễn phí đòi hỏi ngưỡng cao hơn. Nhóm nêu giả định chi phí cụ thể khi bảo vệ ngưỡng.")
H2("13.6.3. Cạm bẫy thường gặp")
B("Báo cáo AUC hay accuracy trên tập huấn luyện.")
B("Fit StandardScaler trên toàn bộ dữ liệu trước khi tách.")
B("Bỏ R khỏi mô hình, làm AUC giảm rõ.")
B("Chọn ngưỡng 0,5 theo mặc định mà không có lập luận.")
B("Kết luận \"biến X gây ra rời bỏ\". Hồi quy trên dữ liệu quan sát cho thấy liên hệ, không chứng minh nhân quả.")
P("Sản phẩm cần nộp: AUC và đường ROC trên tập kiểm tra, ma trận nhầm lẫn tại ngưỡng chọn, bảng đánh đổi ít nhất năm ngưỡng, so sánh với mô hình ngây thơ, ba biến mạnh nhất kèm diễn giải.")

# ------------------------------------------------------------ 13.7
H1("13.7. Yêu cầu 5: Phân tích nhân tố khám phá")
P("Yêu cầu 5 trả lời một nửa câu hỏi thứ ba: người học có những kiểu động cơ nào. 17 câu hỏi được gom thành một số nhân tố có tên gọi rõ ràng.")
H2("13.7.1. Thực hiện bằng Python")
P("Chuẩn bị: lấy 17 cột Q01 đến Q17, kiểm tra và điền giá trị thiếu trước khi chạy. Các hàm chính trong gói factor_analyzer:")
B("calculate_kmo(X) trả về KMO từng biến và KMO tổng.")
B("calculate_bartlett_sphericity(X) trả về chi-square và p-value.")
B("FactorAnalyzer(n_factors=17, rotation=None, method='principal').fit(X), sau đó get_eigenvalues() để lấy eigenvalue và vẽ Scree Plot.")
B("FactorAnalyzer(n_factors=k, rotation='varimax', method='principal').fit(X); loadings_ cho ma trận tải, get_communalities() cho communality, get_factor_variance() cho phương sai giải thích và tích luỹ.")
B("pingouin.cronbach_alpha(data=X[cac_bien]) cho Alpha của từng nhân tố.")
H2("13.7.2. Thực hiện bằng SPSS")
P("Vào Analyze > Dimension Reduction > Factor, đưa 17 biến vào ô Variables. Trong Descriptives, chọn KMO and Bartlett's test of sphericity. Trong Extraction, chọn phương pháp Principal components và Scree plot. Trong Rotation, chọn Varimax. Trong Options, chọn Sorted by size và ẩn hệ số dưới 0,3. Độ tin cậy kiểm tra ở Analyze > Scale > Reliability Analysis, chọn Model Alpha và trong Statistics tích Scale if item deleted.")
H2("13.7.3. Quy trình lọc biến")
P("Đọc ma trận tải sau xoay theo ba quy tắc ở Bảng 13.5. Liệt kê mọi biến vi phạm, ghi rõ vi phạm tiêu chí nào. Loại biến vi phạm nặng nhất trước, chạy lại EFA, rồi xem biến tiếp theo còn vi phạm không. Sau khi cấu trúc sạch, so sánh phương sai giải thích tích luỹ trước và sau. Phương sai tích luỹ có thể giảm sau khi loại biến. Điều đó không sai: cấu trúc sạch quan trọng hơn vài điểm phần trăm phương sai.")
H2("13.7.4. Đặt tên nhân tố")
P("Đặt tên dựa trên nội dung chung của các biến tải mạnh lên nhân tố, đọc từ tệp từ điển biến. Không đặt tên trước rồi tìm biến cho vừa. Bài 6 đã nêu ví dụ MỘC AN: nhóm đặt tên theo kế hoạch thương hiệu và kết luận sai về một nhân tố mà không câu hỏi nào đo. Thứ tự NT1, NT2 phụ thuộc phần mềm. Báo cáo theo tên, không theo số thứ tự.")
H2("13.7.5. Cạm bẫy thường gặp")
B("Chỉ xét communality mà bỏ qua cross-loading, hoặc ngược lại.")
B("Loại nhiều biến cùng lúc mà không chạy lại sau mỗi lần loại.")
B("Chạy EFA khi còn giá trị thiếu: hàm sẽ báo lỗi hoặc âm thầm loại dòng.")
B("Báo cáo Alpha cho cả 17 biến thay vì cho từng nhân tố.")
P("Sản phẩm cần nộp: kết quả KMO và Bartlett kèm kết luận, bảng eigenvalue và Scree Plot, ma trận tải có cột communality trước và sau khi loại biến, lý do loại từng biến, tên các nhân tố và bảng Cronbach's Alpha.")

# ------------------------------------------------------------ 13.8
H1("13.8. Yêu cầu 6: Ghép hai nửa và đề xuất hành động")
P("Yêu cầu 6 ghép giá trị kinh tế với động cơ. Mô hình rời bỏ cho biết ai cần giữ. Phân cụm tâm lý cho biết giữ bằng cách nào. Đây là điểm khác biệt của bài này so với một bài RFM thông thường.")
H2("13.8.1. Phân cụm theo điểm nhân tố")
P("Bước 1. Tính điểm nhân tố cho 600 người học: fa.transform(X) trong Python, hoặc Save as variables, phương pháp Regression trong SPSS. Điểm nhân tố phải tính từ mô hình EFA cuối cùng sau khi đã loại biến.")
P("Bước 2. Chạy KMeans(n_clusters=k, n_init=10, random_state=42) với k từ 2 đến 6 hoặc 8. Với mỗi k, tính silhouette_score(diem_nt, nhan_cum). Lập bảng Silhouette theo k và chọn k.")
P("Bước 3. Mô tả chân dung từng cụm bằng điểm nhân tố trung bình. Điểm dương lớn nghĩa là cụm coi trọng chiều động cơ đó hơn mức bình quân. Đặt tên cụm theo chiều nổi bật nhất. Báo cáo số người học mỗi cụm và giải thích vì sao dùng điểm nhân tố thay vì 17 biến gốc, dựa trên mục 13.1.6.")
H2("13.8.2. Ma trận ưu tiên")
P("Bước 1. Nối cho 600 người học ba thông tin: CLV theo phân khúc từ Yêu cầu 2, xác suất rời bỏ từ Yêu cầu 4 và cụm tâm lý. Xác suất rời bỏ lấy bằng predict_proba của mô hình đã huấn luyện, áp lên dữ liệu đã chuẩn hoá bằng chính scaler đã fit. Một phần trong 600 người nằm trong tập huấn luyện, nên xác suất của họ có thể lạc quan hơn thực tế. Nhóm nên nêu hạn chế này.")
P("Bước 2. Chọn ngưỡng tách cao và thấp cho CLV và cho xác suất rời bỏ, ví dụ trung vị của 600 người. Nêu rõ ngưỡng đã chọn.")
P("Bước 3. Với mỗi ô trong bốn ô, báo cáo số người học, CLV trung bình, xác suất rời bỏ trung bình và giá trị có thể mất bằng tổng CLV × xác suất rời bỏ. Chọn ô ưu tiên số một theo giá trị có thể mất, không theo số người.")
C("Bảng 13.10. Khuôn ma trận ưu tiên can thiệp")
T([["Ô", "Số người học", "CLV trung bình (đ)", "Xác suất rời bỏ TB", "Giá trị có thể mất (đ)"],
   ["Giá trị cao, rủi ro cao", "…", "…", "…", "…"],
   ["Giá trị cao, rủi ro thấp", "…", "…", "…", "…"],
   ["Giá trị thấp, rủi ro cao", "…", "…", "…", "…"],
   ["Giá trị thấp, rủi ro thấp", "…", "…", "…", "…"]])
H2("13.8.3. Thiết kế ba thông điệp")
P("Trong ô ưu tiên số một, đếm số người theo cụm tâm lý và chọn ba cụm đông nhất. Mỗi thông điệp cần bốn thành phần: nội dung, kênh gửi, chi phí đơn vị dự kiến và chỉ số đo hiệu quả. Thông điệp phải khớp với chiều động cơ nổi bật của cụm. Một nhóm học vì công việc ít nhạy với giá; gửi mã giảm giá cho họ vừa tốn tiền vừa không chạm đúng lý do họ ở lại.")
P("Chỉ số đo hiệu quả nên là hành vi đo được, ví dụ tỷ lệ gia hạn hay số lần đăng nhập trong 14 ngày sau khi nhận thông điệp. Nếu có điều kiện, đề xuất thử nghiệm A/B có nhóm đối chứng như Bài 7, mục 7.5.")
H2("13.8.4. Cạm bẫy thường gặp")
B("Phân cụm trên 17 biến gốc, hoặc trên điểm nhân tố tính từ mô hình EFA chưa loại biến.")
B("Chọn ô ưu tiên theo xác suất rời bỏ cao nhất mà bỏ qua CLV.")
B("Ba thông điệp chỉ khác nhau về mức giảm giá.")
P("Sản phẩm cần nộp: bảng Silhouette theo k, bảng chân dung cụm kèm tên, ma trận ưu tiên bốn ô, bảng phân bố cụm trong ô ưu tiên số một và ba thông điệp đủ bốn thành phần.")

# ------------------------------------------------------------ 13.9
H1("13.9. Sản phẩm nộp và tiêu chí đánh giá")
H2("13.9.1. Sản phẩm nộp")
B("Báo cáo dạng Word hoặc PDF, không quá 20 trang, trình bày theo thứ tự sáu yêu cầu. Mỗi bảng và biểu đồ có số thứ tự, tên và một câu diễn giải.")
B("Mã nguồn: tệp .ipynb hoặc .R chạy lại được từ dữ liệu gốc, hoặc tệp .sav và .spv của SPSS. Nhóm làm bằng Excel nộp tệp .xlsx còn giữ công thức.")
B("Một trang tóm tắt cho ban giám đốc ở đầu báo cáo: ba câu hỏi, ba câu trả lời, ba con số chính.")
H2("13.9.2. Thang điểm")
C("Bảng 13.11. Thang điểm theo đề bài và tiêu chí chấm gợi ý")
T([["Yêu cầu", "Điểm", "Tiêu chí chính"],
   ["1. Làm sạch và RFM", "1,5", "Phát hiện đủ vấn đề, ghi nhật ký bốn cột; RFM tính đúng ngày phân tích; quy ước cho người không có giao dịch"],
   ["2. Phân khúc, CLV, LTV:CAC", "2,5", "Quy tắc nhãn rõ; quy đổi tỷ lệ rời bỏ đúng; giải thích LTV:CAC dưới 1; bảng kênh và khuyến nghị; customer equity"],
   ["3. Cohort", "1,0", "Tháng tính theo ngày; che ô chưa quan sát đủ; kết luận xu hướng có số liệu"],
   ["4. Dự báo rời bỏ", "2,0", "AUC trên tập kiểm tra; ma trận nhầm lẫn; bảng ít nhất năm ngưỡng; so với mô hình ngây thơ; ba biến mạnh nhất"],
   ["5. EFA", "2,0", "KMO, Bartlett; số nhân tố; ma trận tải và communality; loại biến có lý do; tên nhân tố; Cronbach's Alpha"],
   ["6. Ghép và hành động", "1,0", "Silhouette; chân dung cụm; ma trận bốn ô có giá trị có thể mất; ba thông điệp đủ bốn thành phần"],
   ["Tổng", "10,0", ""]], "(Nguồn: Đề bài Thực hành 3)")
P("Báo cáo chỉ liệt kê con số mà không diễn giải ý nghĩa kinh doanh sẽ bị trừ điểm ở ý tương ứng.")

# ------------------------------------------------------------ closing
d.plain_heading("Tóm tắt bài học")
P("Bài thực hành 3 đi qua một chuỗi phân tích hoàn chỉnh trên dữ liệu của một nền tảng học trực tuyến. Dữ liệu giao dịch phải được làm sạch trước khi tính RFM, vì lỗi ở bước này lan sang mọi kết quả sau.")
P("CLV theo công thức rút gọn đòi hỏi tử số và mẫu số cùng kỳ. Tỷ lệ rời bỏ quý phải quy đổi về tháng bằng 1 − (1 − q)^(1/3). LTV:CAC dưới 1 nghĩa là mỗi khách mới làm doanh nghiệp lỗ. So sánh kênh thu hút phải tách phần chênh lệch do CLV và phần do CAC.")
P("Bảng cohort tính tháng theo khoảng cách ngày và để trống ô chưa quan sát đủ. Mô hình logistic được đánh giá trên tập kiểm tra; ngưỡng cắt là quyết định kinh doanh. EFA lọc biến theo cả communality và cross-loading, và điểm nhân tố là đầu vào cho K-means. Ma trận giá trị nhân rủi ro chỉ ra ai cần giữ; cụm tâm lý chỉ ra giữ bằng thông điệp nào.")

d.plain_heading("CÂU HỎI ÔN TẬP")
Q("1. Vì sao không được dùng thẳng tỷ lệ rời bỏ quý làm mẫu số trong công thức CLV khi ARPU tính theo tháng? Chứng minh công thức quy đổi tỷ lệ rời bỏ quý sang tháng.")
Q("2. Một kênh thu hút có CLV trung bình cao nhất nhưng LTV:CAC thấp nhất. Giải thích điều đó có thể xảy ra như thế nào và đề xuất hành động cho kênh này.")
Q("3. Khi nào accuracy là thước đo chấp nhận được cho mô hình dự báo rời bỏ, khi nào không? Lấy ví dụ bằng số liệu tự đặt.")
Q("4. Nêu các bước chọn ngưỡng cắt cho chiến dịch giữ chân khi chi phí một lần can thiệp là 20.000 đồng và khi là 300.000 đồng. Hai trường hợp nên chọn ngưỡng khác nhau ra sao?")
Q("5. Một biến có communality 0,62, tải 0,61 lên nhân tố thứ nhất và 0,43 lên nhân tố thứ hai. Có giữ biến này không? Giải thích theo các ngưỡng ở Bài 6.")
Q("6. Vì sao ô ưu tiên can thiệp phải được chọn theo giá trị có thể mất thay vì theo xác suất rời bỏ? Minh hoạ bằng hai ô với số liệu tự đặt.")

d.plain_heading("TÀI LIỆU THAM KHẢO")
R("Nguyễn Bình Minh An, Trương Hoàng Giang (2026). Đề cương bài giảng: Phân tích dữ liệu Marketing. Khoa Kinh doanh số, Trường Kinh tế, Đại học Công nghiệp Hà Nội.")
R("Joseph F. Hair, William C. Black, Barry J. Babin & Rolph E. Anderson (2019). Multivariate Data Analysis (8th ed.). Cengage Learning.")
R("Naresh K. Malhotra (2019). Marketing Research: An Applied Orientation (7th ed.). Pearson.")
R("Arthur M. Hughes (1994). Strategic Database Marketing. Probus Publishing.")
R("Sunil Gupta & Donald R. Lehmann (2003). Customers as assets. Journal of Interactive Marketing, 17(1), 9-24.")
R("David W. Hosmer, Stanley Lemeshow & Rodney X. Sturdivant (2013). Applied Logistic Regression (3rd ed.). John Wiley & Sons.")
R("Henry F. Kaiser (1974). An index of factorial simplicity. Psychometrika, 39(1), 31-36.")
R("Lee J. Cronbach (1951). Coefficient alpha and the internal structure of tests. Psychometrika, 16(3), 297-334.")
R("Peter J. Rousseeuw (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53-65.")
R("Fabian Pedregosa và cộng sự (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830. Tài liệu hướng dẫn: https://scikit-learn.org/stable/")

for _p in d.doc.paragraphs:
    if _p.text.startswith(("Bảng 13.", "Ví dụ 13.")) or _re.match(r"^13\.\d", _p.text):
        _p.paragraph_format.keep_with_next = True
d.save(OUT + "/Bai 13_Thuc hanh 3_ĐCBG.docx")
print("ok")
