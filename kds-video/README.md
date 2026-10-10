# Video giới thiệu Khoa Kinh doanh số: bản A và bản B

Mã nguồn dựng hai phiên bản video bằng [OpenMontage](https://github.com/calesthio/OpenMontage) (bộ dựng Remotion `remotion-composer`).

| Bản | Mô tả | Thời lượng |
|---|---|---|
| **A: thêm ảnh** (`remotion/VersionA.tsx`) | Giữ nguyên hình, giọng đọc Manus và nhạc của v1. Chèn ảnh và video trải nghiệm đúng câu lời dẫn (theo mốc thời gian từng từ). | 3:19 |
| **B: làm mới** (`remotion/VersionB.tsx`, `remotion/bkit.tsx`) | Rút gọn lời dẫn: bỏ các câu sến, ghép lại từ chính giọng đọc Manus của v1. Hình gồm motion graphic (chữ động, số đếm, bản đồ giảng viên, biểu đồ, mạng lưới đối tác) kết hợp ảnh và video thật. | ~2:00 |

## Quy trình
1. Tách giọng đọc khỏi nhạc nền của v1 bằng Demucs (`htdemucs`, two-stems).
2. Nhận dạng giọng nói kèm mốc thời gian từng từ bằng faster-whisper (`scripts/transcribe.py`), kết quả ở `scripts/v1_transcript.json`.
3. Bản B: `scripts/build_voice.py` cắt và ghép các câu tại điểm lặng nhất giữa hai từ, kết quả ở `scripts/b_voice_plan.json`.
4. Render bằng Remotion:
   ```
   npx remotion render src/kds/index.tsx KDS-A out/KDS_A_them_anh.mp4
   npx remotion render src/kds/index.tsx KDS-B out/KDS_B_lam_moi.mp4
   ```
   Đặt thư mục `remotion/` vào `remotion-composer/src/kds/`. Ảnh, clip, âm thanh và font nằm ở `remotion-composer/public/kds/`; chúng không được commit vì dung lượng lớn.
