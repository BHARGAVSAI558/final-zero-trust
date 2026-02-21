import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

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
    <div className="min-h-screen bg-gray-50" style={{fontFamily: 'Inter, system-ui, -apple-system, sans-serif'}}>
      {/* Header */}
      <nav className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center text-white font-semibold text-sm">
              TC
            </div>
            <div>
              <h1 className="text-xl font-semibold text-gray-900">TechCorp Portal</h1>
              <p className="text-xs text-gray-500">Enterprise Platform</p>
            </div>
          </div>
          <div className="flex gap-3">
            <button onClick={() => navigate("/login")} className="px-6 py-2 bg-white border border-gray-300 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-50 transition-colors">
              Login
            </button>
            <button onClick={() => navigate("/register")} className="px-6 py-2 bg-gray-900 text-white text-sm font-medium rounded-lg hover:bg-gray-800 transition-colors">
              Register
            </button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <div className="py-20 px-6 bg-gradient-to-br from-blue-50 to-indigo-50">
        <div className="max-w-7xl mx-auto text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Enterprise <span className="text-blue-600">Business</span> Platform
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
            Streamline your business operations with our comprehensive enterprise platform. Manage documents, projects, employees, and financial reports all in one place.
          </p>
          <div className="flex gap-4 justify-center">
            <button onClick={() => navigate("/login")} className="px-8 py-4 bg-gray-900 text-white rounded-lg font-semibold text-lg hover:bg-gray-800 transition-colors shadow-md">
              Access Platform →
            </button>
          </div>
        </div>
      </div>

      {/* Stats */}
      <div className="py-16 bg-white border-y border-gray-200">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-5xl font-bold text-gray-900 mb-2">{stats.users}</div>
              <div className="text-gray-600">Active Users</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-gray-900 mb-2">{stats.threats}</div>
              <div className="text-gray-600">Live Sessions</div>
            </div>
            <div className="text-center">
              <div className="text-5xl font-bold text-gray-900 mb-2">{stats.uptime}</div>
              <div className="text-gray-600">System Uptime</div>
            </div>
          </div>
        </div>
      </div>

      {/* Features */}
      <div className="py-20 px-6">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-gray-900 text-center mb-16">
            Platform <span className="text-blue-600">Features</span>
          </h2>
          <div className="grid grid-cols-3 gap-6">
            {[
              { title: "Document Management", desc: "Secure file storage with access control and version tracking" },
              { title: "Project Tracking", desc: "Monitor project progress, budgets, and team collaboration" },
              { title: "Employee Directory", desc: "Centralized employee information and contact management" },
              { title: "Financial Reports", desc: "Comprehensive financial analytics and reporting tools" },
              { title: "Team Collaboration", desc: "Real-time collaboration tools for distributed teams" },
              { title: "Analytics Dashboard", desc: "Business intelligence and performance metrics" }
            ].map((feature, i) => (
              <div key={i} className="bg-white p-6 rounded-xl border border-gray-200 shadow-md hover:shadow-xl hover:border-blue-300 transition-all duration-300">
                <h3 className="text-lg font-semibold text-gray-900 mb-3">{feature.title}</h3>
                <p className="text-gray-600 text-sm">{feature.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* CTA */}
      <div className="py-20 px-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-y border-gray-200">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-4xl font-bold text-gray-900 mb-6">
            Transform Your Business
          </h2>
          <p className="text-xl text-gray-600 mb-8">
            Join leading enterprises using our platform to streamline operations.
          </p>
          <button onClick={() => navigate("/register")} className="px-12 py-4 bg-gray-900 text-white rounded-lg font-semibold text-xl hover:bg-gray-800 transition-colors shadow-lg">
            Get Started →
          </button>
        </div>
      </div>

      {/* Footer */}
      <footer className="py-8 px-6 bg-white border-t border-gray-200">
        <div className="max-w-7xl mx-auto text-center text-gray-500 text-sm">
          © 2024 TechCorp Portal. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
