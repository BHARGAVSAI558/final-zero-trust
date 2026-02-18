import { useEffect, useState } from "react";
import { getAuditChain } from "../api/api";


export default function AuditChain() {
  const [chain, setChain] = useState([]);

  useEffect(() => {
    getAuditChain().then(setChain);
  }, []);

  return (
    <div className="bg-slate-800 p-4 rounded-xl text-white">
      <h2 className="text-xl mb-3">⛓ Blockchain Audit Log</h2>

      <div className="space-y-3 max-h-96 overflow-y-auto text-sm">
        {chain.map((b) => (
          <div key={b.index} className="border border-slate-600 p-2 rounded">
            <div><b>Block:</b> {b.index}</div>
            <div><b>Time:</b> {b.timestamp}</div>
            <div className="truncate"><b>Hash:</b> {b.hash}</div>
            <div className="truncate"><b>Prev:</b> {b.prev_hash}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
