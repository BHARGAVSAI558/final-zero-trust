export default function RiskBadge({ decision }) {
  const map = {
    ALLOW: "bg-green-500",
    RESTRICT: "bg-yellow-500",
    DENY: "bg-red-600",
  };

  return (
    <span className={`px-3 py-1 rounded text-black font-bold ${map[decision]}`}>
      {decision}
    </span>
  );
}
