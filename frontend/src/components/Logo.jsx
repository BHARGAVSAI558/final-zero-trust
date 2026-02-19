export default function Logo({ size = "md" }) {
  const sizes = { sm: "w-8 h-8 text-2xl", md: "w-12 h-12 text-4xl", lg: "w-16 h-16 text-5xl" };
  return (
    <div className="flex items-center gap-3">
      <div className={`${sizes[size]} bg-gradient-to-br from-green-500 to-cyan-500 rounded-lg flex items-center justify-center border-2 border-green-400 shadow-lg shadow-green-500/50 animate-pulse`}>
        <span className="text-black font-bold">⚡</span>
      </div>
      <div className="font-mono">
        <div className="text-green-400 font-bold text-xl tracking-wider">ZERO TRUST</div>
        <div className="text-cyan-400 text-xs">SOC PLATFORM</div>
      </div>
    </div>
  );
}
