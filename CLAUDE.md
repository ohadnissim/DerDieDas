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
- **Word pictures** (`img/<letter>-<id>.webp`, 420×420, cream paper background `#F2EFE7`): the school sheet's own drawings.
  Up to the L list they were cut out of the photo of the sheet. From the A list on they are made with **Higgsfield**
  (`nano_banana_2`, 1:1, 1k), with three image references: the drawing cut from the sheet photo, then `img/i-igel.webp`
  and `img/l-lama.webp` as the style. Prompt: "Picture card for a children's word game: <the thing>, drawn like the first
  reference image (the school worksheet drawing: same pose, same shapes and colours). Draw it in exactly the same style as
  the second and third reference images (the hedgehog and the llama): soft hand-drawn coloured pencil and watercolour
  children's book illustration … on a plain flat warm cream paper background (#F2EFE7). No frame … no text, no letters."
  Two takes, keep the one closest to the sheet; set the paper to `#F2EFE7`, trim, fit the drawing into 330 px, centre it on 420×420.
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
- **Sticker islands** (the world next to the garden): each themed sticker set has an island, `img/island-<set>.webp`
  (2400×1792, WebP q80), made with Higgsfield `nano_banana_flash`, `--aspect_ratio 4:3 --resolution 2k`, with the garden
  island `img/island.webp` (uploaded as PNG) as the only reference: "Same floating clay island as the reference image … But
  this one is <the island>. The top surface stays big, flat and mostly empty …". Two takes, keep the better one. Every
  sticker also has a cut-out, `img/cut-<id>.webp`: the sticker picture through Higgsfield `image_background_remover`
  (keeps the white die-cut edge), alpha under 10 dropped, trimmed with a 6 px margin, WebP q82. A new sticker set needs
  its island, its cut-outs and an entry in `ISLANDS` in `index.html`.
  A new island also needs its two visitor spots (front edge, left and right) in `VISIT_SPOTS`.
- **Mila's tree** (`img/mila-tree.webp`, 2400×1792 WebP q80) and its pictures: the leaf `img/leaf.webp` and Mila growing,
  `img/mila-2.webp` to `img/mila-5.webp` (bigger, chubby, cocoon, butterfly). Higgsfield `nano_banana_flash`, the story
  style reference `56a6949f-…` (plus Mila `81a49550-…` for Mila), `--aspect_ratio 1:1 --resolution 1k` on a plain pure white
  background (the tree: 4:3, 2k), two takes, keep the better one, then `image_background_remover`, trimmed, WebP. The
  stages are in `MILA_STAGES` (how many leaves each one needs, and where her mouth is).
  After `LIFE` leaves the butterfly flies away and leaves an egg, `img/mila-egg.webp` (same recipe, 1:1), and a new little
  Mila hatches; `progress.lifeStart` and `progress.butterflies` keep count, and every butterfly that flew away flutters
  around the tree (`BFLY_SPOTS`). Mia's lines for it are in the pack `pk-life`.

