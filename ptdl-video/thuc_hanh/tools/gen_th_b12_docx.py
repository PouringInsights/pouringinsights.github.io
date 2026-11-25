import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from th_b12_lib import D2 as D

W = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = f"{W}/th_out/bai_12"
os.makedirs(OUT, exist_ok=True)

d = D()
d.title("BÀI 12:", "THỰC HÀNH 2: PHÂN KHÚC KHÁCH HÀNG", "VÀ NHÓM HOÁ DANH MỤC SẢN PHẨM BẰNG PHÂN CỤM")
d.objectives("Sau buổi thực hành này, người học có khả năng:", [
    "Thực hiện đủ quy trình phân cụm trên dữ liệu thật của doanh nghiệp: kiểm tra chất lượng dữ liệu, xử lý điểm ngoại lệ, chuẩn hoá biến, chọn số cụm, chạy thuật toán và diễn giải kết quả;",
    "Vận dụng K-means cho tệp khách hàng lớn và Hierarchical Clustering cho tệp danh mục nhỏ, giải thích được vì sao mỗi bài toán cần một phương pháp riêng;",
    "Chọn tham số có căn cứ bằng Elbow Method, Silhouette Score, dendrogram và biểu đồ k-distance;",
    "Chuyển kết quả phân cụm thành chân dung phân khúc, họ sản phẩm có tên gọi kinh doanh;",
    "Viết khuyến nghị marketing có hành động cụ thể, đối tượng áp dụng, phép tính tác động tài chính và chỉ số theo dõi.",
])

d.plain_heading("Chuẩn đầu ra")
d.para("Buổi thực hành đóng góp vào chuẩn đầu ra L1 của học phần: ứng dụng kiến thức về các thuật toán và thống kê vào phân tích dữ liệu, song song với kiến thức kinh tế, kinh doanh để đưa ra khuyến nghị chiến lược về sản phẩm, khách hàng và thị trường cho doanh nghiệp. Mức độ yêu cầu là vận dụng (U2), giống Bài 3.")
d.plain_heading("Kiến thức cần có")
d.para("Sinh viên cần ôn lại các nội dung sau trước buổi thực hành. Mục 12.1 tóm tắt những phần sẽ dùng trực tiếp.")
d.dot("Bài 1, mục 1.2: các loại dữ liệu marketing, dữ liệu giao dịch và dữ liệu hành vi số.")
d.dot("Bài 2, mục 2.1: phân tích mô tả; phần quản trị dữ liệu: chất lượng dữ liệu, giá trị thiếu, quy tắc xử lý ngoại lệ.")
d.dot("Bài 3, mục 3.3.2: mô hình RFM, ý nghĩa và chiều đọc của ba chỉ số Recency, Frequency, Monetary.")
d.dot("Bài 3, mục 3.2: nguyên lý phân cụm, K-means, chọn số cụm bằng Elbow và Silhouette, Hierarchical Clustering, DBSCAN và bảng so sánh ba phương pháp.")
d.dot("Bài 5, mục 5.2: RFM gắn với giá trị vòng đời khách hàng (CLV) và nguyên tắc ưu tiên can thiệp theo giá trị.")
d.dot("Bài 9 và Bài 10: xây dựng Marketing KPI để theo dõi kết quả sau khi triển khai khuyến nghị.")
d.para("Về công cụ, sinh viên chọn một trong ba: Python (pandas, scikit-learn, scipy, matplotlib), R (stats, cluster, factoextra) hoặc SPSS. Hướng dẫn trong đề cương viết theo Python và ghi chú lệnh tương đương của R và SPSS ở những bước khác nhau nhiều.")

# ------------------------------------------------------------------ 12.1
d.h1("12.1. Ôn tập kiến thức lý thuyết trọng tâm")
d.h2("12.1.1. Quy trình phân cụm bảy bước")
d.para("Phân tích cụm (cluster analysis) là kỹ thuật học không giám sát: dữ liệu không có nhãn, thuật toán tự chia các đối tượng thành nhóm sao cho đối tượng trong cùng nhóm giống nhau nhất và các nhóm khác nhau rõ nhất (Bài 3, mục 3.2.1). Kết quả phân cụm phụ thuộc vào từng quyết định của người phân tích. Vì vậy bài thực hành chấm cả quy trình lẫn con số cuối cùng. Quy trình gồm bảy bước:")
for s in [
    "Bước 1. Xác định câu hỏi kinh doanh và đối tượng phân cụm: khách hàng, sản phẩm hay điểm giao hàng.",
    "Bước 2. Chọn biến đầu vào phù hợp với câu hỏi. Biến dùng để phân cụm khác với biến dùng để mô tả cụm sau này.",
    "Bước 3. Kiểm tra chất lượng dữ liệu: dòng trùng, giá trị thiếu, giá trị vô lý.",
    "Bước 4. Phát hiện và quyết định cách xử lý điểm ngoại lệ.",
    "Bước 5. Chuẩn hoá biến để các biến có đơn vị khác nhau đóng góp ngang nhau vào khoảng cách.",
    "Bước 6. Chọn thuật toán và tham số: K, phương pháp liên kết, ε và MinPts; kiểm tra bằng chỉ số và đồ thị.",
    "Bước 7. Diễn giải: lập bảng chân dung, đặt tên, kiểm tra độ ổn định và viết khuyến nghị.",
]:
    d.dot(s)
d.para("Trong đề bài, Yêu cầu 1 tương ứng bước 3 đến bước 5, Yêu cầu 2 và 3 tương ứng bước 6 và 7, Yêu cầu 4 tổng hợp và đưa kết quả về quyết định kinh doanh.")

d.h2("12.1.2. Điểm ngoại lệ theo quy tắc khoảng tứ phân vị")
d.para("Quy tắc khoảng tứ phân vị (interquartile range, IQR) do Tukey (1977) đề xuất. Gọi Q1 là tứ phân vị thứ nhất (25% quan sát nhỏ hơn), Q3 là tứ phân vị thứ ba (75% quan sát nhỏ hơn). Khi đó IQR = Q3 − Q1. Tukey dùng hai cặp ngưỡng, gọi là hàng rào trong và hàng rào ngoài:")
d.dot("Hàng rào trong: Q1 − 1,5·IQR và Q3 + 1,5·IQR. Quan sát vượt hàng rào trong là ngoại lệ nhẹ (mild outlier).")
d.dot("Hàng rào ngoài: Q1 − 3·IQR và Q3 + 3·IQR. Quan sát vượt hàng rào ngoài là ngoại lệ cực trị (extreme outlier).")
d.para("Đề bài yêu cầu ngưỡng ngoại lệ cực trị, tức Q3 + 3·IQR. Với biến chi tiêu, ngưỡng dưới thường âm nên không có ý nghĩa; chỉ cần xét ngưỡng trên. Quy tắc IQR dựa trên thứ hạng nên không bị chính các giá trị cực đoan kéo lệch như quy tắc ba độ lệch chuẩn. Đây là lý do nên dùng IQR cho dữ liệu chi tiêu, vốn lệch phải mạnh.")
d.para("Các phần mềm nội suy tứ phân vị theo cách khác nhau. pandas mặc định dùng nội suy tuyến tính, giống QUARTILE.INC của Excel và type = 7 của R; SPSS dùng cách weighted average. Chênh lệch trên 3.000 quan sát rất nhỏ, nhưng báo cáo cần ghi rõ công cụ.")
d.example("Ví dụ 12.1. Tính ngưỡng ngoại lệ cực trị trên mười khách hàng (số tự đặt)")
d.para("Chi tiêu 12 tháng của mười khách hàng, đơn vị triệu đồng, đã sắp xếp tăng dần: 0,4; 0,8; 1,1; 1,5; 2,0; 2,6; 3,2; 4,0; 5,5; 31,0. Theo nội suy tuyến tính, Q1 nằm ở vị trí (10 − 1) × 0,25 = 2,25 tính từ 0, tức Q1 = 1,1 + 0,25 × (1,5 − 1,1) = 1,2. Q3 nằm ở vị trí 6,75, tức Q3 = 3,2 + 0,75 × (4,0 − 3,2) = 3,8. IQR = 3,8 − 1,2 = 2,6.")
d.para("Ngưỡng ngoại lệ nhẹ là 3,8 + 1,5 × 2,6 = 7,7 triệu đồng. Ngưỡng ngoại lệ cực trị là 3,8 + 3 × 2,6 = 11,6 triệu đồng. Chỉ khách hàng chi 31,0 triệu vượt ngưỡng. Người này chiếm 10% số khách nhưng đóng góp 31,0 / 52,1 = 59,5% tổng chi tiêu. Phép tính này giống hệt phép tính đề bài yêu cầu ở Yêu cầu 1b, chỉ khác quy mô.")

