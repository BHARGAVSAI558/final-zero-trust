import { useEffect, useState } from "react";
import { getUserData } from "../api/api";
import axios from "axios";

export default function UserDashboard() {
  const user = localStorage.getItem("user");
  const [data, setData] = useState(null);
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");

  const availableFiles = [
    { name: "dashboard.html", type: "public", icon: "📄", color: "from-cyan-900 to-cyan-950" },
    { name: "reports.pdf", type: "internal", icon: "📊", color: "from-blue-900 to-blue-950" },
    { name: "analytics.xlsx", type: "internal", icon: "📈", color: "from-blue-900 to-blue-950" },
    { name: "profile.json", type: "public", icon: "👤", color: "from-cyan-900 to-cyan-950" },
    { name: "admin.config", type: "sensitive", icon: "⚙️", color: "from-orange-900 to-orange-950" },
    { name: "credentials.txt", type: "sensitive", icon: "🔐", color: "from-orange-900 to-orange-950" },
    { name: "database.sql", type: "critical", icon: "💾", color: "from-red-900 to-red-950" },
    { name: "secrets.env", type: "critical", icon: "🔑", color: "from-red-900 to-red-950" }
  ];

  useEffect(() => {
    if (user) {
      loadData();
      loadFiles();
      const interval = setInterval(() => {
        loadData();
        loadFiles();
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const loadData = async () => {
    try {
      const result = await getUserData(user);
      if (result && Object.keys(result).length > 0) {
        setData(result);
      }
    } catch (err) {
      console.error("Load data error:", err);
    }
  };

  const loadFiles = async () => {
    try {
      const res = await axios.get(`http://localhost:8000/files/list/${user}`);
      if (res.data && res.data.length > 0) {
        setFiles(res.data);
      }
    } catch (err) {
      console.error("Load files error:", err);
    }
  };

  const handleFileAccess = async (fileName, action) => {
    try {
      await axios.post("http://localhost:8000/files/access", {
        user_id: user,
        file_name: fileName,
        action: action
      });
      setMessage(`✓ ${action} successful: ${fileName}`);
      setTimeout(() => setMessage(""), 3000);
      loadData();
      loadFiles();
    } catch (err) {
      setMessage("✗ ACCESS DENIED - Contact Administrator");
      setTimeout(() => setMessage(""), 3000);
    }
  };

  if (!data) {
    return (
      <div className="flex items-center justify-center h-screen bg-black">
        <div className="text-green-400 text-xl font-mono animate-pulse">
          Loading your workspace...
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="fixed inset-0 opacity-5" style={{
        backgroundImage: 'linear-gradient(#22c55e 1px, transparent 1px), linear-gradient(90deg, #22c55e 1px, transparent 1px)',
        backgroundSize: '50px 50px'
      }}></div>
      
      {message && (
        <div className={`fixed top-20 right-4 z-50 px-6 py-3 rounded-lg font-mono shadow-lg font-bold border-2 ${
          message.includes('✓') 
            ? 'bg-green-900 border-green-500 text-green-100' 
            : 'bg-red-900 border-red-500 text-red-100'
        }`}>
          {message}
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-6 relative z-10">
        {/* Header */}
        <div className="bg-gradient-to-r from-green-950/50 via-black to-green-950/50 rounded-xl p-6 border-2 border-green-900/50 shadow-2xl shadow-green-900/30">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-green-400 font-mono tracking-wider">
                👤 MY WORKSPACE
              </h1>
              <p className="text-green-500 font-mono text-sm mt-1">
                Welcome back, {user}
              </p>
            </div>
            <div className="text-right">
              <div className={`text-lg font-bold font-mono ${data.decision === 'ALLOW' ? 'text-green-400' : data.decision === 'RESTRICT' ? 'text-yellow-400' : 'text-red-400'}`}>
                {data.decision === 'ALLOW' ? '✓ ACCESS GRANTED' : data.decision === 'RESTRICT' ? '⚠ LIMITED ACCESS' : '✗ ACCESS DENIED'}
              </div>
              <div className="text-xs text-gray-500 font-mono mt-1">{new Date().toLocaleString()}</div>
            </div>
          </div>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-black/80 rounded-xl p-6 border-2 border-green-900/50 shadow-lg backdrop-blur">
            <div className="text-green-500 text-xs font-bold mb-2 font-mono">MY STATUS</div>
            <div className="text-3xl font-bold text-green-400 font-mono">ACTIVE</div>
            <div className="text-gray-500 text-xs font-mono mt-2">Account Status</div>
          </div>
          
          <div className="bg-black/80 rounded-xl p-6 border-2 border-cyan-900/50 shadow-lg backdrop-blur">
            <div className="text-cyan-400 text-xs font-bold mb-2 font-mono">TOTAL SESSIONS</div>
            <div className="text-5xl font-bold text-cyan-400 font-mono">
              {data.total_logins || 0}
            </div>
            <div className="text-gray-500 text-xs font-mono mt-2">Login Count</div>
          </div>
          
          <div className="bg-black/80 rounded-xl p-6 border-2 border-purple-900/50 shadow-lg backdrop-blur">
            <div className="text-purple-400 text-xs font-bold mb-2 font-mono">FILE OPERATIONS</div>
            <div className="text-5xl font-bold text-purple-400 font-mono">
              {files.length}
            </div>
            <div className="text-gray-500 text-xs font-mono mt-2">Recent Activities</div>
          </div>
        </div>

        {/* Accessible Resources */}
        <div className="bg-black/80 p-6 rounded-xl border-2 border-green-900/50 shadow-lg backdrop-blur">
          <h3 className="text-xl font-bold text-green-400 mb-4 font-mono">🔓 MY ACCESSIBLE ZONES</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {data.accessible_resources?.map((r, i) => (
              <div key={i} className="bg-green-950/30 border-2 border-green-800 p-4 rounded text-green-300 text-center font-bold font-mono text-sm hover:bg-green-900/30 transition cursor-pointer">
                ✓ {r.toUpperCase()} ZONE
              </div>
            ))}
          </div>
        </div>

        {/* File Operations */}
        <div className="bg-black/80 p-6 rounded-xl border-2 border-cyan-900/50 shadow-lg backdrop-blur">
          <h3 className="text-xl font-bold text-cyan-400 mb-4 font-mono">📁 MY FILES & RESOURCES</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {availableFiles.map((file, i) => (
              <div key={i} className={`bg-gradient-to-br ${file.color} p-4 rounded-lg border-2 ${
                file.type === 'critical' ? 'border-red-700' :
                file.type === 'sensitive' ? 'border-orange-700' :
                file.type === 'internal' ? 'border-blue-700' :
                'border-cyan-700'
              } hover:shadow-lg transition`}>
                <div className="text-4xl mb-2">{file.icon}</div>
                <div className="text-white font-bold mb-1 font-mono text-xs">{file.name}</div>
                <div className={`text-xs mb-3 uppercase font-mono font-bold ${
                  file.type === 'critical' ? 'text-red-400' :
                  file.type === 'sensitive' ? 'text-orange-400' :
                  file.type === 'internal' ? 'text-blue-400' :
                  'text-cyan-400'
                }`}>
                  {file.type}
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleFileAccess(file.name, "READ")}
                    className="flex-1 bg-cyan-900 hover:bg-cyan-800 border-2 border-cyan-700 text-cyan-100 px-2 py-1 rounded text-xs transition font-mono font-bold"
                  >
                    OPEN
                  </button>
                  <button
                    onClick={() => handleFileAccess(file.name, "WRITE")}
                    className="flex-1 bg-yellow-900 hover:bg-yellow-800 border-2 border-yellow-700 text-yellow-100 px-2 py-1 rounded text-xs transition font-mono font-bold"
                  >
                    EDIT
                  </button>
                  <button
                    onClick={() => handleFileAccess(file.name, "DELETE")}
                    className="flex-1 bg-red-900 hover:bg-red-800 border-2 border-red-700 text-red-100 px-2 py-1 rounded text-xs transition font-mono font-bold"
                  >
                    DELETE
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* My Activity History */}
        <div className="bg-black/80 rounded-xl border-2 border-gray-700/50 shadow-lg backdrop-blur overflow-hidden">
          <div className="bg-gray-900/50 p-4 border-b-2 border-gray-700/50">
            <h3 className="text-xl font-bold text-gray-300 font-mono">📋 MY ACTIVITY HISTORY</h3>
          </div>
          <div className="overflow-x-auto">
            {files.length === 0 ? (
              <div className="text-gray-500 text-center py-12 font-mono">
                <div className="text-4xl mb-2">📂</div>
                <div>No recent activity</div>
              </div>
            ) : (
              <table className="w-full text-sm font-mono">
                <thead className="bg-gray-900/50 border-b-2 border-green-700">
                  <tr>
                    <th className="text-left p-3 text-green-400 font-bold">FILE</th>
                    <th className="text-left p-3 text-green-400 font-bold">ACTION</th>
                    <th className="text-left p-3 text-green-400 font-bold">TIMESTAMP</th>
                  </tr>
                </thead>
                <tbody>
                  {files.map((f, i) => (
                    <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-900/30">
                      <td className="p-3 text-gray-300">{f.file_name}</td>
                      <td className="p-3">
                        <span className={`px-3 py-1 rounded text-xs font-bold border-2 ${
                          f.action === "READ" ? "bg-cyan-950 text-cyan-300 border-cyan-700" :
                          f.action === "WRITE" ? "bg-yellow-950 text-yellow-300 border-yellow-700" :
                          "bg-red-950 text-red-300 border-red-700"
                        }`}>
                          {f.action}
                        </span>
                      </td>
                      <td className="p-3 text-gray-400">{new Date(f.access_time).toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
