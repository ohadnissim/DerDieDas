# Der Die Das

A der/die/das practice game for young children. No reading needed: every word is a picture, and a recorded voice says it in German. Articles are circles in the school colours (der blue, die red, das yellow). The voice is **Mila**, the teacher from her school book; her pupils Mia, Mil and Max live in the garden.

**Play it:** https://ohadnissim.github.io/DerDieDas/

- **Practice (purple button):** the app says the word with its article ("der Hund"), the child taps **der** (blue ●), **die** (red ●) or **das** (yellow ●), then says it out loud with the hand sign (der ✊ fist, die ☝️ pointing finger, das ✋ flat hand). A peace sign ✌️ celebrates right answers; Missed words come back a few cards later; across days, known words come back less often.
- **Quiz (pink button, gets a "!" every 2 rounds):** picture only, no hints, one try per word. Missed words are flagged for the grown-ups and go back into practice.
- **Speaking:** in the say-it step she taps the microphone and says the word; she gets kind feedback ("Super gesagt!" / "Fast! Hör mal:") and hears her own voice back. Needs the microphone permission; works on this GitHub version only.
- **Memory (pink cards):** find two pictures that live in the same house; each card says its word.
- **Stimmt das? (thumbs):** a grown-up picks an article (sometimes wrong on purpose); the voice says the answer as a question, she judges 👍/👎 and fixes the mistakes, then hears the right version.
- **Story (book):** a whole picture story each week, read aloud with der/die/das in colour, with little questions along the way ("Wer hilft?") that she answers by tapping a picture.
- **Garden (flower):** a floating clay island that grows one new thing each day she plays; drag to tilt it in 3D.
- **Older words keep coming back:** when a new weekly list arrives, last week's words move to a word bank; up to 3 come back in every round, the tricky ones first.
- **Weekly report (⚙️):** days played, stars per day, rounds, quizzes, words said right, and which words are still tricky.
- **House friends DER, DIE and DAS:** a round (der), pointy (die) and square (das) friend live in the houses and cheer for right answers.
- **Stickers:** every 10 first-try answers unlock a new sticker in the sticker book (24 to collect).
- **Remembering the colours:** every practice round starts with a 6-tap colour warm-up: Mila says der, die or das and the child taps the matching circle. When she misses, the right circle glows and Mila says its article. Tapping Mila on the home screen lights up the three circles while she says der, die, das.
- **Grown-ups:** tap ⚙️ and answer the sum to see which words need practice, edit the word list (`der Hund 🐶`, one per line) and change settings.

**New words each week:** `data/words.json` (bump `version`; add `"replace": true` to drop earlier words instead of keeping them for review) and `data/stories.json`; the app picks them up automatically.

Words and progress are saved in the browser on the device (no account, nothing sent anywhere). Pictures (`img/`) are clay-style illustrations ; the weekly words use the drawings from her school sheet so they look exactly like at school, and Mila, Mia, Mil and Max are clay versions in the sheet's colours; the voice (`audio/`) is pre-recorded. Words added later show their emoji and use the device's German voice until a picture and recording are added.
