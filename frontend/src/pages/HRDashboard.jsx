import { useEffect, useState } from "react";
import { getAdminData } from "../api/api";
import Logo from "../components/Logo";

export default function HRDashboard() {
  const [employees, setEmployees] = useState([]);
  const [stats, setStats] = useState({ total: 0, active: 0, onLeave: 0 });

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 3000);
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const res = await getAdminData();
      const users = res.users || [];
      setEmployees(users);
      setStats({
        total: users.length,
        active: users.filter(u => u.status === 'active').length,
        onLeave: users.filter(u => u.status === 'inactive').length
      });
    } catch (err) {
      console.error("HR data error:", err);
    }
  };

  return (
    <div className="min-h-screen bg-black p-6">
      <div className="fixed inset-0 opacity-5" style={{
        backgroundImage: 'linear-gradient(#00ffff 1px, transparent 1px), linear-gradient(90deg, #00ffff 1px, transparent 1px)',
        backgroundSize: '50px 50px'
      }}></div>

      <div className="max-w-[1600px] mx-auto space-y-6 relative z-10">
        <div className="bg-gradient-to-r from-cyan-950/30 via-black to-cyan-950/30 rounded-xl p-6 border-2 border-cyan-500/50 shadow-2xl shadow-cyan-500/30">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <Logo size="md" />
              <div>
                <h1 className="text-2xl font-bold text-cyan-400 mb-1 font-mono tracking-wider">HR MANAGEMENT PORTAL</h1>
                <p className="text-cyan-400/80 text-sm font-mono">[ EMPLOYEE MONITORING • ATTENDANCE • COMPLIANCE ]</p>
              </div>
            </div>
            <div className="text-right">
              <div className="text-lg font-bold text-green-400 font-mono">● ONLINE</div>
              <div className="text-xs text-cyan-400 font-mono">{new Date().toLocaleString()}</div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4">
          <div className="bg-black/80 rounded-xl p-6 border-2 border-green-500/50 backdrop-blur">
            <div className="text-green-400 text-xs font-bold mb-2 font-mono">[TOTAL EMPLOYEES]</div>
            <div className="text-5xl font-bold text-green-400 font-mono">{stats.total}</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-cyan-500/50 backdrop-blur">
            <div className="text-cyan-400 text-xs font-bold mb-2 font-mono">[ACTIVE TODAY]</div>
            <div className="text-5xl font-bold text-cyan-400 font-mono">{stats.active}</div>
          </div>
          <div className="bg-black/80 rounded-xl p-6 border-2 border-yellow-500/50 backdrop-blur">
            <div className="text-yellow-400 text-xs font-bold mb-2 font-mono">[ON LEAVE]</div>
            <div className="text-5xl font-bold text-yellow-400 font-mono">{stats.onLeave}</div>
          </div>
        </div>

        <div className="bg-black/80 rounded-xl border-2 border-cyan-500/50 overflow-hidden backdrop-blur">
          <div className="bg-cyan-950/30 p-4 border-b-2 border-cyan-500/50">
            <h2 className="text-xl font-bold text-cyan-400 font-mono">👥 EMPLOYEE DIRECTORY</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm font-mono">
              <thead className="bg-gray-900/50 border-b-2 border-cyan-500">
                <tr>
                  <th className="p-4 text-left text-cyan-400 font-bold">EMPLOYEE</th>
                  <th className="p-4 text-center text-cyan-400 font-bold">STATUS</th>
                  <th className="p-4 text-center text-cyan-400 font-bold">LAST SEEN</th>
                  <th className="p-4 text-left text-cyan-400 font-bold">LOCATION</th>
                  <th className="p-4 text-center text-cyan-400 font-bold">LOGINS</th>
                </tr>
              </thead>
              <tbody>
                {employees.map((emp, i) => (
                  <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-900/30">
                    <td className="p-4">
                      <div className="text-cyan-400 font-bold">{emp.username}</div>
                    </td>
                    <td className="p-4 text-center">
                      <span className={`px-3 py-1 rounded text-xs font-bold border-2 ${emp.status === 'active' ? 'bg-green-950 text-green-300 border-green-700' : 'bg-red-950 text-red-300 border-red-700'}`}>
                        {emp.status?.toUpperCase() || 'ACTIVE'}
                      </span>
                    </td>
                    <td className="p-4 text-center text-gray-400">
                      {emp.last_login ? new Date(emp.last_login).toLocaleString() : 'N/A'}
                    </td>
                    <td className="p-4 text-gray-400">
                      {emp.city}, {emp.country}
                    </td>
                    <td className="p-4 text-center text-cyan-400 font-bold">
                      {emp.login_count || 0}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
