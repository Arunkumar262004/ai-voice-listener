const base = import.meta.env.VITE_API_URL || "";

async function req(path, opts = {}) {
  const r = await fetch(base + path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  if (!r.ok) throw new Error(`${r.status} ${await r.text()}`);
  return r.status === 204 ? null : r.json();
}

export const api = {
  list: (q = "", skip = 0, limit = 20) =>
    req(`/api/transcriptions?q=${encodeURIComponent(q)}&skip=${skip}&limit=${limit}`),
  create: (data) => req("/api/transcriptions", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) => req(`/api/transcriptions/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  remove: (id) => req(`/api/transcriptions/${id}`, { method: "DELETE" }),
};

export function wsUrl(lang) {
  const apiBase = import.meta.env.VITE_API_URL;
  const origin = apiBase
    ? apiBase.replace(/^http/, "ws")
    : `${location.protocol === "https:" ? "wss" : "ws"}://${location.host}`;
  return `${origin}/ws/transcribe?lang=${lang}`;
}
