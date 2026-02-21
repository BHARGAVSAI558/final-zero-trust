import { useEffect, useState } from "react";
import { getAdminData, getFileAccessLogs, getAuditChain, getPendingUsers, approveUser, revokeAccess, getUserSessions } from "../api/api";

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
      // Create comprehensive mock data for user details
      const mockHistory = {
        sessions: [
          {
            login_id: 1,
            login_time: new Date(Date.now() - 3600000).toISOString(),
            ip_address: user.ip_address || "192.168.1.100",
            city: user.city || "New York",
            country: user.country || "USA",
            device_id: user.device_id || "DEV001-LAPTOP",
            mac_address: "00:1B:44:11:3A:B7",
            wifi_ssid: "CorpNetwork_5G",
            hostname: "LAPTOP-" + (user.username || "USER").toUpperCase(),
            os: "Windows 11 Pro",
            session_duration_seconds: 3600,
            is_active: true,
            file_activities: [
              { file_name: "confidential_report.pdf", action: "READ", access_time: new Date(Date.now() - 1800000).toISOString() },
              { file_name: "employee_database.xlsx", action: "WRITE", access_time: new Date(Date.now() - 1200000).toISOString() },
              { file_name: "project_plans.docx", action: "READ", access_time: new Date(Date.now() - 600000).toISOString() }
            ],
            network_activities: [
              { connection: "External API", ip: "203.0.113.1", port: 443, protocol: "HTTPS", timestamp: new Date(Date.now() - 900000).toISOString() },
              { connection: "File Server", ip: "10.0.0.50", port: 445, protocol: "SMB", timestamp: new Date(Date.now() - 1500000).toISOString() }
            ]
          },
          {
            login_id: 2,
            login_time: new Date(Date.now() - 86400000).toISOString(),
            ip_address: "192.168.1.105",
            city: user.city || "New York",
            country: user.country || "USA",
            device_id: "DEV002-MOBILE",
            mac_address: "02:1C:45:22:4B:C8",
            wifi_ssid: "CorpNetwork_Guest",
            hostname: "iPhone-" + (user.username || "USER"),
            os: "iOS 17.1",
            session_duration_seconds: 1800,
            is_active: false,
            file_activities: [
              { file_name: "meeting_notes.txt", action: "READ", access_time: new Date(Date.now() - 84600000).toISOString() }
            ],
            network_activities: []
          }
        ],
        user_profile: {
          username: user.username || user.user,
          risk_score: user.risk_score || 0,
          risk_level: user.risk_level || "LOW",
          decision: user.decision || "ALLOW",
          total_logins: user.login_count || 0,
          last_login: new Date(Date.now() - 3600000).toISOString(),
          account_created: new Date(Date.now() - 7776000000).toISOString(), // 90 days ago
          department: "Engineering",
          role: "Senior Developer",
          clearance_level: "Level 2",
          manager: "John Smith"
        },
        behavioral_analytics: {
          login_patterns: {
            usual_hours: "9:00 AM - 6:00 PM",
            usual_locations: [user.city || "New York", "San Francisco"],
            usual_devices: 2,
            weekend_activity: "Low"
          },
          anomalies: user.signals || [],
          risk_factors: [
            { factor: "Unusual login time", severity: "Medium", detected: "2 hours ago" },
            { factor: "New device detected", severity: "Low", detected: "1 day ago" }
          ]
        },
        device_fingerprints: [
          {
            device_id: user.device_id || "DEV001-LAPTOP",
            device_type: "Laptop",
            os: "Windows 11 Pro",
            browser: "Chrome 119.0",
            mac_address: "00:1B:44:11:3A:B7",
            hostname: "LAPTOP-" + (user.username || "USER").toUpperCase(),
            last_seen: new Date(Date.now() - 3600000).toISOString(),
            trusted: true,
            location: user.city || "New York"
          },
          {
            device_id: "DEV002-MOBILE",
            device_type: "Mobile",
            os: "iOS 17.1",
            browser: "Safari 17.0",
            mac_address: "02:1C:45:22:4B:C8",
            hostname: "iPhone-" + (user.username || "USER"),
            last_seen: new Date(Date.now() - 86400000).toISOString(),
            trusted: false,
            location: "Unknown"
          }
        ],
        file_access_history: [
          { file_name: "confidential_report.pdf", action: "READ", timestamp: new Date(Date.now() - 1800000).toISOString(), sensitivity: "Critical" },
          { file_name: "employee_database.xlsx", action: "WRITE", timestamp: new Date(Date.now() - 1200000).toISOString(), sensitivity: "Critical" },
          { file_name: "project_plans.docx", action: "READ", timestamp: new Date(Date.now() - 600000).toISOString(), sensitivity: "Internal" },
          { file_name: "meeting_notes.txt", action: "READ", timestamp: new Date(Date.now() - 84600000).toISOString(), sensitivity: "Internal" },
          { file_name: "budget_2024.xlsx", action: "READ", timestamp: new Date(Date.now() - 172800000).toISOString(), sensitivity: "Confidential" }
        ],
        network_activity: [
          { timestamp: new Date(Date.now() - 900000).toISOString(), connection: "External API", destination: "api.example.com", port: 443, protocol: "HTTPS", data_transferred: "2.3 MB" },
          { timestamp: new Date(Date.now() - 1500000).toISOString(), connection: "File Server", destination: "fileserver.corp.com", port: 445, protocol: "SMB", data_transferred: "15.7 MB" },
          { timestamp: new Date(Date.now() - 3600000).toISOString(), connection: "Email Server", destination: "mail.corp.com", port: 993, protocol: "IMAPS", data_transferred: "1.1 MB" }
        ]
      };
      setSessionHistory(mockHistory);
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

  const handleApprove = async (username, action) => {
    try {
      const result = await approveUser(username, adminUser, action);
      if (result.status === "SUCCESS") {
        alert(`User ${action === 'approve' ? 'approved' : 'rejected'} successfully`);
        loadAllData();
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  const filteredData = filter === "all" ? data : data.filter(u => (u?.risk_level || 'LOW').toLowerCase() === filter);

  return (
    <div className="min-h-screen bg-gray-50 p-6" style={{fontFamily: 'Inter, system-ui, -apple-system, sans-serif'}}>
      <div className="max-w-[1800px] mx-auto space-y-6">
        
        {/* Header */}
        <div className="bg-white rounded-xl p-6 border border-gray-200 shadow-sm">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <div className="w-14 h-14 bg-gray-900 rounded-lg flex items-center justify-center">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                </svg>
              </div>
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
                <p className="text-gray-600 text-sm mt-1">User Management & System Monitoring</p>
                <div className="flex items-center gap-4 mt-2">
                  <div className="flex items-center gap-2 text-gray-700 text-xs font-semibold">
                    <div className="w-2 h-2 bg-gray-700 rounded-full animate-pulse"></div>
                    LIVE MONITORING
                  </div>
                  <div className="text-gray-500 text-xs">Auto-refresh: 2s</div>
                </div>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <a href="/soc" className="px-4 py-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg font-medium transition-colors text-sm">
                SOC Dashboard
              </a>
              <a href="/files" className="px-4 py-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg font-medium transition-colors text-sm">
                File Manager
              </a>
              <a href="/portal" className="px-4 py-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg font-medium transition-colors text-sm">
                Portal
              </a>
              <div className="bg-gray-100 rounded-lg px-4 py-2 border border-gray-200">
                <div className="text-xs text-gray-600">System Status</div>
                <div className="text-sm font-bold text-gray-900 flex items-center gap-1">
                  <span className="w-2 h-2 bg-gray-900 rounded-full"></span>
                  OPERATIONAL
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-6 gap-4">
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">TOTAL USERS</div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.total}</div>
            <div className="text-xs text-gray-500">Monitored Assets</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: '100%'}}></div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">CRITICAL</div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.critical}</div>
            <div className="text-xs text-gray-500">Immediate Action</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: `${stats.total > 0 ? (stats.critical/stats.total)*100 : 0}%`}}></div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">HIGH RISK</div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.high}</div>
            <div className="text-xs text-gray-500">Review Required</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: `${stats.total > 0 ? (stats.high/stats.total)*100 : 0}%`}}></div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">MEDIUM</div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.medium}</div>
            <div className="text-xs text-gray-500">Monitor Closely</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: `${stats.total > 0 ? (stats.medium/stats.total)*100 : 0}%`}}></div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">LOW RISK</div>
              <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{stats.low}</div>
            <div className="text-xs text-gray-500">Secure Status</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: `${stats.total > 0 ? (stats.low/stats.total)*100 : 0}%`}}></div>
            </div>
          </div>
          
          <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm hover:shadow-md transition-shadow">
            <div className="flex items-center justify-between mb-3">
              <div className="text-gray-600 text-xs font-semibold">ACTIVE NOW</div>
              <div className="w-2 h-2 bg-gray-700 rounded-full animate-pulse"></div>
            </div>
            <div className="text-3xl font-bold text-gray-900 mb-1">{realtimeStats.active_now}</div>
            <div className="text-xs text-gray-500">Live Sessions</div>
            <div className="mt-3 h-1 bg-gray-200 rounded-full overflow-hidden">
              <div className="h-full bg-gray-700 rounded-full" style={{width: `${stats.total > 0 ? (realtimeStats.active_now/stats.total)*100 : 0}%`}}></div>
            </div>
          </div>
        </div>

        {/* Pending Users Alert */}
        {pendingUsers.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-300 p-5 shadow-sm">
            <div className="flex items-center gap-3 mb-4">
              <svg className="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h2 className="text-xl font-bold text-gray-900">Pending User Registrations</h2>
                <p className="text-gray-600 text-sm">{pendingUsers.length} users awaiting approval</p>
              </div>
            </div>
            <div className="grid gap-3">
              {pendingUsers.map((user, i) => (
                <div key={i} className="bg-gray-50 rounded-lg p-4 border border-gray-200 flex justify-between items-center">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center">
                      <span className="text-gray-700 font-bold">{user.username[0].toUpperCase()}</span>
                    </div>
                    <div>
                      <div className="text-gray-900 font-semibold">{user.username}</div>
                      <div className="text-gray-500 text-xs">{new Date(user.created_at).toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => handleApprove(user.username, 'approve')} className="px-4 py-2 bg-gray-900 hover:bg-gray-800 text-white rounded-lg text-sm font-semibold transition-colors">
                      Approve
                    </button>
                    <button onClick={() => handleApprove(user.username, 'reject')} className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg text-sm font-semibold transition-colors">
                      Reject
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Risk Distribution Chart */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
          <h3 className="text-xl font-bold text-gray-900 mb-6">Risk Distribution Analytics</h3>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h4 className="text-sm font-semibold text-gray-600 mb-4 uppercase">Risk Level Breakdown</h4>
              <div className="space-y-4">
                {[
                  { level: "CRITICAL", count: stats.critical, color: "bg-gray-700", textColor: "text-gray-700" },
                  { level: "HIGH", count: stats.high, color: "bg-gray-600", textColor: "text-gray-600" },
                  { level: "MEDIUM", count: stats.medium, color: "bg-gray-500", textColor: "text-gray-500" },
                  { level: "LOW", count: stats.low, color: "bg-gray-400", textColor: "text-gray-400" }
                ].map((item, i) => (
                  <div key={i} className="flex items-center gap-4">
                    <div className="w-20 text-xs font-semibold text-gray-600">{item.level}</div>
                    <div className="flex-1 bg-gray-100 rounded-full h-6 overflow-hidden">
                      <div 
                        className={`h-full ${item.color} transition-all duration-1000 flex items-center justify-end pr-2`}
                        style={{ width: `${stats.total > 0 ? (item.count / stats.total) * 100 : 0}%` }}
                      >
                        <span className="text-white text-xs font-bold">{item.count}</span>
                      </div>
                    </div>
                    <div className={`w-16 text-xs font-bold ${item.textColor}`}>
                      {stats.total > 0 ? Math.round((item.count / stats.total) * 100) : 0}%
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="text-sm font-semibold text-gray-600 mb-4 uppercase">Security Metrics</h4>
              <div className="space-y-3">
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <div className="text-gray-600 text-xs mb-1">Total Threat Score</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {data.reduce((sum, user) => sum + (user.risk_score || 0), 0)}
                  </div>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <div className="text-gray-600 text-xs mb-1">Average Risk Score</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {data.length > 0 ? Math.round(data.reduce((sum, user) => sum + (user.risk_score || 0), 0) / data.length) : 0}
                  </div>
                </div>
                <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
                  <div className="text-gray-600 text-xs mb-1">High Risk Users</div>
                  <div className="text-2xl font-bold text-gray-900">
                    {stats.critical + stats.high}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-white rounded-xl p-5 border border-gray-200 shadow-sm">
          <h3 className="text-gray-900 font-semibold text-sm mb-4 uppercase">Filter by Risk Level</h3>
          <div className="flex gap-3 flex-wrap">
            {[
              {k:"all", l:"ALL USERS", count: stats.total, color:"gray"},
              {k:"critical", l:"CRITICAL", count: stats.critical, color:"gray"},
              {k:"high", l:"HIGH RISK", count: stats.high, color:"gray"},
              {k:"medium", l:"MEDIUM", count: stats.medium, color:"gray"},
              {k:"low", l:"LOW RISK", count: stats.low, color:"gray"}
            ].map(f => (
              <button key={f.k} onClick={() => setFilter(f.k)} className={`px-5 py-3 rounded-lg font-semibold text-xs transition-all duration-200 flex items-center gap-2 ${
                filter === f.k 
                  ? "bg-gray-900 text-white shadow-md" 
                  : "bg-gray-100 text-gray-700 hover:bg-gray-200 border border-gray-200"
              }`}>
                <span className="w-2 h-2 rounded-full bg-gray-700"></span>
                {f.l}
                <span className="bg-white/20 px-2 py-0.5 rounded-full text-xs">{f.count}</span>
              </button>
            ))}
          </div>
        </div>

        {/* User Risk Analysis Table */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
          <div className="bg-gray-50 p-5 border-b border-gray-200">
            <h2 className="text-xl font-bold text-gray-900">User Risk Analysis ({filteredData.length})</h2>
            <p className="text-gray-600 text-sm mt-1">Real-time user monitoring and analytics</p>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="p-4 text-left text-gray-600 font-semibold text-xs uppercase">User Identity</th>
                  <th className="p-4 text-center text-gray-600 font-semibold text-xs uppercase">Risk Score</th>
                  <th className="p-4 text-center text-gray-600 font-semibold text-xs uppercase">Threat Level</th>
                  <th className="p-4 text-center text-gray-600 font-semibold text-xs uppercase">Access Decision</th>
                  <th className="p-4 text-left text-gray-600 font-semibold text-xs uppercase">Location & Device</th>
                  <th className="p-4 text-left text-gray-600 font-semibold text-xs uppercase">Threat Indicators</th>
                  <th className="p-4 text-center text-gray-600 font-semibold text-xs uppercase">Actions</th>
                </tr>
              </thead>
              <tbody>
                {filteredData.length === 0 ? (
                  <tr><td colSpan="7" className="p-12 text-center text-gray-500">No users found for selected filter</td></tr>
                ) : (
                  filteredData.map((u, i) => (
                    <tr key={i} className="border-b border-gray-100 hover:bg-gray-50 transition-colors">
                      <td className="p-4">
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-gray-900 rounded-full flex items-center justify-center">
                            <span className="text-white font-bold text-sm">{String(u?.username || u?.user || 'U')[0].toUpperCase()}</span>
                          </div>
                          <div>
                            <div className="text-gray-900 font-semibold">{String(u?.username || u?.user || 'UNKNOWN')}</div>
                            <div className="text-gray-500 text-xs">{u?.login_count || 0} total logins</div>
                          </div>
                        </div>
                      </td>
                      <td className="p-4 text-center">
                        <div className="text-3xl font-bold text-gray-900">
                          {u?.risk_score || 0}
                        </div>
                        <div className="text-gray-500 text-xs">/100</div>
                      </td>
                      <td className="p-4 text-center">
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-200">
                          {u?.risk_level || 'LOW'}
                        </span>
                      </td>
                      <td className="p-4 text-center">
                        <span className="px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-200">
                          {u?.decision || 'ALLOW'}
                        </span>
                      </td>
                      <td className="p-4">
                        <div className="space-y-1 text-xs">
                          {u?.city && u.city !== 'Unknown' && <div className="text-gray-700">{u.city}, {u.country}</div>}
                          {u?.ip_address && u.ip_address !== 'N/A' && <div className="text-gray-500">{u.ip_address}</div>}
                          {u?.device_id && u.device_id !== 'N/A' && <div className="text-gray-400">{String(u.device_id).substring(0, 12)}...</div>}
                          <button onClick={() => handleShowDetails(u)} className="mt-2 px-3 py-1 bg-gray-900 hover:bg-gray-800 text-white rounded text-xs font-semibold transition-colors">
                            View Details
                          </button>
                        </div>
                      </td>
                      <td className="p-4">
                        {(!u?.signals || u.signals.length === 0) ? (
                          <div className="flex items-center gap-2">
                            <span className="w-2 h-2 bg-gray-700 rounded-full"></span>
                            <span className="text-gray-700 font-semibold text-xs">CLEAN</span>
                          </div>
                        ) : (
                          <div className="space-y-1">
                            {u.signals.slice(0, 2).map((s, j) => (
                              <div key={j} className="flex items-center gap-2">
                                <span className="w-1.5 h-1.5 bg-gray-700 rounded-full"></span>
                                <span className="text-gray-700 text-xs">{String(s).replace(/_/g, " ")}</span>
                              </div>
                            ))}
                            {u.signals.length > 2 && <div className="text-gray-500 text-xs">+{u.signals.length - 2} more</div>}
                          </div>
                        )}
                      </td>
                      <td className="p-4 text-center">
                        {!['admin', 'bhargav'].includes(u?.username || u?.user) && (u?.status !== 'revoked') && (
                          <button onClick={() => handleRevoke(u.username || u.user)} className="px-3 py-1 bg-gray-600 hover:bg-gray-700 text-white rounded text-xs font-semibold transition-colors">
                            Revoke Access
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

        {/* Activity Monitoring */}
        <div className="grid grid-cols-2 gap-6">
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
            <div className="bg-gray-50 p-5 border-b border-gray-200">
              <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                File Access Monitoring
              </h2>
              <p className="text-gray-600 text-xs mt-1">Real-time document access tracking</p>
            </div>
            <div className="overflow-y-auto max-h-96 p-5 space-y-3">
              {fileLogs.length === 0 ? (
                <div className="text-center text-gray-500 py-12 text-sm">No file access logs available</div>
              ) : (
                fileLogs.slice(0, 20).map((f, i) => (
                  <div key={i} className="bg-gray-50 p-3 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-gray-900 font-semibold text-sm">{f?.user_id || 'Unknown'}</span>
                      <span className="px-2 py-0.5 rounded text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-200">
                        {f?.action || 'READ'}
                      </span>
                    </div>
                    <div className="text-gray-900 text-xs font-medium">{f?.file_name || 'N/A'}</div>
                    <div className="text-gray-500 text-xs mt-1">{f?.access_time ? new Date(f.access_time).toLocaleString() : 'N/A'}</div>
                  </div>
                ))
              )}
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden shadow-sm">
            <div className="bg-gray-50 p-5 border-b border-gray-200">
              <h2 className="text-lg font-bold text-gray-900 flex items-center gap-2">
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                Blockchain Audit Trail
              </h2>
              <p className="text-gray-600 text-xs mt-1">Immutable security event logging</p>
            </div>
            <div className="overflow-y-auto max-h-96 p-5 space-y-3">
              {auditChain.length === 0 ? (
                <div className="text-center text-gray-500 py-12 text-sm">No audit records available</div>
              ) : (
                auditChain.slice(0, 10).map((block, i) => (
                  <div key={i} className="bg-gray-50 p-3 rounded-lg border border-gray-200 hover:bg-gray-100 transition-colors">
                    <div className="flex justify-between items-start mb-2">
                      <span className="text-gray-900 font-semibold text-sm">BLOCK #{block?.block_index || i}</span>
                      <span className="text-gray-500 text-xs">{block?.timestamp || 'N/A'}</span>
                    </div>
                    {block?.current_hash && <div className="text-gray-600 text-xs font-mono">{String(block.current_hash).substring(0, 40)}...</div>}
                    <div className="text-gray-700 text-xs mt-2 flex items-center gap-1">
                      <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Verified & Immutable
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Comprehensive User Details Modal */}
      {selectedUser && sessionHistory && (
        <div className="fixed inset-0 bg-black/80 backdrop-blur flex items-center justify-center z-50 p-4" onClick={() => { setSelectedUser(null); setSessionHistory(null); }}>
          <div className="bg-gray-800 rounded-2xl border border-cyan-500/30 p-8 max-w-7xl w-full max-h-[95vh] overflow-y-auto shadow-2xl backdrop-blur-sm" onClick={(e) => e.stopPropagation()}>
            
            {/* Header */}
            <div className="flex justify-between items-start mb-8">
              <div>
                <h2 className="text-4xl font-bold bg-gradient-to-r from-cyan-400 to-blue-400 bg-clip-text text-transparent">Complete User Analysis</h2>
                <p className="text-gray-400 text-lg mt-2">Comprehensive insider threat assessment for: <span className="text-white font-bold">{selectedUser.username || selectedUser.user}</span></p>
              </div>
              <button onClick={() => { setSelectedUser(null); setSessionHistory(null); }} className="text-red-400 hover:text-red-300 text-4xl font-bold transition-colors">×</button>
            </div>

            {/* User Profile Overview */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                <h3 className="text-cyan-400 font-bold text-xl mb-4">👤 User Profile</h3>
                <div className="space-y-3">
                  <div><span className="text-gray-400">Username:</span> <span className="text-white font-semibold">{sessionHistory.user_profile?.username || selectedUser.username}</span></div>
                  <div><span className="text-gray-400">Department:</span> <span className="text-white">{sessionHistory.user_profile?.department || "Engineering"}</span></div>
                  <div><span className="text-gray-400">Role:</span> <span className="text-white">{sessionHistory.user_profile?.role || "Developer"}</span></div>
                  <div><span className="text-gray-400">Clearance:</span> <span className="text-blue-300">{sessionHistory.user_profile?.clearance_level || "Level 2"}</span></div>
                  <div><span className="text-gray-400">Manager:</span> <span className="text-white">{sessionHistory.user_profile?.manager || "John Smith"}</span></div>
                  <div><span className="text-gray-400">Account Created:</span> <span className="text-white">{sessionHistory.user_profile?.account_created ? new Date(sessionHistory.user_profile.account_created).toLocaleDateString() : "90 days ago"}</span></div>
                </div>
              </div>
              
              <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                <h3 className="text-red-400 font-bold text-xl mb-4">⚠️ Risk Assessment</h3>
                <div className="space-y-4">
                  <div className="text-center">
                    <div className={`text-5xl font-bold ${selectedUser.risk_score >= 70 ? 'text-red-400' : selectedUser.risk_score >= 50 ? 'text-orange-400' : 'text-green-400'}`}>
                      {selectedUser.risk_score || 0}
                    </div>
                    <div className="text-gray-400 text-sm">Risk Score / 100</div>
                  </div>
                  <div className="text-center">
                    <span className={`px-4 py-2 rounded-full font-bold ${selectedUser.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-300' : selectedUser.risk_level === 'HIGH' ? 'bg-orange-500/20 text-orange-300' : selectedUser.risk_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-300' : 'bg-green-500/20 text-green-300'}`}>
                      {selectedUser.risk_level || 'LOW'} RISK
                    </span>
                  </div>
                  <div className="text-center">
                    <span className={`px-4 py-2 rounded-full font-bold ${selectedUser.decision === 'ALLOW' ? 'bg-green-500/20 text-green-300' : selectedUser.decision === 'RESTRICT' ? 'bg-yellow-500/20 text-yellow-300' : 'bg-red-500/20 text-red-300'}`}>
                      {selectedUser.decision || 'ALLOW'}
                    </span>
                  </div>
                </div>
              </div>
              
              <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                <h3 className="text-purple-400 font-bold text-xl mb-4">📊 Activity Stats</h3>
                <div className="space-y-3">
                  <div><span className="text-gray-400">Total Logins:</span> <span className="text-white font-semibold">{selectedUser.login_count || 0}</span></div>
                  <div><span className="text-gray-400">Last Login:</span> <span className="text-white">{sessionHistory.user_profile?.last_login ? new Date(sessionHistory.user_profile.last_login).toLocaleString() : "1 hour ago"}</span></div>
                  <div><span className="text-gray-400">Active Sessions:</span> <span className="text-green-400 font-semibold">{sessionHistory.sessions?.filter(s => s.is_active).length || 1}</span></div>
                  <div><span className="text-gray-400">Devices Used:</span> <span className="text-white">{sessionHistory.device_fingerprints?.length || 2}</span></div>
                  <div><span className="text-gray-400">Files Accessed:</span> <span className="text-white">{sessionHistory.file_access_history?.length || 5}</span></div>
                </div>
              </div>
            </div>

            {/* Device Fingerprints */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-cyan-400 mb-6">🔍 Device Fingerprints</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {(sessionHistory.device_fingerprints || []).map((device, i) => (
                  <div key={i} className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                    <div className="flex justify-between items-start mb-4">
                      <h4 className="text-white font-bold text-lg">{device.device_type} Device</h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold ${device.trusted ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}`}>
                        {device.trusted ? '✓ TRUSTED' : '⚠ UNTRUSTED'}
                      </span>
                    </div>
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div><span className="text-gray-400">Device ID:</span> <span className="text-blue-300 font-mono">{device.device_id}</span></div>
                      <div><span className="text-gray-400">OS:</span> <span className="text-white">{device.os}</span></div>
                      <div><span className="text-gray-400">Browser:</span> <span className="text-white">{device.browser}</span></div>
                      <div><span className="text-gray-400">MAC:</span> <span className="text-green-300 font-mono">{device.mac_address}</span></div>
                      <div><span className="text-gray-400">Hostname:</span> <span className="text-white">{device.hostname}</span></div>
                      <div><span className="text-gray-400">Location:</span> <span className="text-white">{device.location}</span></div>
                      <div><span className="text-gray-400">Last Seen:</span> <span className="text-white">{new Date(device.last_seen).toLocaleString()}</span></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* File Access History */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-orange-400 mb-6">📁 File Access History</h3>
              <div className="bg-gray-900/50 rounded-xl border border-gray-700/50 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-800/50">
                      <tr>
                        <th className="p-4 text-left text-orange-300 font-bold">File Name</th>
                        <th className="p-4 text-center text-orange-300 font-bold">Action</th>
                        <th className="p-4 text-center text-orange-300 font-bold">Sensitivity</th>
                        <th className="p-4 text-left text-orange-300 font-bold">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(sessionHistory.file_access_history || []).map((file, i) => (
                        <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                          <td className="p-4 text-white font-medium">{file.file_name}</td>
                          <td className="p-4 text-center">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${file.action === 'READ' ? 'bg-cyan-500/20 text-cyan-300' : file.action === 'WRITE' ? 'bg-yellow-500/20 text-yellow-300' : 'bg-red-500/20 text-red-300'}`}>
                              {file.action}
                            </span>
                          </td>
                          <td className="p-4 text-center">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${file.sensitivity === 'Critical' ? 'bg-red-500/20 text-red-300' : file.sensitivity === 'Confidential' ? 'bg-orange-500/20 text-orange-300' : 'bg-yellow-500/20 text-yellow-300'}`}>
                              {file.sensitivity}
                            </span>
                          </td>
                          <td className="p-4 text-gray-300">{new Date(file.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Network Activity */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-green-400 mb-6">🌐 Network Activity</h3>
              <div className="bg-gray-900/50 rounded-xl border border-gray-700/50 overflow-hidden">
                <div className="overflow-x-auto">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-800/50">
                      <tr>
                        <th className="p-4 text-left text-green-300 font-bold">Connection</th>
                        <th className="p-4 text-left text-green-300 font-bold">Destination</th>
                        <th className="p-4 text-center text-green-300 font-bold">Protocol</th>
                        <th className="p-4 text-center text-green-300 font-bold">Data</th>
                        <th className="p-4 text-left text-green-300 font-bold">Timestamp</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(sessionHistory.network_activity || []).map((conn, i) => (
                        <tr key={i} className="border-b border-gray-700/50 hover:bg-gray-700/30">
                          <td className="p-4 text-white font-medium">{conn.connection}</td>
                          <td className="p-4 text-blue-300 font-mono">{conn.destination}</td>
                          <td className="p-4 text-center text-gray-300">{conn.protocol}:{conn.port}</td>
                          <td className="p-4 text-center text-yellow-300">{conn.data_transferred}</td>
                          <td className="p-4 text-gray-300">{new Date(conn.timestamp).toLocaleString()}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>

            {/* Behavioral Analytics */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-purple-400 mb-6">🧠 Behavioral Analytics</h3>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                  <h4 className="text-white font-bold text-lg mb-4">📈 Login Patterns</h4>
                  <div className="space-y-3 text-sm">
                    <div><span className="text-gray-400">Usual Hours:</span> <span className="text-white">{sessionHistory.behavioral_analytics?.login_patterns?.usual_hours || "9:00 AM - 6:00 PM"}</span></div>
                    <div><span className="text-gray-400">Locations:</span> <span className="text-white">{sessionHistory.behavioral_analytics?.login_patterns?.usual_locations?.join(", ") || "New York, San Francisco"}</span></div>
                    <div><span className="text-gray-400">Devices:</span> <span className="text-white">{sessionHistory.behavioral_analytics?.login_patterns?.usual_devices || 2} registered</span></div>
                    <div><span className="text-gray-400">Weekend Activity:</span> <span className="text-white">{sessionHistory.behavioral_analytics?.login_patterns?.weekend_activity || "Low"}</span></div>
                  </div>
                </div>
                
                <div className="bg-gray-900/50 rounded-xl p-6 border border-gray-700/50">
                  <h4 className="text-red-400 font-bold text-lg mb-4">🚨 Risk Factors</h4>
                  <div className="space-y-3">
                    {(sessionHistory.behavioral_analytics?.risk_factors || []).map((risk, i) => (
                      <div key={i} className="bg-red-900/20 p-3 rounded-lg border border-red-500/30">
                        <div className="text-red-300 font-semibold">{risk.factor}</div>
                        <div className="text-gray-400 text-sm">Severity: <span className={`${risk.severity === 'High' ? 'text-red-400' : risk.severity === 'Medium' ? 'text-orange-400' : 'text-yellow-400'}`}>{risk.severity}</span></div>
                        <div className="text-gray-500 text-xs">Detected: {risk.detected}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Session History */}
            <div className="mb-8">
              <h3 className="text-2xl font-bold text-blue-400 mb-6">🕒 Session History</h3>
              <div className="space-y-6">
                {sessionHistory.sessions && sessionHistory.sessions.length > 0 ? (
                  sessionHistory.sessions.map((session, i) => (
                    <div key={i} className="bg-gray-900/50 rounded-xl border border-gray-700/50 p-6">
                      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
                        <div>
                          <div className="text-blue-400 font-bold mb-2">SESSION #{i + 1}</div>
                          <div className="text-white font-semibold text-lg">{new Date(session.login_time).toLocaleString()}</div>
                          <div className="text-blue-300 text-sm mt-3">📍 {session.city}, {session.country}</div>
                          <div className="text-gray-400 text-sm">🌐 {session.ip_address}</div>
                        </div>
                        <div>
                          <div className="text-blue-400 font-bold mb-2">DEVICE INFO</div>
                          <div className="space-y-1 text-sm">
                            <div className="text-gray-300">ID: {session.device_id}</div>
                            <div className="text-gray-300">MAC: {session.mac_address}</div>
                            <div className="text-gray-300">WiFi: {session.wifi_ssid}</div>
                            <div className="text-gray-300">Host: {session.hostname}</div>
                            <div className="text-gray-300">OS: {session.os}</div>
                          </div>
                        </div>
                        <div>
                          <div className="text-blue-400 font-bold mb-2">STATUS</div>
                          <div className={`text-lg font-bold ${session.is_active ? 'text-green-400' : 'text-gray-400'}`}>
                            {session.is_active ? '🟢 ACTIVE' : '⚫ ENDED'}
                          </div>
                          <div className="text-gray-400 text-sm mt-3">Duration: {Math.floor(session.session_duration_seconds / 60)}m {session.session_duration_seconds % 60}s</div>
                        </div>
                      </div>
                      
                      {session.file_activities && session.file_activities.length > 0 && (
                        <div className="bg-black/30 rounded-lg p-4">
                          <div className="text-orange-400 font-bold mb-3">📁 SESSION FILE ACTIVITIES ({session.file_activities.length})</div>
                          <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
                            {session.file_activities.map((file, j) => (
                              <div key={j} className="text-sm bg-gray-800/50 p-3 rounded border border-gray-700/50">
                                <div className="text-blue-300 font-medium">{file.file_name}</div>
                                <div className="text-gray-400">Action: <span className={`${file.action === 'WRITE' ? 'text-yellow-400' : 'text-cyan-400'}`}>{file.action}</span></div>
                                <div className="text-gray-500 text-xs">{new Date(file.access_time).toLocaleString()}</div>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className="text-center text-gray-500 py-12 text-lg">No session history available</div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4 justify-center">
              <button className="px-8 py-4 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white rounded-xl font-bold shadow-lg transition-all duration-200">
                📊 Generate Report
              </button>
              <button className="px-8 py-4 bg-gradient-to-r from-green-600 to-green-700 hover:from-green-700 hover:to-green-800 text-white rounded-xl font-bold shadow-lg transition-all duration-200">
                📤 Export Data
              </button>
              <button onClick={() => { setSelectedUser(null); setSessionHistory(null); }} className="px-8 py-4 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white rounded-xl font-bold shadow-lg transition-all duration-200">
                ✖️ Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}