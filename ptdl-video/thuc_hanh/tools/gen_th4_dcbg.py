import sys, os
W = "/tmp/claude-0/-home-user-pouringinsights-github-io/6f04bc4b-d202-5894-b630-2e6e27c873c2/scratchpad"
sys.path.insert(0, f"{W}/tools")
from kits import Dcbg

OUT = f"{W}/th_out/bai_14"
os.makedirs(OUT, exist_ok=True)
d = Dcbg()
P, B, H1, H2, CAP, EX, T = d.para, d.bullet, d.h1, d.h2, d.caption, d.example, d.table
SRC = lambda s="Tác giả tổng hợp": P(f"(Nguồn: {s})")

d.title("BÀI 14:", "THỰC HÀNH 4: PHÂN TÍCH SẢN PHẨM VÀ CHIẾN LƯỢC GIÁ")

d.plain_heading("Mục tiêu bài học")
P("Sau buổi thực hành, người học có khả năng:")
B("Đánh giá một danh mục sản phẩm bằng phân tích Pareto, lợi nhuận gộp và vai trò của từng gói trong chuỗi mua hàng của khách hàng.")
B("Thiết kế biến giả, ước lượng part-worth utility bằng hồi quy, tính tầm quan trọng tương đối và quy hữu dụng ra mức sẵn lòng chi trả.")
B("Xác định khoảng giá chấp nhận được bằng Van Westendorp và mức giá tối đa hoá doanh thu bằng Gabor-Granger.")
B("Ước lượng độ co giãn của cầu theo giá từ dữ liệu bán hàng, nhận ra sai lệch do mùa vụ và kiểm chứng bằng một cách tính độc lập.")
B("Đánh giá lãi lỗ của một chương trình giảm giá bằng độ co giãn hoà vốn và viết khuyến nghị có con số làm căn cứ.")
P("Chuẩn đầu ra học phần liên quan: L1. Ứng dụng kiến thức về các thuật toán và thống kê vào phân tích dữ liệu, song song với kiến thức kinh tế, kinh doanh để đưa ra khuyến nghị chiến lược về sản phẩm, khách hàng và nghiên cứu thị trường cho doanh nghiệp.")
P("Kiến thức cần có trước buổi học:")
B("Bài 3, mục 3.1.1: mục tiêu đánh giá và tối ưu danh mục sản phẩm.")
B("Bài 4, mục 4.2: phân tích kết hợp (part-worth, tầm quan trọng tương đối, WTP, mô phỏng thị phần); mục 4.3: định giá theo giá trị cảm nhận, Van Westendorp, định giá phân biệt.")
B("Bài 5, mục 5.1: giá trị vòng đời khách hàng, dùng để đọc chi tiêu trọn đời của nhóm khách vào bằng một gói.")
B("Bài 7, mục 7.2.1 và 7.3.2: biến bỏ sót, biến giả, hồi quy log-log và hệ số co giãn.")
B("Bài 10, mục 10.1.3: nguyên tắc trình bày báo cáo cho người ra quyết định.")
P("***********")

# ---------------------------------------------------------------- 14.1
H1("14.1. Ôn tập kiến thức lý thuyết trọng tâm")
H2("14.1.1. Phân tích danh mục: doanh thu, lợi nhuận gộp và vai trò của từng sản phẩm")
P("Phân tích Pareto xếp các sản phẩm theo doanh thu giảm dần rồi tính tỷ trọng luỹ kế. Kết quả cho biết bao nhiêu sản phẩm tạo ra phần lớn doanh thu. Quy tắc 80/20 thường được nhắc tới là một quan sát thực nghiệm, không phải quy luật. Mức tập trung thực tế phụ thuộc vào mô hình kinh doanh. Ở doanh nghiệp bán thuê bao, giá trị một giao dịch phụ thuộc mạnh vào thời hạn gói, nên doanh thu thường dồn vào các gói dài hạn chứ không theo đúng tỷ lệ 80/20.")
P("Doanh thu chưa phải thước đo đóng góp. Hai gói có cùng doanh thu có thể để lại lợi nhuận rất khác nhau nếu chi phí phục vụ khác nhau. Lợi nhuận gộp của một gói bằng tổng giá bán trừ tổng chi phí biến đổi để phục vụ khách. Biên lợi nhuận gộp bằng lợi nhuận gộp chia doanh thu. Khi tổng hợp theo nhóm, phải cộng doanh thu và lợi nhuận của nhóm rồi mới chia. Lấy trung bình cộng các biên của từng gói sẽ cho kết quả sai, vì gói bán ít và gói bán nhiều được tính ngang nhau.")
P("Bài 3 (mục 3.1.1) đặt mục tiêu tối ưu danh mục dựa trên hiệu suất và vị thế của từng sản phẩm. Trong thực hành này cần thêm một góc nhìn nữa: vai trò của sản phẩm trên chuỗi mua hàng. Một sản phẩm doanh thu thấp có thể là cửa ngõ (entry product), tức sản phẩm khách mua đầu tiên trước khi nâng cấp lên gói đắt hơn. Muốn biết sản phẩm có vai trò cửa ngõ hay không, phải nhìn vào chi tiêu trọn đời của nhóm khách vào bằng sản phẩm đó (Bài 5, mục 5.1). Doanh thu của riêng sản phẩm chưa đủ để kết luận.")
CAP("Bảng 14.1. Ba thước đo khi đánh giá một sản phẩm trong danh mục")
T([["Thước đo", "Cách tính", "Câu hỏi trả lời", "Hạn chế"],
   ["Tỷ trọng doanh thu", "Doanh thu gói ÷ tổng doanh thu", "Gói nào mang lại nhiều tiền nhất?", "Bỏ qua chi phí phục vụ"],
   ["Biên lợi nhuận gộp", "(Doanh thu − chi phí biến đổi) ÷ doanh thu", "Mỗi đồng doanh thu để lại bao nhiêu?", "Chưa trừ chi phí cố định và chi phí thu hút khách"],
   ["Chi tiêu trọn đời của nhóm khách vào bằng gói", "Tổng chi tiêu của mọi khách có gói đầu tiên là gói đó", "Gói này dẫn khách tới đâu?", "Chỉ quan sát trong kỳ dữ liệu, chưa phải CLV dự báo"]])
SRC()

