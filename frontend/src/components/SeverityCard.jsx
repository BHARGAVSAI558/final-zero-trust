export default function SeverityCard({ score }) {
  const color =
    score >= 70 ? "border-red-500" :
    score >= 40 ? "border-yellow-400" :
    "border-green-400";

  return (
    <div className={`border-l-4 ${color} bg-slate-800 p-4 rounded`}>
      <h3 className="text-lg font-bold">Risk Score</h3>
      <p className="text-2xl">{score}</p>
    </div>
  );
}
