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
  `pk-sk7`, `pk-sk8`, `pk-sk9`, `pk-sk10`, `pk-xmax-l`), so the files that already exist are not re-encoded. Bump `AUDIO_V`.
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

## Saved progress
- On the website and in the iPad app her progress lives in `localStorage` (`derdiedas.local.v1`). In the app iOS can empty
  that, so the app also keeps the save natively: `SaveStore` in `app/ios/App/App/SceneDelegate.swift` (UserDefaults),
  written right after every save and read at start, and the newer copy wins (`saved` stamp).
- A new field in `state.progress` must also be listed in `normalizeProgress`, or it is dropped at every start.

## Weekly list
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
