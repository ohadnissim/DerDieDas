# Der Die Das: roadmap

Ohad, 2026-11-25: "lets build it all really. and upgrade everything we can."
Built in this order, one PR per step. Tick a step when its PR is merged, and note its number.

## Done
- [x] St and Sp in the Sch-Lok, said with a real Schhh (#21)
- [x] Lesen (blending), step 1 below (#22)
- [x] Lautdetektiv, step 2 below

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
4. [ ] **Mouth guide:** a picture of Mila's mouth for each sound (round lips Sch, flat smile ich, throat ach), shown when
       she is asked to say it and when she gets it wrong.
5. [ ] **Ch-Zoo (Group 2: ich-Ch, ach-Ch, Chs):** a soft hissing cat (ich) and a rough dragon (ach); words go to the right
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
- Same tools and settings as CLAUDE.md (Higgsfield pictures, ElevenLabs Mila, -14 LUFS, speech-to-text check).
- Nothing that needs paid credits while she plays: generation happens when we build, not in the app.
- Test it running in the browser before the PR; say what could not be tested (the microphone on the iPad).