d.h2("12.1.3. Khoảng cách và chuẩn hoá biến")
d.para("K-means và Hierarchical Clustering với liên kết Ward đều đo mức giống nhau bằng khoảng cách Euclidean. Giữa hai khách hàng i và j có p biến, khoảng cách là d(i, j) = √[Σ (x_ik − x_jk)²]. Công thức cộng bình phương chênh lệch của từng biến, nên biến nào có đơn vị lớn sẽ chiếm gần hết khoảng cách. Recency đo bằng ngày (hàng chục, hàng trăm), Frequency đo bằng lần (hàng đơn vị), Monetary đo bằng đồng (hàng triệu). Nếu không chuẩn hoá, khoảng cách gần như chỉ phản ánh chênh lệch chi tiêu (Bài 3, mục 3.2.1).")
d.para("Cách chuẩn hoá phổ biến nhất là z-score: z = (x − trung bình) / độ lệch chuẩn. Sau chuẩn hoá, mỗi biến có trung bình 0 và độ lệch chuẩn 1. Trong Python dùng sklearn.preprocessing.StandardScaler. Lưu ý StandardScaler chia cho độ lệch chuẩn tổng thể (chia n), còn hàm scale() của R và Descriptives của SPSS chia cho độ lệch chuẩn mẫu (chia n − 1). Với vài nghìn quan sát, chênh lệch không đáng kể. Khi biến lệch phải mạnh như Monetary, có thể lấy logarit trước khi chuẩn hoá (numpy.log1p). Đây là lựa chọn bổ sung, phải nêu lý do nếu dùng, vì nó làm thay đổi hình dạng cụm.")
d.example("Ví dụ 12.2. Khoảng cách thay đổi thế nào sau chuẩn hoá (số tự đặt)")
d.para("Ba khách hàng có (R, F, M) như sau. A: 10 ngày, 12 lần, 8,0 triệu. B: 200 ngày, 2 lần, 8,2 triệu. C: 12 ngày, 11 lần, 6,0 triệu. Về hành vi, A và C đều là khách mua đều đặn; B đã lâu không quay lại. Giả sử độ lệch chuẩn của ba biến trong toàn tệp là 80 ngày, 5 lần và 10 triệu đồng.")
d.caption("Bảng 12.1. Khoảng cách Euclidean trước và sau chuẩn hoá")
d.table([
    ["Cặp khách hàng", "Khoảng cách trên dữ liệu thô", "Khoảng cách trên z-score", "Nhận xét"],
    ["A và B", "≈ 200.000", "≈ 3,11", "Thô: rất gần vì chi tiêu gần bằng nhau"],
    ["A và C", "≈ 2.000.000", "≈ 0,28", "Chuẩn hoá: gần vì hành vi mua giống nhau"],
], widths=[2,2,2,4])
d.para("Trên dữ liệu thô, A gần B hơn C gấp mười lần, dù B là khách sắp rời bỏ. Sau chuẩn hoá, chênh lệch R của A và B là 190 / 80 = 2,375 độ lệch chuẩn, chênh lệch F là 10 / 5 = 2 độ lệch chuẩn, nên khoảng cách bằng √(2,375² + 2² + 0,02²) ≈ 3,11. Thứ tự gần xa đã đảo ngược và khớp với trực giác kinh doanh. Yêu cầu 1d chứng minh đúng hiện tượng này trên toàn tệp.")

d.h2("12.1.4. K-means, Elbow Method và Silhouette Score")
d.para("K-means coi một cụm là tập các điểm gần một tâm cụm (centroid) hơn mọi tâm khác. Thuật toán tối thiểu hoá inertia, còn gọi là WCSS (within-cluster sum of squares): tổng bình phương khoảng cách từ mỗi điểm tới tâm cụm của nó (Bài 3, mục 3.2.2a). Ba hệ quả cần nhớ khi thực hành:")
d.dot("Tâm cụm là trung bình, nên một vài điểm cực đoan đủ kéo lệch tâm hoặc chiếm riêng một cụm.")
d.dot("Tâm khởi tạo ngẫu nhiên, nên phải chạy nhiều lần và giữ nghiệm tốt nhất. Trong scikit-learn đặt n_init=10 và cố định random_state. Từ phiên bản 1.4, giá trị mặc định n_init=\"auto\" chỉ chạy một lần khi khởi tạo bằng k-means++, nên cần khai báo rõ.")
d.dot("Inertia luôn giảm khi K tăng. Không được chọn K chỉ vì inertia nhỏ nhất.")
d.para("Elbow Method vẽ inertia theo K và tìm điểm gãy, nơi tăng thêm một cụm không còn làm inertia giảm nhiều. Điểm gãy đôi khi không rõ, nên cần thêm Silhouette Score (Rousseeuw, 1987). Với mỗi điểm i, gọi a(i) là khoảng cách trung bình tới các điểm cùng cụm, b(i) là khoảng cách trung bình nhỏ nhất tới các điểm của một cụm khác. Hệ số silhouette của điểm i là s(i) = [b(i) − a(i)] / max{a(i), b(i)}, nhận giá trị từ −1 đến 1. Silhouette Score của cả mô hình là trung bình s(i) trên mọi điểm.")
d.caption("Bảng 12.2. Thang đọc Silhouette Score (Kaufman và Rousseeuw, 1990)")
d.table([
    ["Silhouette trung bình", "Cách đọc cấu trúc cụm"],
    ["0,71 đến 1,00", "Cấu trúc mạnh"],
    ["0,51 đến 0,70", "Cấu trúc hợp lý"],
    ["0,26 đến 0,50", "Cấu trúc yếu, có thể do thuật toán tạo ra"],
    ["0,25 trở xuống", "Không tìm thấy cấu trúc đáng kể"],
], widths=[1,2])
d.para("Silhouette cao chưa đủ để kết luận phân cụm tốt. Mô hình dành riêng vài cụm cho vài chục điểm cực đoan vẫn có thể đạt silhouette cao. Do đó luôn báo cáo silhouette kèm quy mô từng cụm.")

