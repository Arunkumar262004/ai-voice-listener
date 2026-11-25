import { Routes, Route, Navigate } from "react-router-dom";
import Layout from "./components/Layout.jsx";
import LivePage from "./pages/LivePage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";

// URL registration only — no logic lives here.
export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<LivePage />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}
