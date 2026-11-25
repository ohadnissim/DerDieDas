#!/usr/bin/env python3
"""Make the sound of every tile for the Lesen game (audio/pk-lesen.mp3).

For each word: Mila says it (ElevenLabs, native PCM, the CLAUDE.md settings), ElevenLabs forced alignment gives the time
of every letter, and each tile plays the word up to and including that tile, cut from that take at Mila's own speed
(M … Mau … Maus). Nothing is stretched (stretched single sounds sounded robotic).
The whole word is set to -14 LUFS once and every tile gets that same gain, then one soxr resample and one MP3 encode
for the whole pack. Prints the PACKS entry for index.html.

  python3 tools/make_lesen.py words.json out_dir            # words.json: [{"id", "noun", "parts": [...]}, ...]
Needs ELEVENLABS_API_KEY (in ~/.rtm_secrets), ffmpeg, sox.
"""
import json, os, subprocess, sys

VOICE = "fv11tAuhEP21B7SqCbiG"   # German Girl - Mila
KEY = os.environ["ELEVENLABS_API_KEY"]
HOLD = set("mnlsfwhjrv") | {"sch", "ss", "ch", "ll", "nn", "mm", "ff"}
VOWELS = {"a", "e", "i", "o", "u", "ä", "ö", "ü", "au", "ei", "eu", "ie", "uh", "ee", "er", "ah", "oh"}
SR = 24000


def post(url, body=None, files=None):
    # curl, not urllib: some Python installs on the Mac have no certificate store
    cmd = ["curl", "-sS", "--fail", "-X", "POST", url, "-H", "xi-api-key: " + KEY]
    if files:
        for k, v in files.items():
            cmd += ["-F", f"{k}=@{v}"] if k == "file" else ["--form-string", f"{k}={v}"]
    else:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(body)]
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0:
            return r.stdout
    raise SystemExit(f"{url} failed: {r.stderr.decode()[:200]}")   # (never print cmd: it holds the key)


def save(path, data):
    # write only once the download worked, so a failed run never leaves an empty file behind
    tmp = path + ".part"; open(tmp, "wb").write(data); os.replace(tmp, path)


def sh(*a):
    subprocess.run(a, check=True, capture_output=True)


def lufs(wav):
    out = subprocess.run(["ffmpeg", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in out.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def main(words_file, out):
    os.makedirs(out, exist_ok=True)
    words = json.load(open(words_file))
    pieces, pack = [], {}
    gap = os.path.join(out, "gap.wav")
    sh("sox", "-n", "-r", "44100", "-c", "1", "-b", "32", "-e", "floating-point", gap, "trim", "0", "0.3")
    t = 0.3
    report = []
    for w in words:
        wid, noun, parts = w["id"], w["noun"], w["parts"]
        assert "".join(parts).lower() == noun.lower(), (noun, parts)
        pcm = os.path.join(out, f"{wid}.pcm")
        if not os.path.getsize(pcm) if os.path.exists(pcm) else True:
            save(pcm, post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=pcm_24000",
                                       {"text": noun, "model_id": "eleven_turbo_v2_5", "language_code": "de", "voice_settings": {"speed": 0.9}}))
        raw = os.path.join(out, f"{wid}.raw.wav")
        sh("sox", "-t", "raw", "-r", str(SR), "-e", "signed", "-b", "16", "-c", "1", pcm, raw)   # a plain 16-bit WAV of the take, as recorded
        al = os.path.join(out, f"{wid}.align.json")
        if not os.path.getsize(al) if os.path.exists(al) else True:
            save(al, post("https://api.elevenlabs.io/v1/forced-alignment", files={"file": raw, "text": noun}))
        chars = [c for c in json.load(open(al))["characters"] if c["text"].strip()]
        heard = json.loads(post("https://api.elevenlabs.io/v1/speech-to-text", files={"file": raw, "model_id": "scribe_v1", "language_code": "de"}))["text"]
        report.append(f"{noun:10s} heard: {heard}")
        gain = -14 - lufs(raw)
        # Each tile plays the word SO FAR, at Mila's own speed: M … Mau … Maus. (The first version cut each sound alone and
        # stretched the short ones; Ohad: "the words sound robotic/slowed down".) Nothing is stretched, only cut.
        a0 = max(0, chars[0]["start"] - 0.03)
        total = float(subprocess.run(["soxi", "-D", raw], capture_output=True, text=True).stdout)
        k = 0
        for i, p in enumerate(parts):
            seg = chars[k:k + len(p)]; k += len(p)
            last = i == len(parts) - 1
            b = total if last else min(total, seg[-1]["end"] + 0.02)
            dur = b - a0
            cut = os.path.join(out, f"{wid}-{i}.wav")
            sh("sox", raw, "-b", "32", "-e", "floating-point", cut, "trim", f"{a0:.3f}", f"{dur:.3f}", "vol", f"{gain}dB",
               "fade", "t", "0.008", "0", "0.012" if last else "0.035", "rate", "-v", "44100")
            lim = os.path.join(out, f"{wid}-{i}.l.wav")
            sh("ffmpeg", "-y", "-i", cut, "-af", "alimiter=limit=0.891:attack=5:release=60:level=false", "-c:a", "pcm_f32le", lim)
            d = float(subprocess.run(["soxi", "-D", lim], capture_output=True, text=True).stdout)
            pack[f"lt-{wid}-{i}"] = [round(t, 3), round(d, 3)]
            pieces += [lim, gap]
            t += d + 0.3
    allw = os.path.join(out, "all.wav")
    sh("sox", gap, *pieces, allw)
    return pack, allw, report


if __name__ == "__main__":
    pack, allw, report = main(sys.argv[1], sys.argv[2])
    print("\n".join(report), file=sys.stderr)
    print(json.dumps(pack, separators=(",", ":")))
    print(allw, file=sys.stderr)