H2("14.1.2. Phân tích kết hợp: từ điểm chấm tới part-worth")
P("Phân tích kết hợp (conjoint analysis) cho đáp viên đánh giá các phương án sản phẩm được ghép từ nhiều thuộc tính, rồi dùng mô hình thống kê tách giá trị của từng mức thuộc tính (Bài 4, mục 4.2.1). Bài thực hành dùng dạng chấm điểm (rating-based): mỗi đáp viên chấm 12 thẻ trên thang 1 đến 10. Mười hai thẻ theo thiết kế trực giao nên hồi quy tách được ảnh hưởng riêng của từng thuộc tính.")
P("Mô hình ước lượng là hồi quy tuyến tính: Điểm = hằng số + tổng các hệ số của biến giả + sai số. Một thuộc tính có k mức được mã hoá thành k − 1 biến giả. Mức không có biến giả là mức tham chiếu, có part-worth bằng 0. Hệ số của mỗi biến giả là part-worth của mức đó so với mức tham chiếu. Nếu tạo đủ k biến giả cùng với hằng số, ma trận biến độc lập suy biến (đa cộng tuyến hoàn hảo) và phần mềm không ước lượng được, hoặc tự loại một biến (Bài 7, mục 7.3.2).")
P("Tầm quan trọng tương đối của một thuộc tính tính từ biên độ hữu dụng: lấy part-worth lớn nhất trừ part-worth nhỏ nhất trong các mức của thuộc tính đó, tính cả mức tham chiếu. Tầm quan trọng (%) bằng biên độ của thuộc tính chia tổng biên độ của mọi thuộc tính, nhân 100. Lỗi hay gặp là so part-worth cao nhất thay vì so biên độ (Bài 4, mục 4.2.2). Thêm một lưu ý: hai thuộc tính có tầm quan trọng chênh nhau ít hơn sai số chuẩn của hệ số thì không được kết luận thuộc tính này quan trọng hơn thuộc tính kia.")
P("Thuộc tính giá là thước đo để quy hữu dụng ra tiền. Giá trị một đơn vị hữu dụng bằng chênh lệch giá giữa hai mức ngoài cùng chia biên độ hữu dụng của thuộc tính giá. Mức sẵn lòng chi trả (willingness to pay, WTP) cho một tính năng bằng hệ số của tính năng nhân giá trị một đơn vị hữu dụng. Phép quy đổi này giả định hữu dụng của giá gần tuyến tính trong khoảng đã khảo sát. Nếu giả định không đứng vững, con số WTP không còn ý nghĩa. Ngoài ra không được suy WTP ra ngoài khoảng giá đã đưa vào bảng hỏi.")
P("Mô phỏng thị phần ưu tiên dùng công thức logit: thị phần của phương án i bằng exp(U_i) chia tổng exp(U) của mọi phương án trong tập so sánh. Đây là thị phần trong một tập phương án giả định. Con số chỉ dùng để xếp hạng các phương án với nhau, không dùng để dự báo doanh số tuyệt đối.")
EX("Ví dụ 14.1. Quy hữu dụng ra tiền (số liệu minh hoạ, không lấy từ dữ liệu MOVA)")
P("Một nghiên cứu conjoint về gói học trực tuyến có ba mức giá 100.000 đ, 150.000 đ và 200.000 đ một tháng, mức tham chiếu là 100.000 đ. Hệ số của hai biến giả giá lần lượt là −1,0 và −2,1. Tính năng chấm bài tự động có hệ số +0,8.")
B("Kiểm tra tuyến tính: từ 100.000 đ lên 150.000 đ hữu dụng giảm 1,0; từ 150.000 đ lên 200.000 đ giảm thêm 1,1. Hai mức giảm chênh nhau khoảng 10%, có thể coi là gần tuyến tính.")
B("Giá trị một đơn vị hữu dụng = 100.000 ÷ 2,1 ≈ 47.600 đ/tháng.")
B("WTP cho tính năng chấm bài tự động = 0,8 × 47.600 ≈ 38.100 đ/tháng. Hệ số 0,8 là điểm hấp dẫn, không phải tiền. Chỉ sau khi đổi đơn vị mới so sánh được với giá.")
B("Nếu ba phương án trong một tập so sánh có tổng hữu dụng 2,0; 2,5 và 3,0 thì thị phần ưu tiên theo logit lần lượt là 18,6%; 30,7% và 50,6%.")

H2("14.1.3. Hai phương pháp khảo sát giá trực tiếp: Van Westendorp và Gabor-Granger")
P("Phương pháp Van Westendorp (Price Sensitivity Meter) hỏi đáp viên bốn mức giá cho cùng một sản phẩm: mức rẻ tới mức nghi ngờ chất lượng (quá rẻ), mức rẻ nhưng vẫn mua (rẻ), mức đắt nhưng vẫn cân nhắc (đắt) và mức đắt tới mức không mua (quá đắt). Một phiếu trả lời nhất quán phải thoả mãn Quá rẻ < Rẻ < Đắt < Quá đắt. Phiếu vi phạm cho thấy đáp viên hiểu sai câu hỏi hoặc trả lời đối phó, nên phải loại trước khi vẽ.")
P("Từ bốn câu trả lời, lập bốn đường tần suất tích luỹ theo mức giá x. Đường Quá đắt và Đắt cộng dồn tăng: tỷ lệ người có câu trả lời nhỏ hơn hoặc bằng x. Đường Rẻ và Quá rẻ cộng dồn giảm: tỷ lệ người có câu trả lời lớn hơn hoặc bằng x. Giao điểm của các đường cho bốn điểm giá (Bảng 14.2). Bài 4 (mục 4.3.2) đã giới thiệu ý nghĩa của các điểm này. Ngoài vị trí trên trục giá, cần đọc cả tỷ lệ phần trăm tại điểm giao. Nếu thị trường đồng nhất, các đường sẽ cắt nhau ở tỷ lệ cao. Các đường cắt nhau ở tỷ lệ thấp cho thấy khoảng giá riêng của từng người lệch nhau nhiều, tức thị trường không đồng nhất.")
CAP("Bảng 14.2. Bốn điểm giao của Van Westendorp theo quy ước của đề bài")
T([["Điểm", "Giao của hai đường", "Ý nghĩa"],
   ["PMC (Point of Marginal Cheapness)", "Quá rẻ × Đắt", "Giới hạn dưới của khoảng giá chấp nhận được"],
   ["OPP (Optimal Price Point)", "Quá rẻ × Quá đắt", "Ít người từ chối nhất ở cả hai phía; thường lấy làm giá tham khảo"],
   ["IPP (Indifference Price Point)", "Rẻ × Đắt", "Số người thấy rẻ bằng số người thấy đắt"],
   ["PME (Point of Marginal Expensiveness)", "Rẻ × Quá đắt", "Giới hạn trên; cao hơn mức này thị trường từ chối nhanh"]])
SRC("Van Westendorp (1976); Phụ lục C4 của đề bài")
P("Phương pháp Gabor-Granger hỏi đáp viên có mua hay không ở từng mức giá trong một dãy cố định. Tỷ lệ chấp nhận ở mỗi mức tạo thành một đường cầu khảo sát. Chỉ số doanh thu bằng giá nhân tỷ lệ chấp nhận; mức giá cho chỉ số lớn nhất là mức tối đa hoá doanh thu trong dãy giá đã hỏi. Giữa hai mức giá liền kề, độ co giãn tính theo công thức điểm giữa, còn gọi là độ co giãn cung (arc elasticity). Chữ \"cung\" ở đây là cung đường cong, không phải phía cung của thị trường:")
P("E = [(Q2 − Q1) ÷ ((Q1 + Q2) ÷ 2)] ÷ [(P2 − P1) ÷ ((P1 + P2) ÷ 2)]")
P("Khi |E| < 1, cầu kém co giãn và tăng giá làm tăng doanh thu. Khi |E| > 1, cầu co giãn và tăng giá làm giảm doanh thu. Doanh thu đạt đỉnh quanh mức giá có |E| = 1.")
EX("Ví dụ 14.2. Gabor-Granger với ba mức giá (số liệu minh hoạ)")
P("Một khảo sát hỏi ở ba mức giá 100, 120 và 140 nghìn đồng. Tỷ lệ chấp nhận lần lượt là 80%, 70% và 50%.")
P("Chỉ số doanh thu ở ba mức lần lượt là 80,0; 84,0 và 70,0. Độ co giãn cung từ 100 lên 120 là −0,73; từ 120 lên 140 là −2,17.")
P("Giữa 100 và 120 nghìn đồng, |E| = 0,73 < 1 nên tăng giá vẫn làm doanh thu tăng. Giữa 120 và 140 nghìn đồng, |E| = 2,17 > 1 nên tăng giá làm doanh thu giảm. Mức 120 nghìn đồng cho chỉ số doanh thu cao nhất. Lưu ý rằng chỉ số doanh thu chưa trừ chi phí, nên mức tối đa hoá doanh thu chưa chắc là mức tối đa hoá lợi nhuận.")

