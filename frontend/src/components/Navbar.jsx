export default function Navbar({ onLogout }) {
  const user = localStorage.getItem("user");
  const role = localStorage.getItem("role");

  return (
    <div className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-6 py-3 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center text-white font-semibold text-sm">
            ZT
          </div>
          <h1 className="text-lg font-semibold text-gray-900">Zero Trust Platform</h1>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-sm">
            <span className="text-gray-500">User:</span> <span className="text-gray-900 font-medium">{user}</span>
            <span className="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs font-medium">{role?.toUpperCase()}</span>
          </div>
          <button
            onClick={onLogout}
            className="bg-gray-900 hover:bg-gray-800 px-4 py-2 rounded-lg text-sm font-medium text-white transition-colors"
          >
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