d.h2("12.1.5. Hierarchical Clustering và các phương pháp liên kết")
d.para("Phân cụm phân cấp kiểu gộp (agglomerative) bắt đầu với mỗi đối tượng là một cụm, rồi lần lượt gộp hai cụm gần nhau nhất cho tới khi còn một cụm. Kết quả là dendrogram: trục tung là khoảng cách tại thời điểm gộp. Cắt ngang dendrogram ở một độ cao cho ra một phương án số cụm. Khoảng cách giữa hai cụm được định nghĩa bằng phương pháp liên kết (linkage) như Bảng 12.3.")
d.caption("Bảng 12.3. Bốn phương pháp liên kết thường gặp")
d.table([
    ["Phương pháp", "Khoảng cách giữa hai cụm", "Đặc điểm kết quả"],
    ["Single", "Khoảng cách nhỏ nhất giữa hai điểm thuộc hai cụm", "Dễ tạo chuỗi (chaining): cụm dài, cụm chỉ có một phần tử"],
    ["Complete", "Khoảng cách lớn nhất giữa hai điểm thuộc hai cụm", "Cụm gọn, đường kính nhỏ, nhạy với ngoại lệ"],
    ["Average", "Trung bình khoảng cách mọi cặp điểm giữa hai cụm", "Trung gian giữa single và complete"],
    ["Ward", "Mức tăng tổng bình phương nội cụm khi gộp hai cụm", "Cụm cân đối về quy mô; cần khoảng cách Euclidean"],
], widths=[1.2,3,3])
d.para("Ward (1963) chọn cặp cụm mà khi gộp làm tổng bình phương nội cụm tăng ít nhất. Tiêu chí này cùng bản chất với inertia của K-means, nên Ward thường cho cụm cân đối và là lựa chọn được khuyến nghị cho dữ liệu marketing (Bài 3, mục 3.2.2b). Trong R, cần dùng method = \"ward.D2\" với ma trận khoảng cách Euclidean; tuỳ chọn \"ward.D\" cũ cho kết quả khác. Hạn chế của phương pháp phân cấp là độ phức tạp tối thiểu O(n²) về bộ nhớ và không quay lui được sau khi đã gộp. Với 16 quan sát, hạn chế này không còn ý nghĩa.")
d.para("Cách chọn ngưỡng cắt: tìm đoạn thẳng đứng dài nhất trên dendrogram mà không bị đường gộp nào cắt ngang. Cắt ở giữa đoạn đó cho phương án có khoảng cách giữa các cụm lớn nhất so với khoảng cách bên trong. Sau đó đối chiếu với silhouette và với khả năng đặt tên cho từng nhóm.")

d.h2("12.1.6. DBSCAN và biểu đồ k-distance")
d.para("DBSCAN (Ester và cộng sự, 1996) coi cụm là vùng liên thông có mật độ cao. Hai tham số là ε (bán kính lân cận) và MinPts (số điểm tối thiểu trong bán kính ε, tính cả chính điểm đó). Điểm có ít nhất MinPts điểm trong bán kính ε là điểm lõi; điểm nằm trong bán kính của một điểm lõi nhưng không đủ điều kiện lõi là điểm biên; các điểm còn lại là nhiễu, được gán nhãn −1. Khác với K-means, DBSCAN không cần biết trước số cụm và không ép điểm rải rác vào cụm nào (Bài 3, mục 3.2.2c).")
d.para("Cách chọn tham số theo Ester và cộng sự (1996) và Schubert và cộng sự (2017): với dữ liệu hai chiều, MinPts thường bằng 4; với dữ liệu nhiều điểm hoặc nhiều nhiễu, tăng MinPts lên khoảng 2 lần số chiều hoặc hơn. Sau đó vẽ biểu đồ k-distance: với mỗi điểm, tính khoảng cách tới láng giềng thứ k (k = MinPts − 1 nếu không tính chính điểm), sắp xếp giảm dần hoặc tăng dần và vẽ. Giá trị ε hợp lý nằm ở chỗ đường cong bẻ gập, nơi khoảng cách bắt đầu tăng vọt.")

d.caption("Bảng 12.4. So sánh ba phương pháp phân cụm dùng trong buổi thực hành")
d.table([
    ["Tiêu chí", "K-means", "Hierarchical", "DBSCAN"],
    ["Định nghĩa cụm", "Gần một tâm cụm", "Một nhánh của dendrogram", "Vùng liên thông mật độ cao"],
    ["Tham số phải chọn", "K, n_init, random_state", "Linkage, ngưỡng cắt", "ε, MinPts"],
    ["Cần chuẩn hoá", "Có", "Có", "Không với toạ độ địa lý"],
    ["Điểm ngoại lệ", "Bị ép vào cụm, kéo lệch tâm", "Bị ép vào cụm, có thể tách thành nhánh riêng", "Tách thành nhiễu (−1)"],
    ["Quy mô phù hợp", "Rất lớn", "Nhỏ, dưới vài nghìn", "Trung bình đến lớn"],
    ["Tệp LUMI phù hợp", "Khách hàng", "Nhóm sản phẩm", "Điểm giao hàng"],
], widths=[1.4,2,2,2])

# ------------------------------------------------------------------ 12.2
d.h1("12.2. Tình huống và dữ liệu")
d.h2("12.2.1. Bối cảnh doanh nghiệp LUMI")
d.para("LUMI là chuỗi bán lẻ mỹ phẩm và sản phẩm chăm sóc cá nhân giả định với 24 cửa hàng tại Hà Nội, một website và một ứng dụng di động. Doanh thu năm tài chính 2025 đến 2026 khoảng 420 tỷ đồng, biên lợi nhuận gộp bình quân 34%. Chương trình thành viên có 3.000 khách hàng đang hoạt động. LUMI chăm sóc mọi thành viên theo một cách: mỗi tháng gửi cùng một tin nhắn khuyến mại, mỗi quý gửi cùng một voucher giảm 15%.")
d.para("Kết quả 12 tháng gần nhất có ba tín hiệu xấu. Tỷ lệ phản hồi chiến dịch giảm từ 24% xuống 19%. Chi phí chăm sóc khách hàng tăng 28% trong khi doanh thu từ thành viên chỉ tăng 6%. Chi phí giao hàng chặng cuối tăng 41%, trong khi số đơn chỉ tăng 12%. Giám đốc điều hành đặt ba câu hỏi: khách hàng chia thành mấy nhóm và mỗi nhóm nên được chăm sóc thế nào; 16 nhóm sản phẩm gom được thành mấy họ để thiết kế chính sách giá và khuyến mại; đơn online tập trung ở khu vực nào và có nên lập điểm trung chuyển không.")
d.para("Ba câu hỏi nối thẳng với ba tín hiệu xấu. Câu hỏi về nhóm khách giải thích vì sao chi phí chăm sóc tăng nhanh hơn doanh thu. Câu hỏi về họ sản phẩm liên quan tới voucher 15% áp đồng loạt lên mọi mặt hàng có biên lợi nhuận khác nhau. Câu hỏi về khu vực giao hàng liên quan tới chi phí chặng cuối. Khi viết khuyến nghị ở Yêu cầu 4, sinh viên nên quay lại ba tín hiệu này.")