H2("14.1.4. Độ co giãn từ dữ liệu bán hàng và sai lệch do biến bỏ sót")
P("Độ co giãn của cầu theo giá đo phần trăm thay đổi của lượng bán khi giá thay đổi 1%. Với dữ liệu nhiều kỳ, cách ước lượng thông dụng là hồi quy log-log: ln(Số đơn) = a + b × ln(Giá) + các biến kiểm soát. Hệ số b chính là độ co giãn (Bài 7, mục 7.3.2). Tổng hợp nhiều nghiên cứu thực nghiệm cho thấy độ co giãn giá của hàng hoá tiêu dùng thường âm và có trị tuyệt đối lớn hơn 1, nhưng dao động rất rộng giữa các ngành (Bijmolt và cộng sự, 2005).")
P("Hệ số b chỉ phản ánh đúng độ co giãn khi mô hình không bỏ sót biến vừa ảnh hưởng tới giá vừa ảnh hưởng tới lượng bán. Bài 7 (mục 7.2.1) gọi đây là thiên lệch do biến bị bỏ sót (omitted variable bias). Mùa vụ là ví dụ điển hình. Nếu doanh nghiệp giảm giá sâu nhất đúng vào mùa cao điểm, toàn bộ mức tăng lượng bán do mùa vụ sẽ bị gán cho giá. Hệ số co giãn khi đó bị phóng đại, và doanh nghiệp tin rằng giảm giá hiệu quả hơn thực tế. Cách xử lý là thêm biến giả đánh dấu mùa vụ hoặc sự kiện (Bài 7, mục 7.2.3).")
P("Khi có nhiều sản phẩm với mặt bằng giá khác nhau, cần thêm biến giả cho sản phẩm. Nếu không, chênh lệch giá giữa các sản phẩm sẽ lẫn với biến động giá theo thời gian. Một cách kiểm chứng độc lập là so sánh từng cặp quan sát giống nhau ở mọi mặt trừ giá, ví dụ cùng tháng trong lịch nhưng ở hai năm có hai mức khuyến mãi khác nhau, rồi tính độ co giãn cung cho từng cặp và lấy trung bình. Một cặp đơn lẻ dao động mạnh vì nhiễu ngẫu nhiên, nên phải dùng nhiều cặp.")
P("Ví dụ minh hoạ: một chuỗi đồ bơi giảm giá 30% đúng tháng 6 và bán gấp ba tháng thường. Năm trước tháng 6 không giảm giá vẫn bán gấp 2,2 lần. Phần lớn mức tăng là do mùa hè, nhưng mô hình không có biến giả tháng 6 sẽ quy toàn bộ cho giá.")

H2("14.1.5. Khuyến mãi có lãi không: độ co giãn hoà vốn")
P("Một chương trình giảm giá làm tăng lượng bán nhưng làm giảm lãi trên mỗi đơn. Chương trình chỉ có lãi khi phần tăng lượng bán đủ bù phần lãi bị mất. Gọi P là giá niêm yết, C là chi phí phục vụ mỗi đơn, d là tỷ lệ giảm giá và |E| là trị tuyệt đối của độ co giãn. Theo Phụ lục C6 của đề bài, với mô hình cầu có độ co giãn không đổi:")
B("Hệ số sản lượng k = (1 − d)^(−|E|).")
B("Doanh thu thay đổi (%) = k × (1 − d) − 1.")
B("Lợi nhuận gộp thay đổi (%) = k × [P × (1 − d) − C] ÷ (P − C) − 1.")
B("|E| hoà vốn = ln[(P − C) ÷ (P × (1 − d) − C)] ÷ ln[1 ÷ (1 − d)].")
P("Khi mức giảm rất nhỏ, công thức hoà vốn xấp xỉ 1 ÷ biên lợi nhuận gộp. Biên càng mỏng thì cầu phải càng co giãn mới bù được phần giảm giá. Với mức giảm lớn, ngưỡng thực tế cao hơn mức xấp xỉ này, nên phải tính bằng công thức đầy đủ.")
EX("Ví dụ 14.3. Đánh giá một đợt giảm 20% (số liệu minh hoạ)")
P("Một gói dịch vụ có giá niêm yết 1.000.000 đ, chi phí phục vụ 400.000 đ, biên lợi nhuận gộp 60%. Doanh nghiệp giảm 20%, giá còn 800.000 đ, lãi mỗi đơn còn 400.000 đ, biên còn 50%.")
B("Ngưỡng xấp xỉ cho mức giảm nhỏ: 1 ÷ 0,60 ≈ 1,67.")
B("Ngưỡng đầy đủ: ln(600.000 ÷ 400.000) ÷ ln(1 ÷ 0,8) = 0,405 ÷ 0,223 ≈ 1,82.")
B("Nếu |E| ước lượng là 1,2 thì k = 0,8^(−1,2) ≈ 1,307. Doanh thu tăng khoảng 4,6%, nhưng lợi nhuận gộp giảm khoảng 12,9%.")
P("Ví dụ cho thấy doanh thu tăng không có nghĩa là lợi nhuận tăng. Báo cáo chỉ nhìn số đơn và doanh thu của tháng khuyến mãi sẽ đánh giá sai chương trình.")