## Letters on screen
- The capital I always has its bars on top and bottom, like at school (otherwise it looks like an l). `fonts/schooli-*.woff2`
  hold only that letter (Baloo 2 and Nunito's own I plus the two bars, one file per weight the app uses) and come first in
  `--display` and `--body`. A new font weight needs its own file. `fonts/` is copied into the iPad app with the rest.
- Story pictures that show writing must show it the school way: the L the right way round, and the small l as one straight
  line (no curly ℓ). Check them zoomed in, and ask Higgsfield to edit out anything wrong.

## Voices
- **Mila** (teacher, narrator, every word): ElevenLabs voice "German Girl - Mila".
- **Mia**: ElevenLabs voice "Fünkchen".
- **Löwe and Lama** (the Laden): ElevenLabs "Justus - Slapstick & Cartoon" (`BOXom31b0dZ8zv6QJFfQ`) for the Löwe and "Mrs. Bruelli" (`q6mfXZhCPNqTDA4sX437`) for the Lama, same settings as Mila. Their lines and Mila's words for the shop things are in `pk-laden`.
- **Mil and Max**: Higgsfield "Seed Audio 1.0" (`seed_audio`) voice clones of Ohad's Sep 29 reference clips:
  `--audio-references 5c231e48-60a2-4e03-b0f2-32968633f0cb` for Mil, `7b457cbc-dbfa-451d-b8f6-a6db13f1c6cb` for Max,
  with `--sample_rate 24000 --format mp3 --pitch_rate 0 --speech_rate 0 --loudness_rate 0` (the server adds
  expression 5, mood 0; the CLI doesn't take those two). Max's claims are said as "Der Laden!".
- When only the ElevenLabs connector is available (no API key in the session), make one `tts` node per line with `model_parameters` `{"language_code": "de", "voice_settings": {...}}` and the voice from `creative_list_voices`. It only gives MP3 (44.1 kHz, 128k): decode it once, run the same processing, and encode once into the new pack (as for `pk-billig`).
  For many lines, put 10 to 15 lines in one node separated by `<break time="1.5s" />` and split the take at the pauses
  (0.7 s for words and sentences, 1.6 s for story pages, which have long pauses of their own; check the count). Put a take on
  the flow with `creative_add_flow_asset_node` (its `generation_id`) and transcribe it to get word times (free; it aligns the
  prompt text, which is how the Sätze "malt" and article times are taken).
- ElevenLabs settings: model `eleven_turbo_v2_5`, `language_code: de`, speed 0.90, output `pcm_24000` (native PCM,
  never the MP3 output).
- Processing for every clip: trim the silence (and any click after it), apply gentle 2:1 compression, normalise to
  -14 LUFS with a soft peak catch at -1 dBFS, then do one soxr resample to 44.1 kHz and one MP3 encode (128k mono).
  Never re-encode an existing file; put new clips in a new file instead.
- Check every clip with speech-to-text and re-record any that read back wrong.

## Story steps
A page can have `satz`, `find`, `ask`, `q`, and the two letter games `laut` and `pos` (`{"word": "maus", "letter": "m"}`,
the word must be in `LAUT_WORDS` for that letter and in the page's picture). They use Mila's clips from `pk-laut` and
`pk-pos`, so they need no new recordings. Give every new story one of each.

## Where audio goes
- Each word: `w-<id>` (with its article), `n-<id>` (the word alone), `q-<id>-der|die|das` (said as a question) and
  `st-den-<id>` for der-words. These are packed into `audio/pw-<id>.mp3` and listed in `PACKS` in `index.html`.
- Max's claims: `x-max-<id>-<article>`, listed in `MAX_CLAIMS`.
- Sätze: one recording per sentence. `SENT_T` holds `[start, length, time of "malt", time of second article, file?]`.
- Stories: one sprite file `audio/sp-storyN.mp3`, mapped in `data/stories.json`.
- Mil's and Max's story lines and Max's claims for a new list go in their own packs in `PACKS` (for the L list:
  `pk-sk7`, `pk-sk8`, `pk-sk9`, `pk-sk10`, `pk-xmax-l`; for the A list: `pk-sk12`, `pk-xmax-a`), so the files that already
  exist are not re-encoded. Bump `AUDIO_V`.
- New objects for the old painters in Sätze go in a new file per painter with the file in `SENT_T`'s 5th slot (`ssl-<painter>`
  for the L objects, `ssa-<painter>` for the A objects); a new painter gets all its sentences in `ssp-<painter>`.
- Seed Audio can't say every word: for Arzt every take came out as "der A", so Arzt has no Max claim. Check Max's and Mil's
  clips with a real speech-to-text run (attach the pushed pack's raw GitHub URL, then `creative_transcribe_audio`), not with
  the transcript of an ElevenLabs TTS take: that one only lines up the prompt text (it even keeps the `<break>` tags).
- Lines written but not recorded yet go in `PENDING` in `index.html`, so the app uses the device voice until they exist.
- Every sticker says its word (Mila): themed ones are `stk-<set>-<id>` in `pk-stk`; the first stickers' words are in
  `FIRST_WORDS` (`stk-<id>` in `pk-stk-first`, or an existing clip of the same word).

## The Laden
`LADEN` in `index.html` lists what she can buy: `welt` things go into her island tray like stickers (`img/stk-laden-<id>.webp`,
cut-out `img/cut-laden-<id>.webp`, made like the stickers), `konfetti`, `farbe` (CSS under `data-farbe`), and `insel` (an island
with `shop:` in `ISLANDS`, opened by buying it). Each has a shopkeeper line that says its price (`ld-<id>` in `pk-laden`).
A `gift:` on an item is a `welt` thing that comes with it (marked `extra`, so it has no card of its own; `normalizeProgress` hands it out if she bought the item before the gift existed). Buying takes `progress.stars` only; `progress.owned`, `farbe` and `konfetti` hold what she has.
Home icons are `img/ic-<name>.webp`: Higgsfield `nano_banana_flash` with the story style reference, 1:1 on white, then
`image_background_remover`, trimmed to a 256 px square.

- Schreiben: a letter ends right ON the line and never pokes over it (the school insists). The glyphs are written on the
  lines 0 / 50 / 100 / 150; `wy()` then moves every stroke in by `W_HALF` (half the drawn stroke) from the top, middle and
  base line, so the stroke's edge touches the line. Keep the track (`.wsvg .track`) and the ink no thicker than
  2 × `W_HALF`. The t's bar stays centred on the middle line.

## Halloween
- From 15 October to 2 November (`HW_SEASON` in `index.html`; `?halloween=1` / `?halloween=0` force it for testing)
  everyone dresses up, unless she picked another Laden colour; the Laden colour Kürbisnacht (`farbe-halloween`) keeps it all
  year. `hwDress()` sets `data-hw` on the root: orange and purple background with floating bats and pumpkins (`.hwfly`), the
  der/die/das circles in costume (a `.hw` span: vampire, witch hat, black cat), and every picture listed in `HW_IMG` swapped
  for its costume version `img/hw-<name>.webp` (Mila and her stages, the kids, the Löwe and the Lama), also when the
  picture appears later.
- Costume pictures: the original (on a cream background) as Higgsfield reference, "Exactly the same … but dressed up as …",
  then `image_background_remover`, then fitted into the original's exact canvas size (feet on the bottom), so every layout
  and Mila's mouth spots stay the same. Keep them narrow (tails hanging down), or they come out small.
- The Halloween sticker set is first in `STICKER_SETS` (her current mission); stickers are kept by id, so the other sets keep
  everything she has. Its island is `img/island-halloween.webp`. Story 11 ("Fröhliches Halloween!") uses the M, I and L words.
  Its Mila/Mia lines are in `audio/sp-story11.mp3`, Mil/Max in `pk-sk11`; the stickers', the mission's and the shopkeepers'
  Halloween lines (`lw-hw`, `la-hw`, prices) are in `pk-hw`.

## Weihnachten
- From 24 November to 6 January (`XM_SEASON`; `?weihnachten=1` / `?weihnachten=0` force it, `?tag=2026-12-05` pretends it is
  that day) everyone dresses up for Christmas; the Laden colour Winterwunder (`farbe-weihnachten`) keeps it all year. It wins
  over Halloween. `hwDress()` handles both: `costume()` is "xm", "hw" or "", the root gets `data-xm` / `data-hw` and
  `data-costume`, `HW_IMG` pictures swap to `img/xm-<name>.webp` / `img/hw-<name>.webp`, the circles get an `.xm` span
  (snowman hat and carrot nose, Santa hat, antlers), and `hwSky()` lets it snow.
- Advent calendar: `ADV_GIFT` (what is behind each door), `ADV_ORDER` (where the doors are), door art `img/adv-<art>.webp`
  (clay presents through `image_background_remover`, standing on the bottom of a square), background `img/xm-advent-bg.webp`.
  `progress.xmAdvent = {y, days}` is the year and the opened doors; `progress.xmAdvSeen` makes it open by itself once a day.
- Her tree: `img/xm-baum.webp`, ornaments `img/o-<id>.webp` (`ORNAMENTS`), `progress.xmBox` (ornaments in the box, by id),
  `progress.xmTree` (`{o, x, y}` in % of the picture), `TREE` is the green triangle of the picture where ornaments may hang.
  `progress.xmWin` counts the ornaments won from rounds today (max 3). Lichterkette and Baumspitze are Laden items of kind
  `baum`; the Schmuckkiste is kind `schmuck` and can be bought again and again.
- `XM_ONLY`: pictures with only a Christmas costume (Mila's mouths, the zoo animals, the Lesen / Detektiv / Ch-Zoo icons);
  `hwFix` swaps them at Christmas and leaves them alone at Halloween. Made like the other costumes (original on cream as the
  only reference, "exactly the same … but dressed up for Christmas", background removed, fitted to the original canvas).
- Christmas sticker set and Winterinsel (`island-weihnachten`), stories 14–16 (`sp-story14..16`, Mil/Max in `pk-sk14`),
  everything else Mila, Löwe and Lama say for Christmas in `pk-xm`.

## T and Sch
- `X_WORDS`: picture words for T, Sch and S (Tanne, Tasse, Tisch, Tür, Hut, Schal, Schuh … Sonne, Sofa, Socke, Suppe), cards
  `img/x-<id>.webp` made on Higgsfield in the word-card style (i-igel / l-lama as references). They are NOT in her der/die/das
  list: they only appear in the letter games, the Sch-Lok and the stories (a story "ask" step doesn't score them). Mila's
  `w-<id>` / `n-<id>` are in `pk-xw`.
- St and Sp (`ST_WORDS`, `SP_WORDS`, cards `img/x-<id>.webp`, Mila's `w-`/`n-` and `sl-stsp` in `pk-st`): in the Sch-Lok they go
  on the Lok side, since at the start of a word the S is said Schhh. A round is 3 Sch, 2 St, 2 Sp and 2 S words. They are not
  in the letter games (their Schhh is always the first sound). TTS can't say "Scht" or "Schp" (speech-to-text heard "St" and
  worse), so Mila never says them alone: she says "Hier klingt das S am Anfang wie Schhh!".
- `LAUT_WORDS.t` / `LAUT_WORDS.sch`; Sch is in `LAUT_ONLY` (letter games only, not in Schreiben). T is in `LETTERS` and
  `GLYPHS`.
- The Sch-Lok (`startSch`) listens with the Sch-Meter (`schMeter()`): an AnalyserNode on the microphone (echo cancelling,
  noise suppression and auto gain off, they smear hiss). Only clear-hiss frames count (loud over the room, much more energy
  above 2 kHz than below 1 kHz). Each one gives three numbers: the loudest frequency (3 to 9 kHz), the centre (2.5 to 11 kHz)
  and the low/high balance in dB (`SCH_F`); `schScorer()` turns them into a score (below 0 Sch, above 0 S), smoothed over
  about 0.1 to 0.2 s with a grey zone, so one frame never decides.
- The meter is tuned to her: before the finale (first time, then every `SCH_DAYS` = 30 days) a warm-up (`slTune`) asks for
  the snake's "Sss" and the Lok's "Schhh" and `schFit()` stores her own means and spread in `progress.schCal`; until then the
  textbook values `SCH_TEXTBOOK` count (Sch about 4.8 kHz, S about 6.8 kHz). Grown-ups see it in the Voice section and can
  tune it again.
- After "Mach die Lippen rund … sag es mit mir" for each Sch word, Mila says "Jetzt du!" and the meter listens 3.5 s
  (`slSayCheck`): a Schhh gets "Ja! Das war ein schönes Schhh!", a Sss gets the round-lips tip. The mic stays open from
  then until the train has left. Mila's lines for it are in `pk-schm`.
- Mouth guide: `img/mund-sch|s|ich|ach.webp` (Mila's head, Higgsfield `nano_banana_flash` with the story style and Mila
  references, "close-up … showing clearly how to make a sound with the mouth: …", two takes, `image_background_remover`, cropped to
  the head, 512 px). `MUND` in `index.html`; the Sch-Lok bubble shows the Sch mouth, and S → Sch when the meter or model heard Sss.
- When TTS has to say "Sch" or "S" alone, write "Schhh" / "Sss", or it spells the letters.

## Lesen
- `LESEN_WORDS` (`[id, tiles]`) in `index.html`; a word plays only when its tile sounds exist (`lt-<id>-<k>` in `pk-lesen`) and it
  has a picture. Tile sounds come from `tools/make_lesen.py`: a fresh Mila take of the word (same ElevenLabs settings), ElevenLabs
  forced alignment for the letter times, each tile cut out, sounds you can hold stretched (pitch kept), the whole word's -14 LUFS
  gain on every tile, one soxr resample, one MP3 encode. It checks every take with speech-to-text: re-record any that read back
  wrong (Hand came out as "Hunt" once). New words: add them to the tool's list and run it again, then replace `pk-lesen`.
- Mila's lines are in `pk-le`. Round length grows with `progress.lesen.rounds` (3 tiles, then 4, then 5).

## Lautdetektiv
- `startDet` / `detPool()`: every picture word with sound tiles (`LAUT_WORDS`, `LESEN_WORDS`, `DET_EXTRA`) and a recorded `n-` clip.
  `detHit()` says whether a tile is the sound (St / Sp at the start count as Sch; au is not an a, tz not a t). A round is 4 words
  with the sound and 4 without; for Sch, the "without" words are mostly S words (`S_SOUND`). Mila's lines are in `pk-det`.
  TTS dropped the letter in "Wir suchen das I!", so that line is "Wir suchen das I, wie Igel!".

## Aussprache-Helfer (phon.js)
- `phon.js`: facebook/wav2vec2-lv-60-espeak-cv-ft, the onnx-community **q4** build, through transformers.js 3.5.1 from jsDelivr
  (WebGPU when there is one, else WASM). Not q4f16: on WebGPU it lost almost every sound. For a known word it scores the right
  sounds against the likely mistake (CTC log-likelihood, `phonMargin`); above 0 means the right way fits better.
- `PHON_IPA` in `index.html` (espeak-ng `-v de --ipa`, stress kept, `phon.js` drops it and splits into the model's tokens);
  the mistake is every ʃ made an s. A new Sch-Lok word needs its line there.
- Off until a grown-up switches it on (`state.settings.phon`); it loads when the Sch-Lok opens (`phonStart`). In `slSayCheck`
  the meter still listens, and when it heard a hiss the model's verdict replaces the meter's. Her scores go to
  `progress.phonLog` (last 40); `progress.phonCal.line` is the line (0 until it is set from her own scores).
- `tools/phon-test.html` runs it on Mila's recordings (`?device=wasm&dtype=q4` to force a build). 2026-11-25: Stern 2.03,
  Spinne 2.75, Schal 1.59, Fisch 2.66, Schuh 0.76, Frosch 3.64, Tisch 0.82; Sonne (z vs ʃ) -0.11. Synthetic tests: 85 to 88 %
  right, 75 % on raised "child" voices (ç heard as ʃ).

## ich · ach (was the Ch-Zoo)
- Ohad, 2026-11-25: "in the zoo i dont get the cat dragon … whats the point?" → simplify, and "she cant read though… she needs
  something that will have this in the word". So the buttons are pictures of words with the sound (`ZOO_ANCHOR`: Milch, Buch,
  Fuchs, drawn with `faceHTML(findWord(…))` so they match the game's own picture), lit in turn while Mila says them on the first
  word (`zooIntro`); Buch and Fuchs are met first. Lines without animals in `pk-zoo2` (a later pack wins for the same clip name).
  The animal pictures `img/zoo-*.webp` are no longer used by the game; inside the code the keys are still katze/drache/fuchs.
- `ZOO` (which words each animal gets), `ZOO_IPA` ([right, mistake] for the Aussprache-Helfer), `ZOO_MUND`. Cards `img/x-<id>.webp`
  (word-card recipe), animals `img/zoo-katze|drache|fuchs.webp` (story style, background removed), Mila in `pk-zoo`.
- The model hears Mila's soft ch as ɕ as often as ç, so ich words accept either (`ICH()`); the child's mistake is ʃ. Write ich
  words with spaced sounds, or "tç" in Brötchen merges into the single sound tʃ. Mila's checked margins (2026-11-25): ach words
  +1 to +7, Chs words about +6, ich words +1.1 to +5.1. Milch sat at -0.09 on its older recording, so it is not asked for yet.
- espeak writes Fuchs as fʊxs; it is fʊks (and Dachs daks, Ochse ɔksə). TTS: Mila never says "Ch" alone; she says example words.

## Known words first (Ohad, 2026-11-25)
"We have to make sure to currently use words she knows … happy to introduce slowly new words, but we cant stir too far away."
- `NEW_WORDS`: picture words that are not from her school lists (the St/Sp words and the Ch-Zoo words, added 2026-11-25).
  `isKnown(id)` is true for every other word, and for a new word once Mila has shown it (`progress.met[id]` = the day).
- `meetWords(ids)`: the "Neue Wörter!" card (picture, article in its colour, the word, Mila's `w-` clip, tap on), lines in `pk-mw`.
- At most `NEW_PER_DAY` (2) new words a day across the whole app (`canMeet`). Every game picks only known words: Lesen and
  Lautdetektiv leave new words out; the Sch-Lok and the Ch-Zoo show up to today's two first, then play with what she knows.
- A new picture word that is not from her school sheet goes into `NEW_WORDS`. Words from a new school list are known already.

## Motion (Ohad, 2026-11-25: "so the all app will feel more alive")
- One block of CSS, "Motion pass", inside `@media (prefers-reduced-motion: no-preference)`: devices set to reduce motion keep the
  still version, and JS motion checks `RM()`. Idle life is slow and out of step (`--d` offsets); taps answer fast and springy;
  things travel instead of popping (zoo card arcs `m-arc-*`, a star flies to the counter `flyStar()`, screens slide in `m-in`).
- A new game gets the same: its pictures drop in (`.enter` → `m-drop`), its characters breathe, its buttons spring.

## Her voice book
- `vbKeep(id, buf, margin)`: every word she says in the Sch-Lok, Ch-Zoo or Echo is kept on the device (IndexedDB
  `derdiedas.voicebook`, 16 kHz WAV, the last `VB_KEEP` = 40) with the Aussprache-Helfer's score (or none).
- Grown-ups play and mark them in Sounds → Her voice book; `vbLine()` puts the line where the marks disagree least (between her
  lowest ✓ and highest ✗; only ✓ marks lower it, only ✗ marks raise it) and saves it as `progress.phonCal = {line, t}`.
  `phonLine()` is what every judge uses. Clips never leave the device.

## Die Karte
- `img/karte.webp` (2400×1792, Higgsfield `nano_banana_flash` 4:3 2k with the story style and `img/island.webp` as references; nine
  places asked for in three rows of three; the "ZOO" sign was edited blank) and `img/xm-karte.webp` (the same picture made snowy,
  every place in the same spot). `KARTE` holds each place's % position and the game it opens; `karteOpen()` decides when it opens
  (`progress.letters`, `progress.played`, met St/Sp words); `progress.mapSeen` makes a new place celebrate once. Lines in `pk-mk`.
- A new sound gets a place: add it to the picture (edit both versions, same spot), to `KARTE`, `karteOpen()` and a `mk-<id>` line.

## Mein Buch
- Built from the Sätze engine: `bookObjs(h)` = known words with a sentence recorded in one go for that hero (`SENT_T`), pages are
  `makeSent(h, o)`, drawn with `renderSentRow` and read with `sayLit` (silent first for her, then Mila). `BOOK_HEROES`; books in
  `progress.books` (last 30) on the stories shelf (`openStories` always shows the shelf now). Lines in `pk-bk`. Nothing is
  generated while she plays; new heroes or things need their Sätze recordings first.

## Saved progress
- On the website and in the iPad app her progress lives in `localStorage` (`derdiedas.local.v1`). In the app iOS can empty
  that, so the app also keeps the save natively: `SaveStore` in `app/ios/App/App/SceneDelegate.swift` (UserDefaults),
  written right after every save and read at start, and the newer copy wins (`saved` stamp).
- A new field in `state.progress` must also be listed in `normalizeProgress`, or it is dropped at every start.

## Weekly list
**The tool:** Claude reads the photo of the school sheet and writes the list (`der Bär 🐻 | den Bären`, the `| den …` form for
words whose den-form is not just "den <word>"), then `python3 tools/make_week.py week.txt --title "Wortschatz B,b" [--refs crops/]`
makes the cards (crops of the sheet's own drawings in `--refs/<id>.png` are the first reference), Mila's w/n/q/den clips (checked
with speech-to-text; mismatches are listed) in `pw-<id>`, the new `data/words.json`, the index.html lists and `AUDIO_V`, and builds
last week's words in as `<LETTER>_WORDS`. Look at both card takes in `--work` and re-run with `--pick id=2` where take 2 is closer
to the sheet. Stories, Max's claims and Mil/Max lines are still made by hand. `--root <copy>` runs it on a test copy.
Higgsfield replies also list the reference images: read `result_url`, never the first link in the reply.
`data/words.json` (bump `version`) and `data/stories.json`. When the list changes, the previous week's words move to
review; build them into `index.html` the way `M_WORDS` and `I_WORDS` are.
Every game picks its words with `mixWords` in `index.html`: this week's words she hasn't learned yet (the ones she finds
tricky always come along), plus a few older words she still struggles with (`reviewWords`). Learned words only fill a game
up when there are too few others. A new game should pick its words the same way, so it follows the new list on its own,
and count her answers with `scoreWord` (the first answer to each word in a round). Like Duolingo, a word is learned after
`MASTERED` right answers in a row in any game (3 by default; grown-ups can pick 3, 4 or 5 in the word list). It then
stops repeating and only comes back for a check after 4, 7, 14 and 30 days; a mistake starts the count again. Mila's
tree hangs the words she is learning as leaves, and each branch is one of three games in turn (`TREE_GAMES`): Hör mal
(Mila names a leaf), Mila's favourite (she only wants der, die or das leaves; these answers count with `scoreWord`) and
falling leaves (catch the one she names).
