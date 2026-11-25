"""Bài 5 – Lời giải tham khảo case NAVIO: retention theo cohort, CLV công thức rút gọn (hai phòng),
CLV theo cohort 24 tháng, thời gian hoàn vốn CAC, LTV:CAC theo kênh; bài tập slide 10.

Chạy sau gen_data.py:  python solution.py
Cần: pandas, numpy.
"""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
BIEN_LN = 0.40
CHIET_KHAU_NAM = 0.10
THANG_CUOI = pd.Period("2025-06", "M")
pd.set_option("display.width", 160, "display.max_columns", 30, "display.float_format", "{:,.2f}".format)


def tieu_de(s):
    print("\n" + "=" * 78 + f"\n{s}\n" + "=" * 78)


kh = pd.read_csv(D / "NAVIO_khach_hang.csv")
gd = pd.read_csv(D / "NAVIO_giao_dich.csv")
cp = pd.read_csv(D / "NAVIO_chi_phi_kenh.csv")
kh["cohort"] = pd.PeriodIndex(kh["thang_gia_nhap"], freq="M")
gd["thang"] = pd.PeriodIndex(gd["thang"], freq="M")
gd = gd.merge(kh[["ma_kh", "cohort", "kenh_thu_hut"]], on="ma_kh")
gd["t"] = (gd["thang"] - gd["cohort"]).apply(lambda x: x.n) + 1      # tháng thứ mấy của khách

# ===========================================================================
# 1. Ma trận retention theo cohort
# ===========================================================================
tieu_de("1. RETENTION THEO COHORT")
print(f"{len(kh)} khách hàng, {kh.cohort.nunique()} cohort ({kh.cohort.min()} – {kh.cohort.max()}), "
      f"{len(gd)} lượt thanh toán tháng")
size = kh.groupby("cohort").size()
act = gd.groupby(["cohort", "t"]).size().unstack()
ret = act.div(size, axis=0)
show = ret.loc[["2023-01", "2023-07", "2024-01", "2024-07", "2025-01", "2025-04"], [1, 2, 3, 4, 6, 7, 12, 24]]
print("Tỷ lệ còn hoạt động (một số cohort, tháng 1/2/3/4/6/7/12/24):")
print((show * 100).round(1).to_string())

# Tỷ lệ rời bỏ theo tuổi đời, chỉ tính những khách đã quan sát được tháng kế tiếp (tránh lỗi kiểm duyệt)
last = gd.groupby("ma_kh")["t"].max()
gd["roi_bo"] = gd["ma_kh"].map(last) == gd["t"]
gd["quan_sat_duoc"] = gd["thang"] < THANG_CUOI
h = gd[gd.quan_sat_duoc & (gd.cohort < pd.Period("2025-01", "M"))].groupby("t")["roi_bo"].mean()
a = gd.groupby("t")["doanh_thu"].mean()
bang = pd.DataFrame({"churn_%": h * 100, "ARPU": a}).loc[[1, 2, 3, 4, 5, 6, 7, 12, 18, 24]]
print("\nTỷ lệ rời bỏ theo tháng tuổi đời (cohort trước 2025) và ARPU:")
print(bang.round(1).to_string())

c25 = ret.loc[ret.index >= pd.Period("2025-01", "M"), [2, 3]].mean()
c24 = ret.loc[(ret.index >= pd.Period("2024-01", "M")) & (ret.index < pd.Period("2025-01", "M")), [2, 3]].mean()
print(f"\nRetention tháng 2 / tháng 3: cohort 2024 = {c24[2] * 100:.1f}% / {c24[3] * 100:.1f}%, "
      f"cohort 2025 = {c25[2] * 100:.1f}% / {c25[3] * 100:.1f}%  -> onboarding mới có tác dụng")

# ===========================================================================
# 2. CLV theo cách của hai phòng (công thức rút gọn)
# ===========================================================================
tieu_de("2. CLV CÔNG THỨC RÚT GỌN: PHÒNG TÀI CHÍNH vs PHÒNG MARKETING")
CAC_TB = cp["chi_phi_thu_hut"].sum() / cp["so_kh_moi"].sum()
print(f"CAC bình quân = {CAC_TB:,.0f} đ")
arpu1, churn1 = a[1], h[1]
old = gd[gd.t >= 7]
arpu7 = old["doanh_thu"].mean()
churn7 = gd[gd.quan_sat_duoc & (gd.t >= 7)]["roi_bo"].mean()
for ten, ar, ch in [("Tài chính (tháng 1)", arpu1, churn1), ("Marketing (khách > 6 tháng)", arpu7, churn7)]:
    clv = ar * BIEN_LN / ch
    print(f"{ten:30s} ARPU {ar:>9,.0f}  churn {ch * 100:5.1f}%  CLV {clv:>11,.0f} đ  LTV:CAC {clv / CAC_TB:5.2f}")

