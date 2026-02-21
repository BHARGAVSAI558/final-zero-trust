import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const API = axios.create({ baseURL: "http://localhost:8000" });

export default function SOCDashboard() {
  const [users, setUsers] = useState([]);
  const [realtimeActivity, setRealtimeActivity] = useState([]);
  const [networkActivity, setNetworkActivity] = useState([]);
  const [pendingUsers, setPendingUsers] = useState([]);
  const [stats, setStats] = useState({ total: 0, critical: 0, high: 0, active: 0 });
  const [selectedUser, setSelectedUser] = useState(null);
  const [userDetails, setUserDetails] = useState(null);
  const [loadingDetails, setLoadingDetails] = useState(false);
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("username");
    localStorage.removeItem("role");
    localStorage.removeItem("isAuthenticated");
    navigate("/login");
  };

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [usersRes, filesRes, networkRes, pendingRes] = await Promise.all([
        API.get("/security/analyze/admin").catch(() => ({ data: { users: [] } })),
        API.get("/admin/file-access").catch(() => ({ data: { file_logs: [] } })),
        API.get("/admin/network-activity").catch(() => ({ data: { network_logs: [] } })),
        API.get("/admin/pending-users").catch(() => ({ data: { pending_users: [] } }))
      ]);

      const userData = usersRes.data.users || [];
      setUsers(userData);
      setRealtimeActivity(filesRes.data.file_logs || []);
      setNetworkActivity(networkRes.data.network_logs || []);
      setPendingUsers(pendingRes.data.pending_users || []);

      const critical = userData.filter(u => u.risk_level === "CRITICAL").length;
      const high = userData.filter(u => u.risk_level === "HIGH").length;
      
      setStats({
        total: userData.length,
        critical,
        high,
        active: userData.filter(u => u.status === "active").length
      });
    } catch (err) {
      console.error("Load error:", err);
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      CRITICAL: "from-red-500 via-red-600 to-red-700",
      HIGH: "from-orange-500 via-orange-600 to-orange-700",
      MEDIUM: "from-yellow-500 via-yellow-600 to-yellow-700",
      LOW: "from-emerald-500 via-emerald-600 to-emerald-700"
    };
    return colors[level] || colors.LOW;
  };

  const loadUserDetails = async (username) => {
    try {
      const [deviceRes, fileRes, loginRes, networkRes] = await Promise.all([
        API.get(`/admin/user-devices/${username}`),
        API.get(`/admin/file-access?user=${username}`),
        API.get(`/admin/login-history/${username}`),
        API.get(`/admin/network-activity?user=${username}`)
      ]);
      
      setUserDetails({
        devices: deviceRes.data.devices || [],
        fileAccess: fileRes.data.file_logs || [],
        loginHistory: loginRes.data.login_history || [],
        networkActivity: networkRes.data.network_logs || []
      });
    } catch (error) {
      console.error('Error fetching user details:', error);
    }
  };

  const handleUserClick = async (user) => {
    setSelectedUser(user);
    setLoadingDetails(true);
    await loadUserDetails(user.username);
    setLoadingDetails(false);
  };

  useEffect(() => {
    if (selectedUser) {
      const interval = setInterval(() => loadUserDetails(selectedUser.username), 5000);
      return () => clearInterval(interval);
    }
  }, [selectedUser]);

  const parseUserAgent = (ua) => {
    if (!ua || ua === 'N/A') return 'N/A';
    
    // Extract OS
    let os = 'Unknown';
    if (ua.includes('Windows NT 10.0')) os = 'Windows 10';
    else if (ua.includes('Windows NT')) os = 'Windows';
    else if (ua.includes('Mac OS X')) os = 'macOS';
    else if (ua.includes('Linux')) os = 'Linux';
    else if (ua.includes('Android')) os = 'Android';
    else if (ua.includes('iPhone') || ua.includes('iPad')) os = 'iOS';
    
    // Extract Browser
    let browser = 'Unknown';
    if (ua.includes('Edg/')) browser = 'Edge';
    else if (ua.includes('Chrome/')) browser = 'Chrome';
    else if (ua.includes('Firefox/')) browser = 'Firefox';
    else if (ua.includes('Safari/') && !ua.includes('Chrome')) browser = 'Safari';
    
    return `${os} - ${browser}`;
  };

  const handleApprove = async (username, action) => {
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('admin', localStorage.getItem('username') || 'admin');
      formData.append('action', action);
      
      const result = await API.post('/admin/approve-user', formData);
      if (result.data.status === 'SUCCESS') {
        alert(`User ${action === 'approve' ? 'approved' : 'rejected'} successfully`);
        loadData();
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  const handleRevoke = async (username) => {
    if (!window.confirm(`Revoke access for ${username}? This will block all future logins.`)) return;
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('admin', localStorage.getItem('username') || 'admin');
      
      const result = await API.post('/admin/revoke-access', formData);
      if (result.data.status === 'SUCCESS') {
        alert(`Access revoked for ${username}`);
        loadData();
      }
    } catch (err) {
      alert('Error: ' + err.message);
    }
  };

  return (
    <div className="min-h-screen bg-black" style={{fontFamily: 'Inter, system-ui, -apple-system, sans-serif'}}>
      <style>{`
        ::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }
        ::-webkit-scrollbar-track {
          background: #0a0a0a;
        }
        ::-webkit-scrollbar-thumb {
          background: #00ff00;
          border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
          background: #00cc00;
        }
      `}</style>
      {/* Top Bar */}
      <div className="bg-black border-b-2 border-green-500 px-6 py-5">
        <div className="flex justify-between items-center max-w-[1800px] mx-auto">
          <div className="flex items-center gap-4">
            <div className="w-14 h-14 bg-black border-2 border-green-500 rounded-lg flex items-center justify-center">
              <svg className="w-8 h-8 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24" strokeWidth={2.5}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-green-500">CYBER SOC DASHBOARD</h1>
              <p className="text-sm text-green-400 mt-1 font-medium">Real-Time Threat Monitoring System</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button onClick={() => navigate("/files")} className="px-4 py-2 bg-black border border-green-500 hover:bg-green-500/10 text-green-500 rounded-lg font-semibold transition text-sm">
              FILES
            </button>
            <button onClick={handleLogout} className="px-4 py-2 bg-black border border-red-500 hover:bg-red-500/10 text-red-500 rounded-lg font-semibold transition text-sm">
              LOGOUT
            </button>
          </div>
        </div>
      </div>

      <div className="max-w-[1800px] mx-auto p-6 space-y-6">
        {/* Pending Users Alert */}
        {pendingUsers.length > 0 && (
          <div className="bg-black rounded-xl border border-yellow-500 p-3">
            <div className="flex items-center gap-2 mb-3">
              <svg className="w-4 h-4 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <div>
                <h2 className="text-sm font-semibold text-yellow-500">PENDING REGISTRATIONS</h2>
                <p className="text-yellow-400 text-xs">{pendingUsers.length} awaiting approval</p>
              </div>
            </div>
            <div className="grid gap-2">
              {pendingUsers.map((user, i) => (
                <div key={i} className="bg-yellow-500/10 rounded-lg p-2 border border-yellow-500/30 flex justify-between items-center">
                  <div className="flex items-center gap-2">
                    <div className="w-7 h-7 bg-yellow-500 rounded-full flex items-center justify-center">
                      <span className="text-black font-bold text-xs">{user.username[0].toUpperCase()}</span>
                    </div>
                    <div>
                      <div className="text-yellow-500 font-medium text-sm">{user.username}</div>
                      <div className="text-yellow-400 text-xs">{new Date(user.created_at).toLocaleString()}</div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button onClick={() => handleApprove(user.username, 'approve')} className="px-3 py-1 bg-black border border-green-500 hover:bg-green-500/10 text-green-500 rounded text-xs font-semibold transition">
                      APPROVE
                    </button>
                    <button onClick={() => handleApprove(user.username, 'reject')} className="px-3 py-1 bg-black border border-red-500 hover:bg-red-500/10 text-red-500 rounded text-xs font-semibold transition">
                      REJECT
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="grid grid-cols-4 gap-4">
          <div className="bg-black border border-green-500 rounded-lg p-4 hover:border-green-400 transition-all">
            <div className="text-green-400 text-xs font-semibold mb-1 uppercase tracking-wide">TOTAL ENDPOINTS</div>
            <div className="text-3xl font-bold text-green-500 mb-1">{stats.total}</div>
            <div className="text-xs text-green-400">Monitored Assets</div>
          </div>
          <div className="bg-black border border-red-500 rounded-lg p-4 hover:border-red-400 transition-all">
            <div className="text-red-400 text-xs font-semibold mb-1 uppercase tracking-wide">CRITICAL THREATS</div>
            <div className="text-3xl font-bold text-red-500 mb-1">{stats.critical}</div>
            <div className="text-xs text-red-400">Immediate Action</div>
          </div>
          <div className="bg-black border border-yellow-500 rounded-lg p-4 hover:border-yellow-400 transition-all">
            <div className="text-yellow-400 text-xs font-semibold mb-1 uppercase tracking-wide">HIGH RISK</div>
            <div className="text-3xl font-bold text-yellow-500 mb-1">{stats.high}</div>
            <div className="text-xs text-yellow-400">Under Investigation</div>
          </div>
          <div className="bg-black border border-cyan-500 rounded-lg p-4 hover:border-cyan-400 transition-all">
            <div className="text-cyan-400 text-xs font-semibold mb-1 uppercase tracking-wide">ACTIVE NOW</div>
            <div className="text-3xl font-bold text-cyan-500 mb-1">{stats.active}</div>
            <div className="text-xs text-cyan-400 flex items-center gap-1">
              <span className="w-1.5 h-1.5 bg-cyan-500 rounded-full"></span>
              Live Sessions
            </div>
          </div>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-2 gap-6">
          {/* User Threat Matrix */}
          <div className="col-span-1 bg-black border border-green-500 rounded-xl overflow-hidden">
            <div className="bg-green-500/10 p-4 border-b border-green-500">
              <h2 className="text-lg font-bold text-green-500">USER THREAT MATRIX - LIVE</h2>
              <p className="text-green-400 text-xs mt-1">Real-time behavioral analysis</p>
            </div>
            <div className="p-4 max-h-[600px] overflow-y-auto">
              <table className="w-full text-sm">
                <thead className="bg-green-500/10 sticky top-0">
                  <tr>
                    <th className="p-3 text-left text-green-400 font-semibold text-xs uppercase">User</th>
                    <th className="p-3 text-center text-green-400 font-semibold text-xs uppercase">Risk Score</th>
                    <th className="p-3 text-center text-green-400 font-semibold text-xs uppercase">Level</th>
                    <th className="p-3 text-center text-green-400 font-semibold text-xs uppercase">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.filter(u => u.username !== 'admin').map((user, i) => (
                    <tr key={i} className="border-b border-green-500/20 hover:bg-green-500/5 transition-all cursor-pointer">
                      <td className="p-3">
                        <div className="flex items-center gap-2">
                          <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                            <span className="text-black font-bold text-xs">{user.username[0].toUpperCase()}</span>
                          </div>
                          <div className="text-green-500 font-bold text-sm">{user.username}</div>
                        </div>
                      </td>
                      <td className="p-3 text-center">
                        <div className="text-2xl font-bold text-green-500">{user.risk_score}</div>
                      </td>
                      <td className="p-3 text-center">
                        <span className={`px-3 py-1 rounded-full text-xs font-bold border ${
                          user.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-500 border-red-500' : 
                          user.risk_level === 'HIGH' ? 'bg-yellow-500/20 text-yellow-500 border-yellow-500' : 
                          user.risk_level === 'MEDIUM' ? 'bg-blue-500/20 text-blue-500 border-blue-500' : 
                          'bg-green-500/20 text-green-500 border-green-500'
                        }`}>
                          {user.risk_level}
                        </span>
                      </td>
                      <td className="p-3">
                        <div className="flex gap-2 justify-center">
                          <button onClick={() => handleUserClick(user)} className="px-3 py-1 bg-black border border-cyan-500 hover:bg-cyan-500/10 text-cyan-500 rounded text-xs font-semibold transition">
                            VIEW
                          </button>
                          {(user.risk_level === 'CRITICAL' || user.risk_level === 'HIGH') && !['admin', 'bhargav'].includes(user.username) && (
                            <button onClick={() => handleRevoke(user.username)} className="px-3 py-1 bg-black border border-red-500 hover:bg-red-500/10 text-red-500 rounded text-xs font-semibold transition">
                              REVOKE
                            </button>
                          )}
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Real-time Activity Feed */}
          <div className="space-y-6">
            {/* File Activity */}
            <div className="bg-black border border-cyan-500 rounded-xl overflow-hidden">
              <div className="bg-cyan-500/10 p-3 border-b border-cyan-500">
                <h3 className="text-sm font-bold text-cyan-500 flex items-center gap-2">
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  FILE ACTIVITY STREAM
                </h3>
              </div>
              <div className="p-4 max-h-[600px] overflow-y-auto space-y-3">
                {realtimeActivity.slice(0, 20).map((file, i) => (
                  <div key={i} className="bg-cyan-500/5 rounded-xl p-3 border-l-4 border-cyan-500 hover:bg-cyan-500/10 transition-all">
                    <div className="flex justify-between items-start">
                      <div className="text-sm text-cyan-500 font-bold">{file.user_id}</div>
                      <span className="px-3 py-1 rounded-full text-xs font-bold bg-cyan-500 text-black">
                        {file.action}
                      </span>
                    </div>
                    <div className="text-sm text-cyan-400 mt-2 truncate font-medium">{file.file_name}</div>
                    <div className="text-xs text-cyan-300 mt-1">{new Date(file.access_time).toLocaleTimeString()}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Comprehensive User Detail Modal */}
      {selectedUser && (
        <div className="fixed inset-0 bg-black/90 flex items-center justify-center z-50 p-4" onClick={() => { setSelectedUser(null); setUserDetails(null); }}>
          <div className="bg-black border-2 border-green-500 rounded-2xl p-6 max-w-7xl w-full max-h-[95vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
            <div className="flex justify-between items-start mb-6">
              <div>
                <h2 className="text-3xl font-bold text-green-500">{selectedUser.username}</h2>
                <p className="text-green-400 mt-1">Complete Security Analysis & Threat Assessment</p>
              </div>
              <button onClick={() => { setSelectedUser(null); setUserDetails(null); }} className="text-red-500 hover:text-red-400 text-3xl font-bold">×</button>
            </div>

            {loadingDetails ? (
              <div className="text-center py-12">
                <div className="text-green-500 text-lg">Loading comprehensive user analysis...</div>
              </div>
            ) : userDetails ? (
              <div className="space-y-6">
                {/* Overview Stats */}
                <div className="grid grid-cols-3 gap-4">
                  <div className="bg-red-500/10 border-2 border-red-500 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-red-500">{selectedUser.risk_score}</div>
                    <div className="text-sm text-red-400">Risk Score</div>
                  </div>
                  <div className="bg-yellow-500/10 border-2 border-yellow-500 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-yellow-500">{userDetails?.fileAccess?.length || 0}</div>
                    <div className="text-sm text-yellow-400">Files Accessed</div>
                  </div>
                  <div className="bg-purple-500/10 border-2 border-purple-500 rounded-lg p-4 text-center">
                    <div className="text-2xl font-bold text-purple-500">{userDetails?.loginHistory?.length || 0}</div>
                    <div className="text-sm text-purple-400">Login Sessions</div>
                  </div>
                </div>

                {/* Complete Login & Device History */}
                <div className="bg-purple-500/10 border-2 border-purple-500 rounded-lg p-4">
                  <h3 className="text-xl font-bold text-purple-500 mb-4">COMPLETE LOGIN & DEVICE HISTORY</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-purple-500/20">
                        <tr>
                          <th className="p-3 text-left text-purple-400 font-bold">Timestamp</th>
                          <th className="p-3 text-left text-purple-400 font-bold">IP Address</th>
                          <th className="p-3 text-left text-purple-400 font-bold">Location</th>
                          <th className="p-3 text-left text-purple-400 font-bold">MAC Address</th>
                          <th className="p-3 text-left text-purple-400 font-bold">Hostname</th>
                          <th className="p-3 text-left text-purple-400 font-bold">WiFi SSID</th>
                          <th className="p-3 text-left text-purple-400 font-bold">Device/OS</th>
                          <th className="p-3 text-center text-purple-400 font-bold">Status</th>
                        </tr>
                      </thead>
                      <tbody>
                        {userDetails.loginHistory.map((login, i) => (
                          <tr key={i} className="border-b border-purple-500/30 hover:bg-purple-500/10">
                            <td className="p-3 text-purple-300 font-medium">{new Date(login.login_time).toLocaleString()}</td>
                            <td className="p-3 text-cyan-400 font-mono text-xs">{login.ip_address}</td>
                            <td className="p-3 text-purple-300 text-xs">{login.city}, {login.country}</td>
                            <td className="p-3 text-green-400 font-mono text-xs">{login.mac_address}</td>
                            <td className="p-3 text-purple-300 text-xs">{login.hostname}</td>
                            <td className="p-3 text-yellow-400 text-xs">{login.wifi_ssid || 'N/A'}</td>
                            <td className="p-3 text-purple-300 text-xs" title={login.user_agent}>
                              {login.device_os && login.device_os !== 'N/A' ? login.device_os : parseUserAgent(login.user_agent)}
                            </td>
                            <td className="p-3 text-center">
                              <span className={`px-2 py-1 rounded text-xs font-bold border ${login.success ? 'bg-green-500/20 text-green-500 border-green-500' : 'bg-red-500/20 text-red-500 border-red-500'}`}>
                                {login.success ? 'SUCCESS' : 'FAILED'}
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* File Access History */}
                <div className="bg-yellow-500/10 border-2 border-yellow-500 rounded-lg p-4">
                  <h3 className="text-xl font-bold text-yellow-500 mb-4">FILE ACCESS HISTORY</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-yellow-500/20">
                        <tr>
                          <th className="p-3 text-left text-yellow-400 font-bold">File Name</th>
                          <th className="p-3 text-center text-yellow-400 font-bold">Action</th>
                          <th className="p-3 text-center text-yellow-400 font-bold">Sensitivity</th>
                          <th className="p-3 text-left text-yellow-400 font-bold">Timestamp</th>
                        </tr>
                      </thead>
                      <tbody>
                        {userDetails.fileAccess.map((file, i) => {
                          const action = file.action.toUpperCase();
                          return (
                          <tr key={i} className="border-b border-yellow-500/30 hover:bg-yellow-500/10">
                            <td className="p-3 text-yellow-300 font-medium">{file.file_name}</td>
                            <td className="p-3 text-center">
                              <span className="px-2 py-1 rounded text-xs font-bold border bg-yellow-500/20 text-yellow-500 border-yellow-500">
                                {action}
                              </span>
                            </td>
                            <td className="p-3 text-center">
                              <span className={`px-2 py-1 rounded text-xs font-bold border ${file.sensitivity === 'Critical' ? 'bg-red-500/20 text-red-500 border-red-500' : file.sensitivity === 'Confidential' ? 'bg-orange-500/20 text-orange-500 border-orange-500' : 'bg-blue-500/20 text-blue-500 border-blue-500'}`}>
                                {file.sensitivity}
                              </span>
                            </td>
                            <td className="p-3 text-yellow-300">{new Date(file.access_time).toLocaleString()}</td>
                          </tr>
                        )})}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Network Activity */}
                <div className="bg-cyan-500/10 border-2 border-cyan-500 rounded-lg p-4">
                  <h3 className="text-xl font-bold text-cyan-500 mb-4">NETWORK ACTIVITY</h3>
                  <div className="overflow-x-auto">
                    <table className="w-full text-sm">
                      <thead className="bg-cyan-500/20">
                        <tr>
                          <th className="p-3 text-left text-cyan-400 font-bold">Connection</th>
                          <th className="p-3 text-left text-cyan-400 font-bold">Destination</th>
                          <th className="p-3 text-center text-cyan-400 font-bold">Protocol</th>
                          <th className="p-3 text-left text-cyan-400 font-bold">Timestamp</th>
                        </tr>
                      </thead>
                      <tbody>
                        {userDetails.networkActivity.map((conn, i) => (
                          <tr key={i} className="border-b border-cyan-500/30 hover:bg-cyan-500/10">
                            <td className="p-3 text-cyan-300 font-medium">{conn.connection}</td>
                            <td className="p-3 text-cyan-300 font-mono">{conn.destination}</td>
                            <td className="p-3 text-center text-cyan-300">{conn.protocol}:{conn.port}</td>
                            <td className="p-3 text-cyan-300">{new Date(conn.timestamp).toLocaleString()}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>

                {/* Threat Analysis */}
                <div className="bg-red-500/10 border-2 border-red-500 rounded-lg p-4">
                  <h3 className="text-xl font-bold text-red-500 mb-4">THREAT ANALYSIS</h3>
                  <div className="grid grid-cols-2 gap-6">
                    <div>
                      <h4 className="text-red-400 font-bold mb-3">Risk Assessment</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span className="text-red-300">Risk Level:</span>
                          <span className={`px-3 py-1 rounded font-bold border ${selectedUser.risk_level === 'CRITICAL' ? 'bg-red-500/20 text-red-500 border-red-500' : selectedUser.risk_level === 'HIGH' ? 'bg-yellow-500/20 text-yellow-500 border-yellow-500' : 'bg-green-500/20 text-green-500 border-green-500'}`}>
                            {selectedUser.risk_level}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-red-300">Risk Score:</span>
                          <span className="text-red-400 font-bold">{selectedUser.risk_score}/100</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-red-300">Decision:</span>
                          <span className={`px-2 py-1 rounded text-xs font-bold border ${selectedUser.decision === 'ALLOW' ? 'bg-green-500/20 text-green-500 border-green-500' : 'bg-red-500/20 text-red-500 border-red-500'}`}>
                            {selectedUser.decision || 'ALLOW'}
                          </span>
                        </div>
                      </div>
                    </div>
                    <div>
                      <h4 className="text-red-400 font-bold mb-3">Threat Indicators</h4>
                      {selectedUser.signals && selectedUser.signals.length > 0 ? (
                        <div className="space-y-2">
                          {selectedUser.signals.map((signal, i) => (
                            <div key={i} className="bg-red-500/20 p-2 rounded border border-red-500/50">
                              <div className="text-red-400 text-sm">⚠ {signal.replace(/_/g, ' ')}</div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-green-500">✓ No active threats detected</div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12">
                <div className="text-red-500 text-lg">Failed to load user details</div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
