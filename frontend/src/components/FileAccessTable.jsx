import { useEffect, useState } from "react";
import { getFileAccessLogs } from "../api/api";


export default function FileAccessTable() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    getFileAccessLogs().then(setLogs);
  }, []);

  return (
    <div className="bg-slate-800 p-4 rounded-xl text-white">
      <h2 className="text-xl mb-3">📁 Sensitive File Access</h2>

      <table className="w-full text-xs">
        <thead className="bg-slate-700">
          <tr>
            <th>User</th>
            <th>File</th>
            <th>Action</th>
            <th>IP</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((l, i) => (
            <tr key={i} className="border-t border-slate-600">
              <td>{l.user_id}</td>
              <td className="text-red-400">{l.file_name}</td>
              <td>{l.action}</td>
              <td>{l.ip_address}</td>
              <td>{l.access_time}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
