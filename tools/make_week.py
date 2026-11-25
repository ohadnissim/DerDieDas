#!/usr/bin/env python3
"""A new school word list, the usual way, in one go (roadmap step 10).

Claude reads the photo of the school sheet and writes the list; this tool makes everything else:
  - the word card for each word (Higgsfield nano_banana_2, the word-card recipe in CLAUDE.md, two takes; take 1 is used unless
    --pick says otherwise; a crop of the sheet's own drawing in --refs/<id>.png is used as the first reference when it exists),
  - Mila's recordings for each word: w- ("der Bär"), n- ("Bär"), q-…-der/die/das ("der Bär?"), and st-den- for der-words
    ("den Bären"), ElevenLabs PCM, the CLAUDE.md processing, each checked with speech-to-text, packed into audio/pw-<id>.mp3,
  - data/words.json (the new week, version + 1), and in index.html: PACKS, NOUN_IDS, DEN_IDS and AUDIO_V; the previous week's
    words are built into index.html (const <LETTER>_WORDS, added to KNOWN_WORDS) the way M_WORDS and I_WORDS are, so they keep
    working as review words after words.json moves on.

  python3 tools/make_week.py week.txt --title "Wortschatz B,b" [--letter b] [--refs dir] [--pick bär=2,ball=1] [--dry]

week.txt, one word per line:  der Bär 🐻   or, when "den" is not just "den <word>":  der Affe 🐒 | den Affen
Needs ELEVENLABS_API_KEY (~/.rtm_secrets), the higgsfield CLI (signed in), ffmpeg, sox. Prints what read back wrong, so it can
be re-recorded before the PR. Everything it makes for review (both card takes, a contact sheet) goes to --work.
"""
import argparse, json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # --root points it at a copy, for a test run
VOICE = "fv11tAuhEP21B7SqCbiG"   # German Girl - Mila
STYLE_REFS = ["img/i-igel.webp", "img/l-lama.webp"]


def norm(s):
    s = s.strip().lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9-]", "", s)


def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, **k)


def curl_post(url, key, body=None, files=None):
    cmd = ["curl", "-sS", "--fail", "-X", "POST", url, "-H", "xi-api-key: " + key]
    if files:
        for k, v in files.items():
            cmd += ["-F", f"{k}=@{v}"] if k == "file" else ["--form-string", f"{k}={v}"]
    else:
        cmd += ["-H", "Content-Type: application/json", "--data-binary", json.dumps(body)]
    for _ in range(3):
        r = subprocess.run(cmd, capture_output=True)
        if r.returncode == 0:
            return r.stdout
    raise SystemExit(f"{url} failed: {r.stderr.decode()[:200]}")   # never print cmd: it holds the key


def parse(path):
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        main, _, den = line.partition("|")
        m = re.match(r"^(der|die|das)\s+(\S+)\s*(.*)$", main.strip(), re.I)
        if not m:
            raise SystemExit(f"can't read: {line}")
        art, noun, emoji = m.group(1).lower(), m.group(2), m.group(3).strip() or "⭐"
        out.append({"id": norm(noun), "noun": noun, "article": art, "emoji": emoji,
                    "den": (den.strip() or f"den {noun}") if art == "der" else None})
    return out


def result_urls(out):
    """the finished picture(s) of a Higgsfield job: its result_url, never the reference images also listed in the reply
    (taking the first link in the reply once gave back the hedgehog reference as a "bear" when a job failed)"""
    try:
        d = json.loads(out)
    except ValueError:
        return []
    jobs = d if isinstance(d, list) else [d]
    return [j["result_url"] for j in jobs if isinstance(j, dict) and j.get("result_url")]


