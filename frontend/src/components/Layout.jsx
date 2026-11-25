import { NavLink, Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <main>
      <h1>🎙️ Speech to Text</h1>
      <p className="sub">Real-time multilingual (Hindi + English) transcription · Whisper · PostgreSQL</p>
      <nav className="nav">
        <NavLink to="/" end>Live</NavLink>
        <NavLink to="/history">History</NavLink>
      </nav>
      <Outlet />
    </main>
  );
}
