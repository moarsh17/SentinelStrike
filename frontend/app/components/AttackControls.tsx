"use client";

import { useState } from "react";
import { triggerNmapScan, triggerSshBruteforce } from "../../lib/apiClient";
import { Zap, ShieldAlert, Activity, Skull, Terminal } from "lucide-react";

export default function AttackControls() {
  const [loadingNmap, setLoadingNmap] = useState(false);
  const [loadingSsh, setLoadingSsh] = useState(false);
  const [result, setResult] = useState<any>(null);

  const handleNmap = async () => {
    setLoadingNmap(true);
    setResult(null);
    try {
      const data = await triggerNmapScan();
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ error: "Failed to trigger scan" });
    } finally {
      setLoadingNmap(false);
    }
  };

  const handleSsh = async () => {
    setLoadingSsh(true);
    setResult(null);
    try {
      const data = await triggerSshBruteforce(2222);
      setResult(data);
    } catch (error) {
      console.error(error);
      setResult({ error: "Failed to trigger SSH brute-force attack" });
    } finally {
      setLoadingSsh(false);
    }
  };

  const isBusy = loadingNmap || loadingSsh;

  return (
    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl">
      <h2 className="text-xl font-semibold text-white mb-6 flex items-center justify-between">
        <span className="flex items-center gap-2">
          <Activity className="text-cyan-400" size={24} />
          Offensive Controller
        </span>
        <span className="text-xs font-mono uppercase px-2.5 py-1 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400">
          Target: 127.0.0.1:2222
        </span>
      </h2>
      
      <div className="flex flex-col gap-4">
        {/* Nmap Scan Trigger */}
        <button
          onClick={handleNmap}
          disabled={isBusy}
          className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-xl text-white bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-cyan-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-[0_0_20px_rgba(8,145,178,0.3)] hover:shadow-[0_0_30px_rgba(8,145,178,0.5)] overflow-hidden"
        >
          <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
          <span className="flex items-center gap-2">
            <Zap size={18} className={loadingNmap ? "animate-pulse" : ""} />
            {loadingNmap ? "Launching Nmap Scan..." : "Launch Nmap Recon Scan"}
          </span>
        </button>

        {/* SSH Brute-Force Trigger */}
        <button
          onClick={handleSsh}
          disabled={isBusy}
          className="group relative w-full flex justify-center py-3 px-4 border border-rose-500/40 text-sm font-medium rounded-xl text-white bg-gradient-to-r from-rose-700 via-red-600 to-orange-600 hover:from-rose-600 hover:via-red-500 hover:to-orange-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-rose-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 shadow-[0_0_20px_rgba(225,29,72,0.3)] hover:shadow-[0_0_30px_rgba(225,29,72,0.5)] overflow-hidden"
        >
          <div className="absolute inset-0 w-full h-full bg-gradient-to-r from-transparent via-white/10 to-transparent -translate-x-full group-hover:animate-[shimmer_1.5s_infinite]" />
          <span className="flex items-center gap-2">
            <Skull size={18} className={loadingSsh ? "animate-spin" : ""} />
            {loadingSsh ? "Executing SSH Brute-force..." : "Launch SSH Brute-force Attack"}
          </span>
        </button>
      </div>

      {result && (
        <div className="mt-6 p-4 bg-slate-950 rounded-xl border border-slate-800">
          <div className="flex items-center justify-between mb-2">
            <h3 className="text-xs uppercase font-mono tracking-wider text-slate-400 flex items-center gap-1.5">
              <Terminal size={14} className="text-cyan-400" />
              Attack Execution Output
            </h3>
            <span className="text-[10px] font-mono text-slate-500">
              {result.tool || (result.status === "completed" ? "Completed" : "Response")}
            </span>
          </div>
          <pre className="text-xs text-emerald-400 overflow-x-auto whitespace-pre-wrap max-h-56 scrollbar-thin">
            {typeof result === "string" ? result : JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
