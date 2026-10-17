# Der Die Das: how new material is made

Keep every new word list, story and recording on the same tools and settings as the earlier ones.
If a tool below can't be reached from your session, don't switch to another one. Stop and ask for access (a key in the
project's cloud environment settings), and keep the PR as a draft until the assets are made the usual way.

## Pictures
- **Word pictures** (`img/<letter>-<id>.webp`, 420×420, cream paper background `#F2EFE7`): cut out of the photo of
  the school sheet. They are the school's own drawings, so they look exactly like the sheet at school.
- **Story pictures** (`img/storyN-K.webp`, 1280×720, WebP): made with **Higgsfield** in the clay / plasticine
  stop-motion style of the earlier stories. Mia, Mil, Max and Mila (the caterpillar) must look like
  `img/kid-*.webp` and `img/mila.webp`.
- **Stickers and garden pictures**: clay die-cut style, matching the existing ones.

## Voices
- **Mila** (teacher, narrator, every word): ElevenLabs voice "German Girl - Mila".
- **Mia**: ElevenLabs voice "Fünkchen".
- **Mil and Max**: Higgsfield voices, the same ones as their existing recordings.
- ElevenLabs settings: model `eleven_turbo_v2_5`, `language_code: de`, speed 0.90, output `pcm_24000` (native PCM,
  never the MP3 output).
- Processing for every clip: trim the silence, apply gentle 2:1 compression, normalise to -14 LUFS with a soft peak
  catch at -1 dBFS, then do one soxr resample to 44.1 kHz and one MP3 encode (128k mono). Never re-encode an existing
  file; put new clips in a new file instead.
- Check every clip with speech-to-text and re-record any that read back wrong.

## Where audio goes
- Each word: `w-<id>` (with its article), `n-<id>` (the word alone), `q-<id>-der|die|das` (said as a question) and
  `st-den-<id>` for der-words. These are packed into `audio/pw-<id>.mp3` and listed in `PACKS` in `index.html`.
- Max's claims: `x-max-<id>-<article>`, listed in `MAX_CLAIMS`.
- Sätze: one recording per sentence. `SENT_T` holds `[start, length, time of "malt", time of second article, file?]`.
- Stories: one sprite file `audio/sp-storyN.mp3`, mapped in `data/stories.json`.
- Lines written but not recorded yet go in `PENDING` in `index.html`, so the app uses the device voice until they exist.

## Weekly list
`data/words.json` (bump `version`) and `data/stories.json`. When the list changes, the previous week's words move to
review; build them into `index.html` the way `M_WORDS` and `I_WORDS` are.