H2("14.1.6. Điều khách hàng nói và điều khách hàng làm")
P("Conjoint, Van Westendorp và Gabor-Granger đều dựa trên lời khai (stated preference). Đáp viên không phải trả tiền thật nên thường nói sẽ mua nhiều hơn thực tế. Dữ liệu giao dịch là hành vi thật (revealed preference), đáng tin hơn, nhưng chỉ nói được về những mức giá doanh nghiệp đã từng bán (Bài 4, mục 4.3.2). Quy tắc thực hành là dùng khảo sát để chọn khoảng giá, dùng dữ liệu hành vi để hiệu chỉnh quy mô dự báo, rồi thử nghiệm giá thật ở quy mô nhỏ trước khi triển khai rộng (Bài 7, mục 7.5).")
# ---------------------------------------------------------------- 14.2
H1("14.2. Tình huống và dữ liệu")
H2("14.2.1. Bối cảnh doanh nghiệp MOVA")
P("Công ty Cổ phần MOVA Việt Nam là doanh nghiệp hư cấu, số liệu được mô phỏng cho mục đích giảng dạy. MOVA vận hành hai mảng: ứng dụng tập luyện MOVA Fit và chuỗi 14 câu lạc bộ MOVA Club, gồm 8 cơ sở tại Hà Nội và 6 cơ sở tại Thành phố Hồ Chí Minh. Danh mục hiện có 17 gói thuộc năm nhóm: App, Club, Combo, PT (huấn luyện viên cá nhân) và Lớp nhóm. Nhiều gói có biến thể theo thời hạn tháng, quý hoặc năm.")
P("Ban giám đốc đặt ra ba vấn đề. Thứ nhất, danh mục quá rộng và có đề nghị cắt năm gói doanh thu thấp nhất, trong đó có gói APP01 MOVA Fit Tháng. Thứ hai, sản phẩm mới MOVA Fit Premium có huấn luyện viên AI sẽ ra mắt quý I/2027 nhưng chưa chốt cấu hình, giá và chính sách cam kết. Thứ ba, chương trình giảm 35% cho các gói Năm vào tháng 1 tạo ra nhiều đơn, nhưng giám đốc tài chính nghi ngờ chương trình không có lãi. Bốn phần của đề bài lần lượt trả lời ba vấn đề này rồi tổng hợp thành khuyến nghị.")
H2("14.2.2. Mô tả các tệp dữ liệu")
P("Kỳ dữ liệu từ 01/11/2024 tới 31/10/2026 (24 tháng). Ngày phân tích quy ước là 31/10/2026. Dữ liệu gồm sáu tệp CSV, hoặc một tệp Excel đã gộp đủ sáu bảng kèm sheet 00_Doc truoc mô tả từ điển cột. Dữ liệu đã được làm sạch, nên buổi học tập trung vào phân tích và ra quyết định.")
CAP("Bảng 14.3. Sáu tệp dữ liệu của Thực hành 4")
T([["Tệp", "Số dòng", "Một dòng là", "Dùng cho"],
   ["01_DanhMucGoi", "17", "Một gói dịch vụ", "Phần 1, 3"],
   ["02_KhachHang", "10.500", "Một khách hàng", "Phần 1"],
   ["03_GiaoDich", "22.778", "Một giao dịch", "Phần 1, 3"],
   ["04_TheConjoint", "12", "Một thẻ sản phẩm giả định", "Phần 2"],
   ["05_ChamDiemConjoint", "3.840", "Một lượt chấm của một đáp viên cho một thẻ", "Phần 2"],
   ["06_KhaoSatGia", "320", "Một đáp viên khảo sát giá", "Phần 2, 3"]])
SRC("Đề bài Thực hành 4")
CAP("Bảng 14.4. Các cột cần dùng và lưu ý khi đọc")
T([["Tệp", "Cột chính", "Lưu ý"],
   ["01", "NhomGoi, HinhThuc, ThoiHan_Thang, GiaNiemYet_VND, ChiPhiPhucVu_CaGoi_VND", "Chi phí biến đổi, cột Cả gói đã nhân số tháng"],
   ["02", "GoiDauTien", "Gói ở giao dịch đầu tiên; dùng cho câu 1.4"],
   ["03", "MaKH, MaGoi, Thang, TyLeKhuyenMai, GiaBan_VND", "GiaBan = GiaNiemYet × (1 − TyLeKhuyenMai), làm tròn nghìn"],
   ["04, 05", "MaThe, bốn thuộc tính, MaDapVien, DiemHapDan", "Ghép theo MaThe; điểm 1 đến 10"],
   ["06", "ThuNhapThang, bốn cột VW_, năm cột GG_", "GG mã 1 = sẽ mua, 0 = không mua"]])
SRC("Đề bài và từ điển cột của bộ dữ liệu")
P("Ba lưu ý chất lượng dữ liệu. Thứ nhất, mọi con số lợi nhuận trong bài là lợi nhuận gộp, không phải lợi nhuận ròng. Thứ hai, cột ThoiHan_Thang của thẻ buổi là thời hạn sử dụng thẻ, không phải số tháng thuê bao, nên chỉ quy giá về tháng cho gói thuê bao. Thứ ba, tệp 06 có những phiếu Van Westendorp không nhất quán; ví dụ một đáp viên ghi mức rẻ cao hơn mức đắt. Những phiếu này phải được lọc ở câu 3.1.")
P("Thông tin bổ sung về sản phẩm mới: khảo sát conjoint dùng bốn thuộc tính là thời hạn cam kết (1 tháng, 12 tháng), phạm vi phòng tập (1 cơ sở, toàn hệ thống 14 cơ sở), huấn luyện viên AI (Không, Có) và giá mỗi tháng (490.000 đ, 690.000 đ, 890.000 đ). Chi phí phục vụ dự kiến của gói Premium là 230.000 đ/tháng nếu dùng toàn hệ thống và 190.000 đ/tháng nếu giới hạn một cơ sở.")