d.h2("12.2.2. Mô tả các tệp dữ liệu")
d.para("Kỳ dữ liệu từ 01/04/2025 đến 31/03/2026, ngày phân tích quy ước là 31/03/2026. Dữ liệu gồm ba tệp .csv và một tệp Excel tổng hợp. Lưu ý: đề bài ghi tên tệp Excel là LUMI_du_lieu_BTVN_Bai3.xlsx, còn tệp phát trên thư mục học phần có tên LUMI_du_lieu.xlsx. Nội dung hai cách gọi là một.")
d.caption("Bảng 12.5. Ba tệp dữ liệu của tình huống LUMI")
d.table([
    ["Tệp", "Số dòng", "Đơn vị quan sát", "Dùng cho"],
    ["LUMI_khach_hang.csv", "3.000", "Một khách hàng thành viên", "Yêu cầu 1 và 2, K-means"],
    ["LUMI_nhom_san_pham.csv", "16", "Một nhóm sản phẩm", "Yêu cầu 3, Hierarchical"],
    ["LUMI_diem_giao_hang.csv", "1.140", "Một đơn giao online trong 30 ngày", "Vùng giao hàng, DBSCAN, khuyến nghị ở Yêu cầu 4"],
], widths=[2.6,1,2.4,2.4])
d.caption("Bảng 12.6. Các cột của tệp khách hàng")
d.table([
    ["Cột", "Ý nghĩa", "Đơn vị"],
    ["MaKH", "Mã khách hàng thành viên", "chuỗi"],
    ["GioiTinh, NamSinh, Quan", "Nhân khẩu học và quận đăng ký", "chuỗi, năm"],
    ["SoNgayTuLanMuaGanNhat", "Recency: số ngày từ lần mua gần nhất tới 31/03/2026", "ngày"],
    ["SoLanMua_12T", "Frequency: số lần mua trong 12 tháng", "lần"],
    ["TongChiTieu_12T", "Monetary: tổng chi tiêu trong 12 tháng", "đồng"],
    ["GiaTriDonTrungBinh", "Giá trị đơn trung bình", "đồng"],
    ["SoLanDungVoucher", "Số lần dùng voucher trong 12 tháng", "lần"],
    ["SoPhienApp_30Ngay", "Số phiên dùng ứng dụng trong 30 ngày", "phiên"],
    ["TyLeMuaOnline", "Tỷ trọng đơn online trên tổng số đơn", "0 đến 1"],
    ["PhanHoiChienDich", "Có phản hồi chiến dịch gần nhất hay không", "1 có, 0 không"],
], widths=[2.4,4,1.2])
d.para("Ba biến RFM là biến đầu vào của K-means. Các biến còn lại dùng để mô tả chân dung cụm ở Yêu cầu 2c. Cụm được hình thành từ hành vi giao dịch, sau đó mới so sánh các cụm về kênh mua, voucher và phản hồi.")
d.para("Tệp nhóm sản phẩm có cột NhomSanPham làm nhãn và sáu thuộc tính: giá bán trung bình (đồng), số lần mua lại trên một khách trong 12 tháng, tỷ lệ mua kèm voucher, tỷ trọng khách mới, tỷ lệ trả hàng và biên lợi nhuận gộp; bốn biến cuối là tỷ lệ từ 0 đến 1. Tệp điểm giao hàng có mã đơn, vĩ độ, kinh độ dạng thập phân, giá trị đơn (đồng) và số ngày giao. Tệp Excel có sheet hướng dẫn riêng cho hai tệp này.")
d.h2("12.2.3. Lưu ý về chất lượng dữ liệu và môi trường làm việc")
d.para("Đề bài nói rõ tệp khách hàng được trích nguyên trạng, chưa làm sạch. Việc tìm ra vấn đề là một phần của bài. Sinh viên không nên mở tệp bằng Excel rồi lưu đè, vì Excel có thể đổi định dạng số thập phân, ngày tháng và bảng mã tiếng Việt. Nên đọc trực tiếp bằng pandas với encoding=\"utf-8-sig\" để bỏ ký tự BOM ở đầu tệp.")
d.para("Đặt một hằng số SEED = 42 ở đầu sổ tay và dùng chung cho mọi bước có yếu tố ngẫu nhiên để giảng viên chạy lại được kết quả.")

# ------------------------------------------------------------------ 12.3
d.h1("12.3. Hướng dẫn Yêu cầu 1: Chuẩn bị dữ liệu khách hàng")
d.h2("12.3.1. Mục đích")
d.para("Yêu cầu 1 (2,0 điểm) kiểm tra bước 3 đến bước 5 của quy trình. Mọi sai sót ở đây đi thẳng vào K-means ở Yêu cầu 2. Điểm cao không nằm ở việc ra đúng con số mà ở việc mỗi quyết định xử lý có lý do rõ ràng.")
d.h2("12.3.2. Câu a: kiểm tra dòng trùng và giá trị thiếu")
d.para("Các bước làm như sau.")
d.dot("Đếm dòng trùng hoàn toàn bằng df.duplicated().sum() và dòng trùng mã khách hàng bằng df[\"MaKH\"].duplicated().sum(). Hai con số này có thể khác nhau; mã khách hàng trùng là lỗi nghiêm trọng hơn.")
d.dot("Đếm giá trị thiếu theo cột bằng df.isna().sum(). Trình bày thành bảng: tên cột, số ô thiếu, tỷ lệ phần trăm.")
d.dot("Kiểm tra giá trị vô lý bằng df.describe(): số lần mua bằng 0 nhưng chi tiêu dương, tỷ lệ online ngoài khoảng 0 đến 1, năm sinh bất thường.")
d.para("Với mỗi cột thiếu, chọn một trong ba cách và giải thích. Thứ nhất, suy ra từ các cột khác khi có quan hệ định nghĩa. Ví dụ, giá trị đơn trung bình về định nghĩa bằng tổng chi tiêu chia số lần mua; nếu cột này thiếu mà hai cột kia đủ thì tính lại được chính xác. Thứ hai, điền bằng trung vị khi cột không suy ra được và tỷ lệ thiếu nhỏ; trung vị ít bị ngoại lệ kéo lệch hơn trung bình. Thứ ba, xoá dòng khi dòng thiếu biến đầu vào của mô hình và không có cách suy ra. Khi xoá, ghi rõ số dòng bị xoá và kiểm tra những dòng đó có khác biệt hệ thống với phần còn lại không.")
d.h2("12.3.3. Câu b: phân bố RFM và ngưỡng ngoại lệ của Monetary")
d.para("Vẽ histogram cho ba biến, đặt cạnh nhau trên một hình (plt.subplots(1, 3)). Có thể thêm boxplot cho Monetary để nhìn thấy các điểm nằm ngoài râu. Khi nhận xét, mô tả hình dạng phân bố: lệch trái hay lệch phải, có đuôi dài không, có nhiều giá trị tập trung ở một đầu không.")
d.para("Tính ngưỡng theo mục 12.1.2: q1, q3 = df[\"TongChiTieu_12T\"].quantile([0.25, 0.75]); iqr = q3 − q1; nguong = q3 + 3 * iqr. Sau đó tính ba con số mà đề hỏi: số khách vượt ngưỡng, tỷ lệ phần trăm số khách và tỷ lệ phần trăm tổng doanh thu. Tỷ lệ doanh thu bằng tổng chi tiêu của nhóm vượt ngưỡng chia tổng chi tiêu của cả tệp. Hai tỷ lệ này thường chênh nhau rất xa, giống Ví dụ 12.1. Chính khoảng chênh đó quyết định cách xử lý ở câu c.")
d.h2("12.3.4. Câu c: giữ lại, xoá bỏ hay tách riêng")
d.para("Câu hỏi yêu cầu lập luận từ hai góc nhìn. Bảng 12.7 gợi ý khung so sánh ba phương án; sinh viên điền nhận định của nhóm dựa trên số liệu ở câu b.")
d.caption("Bảng 12.7. Khung lập luận cho quyết định xử lý ngoại lệ")
d.table([
    ["Phương án", "Góc nhìn kỹ thuật", "Góc nhìn kinh doanh"],
    ["Giữ lại trong mô hình", "Ngoại lệ kéo lệch tâm cụm, có thể chiếm riêng một cụm nhỏ", "Không mất khách nào khỏi phân tích"],
    ["Xoá bỏ", "Mô hình sạch hơn", "Mất phần doanh thu mà nhóm này đóng góp; khuyến nghị bỏ sót nhóm có giá trị"],
    ["Tách riêng", "Mô hình sạch hơn, cụm phản ánh khách bán lẻ", "Nhóm được phân tích và chăm sóc bằng chính sách riêng"],
], widths=[1.2,2.5,2.5])
d.para("Khi lập luận góc nhìn kinh doanh, hãy đặt giả thuyết về danh tính của nhóm ngoại lệ dựa trên dữ liệu: giá trị đơn trung bình, tần suất, tỷ lệ online. Một khách chi tiêu gấp nhiều lần mức thường có thể là đại lý, spa, người mua hộ hoặc lỗi nhập liệu. Mỗi giả thuyết dẫn tới một cách xử lý khác. Cần ghi lại cỡ mẫu đưa vào phân cụm sau bước này để giảng viên đối chiếu.")
d.h2("12.3.5. Câu d: chứng minh sự cần thiết của chuẩn hoá")
d.para("Lập bảng thống kê mô tả ba biến RFM bằng df[cols].agg([\"mean\", \"std\", \"min\", \"max\"]).T. So sánh độ lệch chuẩn giữa ba biến và giải thích theo công thức khoảng cách ở mục 12.1.3. Sau đó chạy hai mô hình K-means với K = 4: một trên dữ liệu thô, một trên dữ liệu đã qua StandardScaler. Với mỗi mô hình, báo cáo silhouette_score và số khách mỗi cụm (np.bincount(labels)).")
d.para("Đề bài không nói rõ chạy câu d trên tệp đầy đủ hay tệp đã tách ngoại lệ. Nhóm cần ghi rõ lựa chọn của mình. Khi đọc kết quả, chú ý hiện tượng đã nêu ở mục 12.1.4: mô hình trên dữ liệu thô có thể có silhouette cao hơn nhưng quy mô cụm rất lệch. Nhận xét đúng là so sánh cả hai thông tin, không kết luận chỉ từ silhouette.")
d.h2("12.3.6. Cạm bẫy thường gặp và sản phẩm cần nộp")
d.dot("Dùng ngưỡng 1,5·IQR thay vì 3·IQR như đề yêu cầu.")
d.dot("Xoá dòng thiếu ở cột suy ra được, làm mất khách hàng không cần thiết.")
d.dot("Chuẩn hoá trước rồi mới tách ngoại lệ, khiến trung bình và độ lệch chuẩn dùng để chuẩn hoá bị ngoại lệ chi phối. Thứ tự đúng là tách ngoại lệ, rồi fit StandardScaler trên phần còn lại.")
d.dot("Báo cáo silhouette mà không báo quy mô cụm.")
d.para("Sản phẩm của Yêu cầu 1: bảng chất lượng dữ liệu kèm cách xử lý từng cột; ba biểu đồ phân bố; bảng ngưỡng IQR và ba con số về nhóm vượt ngưỡng; đoạn lập luận hai góc nhìn; bảng thống kê mô tả; bảng so sánh K-means thô và chuẩn hoá.")

