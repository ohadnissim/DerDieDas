# Der Die Das: roadmap

Ohad, 2026-11-25: "lets build it all really. and upgrade everything we can."
Built in this order, one PR per step. Tick a step when its PR is merged, and note its number.

## RESUME HERE (paused 2026-11-25 for an account switch)
Merged to main: #21 St/Sp, #22 Lesen, #23 Lautdetektiv, #24 Aussprache-Helfer, #25 mouth guide, #26 Ch-Zoo + known words
first, #27 grown-ups tabs + Christmas costumes.

**In progress: Echo (step 6), branch `claude/echo` (pushed, not merged, no PR yet).** The code is written (screen, game,
shared `talkMicOpen` / `judgeSaid` used by Ch-Zoo and Echo, home tile, lines in CLIP_TEXT, `ic-echo` in XM_ONLY).
Still to do before its PR:
1. Mila's 4 Echo lines are recorded and checked: `/Volumes/WORK/CLAUDE/Learn German/_wip-echo/ec-*.wav` (processed 44.1 kHz,
   not the `.24.wav`). Pack them into `audio/pk-ec.mp3` (0.3 s gaps, one MP3 encode), add `"pk-ec"` to PACKS, `AUDIO_V` 45.
2. Icon: `_wip-echo/ic-echo-raw.png` (Mila calling, echo off a small mountain). Remove the background (Higgsfield
   `image_background_remover`; it hung twice today, so use `--wait-timeout 4m` and retry), fit into 256 px →
   `img/ic-echo.webp`; then its Christmas costume (Santa hat, snow on the mountain) → `img/xm-ic-echo.webp`.
3. Test in the browser (round of 8 known words, faster after half, no mic in the preview), PR, merge (Ohad: "merge
   everything when it's done", then "keep building the rest of the roadmap").

**Next after Echo: a motion pass across the whole app** (Ohad: "add motion … more interactive … so the all app will feel
more alive"): home tiles breathing out of step, icons wiggle on tap, circle friends blink and sway; Mila, zoo animals and
shopkeepers idle-breathe, blink, bounce when they talk or cheer; Lesen tiles hop and snap like magnets; the zoo card arcs
into the animal, which munches; a real 3D flip in Detektiv; screen changes slide and fade; stars fly to the counter.
Calm for a 6-year-old; prefers-reduced-motion gets the still version.

Then the rest: 7 her own voice / voice book (keep her clips, grown-ups mark right/wrong, which sets the checker's line),
8 map, 9 storybook, 10 weekly-list tool, 11 voice report.

## Done
- [x] St and Sp in the Sch-Lok, said with a real Schhh (#21)
- [x] Lesen (blending), step 1 below (#22)
- [x] Lautdetektiv, step 2 below (#23)
- [x] Ch-Zoo + known words first (#26), grown-ups tabs + Christmas costumes (#27)
- [x] Mouth guide, step 4 (#25): Mila's mouths in img/mund-*.webp; in the Sch-Lok bubble, and the S → Sch pair when she says Sss
- [x] Ch-Zoo, step 5: cat (ich), dragon (ach), fox (chs), speaking checked by the Aussprache-Helfer
- [~] Pronunciation checker, step 3 (#24): in the Sch-Lok, switched on by grown-ups; her scores are logged. Still to do: set her
      line from real scores (a warm-up), then use it in the other speaking steps and the Ch-Zoo.

## Next, in order
1. [x] **Lesen (blending):** sound tiles slide together into a word (M + au + s = Maus); Mila blends slowly, then she taps
       the matching picture. Words from the letters she knows. First step into reading, the way German schools teach it.
2. [x] **Lautdetektiv:** Mila says words one at a time with the picture hidden; she decides whether she hears the sound
       (magnifier yes, hand no). A word parade instead of a story, so it runs on Mila's existing word recordings.
3. [ ] **Pronunciation checker:** a real model that hears which sounds she made (ʃ / s / ç / x …), scored against the word
       she was asked to say and its likely mistakes (Stern vs Schtern, ich vs isch). Model picked from the research run
       on 2026-11-25: facebook/wav2vec2-lv-60-espeak-cv-ft (onnx-community q4f16, about 190 MB, transformers.js) won the
       test on synthetic voices (about 85 to 97 % right; ZIPA-small lower). Weak spot: high child voices push ç toward s/ʃ,
       so it needs her own warm-up recordings and a per-word threshold before it judges her. Replaces the hiss-only check where it is better; the Sch-Meter stays as the fallback.
4. [x] **Mouth guide:** a picture of Mila's mouth for each sound (round lips Sch, flat smile ich, throat ach), shown when
       she is asked to say it and when she gets it wrong.
5. [x] **Ch-Zoo (Group 2: ich-Ch, ach-Ch, Chs):** a soft hissing cat (ich) and a rough dragon (ach); words go to the right
       animal and she feeds them by saying the word right. Chs (Fuchs, Dachs, sechs) as a third friend.
6. [ ] **Echo:** Mila says a word, she repeats, faster and faster, across all the sounds.
7. [ ] **Her own voice:** a word she said well is kept, so the card can play Mila and then her.
8. [ ] **The map:** each letter or sound is a place on her island map (M mill, Sch station, Ch zoo, St star tower …),
       unlocked as she learns it.
9. [ ] **Her storybook:** she picks characters and things she knows; a story is put together from the existing story
       pieces (no paid AI at runtime), she reads the coloured parts aloud, and it is saved as her book.
10. [ ] **Weekly list from a photo:** a Mac tool (`tools/`) that takes a photo of the school sheet and makes the word list,
        cards and Mila's voices the usual way (CLAUDE.md), ready as a PR.
11. [ ] **Weekly voice report for grown-ups:** per sound, how often she said it right, with a couple of her clips.

## Rules for every step
- Known words first: games use only words she knows; new words are shown on a "Neue Wörter!" card first, at most two a day
  (Ohad, 2026-11-25: "we cant stir too far away").
- Same tools and settings as CLAUDE.md (Higgsfield pictures, ElevenLabs Mila, -14 LUFS, speech-to-text check).
- Nothing that needs paid credits while she plays: generation happens when we build, not in the app.
- Test it running in the browser before the PR; say what could not be tested (the microphone on the iPad).