# ---------------------------------------------------------------- 14.3
H1("14.3. Hướng dẫn Phần 1: Phân tích danh mục sản phẩm (2,0 điểm, 40 phút)")
H2("14.3.1. Câu 1.1: Bảng Pareto doanh thu")
P("Mục đích: biết doanh thu tập trung ở bao nhiêu gói và so sánh với quy tắc 80/20.")
P("Các bước làm:")
B("Trên Excel: chọn bảng 03_GiaoDich, Insert, PivotTable. Kéo MaGoi vào Rows, GiaBan_VND vào Values chọn Sum, MaGiaoDich vào Values chọn Count. Sắp xếp giảm dần theo tổng giá bán.")
B("Thêm cột Tỷ trọng = doanh thu gói ÷ tổng doanh thu, và cột Luỹ kế bằng công thức cộng dồn, ví dụ =SUM($C$2:C2)/$C$19.")
B("Tìm hàng đầu tiên có tỷ trọng luỹ kế đạt hoặc vượt 80%. Số hàng tính tới đó là số gói tạo ra 80% doanh thu. Chia cho 17 để ra tỷ lệ phần trăm số gói.")
B("Trên Python: df.groupby('MaGoi')['GiaBan_VND'].agg(['sum','count']).sort_values('sum', ascending=False), sau đó dùng .cumsum() cho cột luỹ kế.")
P("Cách đọc kết quả: nếu tỷ lệ số gói khác xa 20%, hãy giải thích bằng đặc điểm của mô hình thuê bao, ví dụ giá trị một giao dịch phụ thuộc thời hạn gói. Không ép số liệu cho khớp 80/20.")
P("Cạm bẫy: dùng GiaNiemYet_VND thay cho GiaBan_VND. Doanh thu thực là giá bán sau khuyến mãi.")
H2("14.3.2. Câu 1.2: Lợi nhuận gộp và xếp hạng lại")
P("Mục đích: kiểm tra xem xếp hạng theo doanh thu có trùng với xếp hạng theo đóng góp lợi nhuận hay không.")
B("Lấy chi phí cả gói sang bảng giao dịch bằng =XLOOKUP([@MaGoi]; DanhMuc[MaGoi]; DanhMuc[ChiPhiPhucVu_CaGoi_VND]), hoặc VLOOKUP nếu Excel chưa có XLOOKUP.")
B("Lợi nhuận gộp của gói = Tổng giá bán − Số giao dịch × ChiPhiPhucVu_CaGoi_VND. Biên = Lợi nhuận gộp ÷ Tổng giá bán.")
B("Dùng RANK.EQ để có hạng theo doanh thu và hạng theo lợi nhuận gộp. Cột Chênh hạng = Hạng LN − Hạng DT; giá trị dương là tụt hạng.")
B("Lọc ba gói có chênh hạng dương lớn nhất. So sánh nhóm gói và biên của chúng với các gói còn lại.")
P("Cách đọc kết quả: tìm điểm chung về bản chất dịch vụ của các gói tụt hạng. Câu hỏi gợi ý: chi phí phục vụ của gói này tăng theo số khách hay gần như cố định? Doanh thu lớn trên mỗi giao dịch có kéo theo chi phí lớn tương ứng không?")
H2("14.3.3. Câu 1.3: Tổng hợp theo nhóm gói")
B("Dùng PivotTable với NhomGoi ở Rows, cộng doanh thu và cộng lợi nhuận gộp của từng giao dịch.")
B("Tính tỷ trọng doanh thu và tỷ trọng lợi nhuận gộp của từng nhóm. Thêm cột Chênh = tỷ trọng LN − tỷ trọng DT.")
B("Biên của nhóm = tổng lợi nhuận gộp của nhóm ÷ tổng doanh thu của nhóm. Không lấy trung bình cộng các biên của gói.")
P("Cách đọc kết quả: nhóm có tỷ trọng lợi nhuận thấp hơn tỷ trọng doanh thu là nhóm có chi phí biến đổi cao so với giá. Liên hệ với loại chi phí: dịch vụ cần người phục vụ trực tiếp khác sản phẩm số ở chỗ chi phí tăng theo từng khách.")
H2("14.3.4. Câu 1.4: Có nên cắt gói APP01 MOVA Fit Tháng?")
P("Mục đích: kiểm tra vai trò cửa ngõ của gói App trước khi quyết định cắt. Đây là câu phân loại của Phần 1. Kết luận chỉ dựa vào doanh thu của riêng gói, không tra cột GoiDauTien, là chưa đạt yêu cầu.")
P("Các bước làm:")
B("Tạo cột NhomGoiDau trong bảng 02_KhachHang bằng cách tra nhóm gói của GoiDauTien từ bảng 01.")
B("Đánh dấu khách đã từng mua CMB12: =IF(COUNTIFS(GiaoDich[MaKH];[@MaKH];GiaoDich[MaGoi];\"CMB12\")>0;1;0).")
B("Ý (a): trong nhóm khách có cờ CMB12 = 1, đếm tỷ lệ khách có NhomGoiDau = App. Ý (b): làm tương tự với nhóm cờ = 0.")
B("Ý (c): cộng toàn bộ giá bán của mọi giao dịch thuộc những khách có NhomGoiDau = App, chia cho tổng doanh thu công ty. Dùng SUMIFS trên bảng giao dịch sau khi đã tra NhomGoiDau sang.")
B("Trên Python: merge bảng giao dịch với bảng khách hàng theo MaKH, rồi groupby theo NhomGoiDau và cờ CMB12.")
P("Cách đọc kết quả: so sánh ba con số với tỷ trọng doanh thu của riêng nhóm App ở câu 1.3. Nếu nhóm khách vào bằng App chi tiêu nhiều hơn hẳn doanh thu của riêng gói App, thì cắt gói là cắt phễu thu hút khách. Khi đó cần đề xuất cách khác để giảm độ phức tạp, ví dụ bỏ bớt biến thể thời hạn, gộp các gói giống nhau, hoặc giữ gói nhưng không trưng trên trang giá chính.")
P("Cạm bẫy: chi tiêu trọn đời ở đây là tổng chi tiêu quan sát được trong 24 tháng, chưa phải CLV dự báo như Bài 5. Khi trình bày nên gọi đúng tên để tránh hiểu nhầm.")

# ---------------------------------------------------------------- 14.4
H1("14.4. Hướng dẫn Phần 2: Phân tích conjoint cho sản phẩm mới (3,0 điểm, 65 phút)")
H2("14.4.1. Câu 2.1: Ghép bảng và tạo biến giả")
P("Ghép 05_ChamDiemConjoint với 04_TheConjoint theo MaThe bằng XLOOKUP (Excel) hoặc Data, Merge Files, Add Variables (SPSS; phải sắp xếp cả hai tệp theo MaThe trước). Bảng sau khi ghép có 3.840 dòng.")
CAP("Bảng 14.5. Gợi ý mã hoá biến giả cho bốn thuộc tính")
T([["Thuộc tính", "Số mức", "Số biến giả", "Biến giả", "Mức tham chiếu gợi ý"],
   ["Thời hạn cam kết", "2", "1", "CamKetNam", "1 tháng"],
   ["Phạm vi phòng tập", "2", "1", "ToanHeThong", "1 cơ sở"],
   ["Huấn luyện viên AI", "2", "1", "CoAI", "Không"],
   ["Giá mỗi tháng", "3", "2", "Gia690, Gia890", "490.000 đ"]])
SRC("Phụ lục A3 của đề bài")
P("Công thức Excel mẫu: CamKetNam = IF([@ThoiHanCamKet]=\"12 tháng (cam kết năm)\"; 1; 0); Gia690 = IF([@GiaMoiThang_VND]=690000; 1; 0). Sinh viên được chọn mức tham chiếu khác, miễn là nói rõ và diễn giải hệ số theo đúng mức đã chọn. Phần giải thích phải nêu nguyên tắc k − 1 biến giả cho thuộc tính k mức.")
H2("14.4.2. Câu 2.2: Hồi quy part-worth")
B("Excel: bật Analysis ToolPak một lần (File, Options, Add-ins). Sau đó Data, Data Analysis, Regression. Input Y là DiemHapDan, Input X là năm cột biến giả nằm liền nhau, tích Labels.")
B("SPSS: Analyze, Regression, Linear. Đọc cột B trong bảng Coefficients và R Square trong bảng Model Summary.")
B("Python: statsmodels.formula.api.ols('DiemHapDan ~ CamKetNam + ToanHeThong + CoAI + Gia690 + Gia890', data=df).fit().summary().")
P("Cách đọc kết quả: báo cáo hệ số, sai số chuẩn, giá trị t và R². Kiểm tra dấu từng hệ số theo trực giác: giá cao làm giảm hấp dẫn, tính năng tốt làm tăng, cam kết dài làm giảm. Nếu có hệ số trái dấu, kiểm tra lại cách gán biến giả trước khi diễn giải. Với dữ liệu chấm điểm cá nhân, R² ở mức trung bình là bình thường, vì phần còn lại phản ánh khác biệt giữa các đáp viên; phần đó được khai thác ở câu 2.5.")
H2("14.4.3. Câu 2.3: Tầm quan trọng tương đối")
P("Với mỗi thuộc tính, biên độ = hệ số lớn nhất trừ hệ số nhỏ nhất, tính cả mức tham chiếu bằng 0. Với giá có ba mức, biên độ là chênh giữa 0 và hệ số âm nhất. Tầm quan trọng = biên độ ÷ tổng biên độ × 100. Khi so sánh các thuộc tính có tầm quan trọng gần nhau, đối chiếu chênh lệch hệ số với sai số chuẩn ở câu 2.2 trước khi kết luận thuộc tính nào quan trọng hơn.")
H2("14.4.4. Câu 2.4: Quy hữu dụng ra tiền")
P("Làm theo đúng thứ tự trong Ví dụ 14.1. Ý (a) là bước kiểm tra bắt buộc: so mức giảm hữu dụng từ 490.000 đ lên 690.000 đ với mức giảm từ 690.000 đ lên 890.000 đ. Đề bài không cho ngưỡng cố định; sinh viên tự nêu tiêu chí, ví dụ chênh dưới 10 đến 15% thì coi là gần tuyến tính, và giải thích. Ý (b) tính giá trị một đơn vị hữu dụng bằng 400.000 đ chia biên độ hữu dụng của giá. Ý (c) nhân hệ số của AI và của phạm vi toàn hệ thống với giá trị đó. Ý (d) dùng hệ số âm của cam kết 12 tháng: mức giảm giá tối thiểu để bù cho cam kết bằng trị tuyệt đối của hệ số nhân giá trị một đơn vị hữu dụng.")
P("Cạm bẫy: đọc hệ số như đọc tiền. Hệ số lớn nhất chưa chắc tương ứng số tiền lớn khi đề xuất giá. Một cầu nối nên nêu: so sánh mức giảm cần thiết để khách chấp nhận cam kết năm với mức giảm 35% mà MOVA đang áp dụng cho gói Năm, quy về đồng mỗi tháng.")
H2("14.4.5. Câu 2.5: Khác biệt theo nhóm thu nhập")
B("Tra ThuNhapThang từ tệp 06 sang bảng conjoint theo MaDapVien. Tạo biến nhóm: 1 nếu thu nhập từ 20 triệu trở lên, 0 nếu dưới 20 triệu. Kiểm tra các nhãn thu nhập trong dữ liệu để gán nhóm đúng.")
B("SPSS: Data, Split File, Compare groups theo biến nhóm, chạy lại hồi quy, rồi tắt Split File. Excel: lọc từng nhóm sang sheet riêng rồi chạy Regression hai lần.")
B("Tính lại tầm quan trọng và WTP của AI cho từng nhóm, rồi lấy tỷ số WTP giữa hai nhóm.")
P("Cách đọc kết quả: nếu hai nhóm khác nhau rõ về WTP và về tầm quan trọng của giá, con số trung bình ở câu 2.4 không mô tả đúng nhóm nào. Đây là căn cứ cho định giá phân biệt theo phiên bản sản phẩm (Bài 4, mục 4.3.2). Lưu ý cỡ mẫu mỗi nhóm nhỏ hơn mẫu chung nên sai số chuẩn lớn hơn.")

