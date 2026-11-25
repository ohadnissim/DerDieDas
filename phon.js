/* Aussprache-Helfer: hears WHICH sounds she made, for a word we already know.
   The model is facebook/wav2vec2-lv-60-espeak-cv-ft (Apache-2.0), the small ONNX build from onnx-community, run by
   transformers.js in the page (WebGPU when the iPad has it, else WebAssembly). It gives, for every 20 ms of her voice,
   how likely each speech sound is (ç, x, ʃ, s … separately). We never ask it "what word was that": we ask how well
   the right way to say the word fits, and how well her likely mistake fits (Schtern vs Stern, ich vs isch), and
   compare the two (CTC log-likelihood, summed over every timing). Above 0 = it sounded right.
   Tested on synthetic voices 2026-11-25: about 85 to 88 % right; on raised "child" voices 75 %, mostly ç heard as ʃ,
   so a child's own warm-up (her margins on words she says right) sets the line before it judges her.
   Loaded only when a grown-up switches it on (about 240 MB, downloaded once and kept by the browser).
   Browser test 2026-11-25 (tools/phon-test.html, Mila's own words): q4 on WebGPU and on WASM hear Stern as ʃ t ɛ n and score
   4 of 5 right like the full model; about 25 to 150 ms a word on WebGPU after the first, about 1 s on WASM. */
const PHON_MODEL = "onnx-community/wav2vec2-lv-60-espeak-cv-ft-ONNX";
const TJS = "https://cdn.jsdelivr.net/npm/@huggingface/transformers@3.5.1";
// espeak writes German r as ɾ; the model's tokens are whole sounds (aː, uː are one token each)
const PHON_MAP = { "ʁ": "ɾ" };

let phon = null;   // { model, vocab, blank, device }

export async function loadPhon(onProgress, force) {
  if (phon) return phon;
  const T = await import(TJS);
  T.env.allowLocalModels = false;
  const webgpu = !!(navigator.gpu && await navigator.gpu.requestAdapter().catch(() => null));
  // q4 on both: the q4f16 build lost almost every sound on WebGPU (tested 2026-11-25); q4 on WebGPU scores like the full model
  const opts = { dtype: "q4", device: webgpu ? "webgpu" : "wasm", progress_callback: onProgress, ...(force || {}) };
  const model = await T.AutoModelForCTC.from_pretrained(PHON_MODEL, opts);
  const vocab = await (await fetch("https://huggingface.co/" + PHON_MODEL + "/resolve/main/vocab.json")).json();
  phon = { T, model, vocab, inv: Object.fromEntries(Object.entries(vocab).map(([k, v]) => [v, k])), blank: vocab["<pad>"], device: opts.device };
  return phon;
}

// per 20 ms frame: log-probabilities of every sound (Float32Array rows)
export async function phonFrames(wav16k) {
  const { T, model } = phon;
  let m = 0; for (const v of wav16k) m += v; m /= wav16k.length;
  let s = 0; for (const v of wav16k) s += (v - m) ** 2; s = Math.sqrt(s / wav16k.length + 1e-7);
  const x = new Float32Array(wav16k.length); for (let i = 0; i < x.length; i++) x[i] = (wav16k[i] - m) / s;
  const out = await model({ input_values: new T.Tensor("float32", x, [1, x.length]) });
  const lg = out.logits, [, F, V] = lg.dims, d = lg.data, rows = [];
  for (let f = 0; f < F; f++) {
    const r = new Float32Array(V); let mx = -Infinity;
    for (let v = 0; v < V; v++) { r[v] = Number(d[f * V + v]); if (r[v] > mx) mx = r[v]; }
    let z = 0; for (let v = 0; v < V; v++) z += Math.exp(r[v] - mx);
    const lz = mx + Math.log(z); for (let v = 0; v < V; v++) r[v] -= lz;
    rows.push(r);
  }
  return rows;
}

// sounds as the model's tokens: "ʃ t ɛ ʁ n" (spaced) or straight from espeak "ʃtˈɛɾn" (longest token first, stress dropped)
const ids = (ipa) => {
  if (ipa.includes(" ")) return ipa.split(" ").map(p => { const t = PHON_MAP[p] || p; if (!(t in phon.vocab)) throw new Error("no token " + t); return phon.vocab[t]; });
  const x = [...ipa.replace(/[ˈˌ]/g, "")].map(c => PHON_MAP[c] || c).join(""), out = [];
  for (let i = 0; i < x.length;) {
    let k = Math.min(4, x.length - i);
    while (k > 0 && !(x.slice(i, i + k) in phon.vocab)) k--;
    if (!k) throw new Error("no token for " + x.slice(i));
    out.push(phon.vocab[x.slice(i, i + k)]); i += k;
  }
  return out;
};
const lse = (a, b) => a === -Infinity ? b : b === -Infinity ? a : Math.max(a, b) + Math.log1p(Math.exp(-Math.abs(a - b)));

// how well this way of saying it fits her voice (CTC forward, log space)
export function phonFit(rows, ipa) {
  const L = ids(ipa), S = 2 * L.length + 1, b = phon.blank;
  const lab = (s) => s % 2 ? L[(s - 1) / 2] : b;
  let a = new Array(S).fill(-Infinity);
  a[0] = rows[0][b]; if (S > 1) a[1] = rows[0][lab(1)];
  for (let t = 1; t < rows.length; t++) {
    const n = new Array(S).fill(-Infinity), r = rows[t];
    for (let s = 0; s < S; s++) {
      let v = a[s];
      if (s > 0) v = lse(v, a[s - 1]);
      if (s > 1 && s % 2 && lab(s) !== lab(s - 2)) v = lse(v, a[s - 2]);
      n[s] = v + r[lab(s)];
    }
    a = n;
  }
  return lse(a[S - 1], S > 1 ? a[S - 2] : -Infinity);
}

// above 0: the right way fits better than the mistake
export function phonMargin(rows, right, wrong) { return phonFit(rows, right) - phonFit(rows, wrong); }

// what it heard, plainly (for the grown-ups' test page)
export function phonHeard(rows) {
  const out = []; let prev = -1;
  for (const r of rows) { let bi = 0; for (let v = 1; v < r.length; v++) if (r[v] > r[bi]) bi = v; if (bi !== prev && bi !== phon.blank && !/^</.test(phon.inv[bi])) out.push(phon.inv[bi]); prev = bi; }
  return out.join(" ");
}

// her microphone or a recording, as 16 kHz mono
export async function to16k(buffer) {
  const ctx = new OfflineAudioContext(1, Math.ceil(buffer.duration * 16000), 16000);
  const src = ctx.createBufferSource(); src.buffer = buffer; src.connect(ctx.destination); src.start();
  return (await ctx.startRendering()).getChannelData(0);
}
