import { useEffect, useState } from "react";

export default function RealTimeMonitor() {
  const [activities, setActivities] = useState([]);
  const [stats, setStats] = useState({ total_users: 0, active_now: 0 });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch("http://localhost:8000/realtime/stats");
        const data = await res.json();
        setStats(data);
        
        setActivities(prev => [{
          time: new Date().toLocaleTimeString(),
          message: `${data.active_now} users active | ${data.total_users} total`,
          type: "info"
        }, ...prev.slice(0, 19)]);
      } catch (err) {
        console.error("Stats fetch error:", err);
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="bg-black/80 rounded-xl border-2 border-cyan-500/50 p-4 backdrop-blur shadow-lg shadow-cyan-500/20">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-bold text-cyan-400 font-mono">[ LIVE ACTIVITY FEED ]</h3>
        <div className="flex gap-4">
          <div className="text-xs font-mono">
            <span className="text-gray-500">ACTIVE:</span>
            <span className="text-green-400 font-bold ml-2">{stats.active_now}</span>
          </div>
          <div className="text-xs font-mono">
            <span className="text-gray-500">TOTAL:</span>
            <span className="text-cyan-400 font-bold ml-2">{stats.total_users}</span>
          </div>
        </div>
      </div>
      
      <div className="space-y-1 max-h-96 overflow-y-auto">
        {activities.map((activity, i) => (
          <div key={i} className="bg-gray-900/30 p-2 rounded border border-gray-700/50 flex items-center gap-3">
            <span className="text-xs text-gray-500 font-mono w-20">{activity.time}</span>
            <span className={`w-2 h-2 rounded-full ${activity.type === 'alert' ? 'bg-red-500' : 'bg-green-500'} animate-pulse`}></span>
            <span className="text-xs text-cyan-400 font-mono flex-1">{activity.message}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