# ---------------------------------------------------------------- 14.5
H1("14.5. Hướng dẫn Phần 3: Phân tích giá (3,0 điểm, 65 phút)")
H2("14.5.1. Câu 3.1: Van Westendorp")
B("Ý (a): tạo cột NhatQuan = IF(AND(VW_QuaRe<VW_Re; VW_Re<VW_Dat; VW_Dat<VW_QuaDat); 1; 0). Đếm số phiếu bằng 0 và loại khỏi phân tích. Ghi rõ điều kiện dùng dấu nhỏ hơn chặt hay nhỏ hơn hoặc bằng.")
B("Ý (b): tạo cột mức giá từ 100.000 đến 1.900.000, bước 10.000. Với mỗi mức x, Quá đắt = COUNTIF(VW_QuaDat;\"<=\"&x)/n và Đắt tương tự; Rẻ = COUNTIF(VW_Re;\">=\"&x)/n và Quá rẻ tương tự. n là số phiếu sau khi lọc.")
B("Vẽ bốn đường trên cùng một biểu đồ Scatter with Straight Lines, trục hoành là giá, trục tung là tỷ lệ.")
B("Ý (c): tìm giao điểm bằng cột chênh lệch giữa hai đường; điểm giao là nơi chênh lệch đổi dấu. Dùng mức giá đầu tiên tại đó hoặc nội suy tuyến tính, và ghi rõ cách đã dùng.")
B("Ý (d): ghi tỷ lệ phần trăm tại mỗi điểm giao và giải thích theo mục 14.1.3.")
P("Cạm bẫy: nhầm chiều cộng dồn của hai đường Rẻ và Quá rẻ. Dấu hiệu nhận biết là PMC lớn hơn PME, tức giới hạn dưới cao hơn giới hạn trên.")
H2("14.5.2. Câu 3.2: Gabor-Granger")
B("Tỷ lệ chấp nhận ở mỗi mức = trung bình cột GG tương ứng, ví dụ =AVERAGE(GG_690).")
B("Chỉ số doanh thu = giá × tỷ lệ chấp nhận. Có thể tính theo triệu đồng để số gọn.")
B("Độ co giãn cung giữa từng cặp mức liền kề theo công thức điểm giữa ở mục 14.1.3.")
P("Cách đọc kết quả: theo dõi |E| thay đổi khi giá tăng dần và tìm nơi |E| vượt qua 1. So mức tối đa hoá doanh thu với OPP của câu 3.1. Hai phương pháp cho kết quả gần nhau là dấu hiệu tốt, nhưng cả hai cùng dựa trên lời khai nên có thể cùng lệch một hướng; câu 3.5 kiểm tra điều này.")
H2("14.5.3. Câu 3.3: Độ co giãn từ dữ liệu bán hàng")
P("Đây là câu nặng nhất của Phần 3. Chỉ xét hai gói CLB12 và CMB12. Gộp cả 17 gói sẽ làm biến động giá giữa các gói lấn át biến động theo thời gian.")
B("Ý (a): PivotTable với MaGoi và Thang ở Rows, Count của MaGiaoDich và Average của GiaBan_VND ở Values. Bảng có 48 dòng. Thêm cột =LN(SoDon), =LN(GiaBQ), biến giả CMB = 1 nếu là CMB12, biến giả T1 = 1 nếu tháng là tháng 1.")
B("Ý (b): Mô hình 1 hồi quy ln(Số đơn) theo ln(Giá) và CMB. Ý (c): Mô hình 2 thêm T1. Ghi hệ số ln(Giá) và sai số chuẩn của cả hai mô hình.")
B("Python: smf.ols('np.log(SoDon) ~ np.log(GiaBQ) + CMB', d48).fit(), sau đó thêm '+ T1'.")
B("Ý (d): lọc riêng các dòng tháng 1, so mức khuyến mãi và số đơn với các tháng khác. Giải thích sai lệch theo cơ chế biến bỏ sót ở mục 14.1.4: chiều sai lệch và vì sao chiều đó nguy hiểm cho người ra quyết định.")
B("Ý (e): tìm các tháng có một năm giảm 0% và năm kia giảm 25%. Với mỗi cặp tháng của mỗi gói, tính độ co giãn cung giữa hai năm, rồi lấy trung bình và trung vị của các cặp. So với Mô hình 2.")
P("Có thể thử thêm biến xu thế thời gian hoặc đủ 11 biến giả tháng để kiểm tra độ ổn định của hệ số. Một ước lượng ổn định khi thêm biến kiểm soát đáng tin hơn một ước lượng thay đổi mạnh.")
H2("14.5.4. Câu 3.4: Chương trình giảm 35% đầu năm")
B("Ý (a): biên khi bán đúng giá = (P − C) ÷ P; khi giảm 35% = (0,65P − C) ÷ 0,65P, với P và C của gói CMB12 cho trong đề.")
B("Ý (b): dùng |E| ước lượng ở câu 3.3 (nói rõ dùng mô hình nào), tính k, phần trăm thay đổi doanh thu và lợi nhuận gộp theo mục 14.1.5.")
B("Ý (c): tính |E| hoà vốn bằng công thức đầy đủ, so với |E| ước lượng. Nên so thêm với ngưỡng xấp xỉ 1 ÷ biên để thấy kết luận có đổi khi mức giảm nhỏ hơn hay không.")
B("Ý (d): từ dữ liệu CMB12, tính số đơn và lợi nhuận gộp bình quân của một tháng 1 và của một tháng thường. Lập hai tỷ số tháng 1 so với tháng thường rồi giải thích vì sao hai tỷ số khác nhau, dựa trên lãi gộp mỗi đơn.")
P("Ý (d) là bằng chứng lấy thẳng từ sổ sách, không phụ thuộc mô hình. Khi trình bày cho Ban giám đốc, nên đặt nó cạnh kết quả công thức ở ý (b) và (c).")
H2("14.5.5. Câu 3.5: Người ta nói và người ta làm")
B("Lấy tỷ lệ nói sẽ mua ở mức 690.000 đ từ câu 3.2.")
B("Trên bảng giao dịch, chỉ giữ gói có HinhThuc = Thuê bao. Tính GiaThang = GiaBan_VND ÷ ThoiHan_Thang.")
B("Với mỗi khách, lấy MAXIFS của GiaThang. Đếm tỷ lệ khách có mức cao nhất từ 690.000 đ trở lên.")
B("Làm tương tự ở 490.000 đ và 890.000 đ để thấy khoảng cách ở nhiều mức giá. Kiểm tra gói thuê bao đắt nhất của MOVA tính theo tháng để biết mức nào không kiểm chứng được.")
P("Cách đọc kết quả: lời khai và hành vi đều có điểm yếu riêng (mục 14.1.6). Câu trả lời tốt không chọn hẳn một nguồn mà nói rõ dùng nguồn nào cho việc gì. Lưu ý đề viết \"khách đang dùng gói thuê bao\"; nếu nhóm hiểu là khách còn hiệu lực tại 31/10/2026 thay vì khách từng mua gói thuê bao, cần ghi rõ cách hiểu đã chọn.")
P("Cạm bẫy: quên chia cho ThoiHan_Thang. Gói Năm 7.990.000 đ không phải giá 7.990.000 đ mỗi tháng.")

