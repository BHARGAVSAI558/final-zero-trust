import { useEffect, useState } from "react";
import { getUserData } from "../api/api";
import axios from "axios";

export default function UserDashboard() {
  const user = localStorage.getItem("user");
  const [data, setData] = useState(null);
  const [files, setFiles] = useState([]);
  const [message, setMessage] = useState("");
  const [deviceInfo, setDeviceInfo] = useState(null);

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
      collectDeviceInfo();
      const interval = setInterval(() => {
        loadData();
        loadFiles();
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [user]);

  const collectDeviceInfo = async () => {
    const info = {
      browser: navigator.userAgent,
      platform: navigator.platform,
      language: navigator.language,
      screen: `${window.screen.width}x${window.screen.height}`,
      timezone: Intl.DateTimeFormat().resolvedOptions().timeZone
    };
    setDeviceInfo(info);
    
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(async (position) => {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        try {
          const geo = await fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lon}&format=json`);
          const location = await geo.json();
          const exactLocation = `${location.address.village || location.address.town || location.address.city}, ${location.address.state}`;
          localStorage.setItem("exactLocation", exactLocation);
          loadData();
        } catch (err) {
          console.log("GPS error:", err);
        }
      });
    }
    
    try {
      await axios.post("http://localhost:8000/device/register", {
        username: user,
        device_id: navigator.userAgent.substring(0, 50),
        mac_address: "WEB-" + Math.random().toString(36).substring(2, 15),
        os: navigator.platform,
        wifi_ssid: "Browser-Network",
        hostname: window.location.hostname,
        ip_address: "auto-detect"
      });
    } catch (err) {
      console.log("Device registration:", err);
    }
  };

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
      setMessage(`✓ ${action} ${fileName}`);
      setTimeout(() => setMessage(""), 2000);
      loadData();
      loadFiles();
    } catch (err) {
      setMessage("✗ ACCESS DENIED");
      setTimeout(() => setMessage(""), 2000);
    }
  };

  if (!data) {
    return (
      <div className="flex items-center justify-center h-screen bg-black">
        <div className="text-green-400 text-xl font-mono animate-pulse">
          [ INITIALIZING SECURITY PROTOCOL... ]
        </div>
      </div>
    );
  }

  const getRiskColor = (score) => {
    if (score >= 70) return "text-red-500";
    if (score >= 50) return "text-orange-500";
    if (score >= 30) return "text-yellow-500";
    return "text-green-500";
  };

  const getRiskBg = (score) => {
    if (score >= 70) return "from-red-950 to-black border-red-700";
    if (score >= 50) return "from-orange-950 to-black border-orange-700";
    if (score >= 30) return "from-yellow-950 to-black border-yellow-700";
    return "from-green-950 to-black border-green-700";
  };

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="fixed inset-0 bg-gradient-to-b from-green-950/10 via-black to-black pointer-events-none"></div>
      
      {message && (
        <div className="fixed top-4 right-4 z-50 bg-green-900 border border-green-500 text-green-100 px-6 py-3 rounded font-mono shadow-lg shadow-green-500/50">
          {message}
        </div>
      )}

      <div className="max-w-7xl mx-auto space-y-6 relative z-10">
        <div className="bg-gradient-to-r from-black via-green-950 to-black p-6 rounded border border-green-700 shadow-lg shadow-green-900/50">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-green-400 font-mono tracking-wider">
                ⚠ ZERO TRUST SECURITY SYSTEM
              </h1>
              <p className="text-green-500 font-mono text-sm mt-1">
                [ USER: {user.toUpperCase()} ] | [ STATUS: MONITORING ACTIVE ]
              </p>
            </div>
            <div className="text-right text-green-400 font-mono">
              <div className="text-xs text-green-600">LAST SYNC</div>
              <div className="text-lg animate-pulse">{new Date().toLocaleTimeString()}</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className={`bg-gradient-to-br ${getRiskBg(data.risk_score)} p-6 rounded border-2 shadow-lg`}>
            <div className="text-xs text-gray-400 font-mono mb-1">THREAT LEVEL</div>
            <div className={`text-6xl font-bold font-mono ${getRiskColor(data.risk_score)}`}>
              {data.risk_score}
            </div>
            <div className="text-xs text-gray-500 font-mono mt-2">/ 100 RISK SCORE</div>
          </div>
          
          <div className="bg-gradient-to-br from-gray-950 to-black p-6 rounded border-2 border-gray-700 shadow-lg">
            <div className="text-xs text-gray-400 font-mono mb-1">CLASSIFICATION</div>
            <div className={`text-2xl font-bold font-mono ${getRiskColor(data.risk_score)}`}>
              {data.risk_level}
            </div>
            <div className="text-xs text-gray-500 font-mono mt-2">SECURITY STATUS</div>
          </div>
          
          <div className={`bg-gradient-to-br ${
            data.decision === "ALLOW" ? "from-green-950 to-black border-green-700" :
            data.decision === "RESTRICT" ? "from-yellow-950 to-black border-yellow-700" :
            "from-red-950 to-black border-red-700"
          } p-6 rounded border-2 shadow-lg`}>
            <div className="text-xs text-gray-400 font-mono mb-1">ACCESS CONTROL</div>
            <div className={`text-2xl font-bold font-mono ${
              data.decision === "ALLOW" ? "text-green-400" :
              data.decision === "RESTRICT" ? "text-yellow-400" :
              "text-red-400"
            }`}>
              {data.decision}
            </div>
            <div className="text-xs text-gray-500 font-mono mt-2">SYSTEM POLICY</div>
          </div>
          
          <div className="bg-gradient-to-br from-cyan-950 to-black p-6 rounded border-2 border-cyan-700 shadow-lg">
            <div className="text-xs text-gray-400 font-mono mb-1">SESSION COUNT</div>
            <div className="text-6xl font-bold text-cyan-400 font-mono">
              {data.total_logins}
            </div>
            <div className="text-xs text-gray-500 font-mono mt-2">TOTAL LOGINS</div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-black p-6 rounded border-2 border-red-900 shadow-lg shadow-red-900/30">
            <h3 className="text-xl font-bold text-red-400 mb-4 flex items-center gap-2 font-mono">
              ⚠ THREAT DETECTION
              <span className="text-sm bg-red-900 px-2 py-1 rounded border border-red-700">
                {data.signals?.length || 0} ALERTS
              </span>
            </h3>
            <div className="space-y-2 max-h-48 overflow-y-auto">
              {!data.signals || data.signals.length === 0 ? (
                <div className="text-green-400 text-lg font-mono border border-green-700 p-3 rounded bg-green-950/30">
                  ✓ NO THREATS DETECTED - SYSTEM SECURE
                </div>
              ) : (
                data.signals.map((s, i) => (
                  <div key={i} className="bg-red-950/30 border border-red-800 p-3 rounded text-red-300 flex items-start gap-2 font-mono text-sm">
                    <span className="text-red-500">⚠</span>
                    <span>{s.replace(/_/g, " ")}</span>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-black p-6 rounded border-2 border-cyan-900 shadow-lg shadow-cyan-900/30">
            <h3 className="text-xl font-bold text-cyan-400 mb-4 font-mono">💻 DEVICE FINGERPRINT</h3>
            <div className="space-y-2 text-sm text-gray-300 font-mono">
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">📍 LOCATION:</span>
                <span className="text-green-400">{localStorage.getItem("exactLocation") || (data.city && data.country ? `${data.city}, ${data.country}` : "UNKNOWN")}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">🌐 IP ADDR:</span>
                <span className="text-cyan-400">{data.ip_address || "N/A"}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">💻 MAC ADDR:</span>
                <span className="text-cyan-400">{data.mac_address || "N/A"}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">📡 WIFI SSID:</span>
                <span className="text-cyan-400">{data.wifi_ssid || "N/A"}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">🖥️ HOSTNAME:</span>
                <span className="text-cyan-400">{data.hostname || "N/A"}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">💿 OS:</span>
                <span className="text-cyan-400">{data.os || "N/A"}</span>
              </div>
              <div className="flex justify-between border-b border-gray-800 pb-1">
                <span className="text-gray-500">🕐 TIMEZONE:</span>
                <span className="text-cyan-400">{deviceInfo?.timezone}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-500">🔐 LAST LOGIN:</span>
                <span className="text-green-400">{data.last_login ? new Date(data.last_login).toLocaleString() : "N/A"}</span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-black p-6 rounded border-2 border-green-900 shadow-lg shadow-green-900/30">
          <h3 className="text-xl font-bold text-green-400 mb-4 font-mono">🔓 AUTHORIZED RESOURCES</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {data.accessible_resources?.map((r, i) => (
              <div key={i} className="bg-green-950/30 border border-green-800 p-3 rounded text-green-300 text-center font-semibold font-mono text-sm">
                ✓ {r.toUpperCase()}
              </div>
            ))}
          </div>
        </div>

        <div className="bg-black p-6 rounded border-2 border-orange-900 shadow-lg shadow-orange-900/30">
          <h3 className="text-xl font-bold text-orange-400 mb-4 font-mono">📁 FILE ACCESS CONTROL</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {availableFiles.map((file, i) => (
              <div key={i} className={`bg-gradient-to-br ${file.color} p-4 rounded border-2 ${
                file.type === 'critical' ? 'border-red-700' :
                file.type === 'sensitive' ? 'border-orange-700' :
                file.type === 'internal' ? 'border-blue-700' :
                'border-cyan-700'
              } hover:shadow-lg transition`}>
                <div className="text-3xl mb-2">{file.icon}</div>
                <div className="text-white font-semibold mb-1 font-mono text-xs">{file.name}</div>
                <div className={`text-xs mb-3 uppercase font-mono ${
                  file.type === 'critical' ? 'text-red-400' :
                  file.type === 'sensitive' ? 'text-orange-400' :
                  file.type === 'internal' ? 'text-blue-400' :
                  'text-cyan-400'
                }`}>
                  [{file.type}]
                </div>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleFileAccess(file.name, "READ")}
                    className="flex-1 bg-cyan-900 hover:bg-cyan-800 border border-cyan-700 text-cyan-100 px-2 py-1 rounded text-xs transition font-mono"
                  >
                    READ
                  </button>
                  <button
                    onClick={() => handleFileAccess(file.name, "WRITE")}
                    className="flex-1 bg-yellow-900 hover:bg-yellow-800 border border-yellow-700 text-yellow-100 px-2 py-1 rounded text-xs transition font-mono"
                  >
                    WRITE
                  </button>
                  <button
                    onClick={() => handleFileAccess(file.name, "DELETE")}
                    className="flex-1 bg-red-900 hover:bg-red-800 border border-red-700 text-red-100 px-2 py-1 rounded text-xs transition font-mono"
                  >
                    DELETE
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-black p-6 rounded border-2 border-gray-700 shadow-lg">
          <h3 className="text-xl font-bold text-gray-300 mb-4 font-mono">📋 ACCESS LOG [REAL-TIME]</h3>
          <div className="overflow-x-auto">
            {files.length === 0 ? (
              <div className="text-gray-500 text-center py-8 font-mono">[ NO ACTIVITY RECORDED ]</div>
            ) : (
              <table className="w-full text-sm font-mono">
                <thead className="bg-gray-900 border-b-2 border-green-700">
                  <tr>
                    <th className="text-left p-3 text-green-400">FILE NAME</th>
                    <th className="text-left p-3 text-green-400">ACTION</th>
                    <th className="text-left p-3 text-green-400">IP ADDRESS</th>
                    <th className="text-left p-3 text-green-400">TIMESTAMP</th>
                  </tr>
                </thead>
                <tbody>
                  {files.map((f, i) => (
                    <tr key={i} className="border-b border-gray-800 hover:bg-gray-900/50">
                      <td className="p-3 text-gray-300">{f.file_name}</td>
                      <td className="p-3">
                        <span className={`px-3 py-1 rounded text-xs font-bold border ${
                          f.action === "READ" ? "bg-cyan-950 text-cyan-300 border-cyan-700" :
                          f.action === "WRITE" ? "bg-yellow-950 text-yellow-300 border-yellow-700" :
                          "bg-red-950 text-red-300 border-red-700"
                        }`}>
                          {f.action}
                        </span>
                      </td>
                      <td className="p-3 text-cyan-400">{f.ip_address}</td>
                      <td className="p-3 text-gray-400">{new Date(f.access_time).toLocaleString('en-US', { 
                        year: 'numeric', 
                        month: 'numeric', 
                        day: 'numeric', 
                        hour: '2-digit', 
                        minute: '2-digit', 
                        second: '2-digit',
                        hour12: true 
                      })}</td>
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
