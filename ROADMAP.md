# Der Die Das: roadmap

Ohad, 2026-11-25: "lets build it all really. and upgrade everything we can."
Built in this order, one PR per step. Tick a step when its PR is merged, and note its number.

## Done
- [x] St and Sp in the Sch-Lok, said with a real Schhh (#21)
- [x] Lesen (blending), step 1 below (#22)
- [x] Lautdetektiv, step 2 below (#23)
- [x] Her storybook, step 9: Mein Buch on the stories shelf
- [x] Weekly-list tool, step 10 (#33): tools/make_week.py
- [x] Voice report, step 11 (#32): This week → Her sounds this week
- [x] The map, step 8 (#31)
- [x] Her voice book, step 7 (#30) (and the checker's line from grown-ups' marks, finishing step 3)
- [x] Motion pass across the app
- [x] Echo, step 6 (#28)
- [x] Ch-Zoo + known words first (#26), grown-ups tabs + Christmas costumes (#27)
- [x] Mouth guide, step 4 (#25): Mila's mouths in img/mund-*.webp; in the Sch-Lok bubble, and the S → Sch pair when she says Sss
- [x] Ch-Zoo, step 5: cat (ich), dragon (ach), fox (chs), speaking checked by the Aussprache-Helfer
- [x] Pronunciation checker, step 3 (#24), its line set from the voice book: in the Sch-Lok, switched on by grown-ups; her scores are logged. Still to do: set her
      line from real scores (a warm-up), then use it in the other speaking steps and the Ch-Zoo.

## Next, in order (all eleven steps are built as of 2026-11-25)
0. [x] **Motion pass** (Ohad, 2026-11-25: "add motion … more interactive … so the all app will feel more alive"): tiles breathe,
       characters blink and bounce, cards fly and flip, screens slide, stars fly to the counter; still for reduced motion.
1. [–] **Lesen (blending), removed 2026-11-25 ("not working well"):** sound tiles slide together into a word (M + au + s = Maus); Mila blends slowly, then she taps
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
6. [x] **Echo:** Mila says a word, she repeats, faster and faster, across all the sounds.
7. [x] **Her own voice:** a word she said well is kept, so the card can play Mila and then her.
8. [x] **The map:** each letter or sound is a place on her island map (M mill, Sch station, Ch zoo, St star tower …),
       unlocked as she learns it.
9. [x] **Her storybook:** she picks characters and things she knows; a story is put together from the existing story
       pieces (no paid AI at runtime), she reads the coloured parts aloud, and it is saved as her book.
10. [x] **Weekly list from a photo:** a Mac tool (`tools/`) that takes a photo of the school sheet and makes the word list,
        cards and Mila's voices the usual way (CLAUDE.md), ready as a PR.
11. [x] **Weekly voice report for grown-ups:** per sound, how often she said it right, with a couple of her clips.

## Rules for every step
- Known words first: games use only words she knows; new words are shown on a "Neue Wörter!" card first, at most two a day
  (Ohad, 2026-11-25: "we cant stir too far away").
- Same tools and settings as CLAUDE.md (Higgsfield pictures, ElevenLabs Mila, -14 LUFS, speech-to-text check).
- Nothing that needs paid credits while she plays: generation happens when we build, not in the app.
- Test it running in the browser before the PR; say what could not be tested (the microphone on the iPad).