# ---------------------------------------------------------------- 14.6
H1("14.6. Hướng dẫn Phần 4: Khuyến nghị và trình bày (2,0 điểm, 30 phút)")
H2("14.6.1. Câu 4.1: Chốt cấu hình và giá cho MOVA Fit Premium")
B("Tổng hữu dụng của một phương án = hằng số + hệ số của các mức có mặt trong phương án. Mức tham chiếu cộng 0.")
B("Thị phần ưu tiên = EXP(U_i) ÷ tổng EXP(U) của bốn phương án.")
B("Chỉ số doanh thu = thị phần × giá mỗi tháng. Chỉ số lợi nhuận gộp = thị phần × (giá − chi phí phục vụ mỗi tháng), với chi phí 230.000 đ cho phương án toàn hệ thống và 190.000 đ cho phương án một cơ sở.")
B("Xếp hạng bốn phương án theo ba tiêu chí và so sánh thứ hạng.")
P("Cách đọc kết quả: nếu thứ hạng khác nhau giữa ba tiêu chí, nêu rõ MOVA nên chọn theo tiêu chí nào và vì sao, gắn với mục tiêu ra sản phẩm mới. Xem thêm rủi ro ăn mòn: phương án giá thấp có nằm sát giá các gói hiện có không? Có thể mô phỏng riêng cho hai nhóm thu nhập bằng hệ số của câu 2.5. Không nhân thị phần ưu tiên với quy mô thị trường để ra doanh số tuyệt đối.")
H2("14.6.2. Câu 4.2: Ba khuyến nghị")
P("Mỗi khuyến nghị trả lời đúng một vấn đề ở mục 14.2.1 và có ba thành phần: việc cần làm, con số làm căn cứ lấy từ bài làm của nhóm, và ước lượng tác động tài chính. Mẫu câu gợi ý: \"Đề nghị [hành động]. Căn cứ: [con số, câu số]. Tác động ước tính: [số tiền hoặc phần trăm, kèm giả định].\" Theo Bài 10 (mục 10.1.3), mỗi trang trình bày nên có một thông điệp, tiêu đề là kết luận và con số đi kèm.")
EX("Ví dụ 14.4. Một khuyến nghị đủ ba thành phần (bối cảnh minh hoạ, không phải MOVA)")
P("Đề nghị thay đợt giảm 20% tháng 6 của gói X bằng quà tặng trị giá 5% giá niêm yết. Căn cứ: |E| ước lượng 1,2 thấp hơn ngưỡng hoà vốn 1,82 (Ví dụ 14.3). Tác động ước tính: tránh mức giảm lợi nhuận gộp khoảng 12,9% của tháng khuyến mãi, với giả định độ co giãn không đổi.")
H2("14.6.3. Câu 4.3: Hai hạn chế")
P("Mỗi hạn chế phải gắn với một con số hoặc một chi tiết cụ thể trong bài làm, kèm đề xuất khắc phục. Các hướng gợi ý trong đề: cỡ mẫu khảo sát khi chia nhóm; khoảng cách giữa lời khai và hành vi chưa được hiệu chỉnh trong mô phỏng; các yếu tố ảnh hưởng tới số đơn mà dữ liệu không ghi lại, như chi tiêu quảng cáo theo tháng; chi phí cố định và chi phí thu hút khách chưa được trừ. Câu chung chung kiểu \"mẫu còn nhỏ, cần nghiên cứu thêm\" không được tính.")

# ---------------------------------------------------------------- 14.7
H1("14.7. Quy trình thực hiện, sản phẩm nộp và tiêu chí đánh giá")
H2("14.7.1. Phân bổ thời gian gợi ý")
CAP("Bảng 14.6. Phân bổ 210 phút của buổi thực hành")
T([["Thời gian", "Nội dung", "Sản phẩm trung gian"],
   ["0 đến 10 phút", "Đọc bối cảnh, mở dữ liệu, chia việc trong nhóm", "Danh sách câu và người phụ trách"],
   ["10 đến 50 phút", "Phần 1", "Sheet 1.1 tới 1.4"],
   ["50 đến 115 phút", "Phần 2", "Bảng biến giả, kết quả hồi quy, WTP"],
   ["115 đến 180 phút", "Phần 3", "Đồ thị Van Westendorp, bảng co giãn, bảng hoà vốn"],
   ["180 đến 210 phút", "Phần 4 và trình bày", "Bảng mô phỏng, tệp trình bày 8 trang"]])
