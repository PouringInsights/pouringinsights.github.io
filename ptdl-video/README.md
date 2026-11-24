# PTDL Marketing – bài giảng lồng tiếng AI

Lời giảng: `scripts/bN_script.json` (một mục / slide). Giọng mẫu Manus: `voice_ref/`.
Đầu ra: `Bai_N_PTDL_Marketing_long_tieng.pptx` cùng định dạng Bài 9/10 (intro HaUI, mỗi slide 1 file m4a 320k, −23 LUFS, fade 2 s, tự chuyển).

## Chạy trên máy có GPU (F5-TTS)
```
python ptdl-video/tools/prepare.py C:\Users\hoang\tts\work
# mô hình: C:\Users\hoang\tts\work\f5vi\model_last.pt + vocab.txt (hynt/F5-TTS-Vietnamese-ViVoice)
python ptdl-video/tools/f5_narrate.py C:\Users\hoang\tts\work 1 --only 1,2   # thử
python ptdl-video/tools/f5_narrate.py C:\Users\hoang\tts\work 1
python ptdl-video/tools/build_pptx.py C:\Users\hoang\tts\work 1 C:\Users\hoang\tts\work\out\Bai_1_PTDL_Marketing_long_tieng.pptx
```
Công cụ khác: `narrate.py` (VieNeu, CPU), `gem_narrate.py` (Gemini TTS), `manus_worker.sh`, `extract.py`.
