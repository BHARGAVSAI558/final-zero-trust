import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Logo from "./components/Logo";

export default function LandingPage() {
  const navigate = useNavigate();
  const [stats, setStats] = useState({ users: 0, threats: 0, uptime: "99.9%" });

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const res = await fetch("http://localhost:8000/realtime/stats");
        const data = await res.json();
        setStats({ users: data.total_users, threats: data.active_now, uptime: "99.9%" });
      } catch (err) {}
    };
    fetchStats();
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900">
      {/* Header */}
      <nav className="fixed w-full top-0 z-50 bg-black/80 backdrop-blur-lg border-b border-green-500/20">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <Logo size="sm" />
          <div className="flex gap-4">
            <button onClick={() => navigate("/login")} className="px-6 py-2 border-2 border-green-500 text-green-400 rounded-lg font-mono font-bold hover:bg-green-500 hover:text-black transition">
              LOGIN
            </button>
            <button onClick={() => navigate("/register")} className="px-6 py-2 bg-green-500 text-black rounded-lg font-mono font-bold hover:bg-green-400 transition">
              GET STARTED
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto text-center">
          <div className="mb-8">
            <Logo size="lg" />
          </div>
          <h1 className="text-6xl font-bold text-white mb-6 font-mono">
            Enterprise <span className="text-green-400">Zero Trust</span> Security
          </h1>
          <p className="text-xl text-gray-400 mb-8 max-w-3xl mx-auto">
            Real-time insider threat detection powered by AI-driven behavioral analytics. 
            Protect your organization with continuous verification and micro-segmentation.
          </p>
          <div className="flex gap-4 justify-center">
            <button onClick={() => navigate("/login")} className="px-8 py-4 bg-green-500 text-black rounded-lg font-mono font-bold text-lg hover:bg-green-400 transition shadow-lg shadow-green-500/50">
              START MONITORING →
            </button>
            <button className="px-8 py-4 border-2 border-green-500 text-green-400 rounded-lg font-mono font-bold text-lg hover:bg-green-500/10 transition">
              VIEW DEMO
            </button>
          </div>
        </div>
      </div>

      {/* Live Stats */}
      <div className="py-16 bg-black/50 border-y border-green-500/20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-green-400 mb-2 font-mono">{stats.users}+</div>
              <div className="text-gray-400 font-mono">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-cyan-400 mb-2 font-mono">{stats.threats}</div>
              <div className="text-gray-400 font-mono">Threats Blocked</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-green-400 mb-2 font-mono">{stats.uptime}</div>
              <div className="text-gray-400 font-mono">Uptime</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-white text-center mb-16 font-mono">
            Enterprise-Grade <span className="text-green-400">Security Features</span>
          </h2>
          <div className="grid grid-cols-3 gap-8">
            {[
              { icon: "🛡️", title: "Real-Time Monitoring", desc: "24/7 continuous surveillance with instant threat detection" },
              { icon: "🔍", title: "Behavioral Analytics", desc: "AI-powered UEBA with 10+ anomaly detection signals" },
              { icon: "🌐", title: "Micro-Segmentation", desc: "4-tier access control based on dynamic risk scores" },
              { icon: "⛓️", title: "Blockchain Audit", desc: "Immutable audit trail for compliance and forensics" },
              { icon: "📊", title: "Live Dashboards", desc: "Role-based views for Admin, HR, and Security teams" },
              { icon: "🚨", title: "Instant Alerts", desc: "Real-time notifications for critical security events" }
            ].map((feature, i) => (
              <div key={i} className="bg-gradient-to-br from-gray-800 to-gray-900 p-8 rounded-xl border-2 border-green-500/20 hover:border-green-500/50 transition">
                <div className="text-5xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-green-400 mb-3 font-mono">{feature.title}</h3>
                <p className="text-gray-400">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="py-20 px-6 bg-gradient-to-r from-green-900/20 to-cyan-900/20 border-y border-green-500/20">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-white mb-6 font-mono">
            Ready to Secure Your Organization?
          </h2>
          <p className="text-xl text-gray-400 mb-8">
            Join leading enterprises using Zero Trust architecture to protect against insider threats.
          </p>
          <button onClick={() => navigate("/register")} className="px-12 py-4 bg-green-500 text-black rounded-lg font-mono font-bold text-xl hover:bg-green-400 transition shadow-lg shadow-green-500/50">
            START FREE TRIAL →
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-8 px-6 bg-black border-t border-green-500/20">
        <div className="max-w-7xl mx-auto text-center text-gray-500 font-mono text-sm">
          © 2024 Zero Trust Security Platform. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
