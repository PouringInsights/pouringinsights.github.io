"""Bài 6 – Sinh dữ liệu khảo sát Likert cho case MỘC AN (thời trang nội địa).

Chạy:  python gen_data.py   (tạo MOCAN_khaosat.csv và MOCAN_bien_quan_sat.csv)
Dữ liệu hư cấu, chỉ dùng cho giảng dạy. Seed cố định nên chạy lại cho kết quả y hệt.

Cấu trúc cài sẵn:
  5 nhân tố tiềm ẩn: Độ bền sản phẩm (CL), Giá trị kinh tế (GT), Trải nghiệm cửa hàng (TN),
  Hình ảnh thương hiệu (TH), Phong cách thiết kế (PC).
  23 biến quan sát đưa vào EFA, trong đó 2 biến "có vấn đề" để người học phát hiện:
    GT5 tải chéo lên Độ bền và Giá trị kinh tế, giống X4 trong case MỘC AN;
    TN5 tải yếu (communality < 0,5), giống X9 trong slide 6.2.3.
  3 biến kết quả YD1–YD3 (ý định mua lại) KHÔNG đưa vào EFA, dùng để nối sang Bài 7.
  4 phân khúc động cơ ẩn, liên hệ vừa phải với nhân khẩu học và hành vi mua.
"""
from pathlib import Path
import numpy as np
import pandas as pd

SEED = 66
N = 420
OUT = Path(__file__).resolve().parent

ITEMS = [
    ("CL1", "CL", 0.82, "Chất liệu bền, không xù sau nhiều lần giặt"),
    ("CL2", "CL", 0.79, "Đường may chắc chắn, không bung chỉ"),
    ("CL3", "CL", 0.77, "Form dáng giữ nguyên sau khi giặt"),
    ("CL4", "CL", 0.74, "Màu vải không phai sau nhiều lần giặt"),
    ("CL5", "CL", 0.72, "Sản phẩm mặc được qua nhiều mùa"),
    ("GT1", "GT", 0.81, "Thường xuyên có chương trình khuyến mãi"),
    ("GT2", "GT", 0.78, "Giá thấp hơn thương hiệu cùng phân khúc"),
    ("GT3", "GT", 0.74, "Chương trình thành viên, tích điểm có lợi"),
    ("GT4", "GT", 0.71, "Tôi thường chờ đợt giảm giá mới mua"),
    ("GT5", "CL+GT", None, "Giá hợp lý so với chất lượng nhận được"),
    ("TN1", "TN", 0.80, "Nhân viên cửa hàng tư vấn tận tình"),
    ("TN2", "TN", 0.78, "Đổi trả dễ dàng, không gây khó khăn"),
    ("TN3", "TN", 0.76, "Không gian cửa hàng dễ chịu, dễ tìm đồ"),
    ("TN4", "TN", 0.73, "Phòng thử sạch sẽ, đủ chỗ"),
    ("TN5", "TN", 0.45, "Thanh toán nhanh, ít phải xếp hàng"),
    ("TH1", "TH", 0.83, "MỘC AN là thương hiệu uy tín"),
    ("TH2", "TH", 0.80, "Tôi tin vào cam kết của MỘC AN"),
    ("TH3", "TH", 0.76, "Tôi tự hào khi dùng thương hiệu nội địa này"),
    ("TH4", "TH", 0.72, "MỘC AN được nhiều người quanh tôi nhắc tới"),
    ("PC1", "PC", 0.81, "Thiết kế bắt kịp xu hướng"),
    ("PC2", "PC", 0.78, "Mẫu mã đa dạng, thường có bộ sưu tập mới"),
    ("PC3", "PC", 0.75, "Quần áo giúp tôi thể hiện phong cách riêng"),
    ("PC4", "PC", 0.72, "Dễ phối đồ với trang phục sẵn có"),
]
OUTCOME = [("YD1", "Tôi sẽ tiếp tục mua MỘC AN trong 6 tháng tới"),
           ("YD2", "Tôi sẽ giới thiệu MỘC AN cho bạn bè"),
           ("YD3", "MỘC AN là lựa chọn đầu tiên khi tôi mua quần áo")]
F = ["CL", "GT", "TN", "TH", "PC"]

# 4 phân khúc ẩn: tỷ trọng và trung bình nhân tố (đơn vị độ lệch chuẩn)
SEG = {
    "San_uu_dai":       (0.30, [-0.4, 1.2, -0.3, -0.4, 0.0]),
    "Thuc_dung_ben":    (0.25, [1.2, -0.2, 0.0, -0.1, -0.6]),
    "Ua_thuong_hieu":   (0.22, [-0.2, -0.7, 0.0, 1.2, 0.9]),
    "Can_trai_nghiem":  (0.23, [-0.4, -0.5, 1.3, -0.2, 0.0]),
}


