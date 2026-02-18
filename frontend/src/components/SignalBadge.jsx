export default function SignalBadge({ label }) {
  return (
    <span className="bg-red-900/40 text-red-300 px-2 py-1 rounded text-xs mr-1">
      {label}
    </span>
  );
}