def card(w, letter, work, refs, take_pick, dry):
    out = os.path.join(ROOT, "img", f"{letter}-{w['id']}.webp")
    if os.path.exists(out):
        return f"img/{letter}-{w['id']}.webp"
    if dry:
        return f"img/{letter}-{w['id']}.webp"
    up = []
    sheet = os.path.join(refs, w["id"] + ".png") if refs else None
    for p in ([sheet] if sheet and os.path.exists(sheet) else []) + [os.path.join(ROOT, r) for r in STYLE_REFS]:
        png = os.path.join(work, os.path.basename(p).rsplit(".", 1)[0] + ".ref.png")
        sh("magick", p, png)
        up.append(json.loads(sh("higgsfield", "upload", "create", png, "--json").stdout)["id"])
    first = "drawn like the first reference image (the school worksheet drawing: same pose, same shapes and colours). Draw it in exactly the same style as the other reference images (the hedgehog and the llama)" if len(up) == 3 \
        else "Draw it in exactly the same style as the reference images (the hedgehog and the llama)"
    prompt = (f"Picture card for a children's word game: {w['noun']} ({w['article']} {w['noun']}, German), {first}: soft hand-drawn coloured "
              "pencil and watercolour children's book illustration, simple, friendly, clear outline, one object alone in the middle, on a plain "
              "flat warm cream paper background (#F2EFE7). No frame, no border, no shadow box, no text, no letters.")
    takes = []
    for t in (1, 2):
        args = ["higgsfield", "generate", "create", "nano_banana_2", "--prompt", prompt, "--aspect_ratio", "1:1", "--resolution", "1k",
                "--wait", "--wait-timeout", "6m", "--json"]
        for u in up:
            args += ["--image-references", u]
        res = subprocess.run(args, capture_output=True, text=True).stdout
        urls = result_urls(res)
        if urls:
            p = os.path.join(work, f"{w['id']}-{t}.png")
            sh("curl", "-s", "-o", p, urls[0]); takes.append(p)
    if not takes:
        print(f"  ! no card made for {w['noun']}", file=sys.stderr); return None
    src = takes[min(len(takes), take_pick.get(w["id"], 1)) - 1]
    sh("magick", src, "-fuzz", "8%", "-trim", "+repage", "-resize", "330x330", "-background", "#F2EFE7", "-gravity", "center",
       "-extent", "420x420", "-fuzz", "6%", "-fill", "#F2EFE7", "-draw", "color 2,2 floodfill", "-quality", "82", out)
    return f"img/{letter}-{w['id']}.webp"