def likert5(z, shift=0.35):
    cuts = np.array([-1.65, -0.8, 0.1, 1.0]) - shift
    return 1 + np.searchsorted(cuts, z)


def main():
    rng = np.random.default_rng(SEED)
    segs = list(SEG)
    seg = rng.choice(len(segs), N, p=[SEG[s][0] for s in segs])
    mu = np.array([SEG[s][1] for s in segs])[seg]
    fac = mu + rng.normal(0, 0.35, (N, 5))
    fac = (fac - fac.mean(0)) / fac.std(0)                 # chuẩn hoá từng nhân tố
    fz = dict(zip(F, fac.T))

    data = {}
    for code, f, lam, _ in ITEMS:
        if code == "GT5":
            sys_part = 0.58 * fz["CL"] + 0.55 * fz["GT"]
            err_sd = np.sqrt(max(0.05, 1 - np.var(sys_part)))
            z = sys_part + rng.normal(0, err_sd, N)
        else:
            z = lam * fz[f] + rng.normal(0, np.sqrt(1 - lam ** 2), N)
        data[code] = likert5(z)

    yd = 0.38 * fz["CL"] + 0.40 * fz["GT"] + 0.36 * fz["TN"] + 0.28 * fz["TH"] + 0.22 * fz["PC"]
    yd = yd / yd.std() * 0.75
    for code, _ in OUTCOME:
        data[code] = likert5(yd + rng.normal(0, 0.62, N), shift=0.2)

    df = pd.DataFrame(data)
    # Nhân khẩu học và hành vi: liên hệ vừa phải với phân khúc ẩn
    p_tuoi = {0: [.45, .35, .14, .06], 1: [.12, .30, .35, .23], 2: [.20, .48, .24, .08], 3: [.15, .30, .30, .25]}
    p_tn = {0: [.40, .38, .17, .05], 1: [.20, .40, .28, .12], 2: [.08, .30, .37, .25], 3: [.15, .37, .31, .17]}
    p_kenh = {0: [.25, .25, .50], 1: [.45, .30, .25], 2: [.40, .40, .20], 3: [.70, .18, .12]}
    nhom_tuoi = ["18-24", "25-34", "35-44", "45+"]
    thu_nhap = ["Dưới 10 triệu", "10-20 triệu", "20-35 triệu", "Trên 35 triệu"]
    kenh = ["Cửa hàng", "Website/App MỘC AN", "Sàn TMĐT"]
    df.insert(0, "ma_dv", [f"MA{i:03d}" for i in range(1, N + 1)])
    df["gioi_tinh"] = rng.choice(["Nữ", "Nam"], N, p=[0.68, 0.32])
    df["nhom_tuoi"] = [rng.choice(nhom_tuoi, p=p_tuoi[s]) for s in seg]
    df["thu_nhap"] = [rng.choice(thu_nhap, p=p_tn[s]) for s in seg]
    df["kenh_mua_chinh"] = [rng.choice(kenh, p=p_kenh[s]) for s in seg]
    df["thanh_pho"] = rng.choice(["Hà Nội", "TP.HCM", "Đà Nẵng"], N, p=[0.45, 0.40, 0.15])
    lan = np.array([5.5, 3.0, 3.5, 3.8])[seg]
    aov = np.array([380, 620, 850, 560])[seg]              # nghìn đồng / đơn
    df["so_lan_mua_12t"] = np.maximum(1, rng.poisson(lan))
    df["chi_tieu_12t_nghin"] = np.round(df["so_lan_mua_12t"] * aov * np.exp(rng.normal(0, 0.25, N)), -1).astype(int)

    dic = pd.DataFrame([(c, t, "EFA") for c, _, _, t in ITEMS] + [(c, t, "Kết quả (không đưa vào EFA)") for c, t in OUTCOME],
                       columns=["ma_bien", "noi_dung", "vai_tro"])
    df.to_csv(OUT / "MOCAN_khaosat.csv", index=False, encoding="utf-8-sig")
    dic.to_csv(OUT / "MOCAN_bien_quan_sat.csv", index=False, encoding="utf-8-sig")
    # nhãn phân khúc thật chỉ để giảng viên đối chiếu, tách file riêng
    pd.DataFrame({"ma_dv": df["ma_dv"], "phan_khuc_an": np.array(segs)[seg]}).to_csv(
        OUT / "_dap_an_phan_khuc_an.csv", index=False, encoding="utf-8-sig")
    print(f"MOCAN_khaosat.csv        {len(df):>4} dòng, {df.shape[1]} cột")
    print(f"MOCAN_bien_quan_sat.csv  {len(dic):>4} dòng")
    print(f"_dap_an_phan_khuc_an.csv {len(df):>4} dòng (chỉ dành cho giảng viên)")


if __name__ == "__main__":
    main()