SRC("Đề bài Thực hành 4")
H2("14.7.2. Sản phẩm nộp")
B("Tệp Excel bài làm, mỗi câu một sheet đặt tên theo số câu (1.1, 1.2, …). Giữ bảng tính và kết quả hồi quy gốc; con số cuối cùng chép tay không được tính.")
B("Tệp trình bày PowerPoint hoặc PDF, tối đa 8 trang, tóm tắt phát hiện và ba khuyến nghị của câu 4.2. Mỗi trang một thông điệp; tiêu đề biểu đồ nêu kết luận, trục có đơn vị.")
B("Nếu dùng SPSS: nộp thêm tệp đầu ra .spv hoặc ảnh chụp bảng kết quả.")
B("Tên tệp theo mẫu TH4_<Mã lớp>_Nhom<số>.xlsx.")
H2("14.7.3. Thang điểm và tiêu chí đánh giá")
CAP("Bảng 14.7. Thang điểm Thực hành 4")
T([["Phần", "Câu và điểm", "Tổng", "Tiêu chí chính"],
   ["1. Danh mục sản phẩm", "1.1: 0,5; 1.2: 0,5; 1.3: 0,5; 1.4: 0,5", "2,0", "Kiểm tra vai trò cửa ngõ trước khi kết luận"],
   ["2. Conjoint", "2.1: 0,5; 2.2: 0,75; 2.3: 0,5; 2.4: 0,75; 2.5: 0,5", "3,0", "Kiểm tra tuyến tính trước khi quy ra tiền"],
   ["3. Phân tích giá", "3.1: 0,75; 3.2: 0,5; 3.3: 0,75; 3.4: 0,5; 3.5: 0,5", "3,0", "Tách mùa vụ khỏi giá; so với ngưỡng hoà vốn"],
   ["4. Khuyến nghị", "4.1: 0,75; 4.2: 0,75; 4.3: 0,5", "2,0", "Mỗi khuyến nghị có việc, căn cứ, tác động"],
   ["Tổng", "", "10,0", ""]])
SRC("Đề bài Thực hành 4")
P("Các lỗi kỹ thuật bị trừ điểm thường gặp: tạo đủ k biến giả cho thuộc tính k mức; lấy trung bình các biên thay vì biên của tổng; quên lọc gói ở câu 3.3; quên quy giá về tháng ở câu 3.5; nhầm chiều cộng dồn ở Van Westendorp; kết luận từ một cặp tháng duy nhất ở câu 3.3 (e).")

# ---------------------------------------------------------------- end
d.plain_heading("Tóm tắt bài học")
P("Thực hành 4 đặt ba quyết định của một doanh nghiệp dịch vụ lên dữ liệu. Với danh mục, doanh thu của riêng một gói không đủ để quyết định cắt hay giữ; cần xem lợi nhuận gộp và chi tiêu của nhóm khách mà gói đó dẫn vào.")
P("Với sản phẩm mới, hồi quy trên dữ liệu conjoint cho part-worth của từng mức. Tầm quan trọng tính từ biên độ. WTP chỉ tính được khi hữu dụng của giá gần tuyến tính, và trung bình chung có thể che khác biệt giữa các phân khúc. Van Westendorp cho khoảng giá, Gabor-Granger cho mức tối đa hoá doanh thu và độ co giãn khảo sát.")
P("Với khuyến mãi, độ co giãn ước lượng từ dữ liệu bán hàng bị phóng đại khi bỏ sót mùa vụ. Một chương trình giảm giá chỉ có lãi khi |E| vượt ngưỡng hoà vốn, và ngưỡng này tăng khi biên lợi nhuận mỏng hoặc mức giảm lớn. Lời khai thường thổi phồng tỷ lệ chấp nhận, nên cần hiệu chỉnh bằng hành vi thật.")

d.plain_heading("CÂU HỎI ÔN TẬP")
for q in [
    "Vì sao một sản phẩm có tỷ trọng doanh thu thấp vẫn có thể là sản phẩm nên giữ? Nêu hai chỉ số dữ liệu cần kiểm tra trước khi quyết định cắt.",
    "Giải thích nguyên tắc k − 1 biến giả. Điều gì xảy ra nếu đưa đủ k biến giả cùng hằng số vào hồi quy?",
    "Tầm quan trọng tương đối của thuộc tính được tính như thế nào? Vì sao không so part-worth cao nhất giữa các thuộc tính?",
    "Trình bày điều kiện để quy part-worth ra tiền. Nếu hữu dụng của giá giảm 0,5 ở bước đầu và 1,5 ở bước sau, nhà phân tích nên làm gì?",
    "Nêu điều kiện nhất quán của phiếu Van Westendorp. Các đường tần suất tích luỹ cắt nhau ở tỷ lệ thấp nói gì về thị trường?",
    "Vì sao mô hình log-log không có biến giả mùa vụ có thể phóng đại độ co giãn khi doanh nghiệp giảm giá đúng mùa cao điểm? Đề xuất hai cách kiểm chứng.",
    "Một sản phẩm có biên lợi nhuận gộp 40%. Tính ngưỡng |E| hoà vốn xấp xỉ cho mức giảm nhỏ, và giải thích vì sao ngưỡng thực tế cao hơn khi giảm 30%.",
]:
    B(q)

d.plain_heading("TÀI LIỆU THAM KHẢO")
for r in [
    "Nguyễn Bình Minh An, Trương Hoàng Giang (2026). Đề cương bài giảng: Phân tích dữ liệu Marketing. Khoa Kinh doanh số, Trường Kinh tế, Đại học Công nghiệp Hà Nội.",
    "Joseph F. Hair, William C. Black, Barry J. Babin & Rolph E. Anderson (2019). Multivariate Data Analysis. 8th edition. Cengage Learning.",
    "Naresh K. Malhotra (2019). Marketing Research: An Applied Orientation. 7th edition. Pearson.",
    "Paul E. Green & V. Srinivasan (1978). Conjoint analysis in consumer research: Issues and outlook. Journal of Consumer Research, 5(2), 103-123.",
    "Paul E. Green & V. Srinivasan (1990). Conjoint analysis in marketing: New developments with implications for research and practice. Journal of Marketing, 54(4), 3-19.",
    "Peter H. van Westendorp (1976). NSS - Price Sensitivity Meter (PSM): A new approach to study consumer perception of prices. Proceedings of the ESOMAR Congress.",
    "André Gabor & Clive W. J. Granger (1979). Price as an indicator of quality: Report on an enquiry. Management Decision, 17(8), 590-618.",
    "Tammo H. A. Bijmolt, Harald J. van Heerde & Rik G. M. Pieters (2005). New empirical generalizations on the determinants of price elasticity. Journal of Marketing Research, 42(2), 141-156.",
    "Thomas T. Nagle & Georg Müller (2018). The Strategy and Tactics of Pricing: A Guide to Growing More Profitably. 6th edition. Routledge.",
    "Jeffrey M. Wooldridge (2020). Introductory Econometrics: A Modern Approach. 7th edition. Cengage Learning.",
]:
    P(r)

# restart numbering for each group of consecutive list paragraphs
import copy as _c
WN = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
npart = d.doc.part.numbering_part.element
nums = npart.findall(WN + "num")
maxid = max(int(n.get(WN + "numId")) for n in nums)
prev_list = False; cur = None
for el in d.body.iterchildren():
    nid = el.find(".//" + WN + "numPr/" + WN + "numId") if el.tag == WN + "p" else None
    if nid is not None:
        if not prev_list:
            base = next(n for n in nums if n.get(WN + "numId") == nid.get(WN + "val"))
            new = _c.deepcopy(base); maxid += 1; new.set(WN + "numId", str(maxid))
            if new.find(WN + "lvlOverride") is None:
                lo = new.makeelement(WN + "lvlOverride", {WN + "ilvl": "0"}); so = lo.makeelement(WN + "startOverride", {WN + "val": "1"}); lo.append(so); new.append(lo)
            npart.append(new); cur = str(maxid)
        nid.set(WN + "val", cur); prev_list = True
    else:
        prev_list = False

d.save(f"{OUT}/Bai 14_Thuc hanh 4_ĐCBG.docx")
print("ok")
