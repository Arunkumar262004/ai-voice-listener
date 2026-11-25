import { useEffect, useState, useCallback } from "react";
import { api } from "../services/api";

const PAGE = 10;

export default function HistoryTable() {
  const [data, setData] = useState({ total: 0, items: [] });
  const [q, setQ] = useState("");
  const [page, setPage] = useState(0);
  const [editing, setEditing] = useState(null);
  const [draft, setDraft] = useState("");
  const [adding, setAdding] = useState("");
  const [error, setError] = useState("");

  const load = useCallback(async () => {
    try {
      setData(await api.list(q, page * PAGE, PAGE));
      setError("");
    } catch (e) {
      setError(e.message);
    }
  }, [q, page]);

  useEffect(() => { load(); }, [load]);

  async function add() {
    if (!adding.trim()) return;
    await api.create({ text: adding.trim() });
    setAdding("");
    load();
  }
  async function save(id) {
    await api.update(id, { text: draft });
    setEditing(null);
    load();
  }
  async function del(id) {
    if (!confirm("Delete this transcription?")) return;
    await api.remove(id);
    load();
  }

  const pages = Math.max(1, Math.ceil(data.total / PAGE));

  return (
    <section className="card">
      <h2>Transcription history <small>({data.total})</small></h2>
      <div className="row">
        <input placeholder="Search…" value={q} onChange={(e) => { setPage(0); setQ(e.target.value); }} />
      </div>
      <div className="row">
        <input
          placeholder="Add a transcription manually…"
          value={adding}
          onChange={(e) => setAdding(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && add()}
        />
        <button onClick={add}>Add</button>
      </div>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr><th>When</th><th>Lang</th><th>Text</th><th>Sec</th><th></th></tr>
        </thead>
        <tbody>
          {data.items.map((t) => (
            <tr key={t.id}>
              <td>{new Date(t.created_at).toLocaleString()}</td>
              <td>{t.language || "-"}</td>
              <td className="text">
                {editing === t.id ? (
                  <textarea value={draft} onChange={(e) => setDraft(e.target.value)} rows={3} />
                ) : t.text}
              </td>
              <td>{t.duration_sec != null ? t.duration_sec.toFixed(1) : "-"}</td>
              <td className="actions">
                {editing === t.id ? (
                  <>
                    <button onClick={() => save(t.id)}>Save</button>
                    <button onClick={() => setEditing(null)}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => { setEditing(t.id); setDraft(t.text); }}>Edit</button>
                    <button className="danger" onClick={() => del(t.id)}>Delete</button>
                  </>
                )}
              </td>
            </tr>
          ))}
          {data.items.length === 0 && (
            <tr><td colSpan={5} className="empty">No transcriptions yet.</td></tr>
          )}
        </tbody>
      </table>
      <div className="row pager">
        <button disabled={page === 0} onClick={() => setPage(page - 1)}>‹ Prev</button>
        <span>Page {page + 1} / {pages}</span>
        <button disabled={page + 1 >= pages} onClick={() => setPage(page + 1)}>Next ›</button>
      </div>
    </section>
  );
}
