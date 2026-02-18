import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "./api/api";

function Register() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [message, setMessage] = useState("");
  const [success, setSuccess] = useState(false);

  const handleRegister = async (e) => {
    e.preventDefault();
    setMessage("");

    if (password !== confirmPassword) {
      setMessage("Passwords do not match");
      return;
    }

    if (password.length < 6) {
      setMessage("Password must be at least 6 characters");
      return;
    }

    try {
      const result = await register(username, password);
      
      if (result.status === "SUCCESS") {
        setSuccess(true);
        setMessage("Registration successful! Waiting for admin approval.");
        setTimeout(() => navigate("/"), 3000);
      } else {
        setMessage(result.message || "Registration failed");
      }
    } catch (err) {
      setMessage("Error: " + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-black flex items-center justify-center relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-cyan-950/20 via-black to-black"></div>
      
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0" style={{
          backgroundImage: 'linear-gradient(#06b6d4 1px, transparent 1px), linear-gradient(90deg, #06b6d4 1px, transparent 1px)',
          backgroundSize: '50px 50px'
        }}></div>
      </div>

      <form
        onSubmit={handleRegister}
        className="relative z-10 bg-black p-8 rounded border-2 border-cyan-700 shadow-2xl shadow-cyan-900/50 w-96"
      >
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">📝</div>
          <h1 className="text-3xl text-cyan-400 font-bold mb-2 font-mono tracking-wider">
            USER REGISTRATION
          </h1>
          <p className="text-cyan-600 text-sm font-mono border-t border-b border-cyan-900 py-2 mt-2">
            [ REQUEST ACCESS TO SYSTEM ]
          </p>
        </div>

        {message && (
          <div className={`${success ? 'bg-green-950 border-green-700 text-green-300' : 'bg-red-950 border-red-700 text-red-300'} border-2 p-3 rounded mb-4 text-sm font-mono text-center`}>
            {success ? '✓' : '⚠'} {message}
          </div>
        )}

        <div className="mb-4">
          <label className="text-cyan-500 text-xs font-mono mb-2 block">
            [ USERNAME ]
          </label>
          <input
            className="w-full p-3 rounded bg-gray-950 text-cyan-400 border-2 border-cyan-900 focus:border-cyan-500 focus:outline-none font-mono placeholder-cyan-900"
            placeholder="Choose username..."
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-4">
          <label className="text-cyan-500 text-xs font-mono mb-2 block">
            [ PASSWORD ]
          </label>
          <input
            type="password"
            className="w-full p-3 rounded bg-gray-950 text-cyan-400 border-2 border-cyan-900 focus:border-cyan-500 focus:outline-none font-mono placeholder-cyan-900"
            placeholder="Choose password..."
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div className="mb-6">
          <label className="text-cyan-500 text-xs font-mono mb-2 block">
            [ CONFIRM PASSWORD ]
          </label>
          <input
            type="password"
            className="w-full p-3 rounded bg-gray-950 text-cyan-400 border-2 border-cyan-900 focus:border-cyan-500 focus:outline-none font-mono placeholder-cyan-900"
            placeholder="Confirm password..."
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
          />
        </div>

        <button className="w-full bg-cyan-900 hover:bg-cyan-800 text-cyan-100 font-bold py-3 rounded border-2 border-cyan-700 transition font-mono tracking-wider shadow-lg shadow-cyan-900/50">
          [ SUBMIT REQUEST ]
        </button>

        <div className="mt-6 text-center">
          <button
            type="button"
            onClick={() => navigate("/")}
            className="text-cyan-500 text-sm font-mono hover:text-cyan-400"
          >
            ← Back to Login
          </button>
        </div>

        <div className="mt-6 p-3 bg-gray-950 border border-gray-800 rounded">
          <p className="text-gray-600 text-xs font-mono text-center">
            ⏳ ADMIN APPROVAL REQUIRED
          </p>
          <p className="text-gray-700 text-xs font-mono text-center mt-1">
            Your request will be reviewed by administrators
          </p>
        </div>
      </form>
    </div>
  );
}

export default Register;