# ------------------------------------------------------------------ 12.4
d.h1("12.4. Hướng dẫn Yêu cầu 2: Phân khúc khách hàng bằng K-means")
d.h2("12.4.1. Câu a và b: chọn số cụm K")
d.para("Chạy vòng lặp K từ 2 đến 8 trên ba biến RFM đã chuẩn hoá. Với mỗi K, khởi tạo KMeans(n_clusters=k, n_init=10, random_state=SEED), gọi fit, lưu model.inertia_ và silhouette_score(Xs, model.labels_). Lập bảng hai dòng inertia và silhouette theo K, vẽ hai biểu đồ đường. Trong R, dùng kmeans(Xs, centers = k, nstart = 25) và hàm silhouette của gói cluster. SPSS không tính silhouette cho K-means; sinh viên dùng SPSS cần xuất nhãn cụm và tính silhouette bằng công cụ khác hoặc chỉ dựa vào bảng ANOVA kèm Elbow và nêu rõ hạn chế.")
d.para("Đọc hai biểu đồ cùng nhau. Nếu điểm gãy của Elbow trùng với đỉnh silhouette, lựa chọn rõ ràng. Nếu hai tiêu chí lệch nhau, đề bài yêu cầu nêu tiêu chí ưu tiên và lý do. Lý do tốt dựa trên ba điểm: thang đọc silhouette ở Bảng 12.2, quy mô các cụm và khả năng đặt tên, hành động cho từng cụm.")
d.example("Ví dụ 12.3. Khi Elbow và Silhouette không trùng nhau (số tự đặt)")
d.caption("Bảng 12.8. Inertia và Silhouette của một tệp khách hàng giả định")
d.table([
    ["K", "2", "3", "4", "5", "6"],
    ["Inertia", "5.200", "3.100", "2.250", "1.900", "1.700"],
    ["Silhouette", "0,46", "0,41", "0,44", "0,38", "0,35"],
])
d.para("Inertia giảm 2.100 khi đi từ K = 2 lên 3, giảm 850 khi lên 4, rồi chỉ giảm 350 và 200. Điểm gãy nằm quanh K = 3 hoặc 4. Silhouette cao nhất ở K = 2. Tuy vậy, hai nhóm khách thường quá thô cho mục đích chăm sóc khác biệt. K = 4 có silhouette chỉ thấp hơn K = 2 là 0,02, vẫn trong vùng cấu trúc yếu như K = 2, nhưng cho thêm hai phân khúc có thể hành động. Nhóm phân tích trong ví dụ này chọn K = 4 và nêu rõ đánh đổi. Lưu ý rằng mọi giá trị silhouette ở đây đều dưới 0,51, nên báo cáo cần thừa nhận cấu trúc cụm chưa mạnh.")
d.h2("12.4.2. Câu c và d: chân dung và tên phân khúc")
d.para("Sau khi chọn K, gắn nhãn cụm vào bảng dữ liệu gốc chưa chuẩn hoá: df[\"Cum\"] = model.labels_. Lập bảng chân dung bằng groupby với các chỉ số đề yêu cầu. Trung bình tính trên giá trị gốc để người kinh doanh đọc được bằng ngày, lần và đồng. Tỷ trọng doanh thu của mỗi cụm bằng tổng TongChiTieu_12T của cụm chia tổng của mọi khách đưa vào mô hình. Nên thêm một dòng cho nhóm ngoại lệ đã tách ở Yêu cầu 1 để ban giám đốc thấy toàn bộ khách hàng.")
d.caption("Bảng 12.9. Mẫu bảng chân dung phân khúc (sinh viên điền số liệu)")
d.table([
    ["Chỉ số", "Phân khúc 1", "Phân khúc 2", "…", "Nhóm tách riêng"],
    ["Số khách và tỷ lệ số khách", "", "", "", ""],
    ["Recency TB (ngày)", "", "", "", ""],
    ["Số lần mua TB, chi tiêu TB (đồng)", "", "", "", ""],
    ["Giá trị đơn TB (đồng), số phiên app TB", "", "", "", ""],
    ["Tỷ lệ mua online, tỷ lệ phản hồi", "", "", "", ""],
    ["Tỷ trọng doanh thu", "", "", "", ""],
], widths=[3,1.3,1.3,0.6,1.5])
d.para("Đặt tên theo đặc điểm kinh doanh. Tên tốt cho biết khách thuộc nhóm làm gì và nên được đối xử ra sao, ví dụ nhóm mua gần đây và thường xuyên, nhóm lâu không quay lại. Có thể tham khảo năm nhãn RFM của Bài 3 (Champions, khách trung thành, khách mới, At Risk, Hibernating) nhưng phải kiểm tra lại bằng số liệu, không gán nhãn theo thói quen. Mỗi phân khúc kèm một câu chân dung điển hình, viết như mô tả một người: mua bao lâu một lần, mỗi lần bao nhiêu tiền, mua qua kênh nào, phản ứng với khuyến mại ra sao.")
d.para("Khi viết chân dung, hãy so tỷ lệ số khách với tỷ lệ doanh thu của từng cụm. Nhóm có tỷ trọng doanh thu cao hơn nhiều so với tỷ trọng số khách là nhóm cần giữ. Nhóm ngược lại là nơi có thể cắt chi phí chăm sóc. Đây là cách nối kết quả phân cụm với nguyên tắc ưu tiên can thiệp theo giá trị ở Bài 5.")
d.h2("12.4.3. Câu e: kiểm tra tính ổn định")
d.para("Chạy lại K-means với K đã chọn và ít nhất năm giá trị random_state khác nhau, ví dụ 0, 1, 7, 42, 123. Báo cáo silhouette nhỏ nhất, lớn nhất và quy mô cụm của mỗi lần chạy. Thứ tự nhãn cụm có thể đổi giữa các lần chạy; so sánh theo quy mô và tâm cụm, không theo số thứ tự nhãn. Có thể đo mức trùng khớp giữa hai lần chạy bằng adjusted_rand_score của scikit-learn; giá trị gần 1 nghĩa là hai phân hoạch gần như giống nhau.")
d.para("Nếu silhouette dao động mạnh, kiểm tra lại n_init, bước chuẩn hoá và bước tách ngoại lệ. Nghiệm ổn định cho thấy cấu trúc cụm có thật, không do khởi tạo ngẫu nhiên.")
d.h2("12.4.4. Cạm bẫy thường gặp và sản phẩm cần nộp")
d.dot("Chạy K-means trên cả cột MaKH hoặc các biến mô tả, làm khoảng cách mất ý nghĩa.")
d.dot("Báo cáo trung bình trên giá trị đã chuẩn hoá, người đọc không hiểu được.")
d.dot("Đặt tên chung chung như nhóm cao, nhóm thấp, hoặc tên không khớp số liệu.")
d.dot("Quên khai báo n_init và random_state, kết quả không lặp lại được.")
d.para("Sản phẩm của Yêu cầu 2: bảng và hai biểu đồ Elbow, Silhouette; đoạn biện luận chọn K; bảng chân dung đầy đủ; tên và câu chân dung cho mỗi phân khúc; bảng kiểm tra ổn định.")

