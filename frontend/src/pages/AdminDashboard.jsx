import { useEffect, useState } from "react";
import { getAdminData, getFileAccessLogs, getAuditChain, getPendingUsers, approveUser, revokeAccess, getUserSessions } from "../api/api";
import Logo from "../components/Logo";

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
  const [realtimeStats, setRealtimeStats] = useState({ active_now: 0, total_users: 0 });

  useEffect(() => {
    loadAllData();
    const interval = setInterval(loadAllData, 2000);
    return () => clearInterval(interval);
  }, []);

  const loadAllData = async () => {
    try {
      const [usersRes, filesRes, auditRes, pendingRes, statsRes] = await Promise.all([
        getAdminData().catch(() => ({ users: [] })),
        getFileAccessLogs().catch(() => ({ file_logs: [] })),
        getAuditChain().catch(() => ({ blockchain: [] })),
        getPendingUsers().catch(() => ({ pending_users: [] })),
        fetch("http://localhost:8000/realtime/stats").then(r => r.json()).catch(() => ({ active_now: 0, total_users: 0 }))
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
      setRealtimeStats(statsRes);
    } catch (err) {
      console.error("Admin dashboard error:", err);
    }
  };

  const handleShowDetails = async (user) => {
    setSelectedUser(user);
    try {
      const history = await getUserSessions(user.username || user.user);
      setSessionHistory(history);
    } catch (err) {
      setSessionHistory({ sessions: [], file_activity: [], network_activity: [] });
    }
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

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6">
      <div className="max-w-[1800px] mx-auto space-y-6">
        
        {/* Header */}
        <div className="bg-gradient-to-r from-blue-900/30 via-gray-800 to-purple-900/30 rounded-2xl p-6 border border-blue-500/30 shadow-2xl">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <Logo size="md" />
              <div>
                <h1 className="text-3xl font-bold text-white mb-1">Security Operations Center</h1>
                <p className="text-blue-300 text-sm">Real-Time Threat Intelligence & Monitoring</p>
                <p className="text-green-400 text-xs mt-1 flex items-center gap-2">
                  <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                  Live - Auto-refresh every 2s
                </p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-400 mb-1">System Status</div>
              <div className="text-2xl font-bold text-green-400 flex items-center gap-2">
                <span className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></span>
                OPERATIONAL
              </div>
              <div className="text-xs text-gray-400 mt-1">{new Date().toLocaleString()}</div>
            </div>
          </div>
        </div>

        {/* Real-time Stats Bar */}
        <div className="grid grid-cols-6 gap-4">
          <div className="bg-gradient-to-br from-green-900/40 to-green-800/40 rounded-xl p-6 border border-green-500/30 shadow-lg">
            <div className="text-green-300 text-xs font-semibold mb-2">TOTAL ASSETS</div>
            <div className="text-4xl font-bold text-white mb-1">{stats.total}</div>
            <div className="text-green-400 text-xs">Monitored Users</div>
          </div>
          <div className="bg-gradient-to-br from-red-900/40 to-red-800/40 rounded-xl p-6 border border-red-500/30 shadow-lg">
            <div className="text-red-300 text-xs font-semibold mb-2">CRITICAL</div>
            <div className="text-4xl font-bold text-white mb-1">{stats.critical}</div>
            <div className="text-red-400 text-xs">Immediate Action</div>
          </div>
          <div className="bg-gradient-to-br from-orange-900/40 to-orange-800/40 rounded-xl p-6 border border-orange-500/30 shadow-lg">
            <div className="text-orange-300 text-xs font-semibold mb-2">HIGH RISK</div>
            <div className="text-4xl font-bold text-white mb-1">{stats.high}</div>
            <div className="text-orange-400 text-xs">Review Required</div>
          </div>
          <div className="bg-gradient-to-br from-yellow-900/40 to-yellow-800/40 rounded-xl p-6 border border-yellow-500/30 shadow-lg">
            <div className="text-yellow-300 text-xs font-semibold mb-2">MEDIUM</div>
            <div className="text-4xl font-bold text-white mb-1">{stats.medium}</div>
            <div className="text-yellow-400 text-xs">Monitor Closely</div>
          </div>
          <div className="bg-gradient-to-br from-blue-900/40 to-blue-800/40 rounded-xl p-6 border border-blue-500/30 shadow-lg">
            <div className="text-blue-300 text-xs font-semibold mb-2">LOW RISK</div>
            <div className="text-4xl font-bold text-white mb-1">{stats.low}</div>
            <div className="text-blue-400 text-xs">Secure Status</div>
          </div>
          <div className="bg-gradient-to-br from-purple-900/40 to-purple-800/40 rounded-xl p-6 border border-purple-500/30 shadow-lg">
            <div className="text-purple-300 text-xs font-semibold mb-2">ACTIVE NOW</div>
            <div className="text-4xl font-bold text-white mb-1">{realtimeStats.active_now}</div>
            <div className="text-purple-400 text-xs">Live Sessions</div>
          </div>
        </div>

        {/* Filter Tabs */}
        <div className="flex gap-3">
          {[{k:"all",l:"ALL USERS"},{k:"critical",l:"CRITICAL"},{k:"high",l:"HIGH"},{k:"medium",l:"MEDIUM"},{k:"low",l:"LOW"}].map(f => (
            <button key={f.k} onClick={() => setFilter(f.k)} className={`px-6 py-3 rounded-lg font-semibold text-sm transition ${filter === f.k ? "bg-blue-600 text-white shadow-lg" : "bg-gray-800 text-gray-400 hover:bg-gray-700"}`}>
              {f.l}
            </button>
          ))}
        </div>

        {/* User Table */}
        <div className="bg-gray-800/50 rounded-2xl border border-gray-700/50 overflow-hidden shadow-2xl">
          <div className="bg-gradient-to-r from-blue-900/50 to-purple-900/50 p-4 border-b border-gray-700/50">
            <h2 className="text-xl font-bold text-white">User Risk Analysis ({filteredData.length})</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-900/50 border-b border-gray-700">
                <tr>
                  <th className="p-4 text-left text-blue-300 font-semibold">USER</th>
                  <th className="p-4 text-center text-blue-300 font-semibold">RISK</th>
                  <th className="p-4 text-center text-blue-300 font-semibold">LEVEL</th>
                  <th className="p-4 text-center text-blue-300 font-semibold">DECISION</th>
                  <th className="p-4 text-left text-blue-300 font-semibold">LOCATION</th>
                  <th className="p-4 text-left text-blue-300 font-semibold">THREATS</th>
                  <th className="p-4 text-center text-blue-300 font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.length === 0 ? (
                  <tr><td colSpan="7" className="p-8 text-center text-gray-500">No users found</td></tr>
                ) : (
                  filteredData.map((u, i) => (
                    <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-700/30 transition">
                      <td className="p-4">
                        <div className="text-white font-semibold">{String(u?.username || u?.user || 'UNKNOWN')}</div>
                        <div className="text-xs text-gray-400">{u?.login_count || 0} logins</div>
                      </td>
                      <td className="p-4 text-center">
                        <div className={`text-3xl font-bold ${(u?.risk_score||0)>=70?"text-red-400":(u?.risk_score||0)>=50?"text-orange-400":"text-green-400"}`}>
                          {u?.risk_score || 0}
                        </div>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${(u?.risk_level||'LOW')==="CRITICAL"?"bg-red-500/20 text-red-300":(u?.risk_level||'LOW')==="HIGH"?"bg-orange-500/20 text-orange-300":(u?.risk_level||'LOW')==="MEDIUM"?"bg-yellow-500/20 text-yellow-300":"bg-green-500/20 text-green-300"}`}>
                          {u?.risk_level || 'LOW'}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-semibold ${(u?.decision||'ALLOW')==="ALLOW"?"bg-green-500/20 text-green-300":(u?.decision||'ALLOW')==="RESTRICT"?"bg-yellow-500/20 text-yellow-300":"bg-red-500/20 text-red-300"}`}>
                          {u?.decision || 'ALLOW'}
                        </span>
                      </td>
                      <td className="p-4 text-xs text-gray-300">
                        {u?.city && u.city !== 'Unknown' && <div>📍 {u.city}, {u.country}</div>}
                        {u?.ip_address && u.ip_address !== 'N/A' && <div>🌐 {u.ip_address}</div>}
                        <button onClick={() => handleShowDetails(u)} className="mt-2 px-3 py-1 bg-blue-600 hover:bg-blue-500 text-white rounded text-xs font-semibold transition">
                          VIEW DETAILS
                        </button>
                      </td>
                      <td className="p-4 text-xs">
                        {(!u?.signals || u.signals.length === 0) ? (
                          <span className="text-green-400 font-semibold">✓ CLEAN</span>
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
                          <button onClick={() => handleRevoke(u.username || u.user)} className="px-3 py-1.5 bg-red-600 hover:bg-red-500 text-white rounded-lg text-xs font-semibold transition">
                            REVOKE
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

        {/* File Access & Audit */}
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-gray-800/50 rounded-2xl border border-gray-700/50 overflow-hidden shadow-xl">
            <div className="bg-gradient-to-r from-orange-900/50 to-red-900/50 p-4 border-b border-gray-700/50">
              <h2 className="text-lg font-bold text-white">📁 File Access Logs</h2>
            </div>
            <div className="overflow-y-auto max-h-96 p-4 space-y-2">
              {fileLogs.length === 0 ? (
                <div className="text-center text-gray-500 py-8">No logs available</div>
              ) : (
                fileLogs.slice(0, 20).map((f, i) => (
                  <div key={i} className="bg-gray-900/30 p-3 rounded-lg border border-gray-700/50">
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-blue-300 font-semibold text-sm">{f?.user_id || 'Unknown'}</span>
                      <span className={`px-2 py-0.5 rounded text-xs font-semibold ${(f?.action||'READ')==="READ"?"bg-cyan-500/20 text-cyan-300":(f?.action||'READ')==="WRITE"?"bg-yellow-500/20 text-yellow-300":"bg-red-500/20 text-red-300"}`}>
                        {f?.action || 'READ'}
                      </span>
                    </div>
                    <div className="text-xs text-gray-400">{f?.file_name || 'N/A'}</div>
                    <div className="text-xs text-gray-500 mt-1">{f?.access_time ? new Date(f.access_time).toLocaleString() : 'N/A'}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-gray-800/50 rounded-2xl border border-gray-700/50 overflow-hidden shadow-xl">
            <div className="bg-gradient-to-r from-green-900/50 to-teal-900/50 p-4 border-b border-gray-700/50">
              <h2 className="text-lg font-bold text-white">⛓️ Blockchain Audit</h2>
            </div>
            <div className="overflow-y-auto max-h-96 p-4 space-y-2">
              {auditChain.length === 0 ? (
                <div className="text-center text-gray-500 py-8">No audit records</div>
              ) : (
                auditChain.slice(0, 10).map((block, i) => (
                  <div key={i} className="bg-gray-900/30 p-3 rounded-lg border border-gray-700/50">
                    <div className="flex justify-between items-start mb-1">
                      <span className="text-green-400 font-semibold text-sm">BLOCK #{block?.block_index || i}</span>
                      <span className="text-xs text-gray-500">{block?.timestamp || 'N/A'}</span>
                    </div>
                    {block?.current_hash && <div className="text-xs text-gray-500">{String(block.current_hash).substring(0, 40)}...</div>}
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Session Details Modal */}
      {selectedUser && sessionHistory && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur flex items-center justify-center z-50 p-4" onClick={() => { setSelectedUser(null); setSessionHistory(null); }}>
          <div className="bg-gray-800 rounded-2xl border border-blue-500/30 p-6 max-w-6xl w-full max-h-[90vh] overflow-y-auto shadow-2xl" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-3xl font-bold text-white">Session History</h2>
                <p className="text-gray-400 text-sm mt-1">User: {selectedUser.username || selectedUser.user}</p>
              </div>
              <button onClick={() => { setSelectedUser(null); setSessionHistory(null); }} className="text-red-400 hover:text-red-300 text-3xl font-bold">×</button>
            </div>

            <div className="space-y-4">
              {sessionHistory.sessions && sessionHistory.sessions.length > 0 ? (
                sessionHistory.sessions.map((session, i) => (
                  <div key={i} className="bg-gray-900/50 rounded-lg border border-gray-700/50 p-4">
                    <div className="grid grid-cols-3 gap-4 mb-4">
                      <div>
                        <div className="text-xs text-gray-500 mb-1">SESSION #{i + 1}</div>
                        <div className="text-blue-300 font-semibold text-sm">{new Date(session.login_time).toLocaleString()}</div>
                        <div className="text-xs text-gray-400 mt-2">📍 {session.city}, {session.country}</div>
                        <div className="text-xs text-gray-400">🌐 {session.ip_address}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 mb-1">DEVICE</div>
                        <div className="text-xs text-gray-400">ID: {session.device_id || 'N/A'}</div>
                        <div className="text-xs text-gray-400">MAC: {session.mac_address || 'N/A'}</div>
                        <div className="text-xs text-gray-400">OS: {session.os || 'N/A'}</div>
                      </div>
                      <div>
                        <div className="text-xs text-gray-500 mb-1">STATUS</div>
                        <div className={`text-sm font-semibold ${session.is_active ? 'text-green-400' : 'text-gray-400'}`}>
                          {session.is_active ? '● ACTIVE' : '○ ENDED'}
                        </div>
                      </div>
                    </div>
                    {session.file_activities && session.file_activities.length > 0 && (
                      <div className="bg-black/30 rounded p-3 mt-3">
                        <div className="text-xs text-orange-400 font-semibold mb-2">FILE ACTIVITIES ({session.file_activities.length})</div>
                        <div className="space-y-1">
                          {session.file_activities.slice(0, 5).map((file, j) => (
                            <div key={j} className="text-xs text-gray-400">{file.file_name} - {file.action}</div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))
              ) : (
                <div className="text-center text-gray-500 py-8">No session history available</div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
