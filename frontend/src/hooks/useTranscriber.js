import { useRef, useState } from "react";
import { wsUrl } from "../services/api";

/** Streams mic audio (16kHz PCM) to the backend and exposes live/final text. */
export default function useTranscriber(lang) {
  const [recording, setRecording] = useState(false);
  const [partial, setPartial] = useState("");
  const [finals, setFinals] = useState([]);
  const [error, setError] = useState("");
  const [level, setLevel] = useState(0);
  const ref = useRef({});

  function cleanup() {
    const { stream, ctx, ws } = ref.current;
    stream?.getTracks().forEach((t) => t.stop());
    ctx?.close();
    ws?.close();
    ref.current = {};
  }

  async function start() {
    setError("");
    setPartial("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        // Browser filters off: they can strip speech played from a speaker/phone and distort voices.
        audio: { channelCount: 1, echoCancellation: false, noiseSuppression: false, autoGainControl: true },
      });
      const ctx = new AudioContext();
      await ctx.resume(); // Chrome may start the context suspended
      await ctx.audioWorklet.addModule("/pcm-worklet.js");
      const src = ctx.createMediaStreamSource(stream);
      const node = new AudioWorkletNode(ctx, "pcm-processor");
      // Route through a muted gain to the destination so the browser keeps processing the node.
      const mute = ctx.createGain();
      mute.gain.value = 0;
      node.connect(mute).connect(ctx.destination);
      const ws = new WebSocket(wsUrl(lang));
      ws.binaryType = "arraybuffer";

      ws.onmessage = (e) => {
        const m = JSON.parse(e.data);
        if (m.type === "partial") setPartial(m.text);
        else if (m.type === "final") {
          setPartial("");
          if (m.text) setFinals((f) => [m.text, ...f]);
          if (ref.current.closing) cleanup();
        }
      };
      ws.onerror = () => setError("WebSocket connection failed. Is the backend running?");
      node.port.onmessage = (e) => {
        setLevel(e.data.rms); // mic loudness for the on-screen meter
        if (ws.readyState === 1) ws.send(e.data.pcm);
      };
      src.connect(node);

      ref.current = { stream, ctx, node, ws, closing: false };
      setRecording(true);
    } catch (err) {
      setError(err.message || String(err));
    }
  }

  function stop() {
    const { node, ws } = ref.current;
    if (!ws) return;
    node.disconnect();
    ref.current.closing = true;
    setRecording(false);
    if (ws.readyState === 1) ws.send("stop");
    else cleanup();
  }

  return { recording, partial, finals, error, level, start, stop };
}
