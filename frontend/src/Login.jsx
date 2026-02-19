import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "./components/Logo";

function Login({ setIsAuthenticated }) {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);

      const res = await fetch(`http://localhost:8000/auth/login`, { method: "POST", body: formData });
      const data = await res.json();

      if (data.status !== "SUCCESS") {
        setError("ACCESS DENIED - INVALID CREDENTIALS");
        return;
      }

      localStorage.setItem("user", data.user);
      localStorage.setItem("username", data.user);
      localStorage.setItem("role", data.role);
      setIsAuthenticated(true);
      navigate("/dashboard");
    } catch (err) {
      setError("CONNECTION ERROR - CHECK BACKEND");
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden">
      {/* Matrix-style background */}
      <div className="absolute inset-0 bg-gradient-to-b from-green-950/20 via-black to-black"></div>
      
      {/* Animated grid */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(#22c55e 1px, transparent 1px), linear-gradient(90deg, #22c55e 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }}></div>
      </div>

      <form
        onSubmit={handleLogin}
        className="relative z-10 bg-black p-8 rounded border-2 border-green-700 shadow-2xl shadow-green-900/50 w-96"
      >
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <Logo size="lg" />
          </div>
          <p className="text-green-600 text-sm font-mono border-t border-b border-green-900 py-2 mt-2">
            [ INSIDER THREAT MONITORING SYSTEM ]
          </p>
          <div className="text-red-500 text-xs font-mono mt-2 animate-pulse">
            ⚠ AUTHORIZED ACCESS ONLY ⚠
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-950 border-2 border-red-700 text-red-300 p-3 rounded mb-4 text-sm font-mono text-center animate-pulse">
            ⚠ {error}
          </div>
        )}

        {/* Username Input */}
        <div className="mb-4">
          <label className="text-green-500 text-xs font-mono mb-2 block">
            [ USER ID ]
          </label>
          <input
            className="w-full p-3 rounded bg-gray-950 text-green-400 border-2 border-green-900 focus:border-green-500 focus:outline-none font-mono placeholder-green-900"
            placeholder="Enter username..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        {/* Password Input */}
        <div className="mb-6">
          <label className="text-green-500 text-xs font-mono mb-2 block">
            [ ACCESS CODE ]
          </label>
          <input
            type="password"
            className="w-full p-3 rounded bg-gray-950 text-green-400 border-2 border-green-900 focus:border-green-500 focus:outline-none font-mono placeholder-green-900"
            placeholder="Enter password..."
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        {/* Login Button */}
        <button className="w-full bg-green-900 hover:bg-green-800 text-green-100 font-bold py-3 rounded border-2 border-green-700 transition font-mono tracking-wider shadow-lg shadow-green-900/50">
          [ AUTHENTICATE ]
        </button>

        {/* Footer */}
        <div className="mt-6 text-center">
       
          <div className="mt-4">
            <button
              type="button"
              onClick={() => navigate("/register")}
              className="text-cyan-500 text-sm font-mono hover:text-cyan-400"
            >
              📝 New User? Register Here →
            </button>
          </div>
        </div>

        {/* Security Notice */}
        <div className="mt-6 p-3 bg-gray-950 border border-gray-800 rounded">
          <p className="text-gray-600 text-xs font-mono text-center">
            🔒 ALL ACCESS ATTEMPTS ARE LOGGED
          </p>
          <p className="text-gray-700 text-xs font-mono text-center mt-1">
            CONTINUOUS MONITORING ACTIVE
          </p>
        </div>
      </form>
    </div>
  );
}

export default Login;
