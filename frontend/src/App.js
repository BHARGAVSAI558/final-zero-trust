import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import SOCDashboard from "./pages/SOCDashboard";
import FileManager from "./pages/FileManager";
import Login from "./Login";
import Register from "./Register";
import LandingPage from "./LandingPage";

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(() => {
    return localStorage.getItem("isAuthenticated") === "true";
  });

  useEffect(() => {
    const authStatus = localStorage.getItem("isAuthenticated");
    if (authStatus === "true") {
      setIsAuthenticated(true);
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    localStorage.removeItem("isAuthenticated");
    setIsAuthenticated(false);
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
          isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" replace />
        } />
        <Route path="/soc" element={
          isAuthenticated ? <SOCDashboard /> : <Navigate to="/login" replace />
        } />
        <Route path="/files" element={
          isAuthenticated ? <FileManager /> : <Navigate to="/login" replace />
        } />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