# ------------------------------------------------------------------ 12.5
d.h1("12.5. Hướng dẫn Yêu cầu 3: Nhóm hoá danh mục sản phẩm bằng Hierarchical Clustering")
d.h2("12.5.1. Câu a: vì sao chọn phương pháp phân cấp")
d.para("Đề yêu cầu ít nhất hai lý do. Sinh viên nên lập luận từ đặc điểm của tệp, không chép lại ưu điểm chung. Các hướng lập luận gồm: số quan sát rất nhỏ nên dendrogram đọc được bằng mắt; chưa biết trước số họ sản phẩm; mục tiêu là khám phá cấu trúc danh mục và quan hệ lồng nhau giữa các họ; nhược điểm về tốc độ của phương pháp phân cấp không còn ý nghĩa; K-means trên 16 điểm có tâm cụm thiếu ổn định vì mỗi cụm chỉ có vài điểm.")
d.h2("12.5.2. Câu b: dendrogram và ba phương pháp liên kết")
d.para("Chuẩn hoá sáu thuộc tính bằng StandardScaler. Sáu thuộc tính có đơn vị rất khác nhau: giá tính bằng đồng, số lần mua lại tính bằng lần, bốn biến còn lại là tỷ lệ. Không chuẩn hoá thì giá bán quyết định toàn bộ cây. Với mỗi phương pháp single, complete, ward: Z = linkage(Xs, method=m); nhãn = fcluster(Z, t=4, criterion=\"maxclust\"); tính silhouette_score(Xs, nhãn) và đếm quy mô cụm. Vẽ ba dendrogram cạnh nhau, dùng labels=df[\"NhomSanPham\"].tolist() và orientation=\"right\" để tên nhóm sản phẩm dễ đọc.")
d.para("Khi so sánh, chú ý hai điều. Thứ nhất, single linkage dễ sinh hiện tượng chuỗi: có cụm chỉ gồm một nhóm sản phẩm, có cụm rất dài. Thứ hai, silhouette trên 16 điểm biến động mạnh khi một điểm đổi cụm, nên cần nhìn kèm quy mô cụm và hình dạng cây. Có thể bổ sung hệ số tương quan cophenetic (scipy.cluster.hierarchy.cophenet) để đo mức cây giữ đúng khoảng cách gốc; giá trị càng gần 1 càng tốt.")
d.para("Trong R: hc = hclust(dist(scale(X)), method = \"ward.D2\"); cutree(hc, k = 4); rect.hclust(hc, k = 4). Trong SPSS: Analyze, Classify, Hierarchical Cluster; ở mục Method chọn Ward's method và Squared Euclidean distance, ở mục Transform Values chọn Z scores; ở mục Plots chọn Dendrogram.")
d.h2("12.5.3. Câu c: chọn ngưỡng cắt và đặt tên họ sản phẩm")
d.example("Ví dụ 12.4. Đọc ngưỡng cắt trên dendrogram (số tự đặt)")
d.para("Một dendrogram có các độ cao gộp cuối cùng lần lượt là 0,8; 1,1; 1,3; 2,0; 4,5; 6,8. Khoảng trống lớn nhất nằm giữa 2,0 và 4,5. Cắt ở độ cao khoảng 3,0 sẽ cắt qua ba đường thẳng đứng, cho ba cụm. Cắt ở 1,6 cho bốn cụm, nhưng khoảng trống chỉ 0,7, nghĩa là hai trong bốn cụm khá giống nhau. Quyết định cuối cùng kết hợp khoảng trống, silhouette và khả năng đặt tên.")
d.para("Vẽ dendrogram của phương pháp đã chọn, thêm đường ngang tại ngưỡng cắt bằng plt.axhline(y=h, linestyle=\"--\") và tô màu nhánh bằng tham số color_threshold=h. Liệt kê các nhóm sản phẩm thuộc từng họ. Tên họ nên phản ánh hai hoặc ba thuộc tính nổi bật nhất, ví dụ một họ giá cao và biên cao, một họ mua lặp lại thường xuyên.")
d.h2("12.5.4. Câu d: bảng thuộc tính theo họ và chính sách khuyến mại")
d.para("Tính trung bình sáu thuộc tính theo họ trên giá trị gốc (df.groupby(\"Ho\").mean()). Đọc bảng theo từng cột để tìm thuộc tính phân biệt mỗi họ. Chính sách khuyến mại cần bám vào số liệu: họ có biên lợi nhuận gộp cao chịu được ưu đãi lớn hơn về tiền nhưng có thể không cần giảm giá; họ có tỷ lệ mua kèm voucher đã cao cho thấy khách đã quen chờ khuyến mại; họ có tỷ lệ trả hàng cao cần giảm rủi ro trả hàng trước khi đẩy doanh số; họ mua lại thường xuyên hợp với gói định kỳ hoặc combo.")
d.para("Một phép kiểm tra nhanh cho mỗi chính sách: voucher 15% hiện tại của LUMI lấy đi bao nhiêu điểm phần trăm biên lợi nhuận gộp của mỗi họ. Ví dụ với số tự đặt, một họ có biên gộp 20% mà giảm giá 15% thì chỉ còn khoảng 5 điểm phần trăm biên trên giá gốc, chưa kể chi phí vận hành.")
d.h2("12.5.5. Cạm bẫy thường gặp và sản phẩm cần nộp")
d.dot("Không chuẩn hoá sáu thuộc tính, cây chỉ phản ánh giá bán.")
d.dot("Dùng Ward với khoảng cách không phải Euclidean, hoặc dùng ward.D thay cho ward.D2 trong R.")
d.dot("Chọn ngưỡng cắt mà không đánh dấu trên hình, hoặc chọn theo số đẹp.")
d.dot("Đề xuất chính sách khuyến mại không dẫn chiếu thuộc tính nào trong bảng.")
d.para("Sản phẩm của Yêu cầu 3: hai đến ba câu lý do; bảng so sánh ba phương pháp liên kết; dendrogram có ngưỡng cắt; danh sách họ sản phẩm và tên; bảng trung bình theo họ; một chính sách cho mỗi họ.")

