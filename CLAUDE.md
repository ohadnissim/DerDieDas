# Der Die Das: how new material is made

Keep every new word list, story and recording on the same tools and settings as the earlier ones.
If a tool below can't be reached from your session, don't switch to another one. Stop and ask for access, and keep the
PR as a draft until the assets are made the usual way.

## Higgsfield from a cloud session (the CLI, signed in as Ohad; no API keys)
- Install: `npm i -g @higgsfield/cli` (optional skills: `npx skills add higgsfield-ai/skills`; don't commit what that
  adds to the repo).
- Sign in: run `higgsfield auth login --port 8765` in the background and send Ohad the `clerk.higgsfield.ai/oauth/authorize…`
  link from the `sign-in.html` file it prints. After he approves, his browser lands on a page that won't load
  (`localhost:8765/callback?code=…`); he pastes that address back, and you open it inside the session with
  `curl --noproxy localhost "<address>"`. The login waits about 5 minutes, so start a fresh one if it timed out.
- Then `higgsfield workspace set b450fa9f-048b-4932-a880-2b9633a968f2` (his Private workspace) and
  `higgsfield account status` to see the credits.
- Credentials stay in `~/.config/higgsfield/`; never copy tokens into files, commits or PRs.
- Plus plan: at most 6 jobs at once, so run 5 in parallel.
- The claude.ai Higgsfield connector only browses (balance, models, past generations); it can't generate.

## Pictures
- **Word pictures** (`img/<letter>-<id>.webp`, 420×420, cream paper background `#F2EFE7`): cut out of the photo of
  the school sheet. They are the school's own drawings, so they look exactly like the sheet at school.
- **Story pictures** (`img/storyN-K.webp`, 1280×720, WebP): made with **Higgsfield** in the clay / plasticine
  stop-motion style of the earlier stories. Mia, Mil, Max and Mila (the caterpillar) must look like
  `img/kid-*.webp` and `img/mila.webp`. Recipe (stories 5 to 8): model `nano_banana_flash` (Nano Banana 2),
  `--aspect_ratio 16:9 --resolution 1k`, and these `--image-references` in this order:
  style `56a6949f-0dc8-4c09-a972-940f8bd2ba9f`, then only the characters on the page: Mila
  `81a49550-6efa-4a9e-9e5e-81f2f37e2084`, Mia `1a34b003-48f7-49f9-b87e-fbda50df0008`, Mil
  `15959c03-163c-47ce-be89-4b96fa2922c0`, Max `c815a416-a207-4f63-a986-0694152b7dd5`, then the word pictures of the
  objects on the page (upload `img/<letter>-<id>.webp` as PNG with `higgsfield upload create`). Prompt: "Clay
  stop-motion style scene, same style as the style reference: handmade plasticine look. <scene>. Characters: <Mila
  (exactly like the caterpillar reference: round beige head, curly brown antennae, blue-yellow-red segmented body);
  Mia (girl with BLACK hair in two braids, white long-sleeve top, light blue-grey overalls); Mil (boy with neat BROWN
  hair, navy blue sweater with white collar); Max (boy with SPIKY RED hair, light blue shirt, grey trousers)>.
  Objects follow their reference drawings but are made of clay like everything else. Each character looks exactly
  like their own reference image. Bright, warm, cheerful children's picture book. No text, no letters."
  Make two takes per page and keep the better one; resize 1376×768 to 1290×720, centre-crop to 1280×720, WebP q80.
  If a page has a "find" spot, set its `x`/`y`/`r` in `data/stories.json` to where the object landed.
- **Stickers and garden pictures**: clay die-cut style, matching the existing ones.

## Voices
- **Mila** (teacher, narrator, every word): ElevenLabs voice "German Girl - Mila".
- **Mia**: ElevenLabs voice "Fünkchen".
- **Mil and Max**: Higgsfield "Seed Audio 1.0" (`seed_audio`) voice clones of Ohad's Sep 29 reference clips:
  `--audio-references 5c231e48-60a2-4e03-b0f2-32968633f0cb` for Mil, `7b457cbc-dbfa-451d-b8f6-a6db13f1c6cb` for Max,
  with `--sample_rate 24000 --format mp3 --pitch_rate 0 --speech_rate 0 --loudness_rate 0` (the server adds
  expression 5, mood 0; the CLI doesn't take those two). Max's claims are said as "Der Laden!".
- ElevenLabs settings: model `eleven_turbo_v2_5`, `language_code: de`, speed 0.90, output `pcm_24000` (native PCM,
  never the MP3 output).
- Processing for every clip: trim the silence (and any click after it), apply gentle 2:1 compression, normalise to
  -14 LUFS with a soft peak catch at -1 dBFS, then do one soxr resample to 44.1 kHz and one MP3 encode (128k mono).
  Never re-encode an existing file; put new clips in a new file instead.
- Check every clip with speech-to-text and re-record any that read back wrong.

## Where audio goes
- Each word: `w-<id>` (with its article), `n-<id>` (the word alone), `q-<id>-der|die|das` (said as a question) and
  `st-den-<id>` for der-words. These are packed into `audio/pw-<id>.mp3` and listed in `PACKS` in `index.html`.
- Max's claims: `x-max-<id>-<article>`, listed in `MAX_CLAIMS`.
- Sätze: one recording per sentence. `SENT_T` holds `[start, length, time of "malt", time of second article, file?]`.
- Stories: one sprite file `audio/sp-storyN.mp3`, mapped in `data/stories.json`.
- Mil's and Max's story lines and Max's claims for a new list go in their own packs in `PACKS` (for the L list:
  `pk-sk7`, `pk-sk8`, `pk-xmax-l`), so the files that already exist are not re-encoded. Bump `AUDIO_V`.
- Lines written but not recorded yet go in `PENDING` in `index.html`, so the app uses the device voice until they exist.

## Weekly list
`data/words.json` (bump `version`) and `data/stories.json`. When the list changes, the previous week's words move to
review; build them into `index.html` the way `M_WORDS` and `I_WORDS` are.
