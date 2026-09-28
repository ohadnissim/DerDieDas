# Der Die Das

A der/die/das practice game for young children. No reading needed: every word is a picture, and a recorded voice says it in German.

**Play it:** https://ohadnissim.github.io/DerDieDas/

- **Practice (purple button):** the app says the word with its article ("der Hund"), the child taps **der** (blue ●), **die** (red ▲) or **das** (yellow ■), then says it out loud with the hand sign (der ✊ fist, die ☝️ pointing finger, das ✋ flat hand). A peace sign ✌️ celebrates right answers; short sentences ("Der Hund bellt.") put the word in context. Missed words come back a few cards later; across days, known words come back less often.
- **Quiz (pink button, gets a "!" every 2 rounds):** picture only, no hints, one try per word. Missed words are flagged for the grown-ups and go back into practice.
- **Speaking:** in the say-it step she taps the microphone and says the word; she gets kind feedback ("Super gesagt!" / "Fast! Hör mal:") and hears her own voice back. Needs the microphone permission; works on this GitHub version only.
- **Memory (pink cards):** find two pictures that live in the same house; each card says its word.
- **Stimmt das? (thumbs):** a grown-up picks an article (sometimes wrong on purpose), she judges 👍/👎 and fixes the mistakes.
- **Story (book):** a short picture story each week, read aloud, with der/die/das in colour.
- **Garden (flower):** a floating clay island that grows one new thing each day she plays; drag to tilt it in 3D.
- **House friends:** a round (der), pointy (die) and square (das) friend live in the houses and cheer for right answers.
- **Stickers:** every 10 first-try answers unlock a new sticker in the sticker book (24 to collect).
- **Grown-ups:** tap ⚙️ and answer the sum to see which words need practice, edit the word list (`der Hund 🐶 | Der Hund bellt.`, one per line) and change settings.

**New words each week:** `data/words.json` (bump `version`) and `data/stories.json`; the app picks them up automatically.

Words and progress are saved in the browser on the device (no account, nothing sent anywhere). Pictures (`img/`) are clay-style illustrations; the voice (`audio/`) is pre-recorded. Words added later show their emoji and use the device's German voice until a picture and recording are added.
