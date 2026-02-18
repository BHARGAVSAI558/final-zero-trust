export default function Navbar({ onLogout }) {
  const user = localStorage.getItem("user");
  const role = localStorage.getItem("role");

  return (
    <div className="bg-black/90 backdrop-blur p-4 flex justify-between items-center border-b-2 border-green-900/50 shadow-lg shadow-green-900/20 sticky top-0 z-50">
      <h1 className="font-bold text-xl text-green-400 font-mono">🛡️ Zero Trust Platform</h1>
      <div className="flex items-center gap-4">
        <span className="text-sm font-mono">
          <span className="text-gray-500">User:</span> <span className="text-cyan-400 font-bold">{user}</span>
          <span className="ml-2 px-2 py-1 bg-green-900/50 border border-green-700 rounded text-xs text-green-400 font-bold">{role?.toUpperCase()}</span>
        </span>
        <button
          onClick={onLogout}
          className="bg-red-900 hover:bg-red-800 border-2 border-red-700 px-4 py-2 rounded text-sm font-bold font-mono text-red-100 transition"
        >
          LOGOUT
        </button>
      </div>
    </div>
  );
}
