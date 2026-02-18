import { useEffect, useState } from "react";
import { getAdminData, getFileAccessLogs, getAuditChain, getPendingUsers, approveUser, revokeAccess, getUserSessions } from "../api/api";
import { Chart as ChartJS, ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Filler } from "chart.js";
import { Doughnut, Bar, Line } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend, CategoryScale, LinearScale, BarElement, LineElement, PointElement, Filler);

export default function AdminDashboard() {
  const [data, setData] = useState([]);
  const [fileLogs, setFileLogs] = useState([]);
  const [auditChain, setAuditChain] = useState([]);
  const [pendingUsers, setPendingUsers] = useState([]);
  const [stats, setStats] = useState({ critical: 0, high: 0, medium: 0, low: 0, total: 0 });
  const [filter, setFilter] = useState("all");
  const [adminUser] = useState(localStorage.getItem("username") || "admin");
  const [selectedUser, setSelectedUser] = useState(null);
  const [sessionHistory, setSessionHistory] = useState(null);
  const [loadingHistory, setLoadingHistory] = useState(false);

  useEffect(() => {
    loadAllData();
    const interval = setInterval(loadAllData, 3000); // Real-time: refresh every 3 seconds
    return () => clearInterval(interval);
  }, []);

  const loadAllData = async () => {
    try {
      const [usersRes, filesRes, auditRes, pendingRes] = await Promise.all([
        getAdminData().catch(() => ({ users: [] })),
        getFileAccessLogs().catch(() => ({ file_logs: [] })),
        getAuditChain().catch(() => ({ blockchain: [] })),
        getPendingUsers().catch(() => ({ pending_users: [] }))
      ]);
      
      const users = usersRes.users || [];
      if (users.length > 0) {
        setData(users);
        const counts = { critical: 0, high: 0, medium: 0, low: 0, total: users.length };
        users.forEach(u => {
          const level = (u?.risk_level || 'LOW').toLowerCase();
          if (counts[level] !== undefined) counts[level]++;
        });
        setStats(counts);
      }
      
      setFileLogs(filesRes.file_logs || []);
      setAuditChain(auditRes.blockchain || []);
      setPendingUsers(pendingRes.pending_users || []);
    } catch (err) {
      console.error("Admin dashboard error:", err);
    }
  };

  const handleApprove = async (username, action) => {
    try {
      const result = await approveUser(username, adminUser, action);
      if (result.status === "SUCCESS") {
        alert(`User ${action}d successfully`);
        loadAllData();
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const handleShowDetails = async (user) => {
    setSelectedUser(user);
    setLoadingHistory(true);
    try {
      const history = await getUserSessions(user.username || user.user);
      setSessionHistory(history);
    } catch (err) {
      console.error("Failed to load session history:", err);
      setSessionHistory({ sessions: [], file_activity: [], network_activity: [] });
    } finally {
      setLoadingHistory(false);
    }
  };

  const formatDuration = (seconds) => {
    if (!seconds) return "0s";
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = seconds % 60;
    return h > 0 ? `${h}h ${m}m` : m > 0 ? `${m}m ${s}s` : `${s}s`;
  };

  const handleRevoke = async (username) => {
    if (!window.confirm(`Revoke access for ${username}?`)) return;
    try {
      const result = await revokeAccess(username, adminUser);
      if (result.status === "SUCCESS") {
        alert("Access revoked successfully");
        loadAllData();
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const filteredData = filter === "all" ? data : data.filter(u => (u?.risk_level || 'LOW').toLowerCase() === filter);

  const doughnutData = {
    labels: ["Critical", "High", "Medium", "Low"],
    datasets: [{
      data: [stats.critical, stats.high, stats.medium, stats.low],
      backgroundColor: ["#dc2626", "#ea580c", "#ca8a04", "#16a34a"],
      borderWidth: 3,
      borderColor: "#000",
      cutout: "65%"
    }]
  };

  const barData = {
    labels: data.slice(0, 8).map(u => String(u?.username || u?.user || 'UNKNOWN').substring(0, 8)),
    datasets: [{
      label: "Risk Score",
      data: data.slice(0, 8).map(u => u?.risk_score || 0),
      backgroundColor: data.slice(0, 8).map(u => 
        (u?.risk_score || 0) >= 70 ? "#dc2626" : (u?.risk_score || 0) >= 50 ? "#ea580c" : "#16a34a"
      ),
      borderRadius: 4,
      borderWidth: 2,
      borderColor: "#22c55e"
    }]
  };

  // Calculate real hourly login activity from user data
  const hourlyLogins = Array(24).fill(0);
  data.forEach(u => {
    if (u?.last_login) {
      const hour = new Date(u.last_login).getHours();
      hourlyLogins[hour]++;
    }
  });

  const currentHour = new Date().getHours();
  const last12Hours = Array.from({length: 12}, (_, i) => {
    const hour = (currentHour - 11 + i + 24) % 24;
    return { hour, count: hourlyLogins[hour] };
  });

  const lineData = {
    labels: last12Hours.map(h => h.hour + ':00'),
    datasets: [{
      label: "Logins",
      data: last12Hours.map(h => h.count),
      borderColor: "#22c55e",
      backgroundColor: "rgba(34, 197, 94, 0.1)",
      tension: 0.3,
      fill: true,
      pointRadius: 3,
      pointBackgroundColor: "#22c55e",
      pointBorderColor: "#000",
      pointBorderWidth: 2,
      borderWidth: 3
    }]
  };

  return (
    <div className="min-h-screen bg-black p-6">
      {/* Cyber grid background */}
      <div className="fixed inset-0 opacity-5" style={{
        backgroundImage: 'linear-gradient(#22c55e 1px, transparent 1px), linear-gradient(90deg, #22c55e 1px, transparent 1px)',
        backgroundSize: '50px 50px'
      }}></div>
      
      <div className="max-w-[1600px] mx-auto space-y-6 relative z-10">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-red-950/50 via-black to-red-950/50 rounded-xl p-6 border-2 border-red-900/50 shadow-2xl shadow-red-900/30">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-red-500 mb-1 font-mono tracking-wider">🛡️ SECURITY OPERATIONS CENTER</h1>
              <p className="text-red-400/80 text-sm font-mono">[ THREAT INTELLIGENCE • REAL-TIME MONITORING • INCIDENT RESPONSE ]</p>
              <p className="text-green-400 text-xs font-mono mt-1 animate-pulse">● LIVE - Auto-refresh every 3s</p>
            </div>
            <div className="text-right">
              <div className="text-xs text-red-500/60 mb-1 font-mono">SYSTEM STATUS</div>
              <div className="text-lg font-bold text-green-400 font-mono animate-pulse">● ACTIVE</div>
              <div className="text-xs text-gray-500 font-mono">{new Date().toLocaleTimeString()}</div>
            </div>
          </div>
        </div>

        {/* Pending Approvals */}
        {pendingUsers.length > 0 && (
          <div className="bg-yellow-950/30 rounded-xl p-4 border-2 border-yellow-600/50 shadow-lg shadow-yellow-900/20">
            <h2 className="text-lg font-bold text-yellow-400 mb-3 font-mono">⏳ PENDING APPROVALS ({pendingUsers.length})</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {pendingUsers.map((u, i) => (
                <div key={i} className="bg-black/50 p-4 rounded-lg border-2 border-yellow-700/50">
                  <div className="text-cyan-400 font-bold mb-1 font-mono">{u.username}</div>
                  <div className="text-xs text-gray-500 mb-3 font-mono">{new Date(u.created_at).toLocaleString()}</div>
                  <div className="flex gap-2">
                    <button onClick={() => handleApprove(u.username, "approve")} className="flex-1 px-3 py-1.5 bg-green-900 hover:bg-green-800 text-green-100 rounded-lg text-sm font-bold font-mono border-2 border-green-700 transition">✓ APPROVE</button>
                    <button onClick={() => handleApprove(u.username, "deny")} className="flex-1 px-3 py-1.5 bg-red-900 hover:bg-red-800 text-red-100 rounded-lg text-sm font-bold font-mono border-2 border-red-700 transition">✗ DENY</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Stats Cards */}
        <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-black/80 rounded-xl p-6 border-2 border-green-900/50 shadow-lg shadow-green-900/30 backdrop-blur">
            <div className="text-green-500 text-xs font-bold mb-2 font-mono">[TOTAL ASSETS]</div>
            <div className="text-5xl font-bold text-green-400 mb-1 font-mono">{stats.total}</div>
            <div className="text-green-700 text-xs font-mono">MONITORED</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-red-900/50 shadow-lg shadow-red-900/40 backdrop-blur">
            <div className="text-red-400 text-xs font-bold mb-2 font-mono">[CRITICAL]</div>
            <div className="text-5xl font-bold text-red-500 mb-1 font-mono">{stats.critical}</div>
            <div className="text-red-700 text-xs font-mono">IMMEDIATE</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-orange-900/50 shadow-lg shadow-orange-900/40 backdrop-blur">
            <div className="text-orange-400 text-xs font-bold mb-2 font-mono">[HIGH RISK]</div>
            <div className="text-5xl font-bold text-orange-500 mb-1 font-mono">{stats.high}</div>
            <div className="text-orange-700 text-xs font-mono">REVIEW</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-yellow-900/50 shadow-lg shadow-yellow-900/40 backdrop-blur">
            <div className="text-yellow-400 text-xs font-bold mb-2 font-mono">[MEDIUM]</div>
            <div className="text-5xl font-bold text-yellow-500 mb-1 font-mono">{stats.medium}</div>
            <div className="text-yellow-700 text-xs font-mono">MONITOR</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-green-900/50 shadow-lg shadow-green-900/40 backdrop-blur">
            <div className="text-green-400 text-xs font-bold mb-2 font-mono">[LOW RISK]</div>
            <div className="text-5xl font-bold text-green-500 mb-1 font-mono">{stats.low}</div>
            <div className="text-green-700 text-xs font-mono">SECURE</div>
          </div>
        </div>

        {/* Analytics Charts */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-black/80 rounded-xl p-6 border-2 border-red-900/50 backdrop-blur shadow-lg shadow-red-900/20">
            <h3 className="text-lg font-bold text-red-400 mb-4 font-mono">[THREAT DISTRIBUTION]</h3>
            <div className="relative">
              <Doughnut data={doughnutData} options={{ 
                maintainAspectRatio: true,
                plugins: {
                  legend: { labels: { color: '#9ca3b8', font: { size: 11, family: 'monospace' } } }
                }
              }} />
              <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400 font-mono">{stats.total}</div>
                  <div className="text-xs text-gray-500 font-mono">USERS</div>
                </div>
              </div>
            </div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-cyan-900/50 backdrop-blur shadow-lg shadow-cyan-900/20">
            <h3 className="text-lg font-bold text-cyan-400 mb-4 font-mono">[RISK SCORES]</h3>
            <Bar data={barData} options={{ 
              maintainAspectRatio: true,
              scales: { 
                y: { max: 100, ticks: { color: '#22c55e', font: { family: 'monospace' } }, grid: { color: '#1e293b' }, border: { display: false } },
                x: { ticks: { color: '#22c55e', font: { family: 'monospace' } }, grid: { display: false }, border: { display: false } }
              },
              plugins: { legend: { display: false } }
            }} />
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-green-900/50 backdrop-blur shadow-lg shadow-green-900/20">
            <h3 className="text-lg font-bold text-green-400 mb-4 font-mono">[HOURLY LOGIN ACTIVITY]</h3>
            <Line data={lineData} options={{ 
              maintainAspectRatio: true,
              scales: { 
                y: { ticks: { color: '#22c55e', font: { family: 'monospace' } }, grid: { color: '#1e293b' }, border: { display: false } },
                x: { ticks: { color: '#22c55e', font: { family: 'monospace' } }, grid: { display: false }, border: { display: false } }
              },
              plugins: { legend: { display: false } }
            }} />
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-2 flex-wrap">
          {[{k:"all",l:"ALL USERS"},{k:"critical",l:"CRITICAL"},{k:"high",l:"HIGH"},{k:"medium",l:"MEDIUM"},{k:"low",l:"LOW"}].map(f => (
            <button key={f.k} onClick={() => setFilter(f.k)} className={`px-4 py-2 rounded-lg font-bold text-sm font-mono transition border-2 ${filter === f.k ? "bg-green-900 text-green-100 border-green-500" : "bg-black text-gray-400 border-gray-700 hover:border-green-700"}`}>
              [{f.l}]
            </button>
          ))}
        </div>

        {/* User Table */}
        <div className="bg-black/80 rounded-xl border-2 border-red-900/50 overflow-hidden backdrop-blur shadow-lg shadow-red-900/20">
          <div className="bg-red-950/30 p-4 border-b-2 border-red-700/50">
            <h2 className="text-xl font-bold text-red-400 font-mono">👥 USER RISK ANALYSIS ({filteredData.length})</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm font-mono">
              <thead className="bg-gray-900/50 border-b-2 border-green-700">
                <tr>
                  <th className="p-4 text-left text-green-400 font-bold">USER</th>
                  <th className="p-4 text-center text-green-400 font-bold">RISK</th>
                  <th className="p-4 text-center text-green-400 font-bold">LEVEL</th>
                  <th className="p-4 text-center text-green-400 font-bold">STATUS</th>
                  <th className="p-4 text-center text-green-400 font-bold">DECISION</th>
                  <th className="p-4 text-left text-green-400 font-bold">DEVICE</th>
                  <th className="p-4 text-left text-green-400 font-bold">THREATS</th>
                  <th className="p-4 text-center text-green-400 font-bold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.length === 0 ? (
                  <tr><td colSpan="8" className="p-8 text-center text-gray-500">No users found</td></tr>
                ) : (
                  filteredData.map((u, i) => (
                    <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-900/30 transition">
                      <td className="p-4">
                        <div className="text-cyan-400 font-bold">{String(u?.username || u?.user || 'UNKNOWN')}</div>
                        <div className="text-xs text-gray-500">{u?.login_count || 0} logins</div>
                      </td>
                      <td className="p-4 text-center">
                        <div className={`text-3xl font-bold ${(u?.risk_score||0)>=70?"text-red-500":(u?.risk_score||0)>=50?"text-orange-500":"text-green-500"}`}>
                          {u?.risk_score || 0}
                        </div>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`px-3 py-1 rounded text-xs font-bold border-2 ${(u?.risk_level||'LOW')==="CRITICAL"?"bg-red-950 text-red-300 border-red-700":(u?.risk_level||'LOW')==="HIGH"?"bg-orange-950 text-orange-300 border-orange-700":(u?.risk_level||'LOW')==="MEDIUM"?"bg-yellow-950 text-yellow-300 border-yellow-700":"bg-green-950 text-green-300 border-green-700"}`}>
                          {u?.risk_level || 'LOW'}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`px-3 py-1 rounded text-xs font-bold border-2 ${(u?.status||'active')==="active"?"bg-green-950 text-green-300 border-green-700":"bg-red-950 text-red-300 border-red-700"}`}>
                          {(u?.status || 'active').toUpperCase()}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`px-3 py-1 rounded text-xs font-bold border-2 ${(u?.decision||'ALLOW')==="ALLOW"?"bg-green-950 text-green-300 border-green-700":(u?.decision||'ALLOW')==="RESTRICT"?"bg-yellow-950 text-yellow-300 border-yellow-700":"bg-red-950 text-red-300 border-red-700"}`}>
                          {u?.decision || 'ALLOW'}
                        </span>
                      </td>
                      <td className="p-4 text-xs text-gray-400 space-y-1">
                        {u?.ip_address && u.ip_address !== 'N/A' && <div>🌐 {u.ip_address}</div>}
                        {u?.city && u.city !== 'Unknown' && <div>📍 {u.city}, {u.country}</div>}
                        <button onClick={() => handleShowDetails(u)} className="mt-2 px-3 py-1 bg-cyan-900 hover:bg-cyan-800 text-cyan-100 rounded text-xs font-bold font-mono border-2 border-cyan-700 transition">
                          MORE DETAILS
                        </button>
                      </td>
                      <td className="p-4 text-xs">
                        {(!u?.signals || u.signals.length === 0) ? (
                          <span className="text-green-400 font-bold">✓ CLEAN</span>
                        ) : (
                          <div className="space-y-1">
                            {u.signals.slice(0, 2).map((s, j) => (
                              <div key={j} className="text-red-400">⚠ {String(s).replace(/_/g, " ")}</div>
                            ))}
                            {u.signals.length > 2 && <div className="text-gray-500">+{u.signals.length - 2} more</div>}
                          </div>
                        )}
                      </td>
                      <td className="p-4 text-center">
                        {!['admin', 'bhargav'].includes(u?.username || u?.user) && (u?.status !== 'revoked') && (
                          <button onClick={() => handleRevoke(u.username || u.user)} className="px-3 py-1.5 bg-red-900 hover:bg-red-800 text-red-100 rounded-lg text-xs font-bold font-mono border-2 border-red-700 transition">
                            🚫 REVOKE
                          </button>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* File Access & Blockchain */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-black/80 rounded-xl border-2 border-orange-900/50 overflow-hidden backdrop-blur shadow-lg shadow-orange-900/20">
            <div className="bg-orange-950/30 p-4 border-b-2 border-orange-700/50">
              <h2 className="text-lg font-bold text-orange-400 font-mono">📁 FILE ACCESS LOGS</h2>
            </div>
            <div className="overflow-y-auto max-h-96 p-4 space-y-2">
              {fileLogs.length === 0 ? (
                <div className="text-center text-gray-500 py-8 font-mono">No logs available</div>
              ) : (
                fileLogs.slice(0, 20).map((f, i) => (
                  <div key={i} className="bg-gray-900/30 p-3 rounded-lg border border-gray-700/50">
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-cyan-400 font-bold text-sm font-mono">{f?.user_id || 'Unknown'}</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-bold border ${(f?.action||'READ')==="READ"?"bg-cyan-950 text-cyan-300 border-cyan-700":(f?.action||'READ')==="WRITE"?"bg-yellow-950 text-yellow-300 border-yellow-700":"bg-red-950 text-red-300 border-red-700"}`}>
                        {f?.action || 'READ'}
                      </span>
                    </div>
                    <div className="text-xs text-gray-400 font-mono">{f?.file_name || 'N/A'}</div>
                    <div className="text-xs text-gray-500 mt-1 font-mono">{f?.access_time ? new Date(f.access_time).toLocaleString() : 'N/A'}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-black/80 rounded-xl border-2 border-green-900/50 overflow-hidden backdrop-blur shadow-lg shadow-green-900/20">
            <div className="bg-green-950/30 p-4 border-b-2 border-green-700/50">
              <h2 className="text-lg font-bold text-green-400 font-mono">⛓️ BLOCKCHAIN AUDIT</h2>
            </div>
            <div className="overflow-y-auto max-h-96 p-4 space-y-2">
              {auditChain.length === 0 ? (
                <div className="text-center text-gray-500 py-8 font-mono">No audit records</div>
              ) : (
                auditChain.slice(0, 10).map((block, i) => (
                  <div key={i} className="bg-gray-900/30 p-3 rounded-lg border border-gray-700/50">
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-green-400 font-bold text-sm font-mono">BLOCK #{block?.block_index || i}</span>
                      <span className="text-xs text-gray-500 font-mono">{block?.timestamp || 'N/A'}</span>
                    </div>
                    {block?.current_hash && <div className="text-xs text-gray-500 font-mono">{String(block.current_hash).substring(0, 40)}...</div>}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Session History Modal */}
      {selectedUser && (
        <div className="fixed inset-0 bg-black/90 backdrop-blur flex items-center justify-center z-50 p-4" onClick={() => { setSelectedUser(null); setSessionHistory(null); }}>
          <div className="bg-black/95 rounded-xl border-2 border-cyan-900/50 p-6 max-w-7xl w-full max-h-[90vh] overflow-y-auto shadow-2xl shadow-cyan-900/30" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-3xl font-bold text-cyan-400 font-mono">📊 SESSION HISTORY</h2>
                <p className="text-gray-500 font-mono text-sm mt-1">User: {selectedUser.username || selectedUser.user}</p>
              </div>
              <button onClick={() => { setSelectedUser(null); setSessionHistory(null); }} className="text-red-400 hover:text-red-300 text-3xl font-bold">×</button>
            </div>

            {loadingHistory ? (
              <div className="text-center py-12">
                <div className="text-green-400 text-xl font-mono animate-pulse">⏳ LOADING SESSION DATA...</div>
              </div>
            ) : sessionHistory ? (
              <div className="space-y-6">
                {/* Summary Stats */}
                <div className="bg-gradient-to-r from-green-950/50 to-cyan-950/50 p-4 rounded-lg border-2 border-green-700/50">
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div>
                      <div className="text-xs text-gray-500 font-mono mb-1">ACTIVE SESSIONS</div>
                      <div className="text-2xl text-green-400 font-bold font-mono">{sessionHistory.active_sessions || 0}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 font-mono mb-1">CURRENT DURATION</div>
                      <div className="text-2xl text-cyan-400 font-bold font-mono">{formatDuration(sessionHistory.current_session_duration || 0)}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 font-mono mb-1">TOTAL LOGINS</div>
                      <div className="text-2xl text-yellow-400 font-bold font-mono">{sessionHistory.total_sessions || 0}</div>
                    </div>
                    <div>
                      <div className="text-xs text-gray-500 font-mono mb-1">RISK SCORE</div>
                      <div className={`text-2xl font-bold font-mono ${selectedUser.risk_score >= 70 ? 'text-red-500' : selectedUser.risk_score >= 50 ? 'text-orange-500' : 'text-green-500'}`}>
                        {selectedUser.risk_score || 0}
                      </div>
                    </div>
                  </div>
                </div>

                {/* All Sessions with Activities */}
                <div className="space-y-4">
                  <h3 className="text-2xl font-bold text-purple-400 font-mono">🔐 ALL LOGIN SESSIONS ({sessionHistory.sessions?.length || 0})</h3>
                  {sessionHistory.sessions && sessionHistory.sessions.length > 0 ? (
                    sessionHistory.sessions.map((session, i) => (
                      <div key={i} className="bg-gray-900/50 rounded-lg border-2 border-purple-900/50 p-4">
                        {/* Session Header */}
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4 pb-4 border-b border-gray-700">
                          {/* Time & Location */}
                          <div>
                            <div className="text-xs text-gray-500 font-mono mb-2">⏰ SESSION #{i + 1}</div>
                            <div className="text-cyan-400 font-bold font-mono text-sm">
                              {new Date(session.login_time).toLocaleString()}
                            </div>
                            <div className="text-xs text-gray-500 font-mono mt-2">📍 LOCATION</div>
                            <div className="text-green-400 font-mono text-sm">
                              {session.city}, {session.country}
                            </div>
                            <div className="text-xs text-gray-400 font-mono">
                              🌐 {session.ip_address}
                            </div>
                          </div>

                          {/* Device Info */}
                          <div>
                            <div className="text-xs text-gray-500 font-mono mb-2">💻 DEVICE FINGERPRINT</div>
                            <div className="space-y-1 text-xs">
                              <div className="text-gray-400 font-mono">ID: <span className="text-cyan-400">{session.device_id || 'N/A'}</span></div>
                              <div className="text-gray-400 font-mono">MAC: <span className="text-cyan-400">{session.mac_address || 'N/A'}</span></div>
                              <div className="text-gray-400 font-mono">WiFi: <span className="text-cyan-400">{session.wifi_ssid || 'N/A'}</span></div>
                              <div className="text-gray-400 font-mono">Host: <span className="text-cyan-400">{session.hostname || 'N/A'}</span></div>
                              <div className="text-gray-400 font-mono">OS: <span className="text-cyan-400">{session.os || 'N/A'}</span></div>
                            </div>
                          </div>

                          {/* Session Duration */}
                          <div>
                            <div className="text-xs text-gray-500 font-mono mb-2">⏱️ SESSION INFO</div>
                            <div className="space-y-1 text-xs">
                              <div className="text-gray-400 font-mono">Duration: <span className="text-yellow-400 font-bold">{formatDuration(session.session_duration_seconds || 0)}</span></div>
                              <div className="text-gray-400 font-mono">Status: <span className={session.is_active ? 'text-green-400' : 'text-red-400'}>{session.is_active ? '● ACTIVE' : '○ ENDED'}</span></div>
                              {session.last_activity && (
                                <div className="text-gray-400 font-mono">Last: <span className="text-gray-300">{new Date(session.last_activity).toLocaleTimeString()}</span></div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Activities During This Session */}
                        <div className="bg-black/50 rounded-lg border border-orange-900/50 p-3">
                          <h4 className="text-sm font-bold text-orange-400 font-mono mb-2">📁 FILE ACTIVITIES ({session.file_activities?.length || 0})</h4>
                          <div className="space-y-1 max-h-40 overflow-y-auto">
                            {session.file_activities && session.file_activities.length > 0 ? (
                              session.file_activities.map((file, j) => (
                                <div key={j} className="text-xs">
                                  <div className="flex justify-between items-start">
                                    <span className="text-cyan-400 font-mono truncate flex-1">{file.file_name}</span>
                                    <span className={`px-1 py-0.5 rounded font-bold ml-2 ${file.action === 'DELETE' ? 'bg-red-950 text-red-300' : file.action === 'WRITE' ? 'bg-yellow-950 text-yellow-300' : 'bg-cyan-950 text-cyan-300'}`}>
                                      {file.action}
                                    </span>
                                  </div>
                                  <div className="text-gray-500 font-mono">{new Date(file.access_time).toLocaleTimeString()}</div>
                                </div>
                              ))
                            ) : (
                              <div className="text-gray-500 text-xs font-mono">No file activity</div>
                            )}
                          </div>
                        </div>
                      </div>
                    ))
                  ) : (
                    <div className="text-center text-gray-500 py-8 font-mono">No session history available</div>
                  )}
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-500 py-12 font-mono">Failed to load session history</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
