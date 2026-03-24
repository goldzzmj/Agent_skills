from __future__ import annotations

from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from moviepy.config import change_settings
from moviepy.editor import AudioFileClip, CompositeAudioClip, CompositeVideoClip, ImageClip, concatenate_videoclips


change_settings({"FFMPEG_BINARY": imageio_ffmpeg.get_ffmpeg_exe()})

ROOT = Path(r"E:\Project\AI_Agent\自动视频剪辑\AI视频-2026-03-24")
PHOTO_DIR = ROOT / "领证照片"
MUSIC_DIR = ROOT / "bgm" / "音乐文件"
OUT_DIR = ROOT / "output" / "ltx_assets"
FRAME_DIR = OUT_DIR / "frames"
VIDEO_PATH = OUT_DIR / "ltx_ready_beatcut.mp4"

W = 1280
H = 720
FPS = 24
TARGET_DURATION = 180.0


def fit_frame(path: Path) -> Path:
    out = FRAME_DIR / f"{path.stem}.jpg"
    if out.exists():
        return out
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img).convert("RGB")
        bg = img.resize((W, H), Image.Resampling.LANCZOS).filter(ImageFilter.GaussianBlur(18))
        bg = Image.blend(bg, Image.new("RGB", (W, H), (0, 0, 0)), 0.2)
        fg = img.copy()
        fg.thumbnail((W, H), Image.Resampling.LANCZOS)
        x = (W - fg.width) // 2
        y = (H - fg.height) // 2
        bg.paste(fg, (x, y))
        out.parent.mkdir(parents=True, exist_ok=True)
        bg.save(out, quality=92)
    return out


def pick_images() -> list[Path]:
    files = sorted(PHOTO_DIR.glob("*.JPG"))
    need = 122
    idxs = np.linspace(0, len(files) - 1, need)
    return [files[int(round(i))] for i in idxs]


def clip_pattern(count: int) -> list[float]:
    patt = [1.00, 0.82, 0.68, 0.92, 1.10, 0.74, 0.86, 1.18]
    vals = [patt[i % len(patt)] for i in range(count)]
    scale = TARGET_DURATION / sum(vals)
    vals = [round(v * scale, 3) for v in vals]
    diff = TARGET_DURATION - sum(vals)
    vals[-1] += diff
    return vals


def build_video(images: list[Path]):
    durations = clip_pattern(len(images))
    clips = []
    for i, (img, dur) in enumerate(zip(images, durations)):
        base = ImageClip(str(fit_frame(img))).set_duration(dur)
        start_zoom = 1.0 + (0.02 if i % 2 == 0 else 0.05)
        end_zoom = start_zoom + (0.04 if dur < 0.9 else 0.02)
        mov = base.resize(lambda t, sz=start_zoom, ez=end_zoom, dd=dur: sz + (ez - sz) * (t / dd)).set_position("center")
        comp = CompositeVideoClip([mov], size=(W, H)).set_duration(dur)
        clips.append(comp.fadein(min(0.08, dur / 5)).fadeout(min(0.08, dur / 5)))
    return concatenate_videoclips(clips, method="compose", padding=-0.06)


def build_audio():
    songs = sorted(MUSIC_DIR.glob("*.mp3"))
    if len(songs) < 2:
        raise SystemExit("Need at least two mp3 files")
    src1 = AudioFileClip(str(songs[0]))
    src2 = AudioFileClip(str(songs[1]))
    a1 = src1.subclip(0, min(88, src1.duration)).audio_fadeout(0.8)
    start2 = max(0, src2.duration - 92)
    a2 = src2.subclip(start2, min(src2.duration, start2 + 92)).audio_fadein(0.8)
    return CompositeAudioClip([a1.set_start(0), a2.set_start(87.2)]).set_duration(TARGET_DURATION)


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    imgs = pick_images()
    vid = build_video(imgs).set_duration(TARGET_DURATION)
    audio = build_audio()
    final = vid.set_audio(audio)
    final.write_videofile(
        str(VIDEO_PATH),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        bitrate="5500k",
        ffmpeg_params=["-pix_fmt", "yuv420p"],
        threads=4,
    )


if __name__ == "__main__":
    main()
