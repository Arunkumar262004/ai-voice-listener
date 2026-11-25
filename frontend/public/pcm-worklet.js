// Downsamples mic audio to 16kHz mono int16 and posts ~100ms chunks (plus a level) to the main thread.
class PCMProcessor extends AudioWorkletProcessor {
  constructor() {
    super();
    this.ratio = sampleRate / 16000;
    this.pos = 0;
    this.out = [];
  }
  process(inputs) {
    const ch = inputs[0][0];
    if (!ch) return true;
    while (this.pos < ch.length) {
      const s = Math.max(-1, Math.min(1, ch[Math.floor(this.pos)]));
      this.out.push(s < 0 ? s * 0x8000 : s * 0x7fff);
      this.pos += this.ratio;
    }
    this.pos -= ch.length;
    if (this.out.length >= 1600) {
      let sum = 0;
      for (const v of this.out) sum += (v / 32768) ** 2;
      const rms = Math.sqrt(sum / this.out.length);
      const pcm = Int16Array.from(this.out).buffer;
      this.out = [];
      this.port.postMessage({ pcm, rms }, [pcm]);
    }
    return true;
  }
}
registerProcessor("pcm-processor", PCMProcessor);
