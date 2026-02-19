import { useEffect, useState } from "react";
import { getUserData } from "../api/api";
import Logo from "../components/Logo";
import axios from "axios";

export default function UserDashboard() {
  const user = localStorage.getItem("user");
  const [data, setData] = useState(null);
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [realtimeStats, setRealtimeStats] = useState({ cpu: 0, memory: 0, network: 0 });

  const availableFiles = [
    { name: "dashboard.html", type: "public", icon: "📄", color: "from-blue-600 to-blue-700" },
    { name: "reports.pdf", type: "internal", icon: "📊", color: "from-purple-600 to-purple-700" },
    { name: "analytics.xlsx", type: "internal", icon: "📈", color: "from-indigo-600 to-indigo-700" },
    { name: "profile.json", type: "public", icon: "👤", color: "from-cyan-600 to-cyan-700" },
    { name: "admin.config", type: "sensitive", icon: "⚙️", color: "from-orange-600 to-orange-700" },
    { name: "credentials.txt", type: "sensitive", icon: "🔐", color: "from-red-600 to-red-700" },
    { name: "database.sql", type: "critical", icon: "💾", color: "from-rose-600 to-rose-700" },
    { name: "secrets.env", type: "critical", icon: "🔑", color: "from-pink-600 to-pink-700" }
  ];

  useEffect(() => {
    if (user) {
      loadData();
      loadFiles();
      const interval = setInterval(() => {
        loadData();
        loadFiles();
        updateRealtimeStats();
      }, 3000);
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

  const updateRealtimeStats = () => {
    setRealtimeStats({
      cpu: Math.floor(Math.random() * 100),
      memory: Math.floor(Math.random() * 100),
      network: Math.floor(Math.random() * 50)
    });
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
      <div className="flex items-center justify-center h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-blue-500 mx-auto mb-4"></div>
          <div className="text-white text-xl font-semibold">Loading your workspace...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      {message && (
        <div className={`fixed top-20 right-6 z-50 px-6 py-4 rounded-xl font-semibold shadow-2xl border-2 ${
          message.includes('✓') 
            ? 'bg-green-600 border-green-400 text-white' 
            : 'bg-red-600 border-red-400 text-white'
        }`}>
          {message}
        </div>
      )}

      <div className="max-w-[1600px] mx-auto space-y-6">
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-900/30 via-gray-800 to-purple-900/30 rounded-2xl p-6 border border-blue-500/30 shadow-2xl">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <Logo size="md" />
              <div>
                <h1 className="text-3xl font-bold text-white mb-1">My Workspace</h1>
                <p className="text-blue-300 text-sm">Welcome back, {user}</p>
              </div>
            </div>
            <div className="text-right">
              <div className={`text-2xl font-bold mb-1 ${data.decision === 'ALLOW' ? 'text-green-400' : data.decision === 'RESTRICT' ? 'text-yellow-400' : 'text-red-400'}`}>
                {data.decision === 'ALLOW' ? '✓ ACCESS GRANTED' : data.decision === 'RESTRICT' ? '⚠ LIMITED ACCESS' : '✗ ACCESS DENIED'}
              </div>
              <div className="text-xs text-gray-400">{new Date().toLocaleString()}</div>
            </div>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-4">
          <div className="bg-gradient-to-br from-green-900/40 to-green-800/40 rounded-xl p-6 border border-green-500/30 shadow-lg">
            <div className="text-green-300 text-xs font-semibold mb-2">ACCOUNT STATUS</div>
            <div className="text-3xl font-bold text-white mb-1">ACTIVE</div>
            <div className="text-green-400 text-xs">All Systems Operational</div>
          </div>
          
          <div className="bg-gradient-to-br from-blue-900/40 to-blue-800/40 rounded-xl p-6 border border-blue-500/30 shadow-lg">
            <div className="text-blue-300 text-xs font-semibold mb-2">TOTAL SESSIONS</div>
            <div className="text-4xl font-bold text-white mb-1">{data.login_count || 0}</div>
            <div className="text-blue-400 text-xs">Login History</div>
          </div>
          
          <div className="bg-gradient-to-br from-purple-900/40 to-purple-800/40 rounded-xl p-6 border border-purple-500/30 shadow-lg">
            <div className="text-purple-300 text-xs font-semibold mb-2">FILE OPERATIONS</div>
            <div className="text-4xl font-bold text-white mb-1">{files.length}</div>
            <div className="text-purple-400 text-xs">Recent Activities</div>
          </div>

          <div className="bg-gradient-to-br from-orange-900/40 to-orange-800/40 rounded-xl p-6 border border-orange-500/30 shadow-lg">
            <div className="text-orange-300 text-xs font-semibold mb-2">RISK SCORE</div>
            <div className={`text-4xl font-bold mb-1 ${data.risk_score >= 70 ? 'text-red-400' : data.risk_score >= 50 ? 'text-yellow-400' : 'text-green-400'}`}>
              {data.risk_score || 0}
            </div>
            <div className="text-orange-400 text-xs">{data.risk_level || 'LOW'} Risk</div>
          </div>
        </div>

        {/* System Metrics */}
        <div className="grid grid-cols-3 gap-4">
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <div className="flex justify-between items-center mb-2">
              <span className="text-cyan-400 text-sm font-semibold">CPU Usage</span>
              <span className="text-white font-bold">{realtimeStats.cpu}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="bg-cyan-500 h-2 rounded-full transition-all" style={{width: `${realtimeStats.cpu}%`}}></div>
            </div>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <div className="flex justify-between items-center mb-2">
              <span className="text-yellow-400 text-sm font-semibold">Memory</span>
              <span className="text-white font-bold">{realtimeStats.memory}%</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="bg-yellow-500 h-2 rounded-full transition-all" style={{width: `${realtimeStats.memory}%`}}></div>
            </div>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4 border border-gray-700/50">
            <div className="flex justify-between items-center mb-2">
              <span className="text-purple-400 text-sm font-semibold">Network</span>
              <span className="text-white font-bold">{realtimeStats.network} conn</span>
            </div>
            <div className="w-full bg-gray-700 rounded-full h-2">
              <div className="bg-purple-500 h-2 rounded-full transition-all" style={{width: `${realtimeStats.network * 2}%`}}></div>
            </div>
          </div>
        </div>

        {/* Accessible Zones */}
        <div className="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 shadow-xl">
          <h3 className="text-xl font-bold text-white mb-4">🔓 My Accessible Zones</h3>
          <div className="grid grid-cols-4 gap-3">
            {data.accessible_resources?.map((r, i) => (
              <div key={i} className="bg-gradient-to-br from-green-900/30 to-green-800/30 border-2 border-green-600/50 p-4 rounded-xl text-green-300 text-center font-semibold hover:from-green-800/40 hover:to-green-700/40 transition cursor-pointer">
                ✓ {r.toUpperCase()}
              </div>
            ))}
          </div>
        </div>

        {/* File Resources */}
        <div className="bg-gray-800/50 rounded-2xl p-6 border border-gray-700/50 shadow-xl">
          <h3 className="text-xl font-bold text-white mb-4">📁 My Files & Resources</h3>
          <div className="grid grid-cols-4 gap-4">
            {availableFiles.map((file, i) => (
              <div key={i} className={`bg-gradient-to-br ${file.color} p-5 rounded-xl border-2 border-white/20 hover:border-white/40 transition shadow-lg`}>
                <div className="text-5xl mb-3">{file.icon}</div>
                <div className="text-white font-bold mb-1 text-sm">{file.name}</div>
                <div className="text-xs mb-4 uppercase font-semibold text-white/80">{file.type}</div>
                <div className="flex gap-2">
                  <button onClick={() => handleFileAccess(file.name, "READ")} className="flex-1 bg-white/20 hover:bg-white/30 border border-white/40 text-white px-2 py-2 rounded text-xs transition font-semibold">
                    OPEN
                  </button>
                  <button onClick={() => handleFileAccess(file.name, "WRITE")} className="flex-1 bg-white/20 hover:bg-white/30 border border-white/40 text-white px-2 py-2 rounded text-xs transition font-semibold">
                    EDIT
                  </button>
                  <button onClick={() => handleFileAccess(file.name, "DELETE")} className="flex-1 bg-red-600/80 hover:bg-red-600 border border-red-400 text-white px-2 py-2 rounded text-xs transition font-semibold">
                    DEL
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Activity History */}
        <div className="bg-gray-800/50 rounded-2xl border border-gray-700/50 shadow-xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 p-4 border-b border-gray-700/50">
            <h3 className="text-xl font-bold text-white">📋 My Activity History</h3>
          </div>
          <div className="overflow-x-auto">
            {files.length === 0 ? (
              <div className="text-gray-500 text-center py-12">
                <div className="text-5xl mb-3">📂</div>
                <div className="text-lg">No recent activity</div>
              </div>
            ) : (
              <table className="w-full text-sm">
                <thead className="bg-gray-900/50 border-b border-gray-700">
                  <tr>
                    <th className="text-left p-4 text-blue-300 font-semibold">FILE</th>
                    <th className="text-left p-4 text-blue-300 font-semibold">ACTION</th>
                    <th className="text-left p-4 text-blue-300 font-semibold">TIMESTAMP</th>
                  </tr>
                </thead>
                <tbody>
                  {files.map((f, i) => (
                    <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-700/30 transition">
                      <td className="p-4 text-gray-300">{f.file_name}</td>
                      <td className="p-4">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${
                          f.action === "READ" ? "bg-cyan-500/20 text-cyan-300" :
                          f.action === "WRITE" ? "bg-yellow-500/20 text-yellow-300" :
                          "bg-red-500/20 text-red-300"
                        }`}>
                          {f.action}
                        </span>
                      </td>
                      <td className="p-4 text-gray-400">{new Date(f.access_time).toLocaleString()}</td>
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