# ===========================================================================
# 3. CLV theo cohort: cộng dồn lợi nhuận gộp thực nhận trong 24 tháng
# ===========================================================================
tieu_de("3. CLV THEO COHORT (24 THÁNG, cohort 07/2022 – 06/2023)")
mature = kh[kh.cohort <= pd.Period("2023-06", "M")]
g24 = gd[gd.ma_kh.isin(mature.ma_kh) & (gd.t <= 24)]
lnt = g24.groupby("t")["doanh_thu"].sum() * BIEN_LN / len(mature)       # lợi nhuận gộp bình quân / KH mới
clv24 = lnt.sum()
r = (1 + CHIET_KHAU_NAM) ** (1 / 12) - 1
clv24_ck = (lnt / (1 + r) ** lnt.index).sum()
song = g24.groupby("t").size() / len(mature)
cum = lnt.cumsum()
payback = int(cum[cum >= CAC_TB].index.min())
print(f"Số khách mới trong các cohort đủ 24 tháng: {len(mature)}")
print(f"CLV cohort 24 tháng (không chiết khấu) = {clv24:,.0f} đ  -> LTV:CAC = {clv24 / CAC_TB:.2f}")
print(f"CLV cohort 24 tháng (chiết khấu 10%/năm) = {clv24_ck:,.0f} đ  -> LTV:CAC = {clv24_ck / CAC_TB:.2f}")
print(f"Tuổi thọ kỳ vọng trong 24 tháng = {song.sum():.1f} tháng")
print(f"Tháng hoàn vốn CAC: tháng thứ {payback}")
print(f"Tỷ trọng giá trị nằm ở tháng 7 trở đi: {lnt[lnt.index >= 7].sum() / clv24 * 100:.0f}%")

# ===========================================================================
# 4. LTV:CAC theo kênh thu hút
# ===========================================================================
tieu_de("4. LTV:CAC THEO KÊNH THU HÚT")
cp["CAC"] = cp["chi_phi_thu_hut"] / cp["so_kh_moi"]
rows = []
for k, g in mature.groupby("kenh_thu_hut"):
    gg = g24[g24.ma_kh.isin(g.ma_kh)]
    v = gg["doanh_thu"].sum() * BIEN_LN / len(g)
    s2 = gg[gg.t == 2].shape[0] / len(g)
    rows.append((k, len(g), s2 * 100, v))
t = pd.DataFrame(rows, columns=["kenh_thu_hut", "so_kh_mature", "con_lai_thang2_%", "CLV24"]).merge(
    cp[["kenh_thu_hut", "CAC"]], on="kenh_thu_hut")
t["LTV_CAC"] = t["CLV24"] / t["CAC"]


def danh_gia(x):
    if x < 1:
        return "Lỗ: dừng mở rộng"
    if x < 3:
        return "Mỏng: giảm CAC / tăng giữ chân"
    if x <= 5:
        return "Lành mạnh"
    return "Rất tốt: có thể tăng ngân sách"


t["danh_gia"] = t["LTV_CAC"].apply(danh_gia)
print(t.sort_values("LTV_CAC", ascending=False).round(2).to_string(index=False))

# ===========================================================================
# 5. Bài tập slide 10 – ứng dụng học tiếng Anh
# ===========================================================================
tieu_de("5. BÀI TẬP SLIDE 10 – ỨNG DỤNG HỌC TIẾNG ANH (biên 62%, CAC 260.000 đ)")
bt = pd.read_csv(D / "bai_tap_app_tieng_anh.csv")
bt["ARPU_thang"] = bt["doanh_thu_kh_6_thang"] / 6
bt["CLV"] = bt["ARPU_thang"] * 0.62 / bt["ty_le_roi_bo_thang"]
bt["LTV_CAC"] = bt["CLV"] / 260_000
bt["customer_equity"] = bt["CLV"] * bt["so_kh"]
bt["gia_tri_rui_ro_thang"] = bt["so_kh"] * bt["ty_le_roi_bo_thang"] * bt["CLV"]
print(bt.round(2).to_string(index=False))
print(f"Tổng customer equity = {bt['customer_equity'].sum():,.0f} đ")
print("Phân khúc LTV:CAC < 1:", ", ".join(bt.loc[bt.LTV_CAC < 1, "phan_khuc"]))
