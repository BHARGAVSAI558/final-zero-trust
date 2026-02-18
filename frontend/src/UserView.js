import { useEffect, useState } from "react";

function UserView() {
  const user = localStorage.getItem("user");
  const [record, setRecord] = useState(null);

  const fetchStatus = async () => {
    const res = await fetch("http://127.0.0.1:8000/security/analyze");
    const data = await res.json();
    const me = data.find((d) => d.user === user);
    setRecord(me);
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const logout = () => {
    localStorage.clear();
    window.location.reload();
  };

  if (!record)
    return (
      <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
        Loading security status...
      </div>
    );

  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center">
      <div className="bg-slate-800 p-8 rounded-xl w-96 text-center">
        <h2 className="text-xl font-bold mb-4">
          🔐 Zero Trust Access Status
        </h2>

        <p className="mb-2">User: <b>{user}</b></p>
        <p className="mb-2">Risk Score: <b>{record.risk_score}</b></p>

        <div
          className={`py-2 rounded font-bold mb-4 ${
            record.decision === "DENY"
              ? "bg-red-600"
              : record.decision === "RESTRICTED"
              ? "bg-yellow-500 text-black"
              : "bg-green-600"
          }`}
        >
          {record.decision}
        </div>

        <p className="text-sm text-slate-300 mb-4">
          Signals: {record.signals.join(", ")}
        </p>

        <button
          onClick={logout}
          className="bg-red-500 px-4 py-2 rounded font-bold"
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default UserView;