# ------------------------------------------------------------------ 12.6
d.h1("12.6. Dữ liệu điểm giao hàng: phân tích vùng bằng DBSCAN")
d.para("Câu hỏi thứ ba của giám đốc điều hành liên quan tới tệp LUMI_diem_giao_hang.csv. Bảng 1 của đề gắn tệp này với DBSCAN, và Yêu cầu 4 cần kết quả về khu vực để so sánh phương pháp và viết khuyến nghị điểm trung chuyển. Phần này hướng dẫn cách phân tích tệp toạ độ.")
d.h2("12.6.1. Chuẩn bị toạ độ")
d.para("Không chuẩn hoá vĩ độ và kinh độ bằng z-score, vì như vậy làm méo khoảng cách địa lý. Ở vĩ độ Hà Nội, khoảng 21 độ bắc, một độ vĩ ứng với khoảng 111 km còn một độ kinh chỉ khoảng 104 km. Cách đúng là đổi toạ độ sang radian (np.radians) và dùng khoảng cách haversine. Bán kính ε tính bằng km được đổi sang radian bằng cách chia cho bán kính Trái Đất khoảng 6.371 km.")
d.h2("12.6.2. Chọn ε và MinPts bằng biểu đồ k-distance")
d.para("Chọn MinPts trước, theo mục 12.1.6, rồi vẽ k-distance: nn = NearestNeighbors(n_neighbors=MinPts, metric=\"haversine\").fit(X_rad); dist, _ = nn.kneighbors(X_rad); lấy cột cuối nhân 6.371 để ra km, sắp xếp và vẽ. Trong scikit-learn, kneighbors trên chính tập huấn luyện tính cả điểm đó là láng giềng đầu tiên với khoảng cách 0, nên n_neighbors=MinPts khớp với cách DBSCAN đếm min_samples. Đọc ε tại điểm bẻ gập của đường cong.")
d.para("Chạy DBSCAN(eps=eps_km / 6371, min_samples=MinPts, metric=\"haversine\", algorithm=\"ball_tree\").fit(X_rad). Báo cáo số vùng, số đơn mỗi vùng, số điểm nhiễu (nhãn −1) và tỷ lệ nhiễu. Thử thêm hai giá trị ε lân cận để xem kết quả có nhạy không. Vẽ bản đồ phân tán kinh độ, vĩ độ tô màu theo nhãn, điểm nhiễu màu xám. Gọi tên vùng theo địa danh của toạ độ tâm vùng. SPSS không có DBSCAN; trong R dùng gói dbscan với hàm kNNdistplot.")
d.h2("12.6.3. Đối chứng với K-means trên toạ độ")
d.para("Để có tư liệu cho Yêu cầu 4a, chạy K-means trên cùng toạ độ với K bằng số vùng DBSCAN tìm được. So sánh hai điều: K-means có gán điểm nhiễu vào vùng nào không, và bán kính vùng (khoảng cách xa nhất từ tâm tới điểm thuộc vùng) thay đổi thế nào. Câu hỏi kinh doanh: lập tuyến giao hàng theo kết quả nào thì xe chạy ít hơn (Bài 3, mục 3.2.2c).")

# ------------------------------------------------------------------ 12.7
d.h1("12.7. Hướng dẫn Yêu cầu 4: So sánh và khuyến nghị")
d.h2("12.7.1. Câu a: bảng so sánh các phương pháp đã dùng")
d.para("Bảng so sánh cần bốn phương diện đề nêu: yêu cầu về số cụm, cách xử lý điểm ngoại lệ, khả năng mở rộng, và điểm yếu đã bộc lộ trong chính bài tập. Ba phương diện đầu có thể dựa vào Bảng 12.4. Phương diện thứ tư phải lấy từ kết quả của nhóm: ví dụ chênh lệch giữa K-means thô và chuẩn hoá ở Yêu cầu 1d, cụm một phần tử của single linkage ở Yêu cầu 3b, hay điểm nhiễu bị K-means ép vào vùng ở mục 12.6.3. Ô nào chỉ chép lý thuyết chung sẽ không đạt điểm tối đa.")
d.h2("12.7.2. Câu b: khuyến nghị có ước tính tác động tài chính")
d.para("Mỗi khuyến nghị gồm bốn phần: hành động cụ thể; phân khúc, họ sản phẩm hoặc khu vực áp dụng; ước tính tác động tài chính kèm phép tính; chỉ số theo dõi sau triển khai. Phép tính nên ghi rõ giả định nào lấy từ dữ liệu, giả định nào do nhóm đặt ra. Biên lợi nhuận gộp 34% của LUMI giúp quy doanh thu tăng thêm thành lợi nhuận gộp.")
d.example("Ví dụ 12.5. Một khuyến nghị mẫu với số tự đặt")
d.para("Giả sử một chuỗi bán lẻ có phân khúc khách mua một lần gồm 800 khách. Chuỗi đang gửi 12 tin nhắn khuyến mại mỗi năm cho nhóm này, chi phí 2.500 đồng một lượt. Hành động đề xuất: giảm còn 4 tin mỗi năm, thay bằng một chuỗi chào mừng ưu đãi lần mua thứ hai.")
d.caption("Bảng 12.10. Ước tính tác động của khuyến nghị mẫu")
d.table([
    ["Hạng mục", "Phép tính", "Kết quả"],
    ["Chi phí tin nhắn tiết kiệm", "800 khách × (12 − 4) lượt × 2.500 đồng", "16.000.000 đồng/năm"],
    ["Doanh thu tăng thêm từ lần mua thứ hai", "800 × 3% khách quay lại × 400.000 đồng mỗi đơn", "9.600.000 đồng"],
    ["Lợi nhuận gộp tăng thêm", "9.600.000 × 34%", "3.264.000 đồng"],
    ["Tổng tác động lên lợi nhuận", "16.000.000 + 3.264.000", "≈ 19,3 triệu đồng/năm"],
], widths=[2,3,1.8])
d.para("Chỉ số theo dõi: tỷ lệ mua lần hai trong 60 ngày, tỷ lệ huỷ nhận tin, chi phí chăm sóc trên mỗi khách. Nên giữ một nhóm đối chứng nhỏ tiếp tục nhận chính sách cũ để đo tác động thật. Cách xây chỉ số và dashboard theo dõi đã học ở Bài 9 và Bài 10.")
d.para("Khuyến nghị về điểm trung chuyển giao hàng làm tương tự: số đơn trong các vùng mật độ cao nhân với mức tiết kiệm chi phí chặng cuối giả định cho mỗi đơn, quy ra năm, rồi so với chi phí thuê và vận hành điểm trung chuyển. Khuyến nghị chỉ có giá trị khi so cả lợi ích và chi phí.")
d.h2("12.7.3. Cạm bẫy thường gặp")
d.dot("Khuyến nghị chung chung, không có phân khúc hay khu vực cụ thể.")
d.dot("Có con số tác động nhưng không có phép tính và giả định.")
d.dot("Tính tác động bằng doanh thu mà quên biên lợi nhuận và chi phí triển khai.")
d.dot("Không nêu chỉ số theo dõi, ban giám đốc không biết khi nào khuyến nghị thành công.")