def lufs(wav):
    o = subprocess.run(["ffmpeg", "-nostats", "-i", wav, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float([l for l in o.splitlines() if l.strip().startswith("I:")][-1].split()[1])


def clip(key, text, work, api):
    """one Mila clip: PCM take → trim, 2:1 compression, -14 LUFS, soft peak catch, one soxr resample to 44.1 kHz (float WAV)"""
    pcm = os.path.join(work, key + ".pcm")
    if not (os.path.exists(pcm) and os.path.getsize(pcm)):
        data = curl_post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format=pcm_24000", api,
                         {"text": text, "model_id": "eleven_turbo_v2_5", "language_code": "de", "voice_settings": {"speed": 0.9}})
        open(pcm + ".part", "wb").write(data); os.replace(pcm + ".part", pcm)
    pre = ("silenceremove=start_periods=1:start_threshold=-50dB:start_silence=0.02,areverse,silenceremove=start_periods=1:"
           "start_threshold=-50dB:start_silence=0.06,areverse,acompressor=ratio=2:threshold=-24dB:attack=10:release=120")
    raw = os.path.join(work, key + ".24.wav")
    sh("ffmpeg", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", pcm, "-af", pre, "-c:a", "pcm_f32le", raw)
    g = -14 - lufs(raw)
    lim = os.path.join(work, key + ".l.wav")
    sh("ffmpeg", "-y", "-i", raw, "-af", f"volume={g}dB,alimiter=limit=0.891:attack=5:release=60:level=false", "-c:a", "pcm_f32le", lim)
    out = os.path.join(work, key + ".wav")
    sh("sox", lim, "-b", "32", "-e", "floating-point", out, "rate", "-v", "44100")
    heard = json.loads(curl_post("https://api.elevenlabs.io/v1/speech-to-text", api, files={"file": out, "model_id": "scribe_v1", "language_code": "de"})).get("text", "")
    return out, heard


def pack(name, clips, work):
    gap = os.path.join(work, "gap.wav")
    sh("sox", "-n", "-r", "44100", "-c", "1", "-b", "32", "-e", "floating-point", gap, "trim", "0", "0.3")
    files, t, m = [gap], 0.3, {}
    for key, f in clips:
        d = float(sh("soxi", "-D", f, text=True).stdout)
        m[key] = [round(t, 3), round(d, 3)]; t += d + 0.3; files += [f, gap]
    allw = os.path.join(work, name + ".all.wav")
    sh("sox", *files, allw)
    sh("ffmpeg", "-y", "-i", allw, "-c:a", "libmp3lame", "-b:a", "128k", "-ac", "1", os.path.join(ROOT, "audio", name + ".mp3"))
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("list"); ap.add_argument("--title", required=True); ap.add_argument("--letter", default=None)
    ap.add_argument("--refs", default=None); ap.add_argument("--pick", default=""); ap.add_argument("--work", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "make_week"))
    ap.add_argument("--dry", action="store_true", help="only read the list and show what would be made")
    ap.add_argument("--root", default=None, help="the app folder to write into (default: this repo)")
    a = ap.parse_args()
    global ROOT
    if a.root:
        ROOT = os.path.abspath(a.root)
    words = parse(a.list)
    letter = (a.letter or norm(words[0]["noun"])[:1]).lower()
    pick = {norm(k): int(v) for k, v in (x.split("=") for x in a.pick.split(",") if x)}
    os.makedirs(a.work, exist_ok=True)
    print(f"{len(words)} words, cards img/{letter}-<id>.webp, packs audio/pw-<id>.mp3")
    for w in words:
        print(f"  {w['article']} {w['noun']} {w['emoji']}  id={w['id']}" + (f"  ({w['den']})" if w["den"] else ""))
    if a.dry:
        return
    api = os.environ["ELEVENLABS_API_KEY"]
    packs, wrong = {}, []
    for w in words:
        w["pic"] = card(w, letter, a.work, a.refs, pick, False)
        lines = [("w-" + w["id"], f"{w['article']} {w['noun']}"), ("n-" + w["id"], w["noun"])]
        lines += [(f"q-{w['id']}-{x}", f"{x} {w['noun']}?") for x in ("der", "die", "das")]
        if w["den"]:
            lines.append(("st-den-" + w["id"], w["den"]))
        made = []
        for key, text in lines:
            f, heard = clip(key, text, a.work, api)
            made.append((key, f))
            if norm(heard.replace("?", "")) != norm(text.replace("?", "")):
                wrong.append(f"{key}: wanted '{text}', heard '{heard}'")
        packs["pw-" + w["id"]] = pack("pw-" + w["id"], made, a.work)
        print(f"  ✓ {w['noun']}")
    # data/words.json: the new week
    wj = os.path.join(ROOT, "data", "words.json")
    old = json.load(open(wj, encoding="utf-8"))
    new = {"version": int(old.get("version", 0)) + 1, "week": a.title,
           "words": [{"id": w["id"], "noun": w["noun"], "article": w["article"], "emoji": w["emoji"], "rec": True, **({"pic": w["pic"]} if w.get("pic") else {})} for w in words]}
    json.dump(new, open(wj, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    prev = [w for w in old.get("words", []) if w.get("id")]
    # index.html: packs, noun ids, den ids, audio version
    p = os.path.join(ROOT, "index.html"); s = open(p, encoding="utf-8").read()
    for name, m in packs.items():
        s = re.sub(r',"' + re.escape(name) + r'":\{[^}]*\}', "", s)   # a re-run replaces the word's old pack entry
        s = s.replace("}/*END*/", "," + json.dumps(name) + ":" + json.dumps(m, separators=(",", ":")) + "}/*END*/", 1)
    ids = [w["id"] for w in words]
    s = s.replace("const NOUN_IDS = new Set([", "const NOUN_IDS = new Set([" + "".join(json.dumps(i) + ", " for i in ids if f'"{i}"' not in s.split("const NOUN_IDS = new Set([", 1)[1].split("]", 1)[0]), 1)
    dens = [w["id"] for w in words if w["den"]]
    s = s.replace("const DEN_IDS = [", "const DEN_IDS = [" + "".join(json.dumps(i) + ", " for i in dens if f'"{i}"' not in s.split("const DEN_IDS = [", 1)[1].split("]", 1)[0]), 1)
    s = re.sub(r"const AUDIO_V = (\d+);", lambda m: f"const AUDIO_V = {int(m.group(1)) + 1};", s, count=1)
    # last week's words become built-in review words (like M_WORDS), named after their letter (A_WORDS, …)
    if prev:
        pl = (re.match(r"img/([a-z])-", prev[0].get("pic", "")) or re.match(r"(.)", prev[0]["id"])).group(1).upper()
        name = f"{pl}_WORDS"
        if f"const {name} = " not in s:
            row = "const " + name + " = " + json.dumps(prev, ensure_ascii=False, separators=(",", ":")) + ";\n"
            s = s.replace("const KNOWN_WORDS = () => normalizeWords([", row + "const KNOWN_WORDS = () => normalizeWords([..." + name + ", ", 1)
            print(f"last week's {len(prev)} words built in as {name}")
    open(p, "w", encoding="utf-8").write(s)
    print(f"data/words.json → version {new['version']} ({a.title}); index.html updated; review the cards in {a.work}")
    if wrong:
        print("Read back differently (listen, re-record by deleting the .pcm in --work and running again):")
        for x in wrong:
            print("  " + x)


if __name__ == "__main__":
    main()
