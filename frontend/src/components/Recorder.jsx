import { useState } from "react";
import useTranscriber from "../hooks/useTranscriber";

export default function Recorder() {
  const [lang, setLang] = useState("auto");
  const { recording, partial, finals, error, level, start, stop } = useTranscriber(lang);

  return (
    <section className="card">
      <h2>Live transcription</h2>
      <div className="row">
        <select value={lang} onChange={(e) => setLang(e.target.value)} disabled={recording}>
          <option value="auto">Auto-detect (Hindi + English)</option>
          <option value="hi">Hindi</option>
          <option value="en">English</option>
          <option value="ta">Tamil</option>
          <option value="te">Telugu</option>
          <option value="kn">Kannada</option>
          <option value="ml">Malayalam</option>
        </select>
        {recording ? (
          <button className="danger" onClick={stop}>■ Stop &amp; save</button>
        ) : (
          <button className="primary" onClick={start}>🎤 Start speaking</button>
        )}
        {recording && <span className="pulse">● listening</span>}
      </div>
      {recording && (
        <div className="meter" title="Mic level - should move when you speak">
          <div className="meter-bar" style={{ width: `${Math.min(100, level * 400)}%` }} />
        </div>
      )}
      {error && <p className="error">{error}</p>}
      <div className="live">
        {partial || (recording ? "Speak now…" : "Press start and speak.")}
      </div>
      {finals.length > 0 && (
        <ul className="finals">
          {finals.map((t, i) => <li key={i}>{t}</li>)}
        </ul>
      )}
    </section>
  );
}