# ------------------------------------------------------------------ 12.8
d.h1("12.8. Sản phẩm nộp và tiêu chí đánh giá")
d.para("Mỗi nhóm nộp cuối buổi hai tệp: báo cáo Word hoặc PDF theo thứ tự các yêu cầu, và tệp mã nguồn chạy lại được từ dữ liệu gốc. Bảng và biểu đồ có số thứ tự và tên. Thang điểm theo đề bài như Bảng 12.11.")
d.caption("Bảng 12.11. Thang điểm và tiêu chí chấm")
d.table([
    ["Yêu cầu", "Điểm", "Tiêu chí đạt điểm tối đa"],
    ["1. Chuẩn bị dữ liệu", "2,0", "Đủ kiểm tra trùng, thiếu; cách xử lý có lý do; ngưỡng 3·IQR đúng; lập luận hai góc nhìn; minh chứng chuẩn hoá có silhouette và quy mô cụm"],
    ["2. K-means", "2,5", "Bảng và hai biểu đồ K từ 2 đến 8; biện luận chọn K; bảng chân dung đủ chỉ số; tên có nghĩa kinh doanh; kiểm tra ổn định ít nhất 5 hạt giống"],
    ["3. Hierarchical", "2,0", "Ít nhất hai lý do gắn với tệp; so sánh ba linkage; dendrogram có ngưỡng cắt; họ có tên; chính sách dựa trên bảng thuộc tính"],
    ["4. So sánh và khuyến nghị", "1,5", "Bảng so sánh bốn phương diện có dẫn chứng từ bài; ít nhất hai khuyến nghị đủ bốn phần, có phép tính"],
    ["Tổng", "8,0", "Theo thang điểm ghi trong đề bài"],
], widths=[1.6,0.8,5])

# ------------------------------------------------------------------ end matter
d.plain_heading("Tóm tắt bài học")
d.para("Buổi thực hành vận dụng toàn bộ phần phân cụm của Bài 3 trên ba tệp dữ liệu của chuỗi LUMI. Tệp khách hàng lớn và có ngoại lệ, nên cần làm sạch, tách ngoại lệ theo quy tắc 3·IQR, chuẩn hoá z-score rồi mới chạy K-means. Số cụm chọn bằng Elbow và Silhouette, đọc cùng quy mô cụm và khả năng đặt tên.")
d.para("Tệp sản phẩm chỉ có 16 quan sát, nên Hierarchical Clustering phù hợp hơn. Dendrogram cho thấy mọi phương án số cụm trên một hình; Ward thường cho các họ cân đối. Tệp điểm giao hàng là dữ liệu toạ độ có điểm rải rác, nên DBSCAN với khoảng cách haversine và biểu đồ k-distance cho vùng mật độ cao và tách được nhiễu.")
d.para("Kết quả phân cụm chỉ có giá trị khi chuyển thành hành động. Mỗi khuyến nghị cần đối tượng cụ thể, phép tính tác động tài chính có giả định rõ ràng và chỉ số theo dõi.")

d.plain_heading("CÂU HỎI ÔN TẬP")
for q in [
    "Viết công thức hàng rào trong và hàng rào ngoài của quy tắc IQR. Vì sao quy tắc IQR phù hợp với biến chi tiêu hơn quy tắc ba độ lệch chuẩn?",
    "Giải thích bằng công thức khoảng cách Euclidean vì sao K-means trên dữ liệu RFM thô gần như chỉ phân cụm theo Monetary.",
    "Vì sao phải tách ngoại lệ trước rồi mới fit StandardScaler? Điều gì xảy ra nếu làm ngược lại?",
    "Một mô hình có silhouette 0,76 nhưng hai trong bốn cụm chỉ có vài chục khách. Mô hình đó tốt hay không? Lập luận.",
    "Nêu khác biệt giữa single, complete và Ward linkage. Hiện tượng chuỗi là gì và nhận ra nó trên dendrogram thế nào?",
    "Vì sao không chuẩn hoá z-score cho toạ độ địa lý khi chạy DBSCAN? Cách chọn ε bằng biểu đồ k-distance như thế nào?",
    "Viết một khuyến nghị cho một phân khúc khách hàng tự chọn, gồm đủ bốn phần: hành động, đối tượng, phép tính tác động, chỉ số theo dõi.",
]:
    d.bullet(q)

d.plain_heading("TÀI LIỆU THAM KHẢO")
for r in [
    "Nguyễn Bình Minh An, Trương Hoàng Giang (2026). Đề cương bài giảng: Phân tích dữ liệu Marketing. Khoa Kinh doanh số, Trường Kinh tế, Đại học Công nghiệp Hà Nội.",
    "Joseph F. Hair, William C. Black, Barry J. Babin & Rolph E. Anderson (2019). Multivariate Data Analysis. 8th edition. Cengage Learning.",
    "Naresh K. Malhotra (2019). Marketing Research: An Applied Orientation. 7th edition. Pearson.",
    "Chris Chapman & Elea McDonnell Feit (2015). R for Marketing Research and Analytics. Springer. DOI 10.1007/978-3-319-14436-8.",
    "John W. Tukey (1977). Exploratory Data Analysis. Addison-Wesley.",
    "Peter J. Rousseeuw (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, 53-65.",
    "Leonard Kaufman & Peter J. Rousseeuw (1990). Finding Groups in Data: An Introduction to Cluster Analysis. John Wiley & Sons.",
    "Joe H. Ward Jr. (1963). Hierarchical grouping to optimize an objective function. Journal of the American Statistical Association, 58(301), 236-244.",
    "Martin Ester, Hans-Peter Kriegel, Jörg Sander & Xiaowei Xu (1996). A density-based algorithm for discovering clusters in large spatial databases with noise. Proceedings of KDD-96, 226-231.",
    "Erich Schubert, Jörg Sander, Martin Ester, Hans-Peter Kriegel & Xiaowei Xu (2017). DBSCAN revisited, revisited: Why and how you should (still) use DBSCAN. ACM Transactions on Database Systems, 42(3), Article 19.",
    "Arthur M. Hughes (1994). Strategic Database Marketing. Probus Publishing.",
    "Fabian Pedregosa và cộng sự (2011). Scikit-learn: Machine learning in Python. Journal of Machine Learning Research, 12, 2825-2830. Tài liệu hướng dẫn mục Clustering: https://scikit-learn.org/stable/modules/clustering.html",
]:
    d.ref(r)

d.save(f"{OUT}/Bai 12_Thuc hanh 2_ĐCBG.docx")
print("ok")
