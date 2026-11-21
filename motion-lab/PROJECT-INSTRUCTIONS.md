# Instruction cho project "Thảo Go Social" trên claude.ai

Dán toàn bộ phần trong khung dưới vào **Project → Instructions** (Set project instructions).

```text
Đây là project làm nội dung mạng xã hội có chuyển động, 3D và video.

BỘ CÔNG CỤ
Mọi thư viện đã được khai báo sẵn, có phiên bản cố định, trong repo công khai:
https://github.com/PouringInsights/pouringinsights.github.io (thư mục motion-lab/)
- JS: Three.js, React Three Fiber, React Three Rapier, React Postprocessing, three.quarks,
  Tweakpane, GSAP, lottie-web, Motion, Remotion.
- Python: Manim, librosa, WhisperX (bản CPU). Hệ thống: FFmpeg.
- Openverse API (https://api.openverse.org/v1/) để tìm âm thanh/nhạc miễn phí.

CÀI ĐẶT (làm tự động, không hỏi lại tôi)
Khi một việc cần chạy code với các thư viện trên, ở đầu cuộc chat hãy chạy:
  git clone --depth 1 -b claude/ecstatic-hawking-y3r2wt https://github.com/PouringInsights/pouringinsights.github.io /tmp/tgs
  bash /tmp/tgs/motion-lab/setup.sh js     # nếu chỉ cần JS (nhanh)
  bash /tmp/tgs/motion-lab/setup.sh py     # nếu cần Manim/librosa/WhisperX
  bash /tmp/tgs/motion-lab/setup.sh        # nếu cần tất cả
Chỉ cài phần cần cho việc đang làm. Python: source /tmp/tgs/motion-lab/.venv/bin/activate.
Nếu không clone được repo, cài trực tiếp đúng phiên bản trong motion-lab/package.json và
motion-lab/requirements.txt (torch==2.8.0 bản CPU từ https://download.pytorch.org/whl/cpu).
Hướng dẫn chọn thư viện nào cho việc gì: .claude/skills/motion-video-toolkit/SKILL.md trong repo.

QUY TẮC
- Dùng các skill motion-design, motion, remotion-* , anatomy-reveal khi phù hợp.
- Âm thanh từ Openverse: luôn ghi lại license, tác giả và link gốc của từng file.
- Video xuất ra: MP4 H.264, yuv420p, +faststart; khung dọc 9:16 cho Reels/TikTok/Shorts trừ khi tôi nói khác.
- Tôn trọng prefers-reduced-motion khi làm animation cho web.
```

## Cần bật trên claude.ai

- **Settings → Capabilities → Code execution and file creation**: bật.
- Trong cùng mục, **network/domain allowlist**: cho phép `github.com` (để clone repo), các package
  registry (npm, PyPI), `download.pytorch.org` và `api.openverse.org`. Nếu có tuỳ chọn "All domains" thì chọn cái đó cho đơn giản.
- Môi trường chạy code của claude.ai bị xoá sau mỗi cuộc chat, nên Claude sẽ tự chạy `setup.sh`
  mỗi lần cần. Phần JS mất khoảng nửa phút, phần Python khoảng một phút (tải ~3GB).
- WhisperX trên CPU chạy chậm với file dài; nên cắt audio thành đoạn ngắn.
