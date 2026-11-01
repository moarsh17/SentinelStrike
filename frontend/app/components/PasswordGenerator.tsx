"use client";

import { useState } from "react";
import { 
  generateMutatedPasswords, 
  applyWordlist, 
  PasswordMutationParams 
} from "../../lib/apiClient";
import { 
  BrainCircuit, 
  Sparkles, 
  Copy, 
  Check, 
  Download, 
  Sliders, 
  KeyRound, 
  ShieldCheck,
  Terminal,
  Layers
} from "lucide-react";

interface Candidate {
  password: string;
  pattern: string;
  entropy_bits: number;
  human_likelihood: number;
  base_token: string;
}

export default function PasswordGenerator() {
  const [brandTokens, setBrandTokens] = useState("Sentinel, Strike");
  const [userHandle, setUserHandle] = useState("admin");
  const [department, setDepartment] = useState("Security");
  const [year, setYear] = useState("2026");
  const [temperature, setTemperature] = useState(0.7);
  const [count, setCount] = useState(12);

  const [loading, setLoading] = useState(false);
  const [applying, setApplying] = useState(false);
  const [candidates, setCandidates] = useState<Candidate[]>([]);
  const [copiedIndex, setCopiedIndex] = useState<number | null>(null);
  const [applySuccess, setApplySuccess] = useState<string | null>(null);

  const handleGenerate = async () => {
    setLoading(true);
    setApplySuccess(null);
    try {
      const tokens = brandTokens
        .split(",")
        .map((t) => t.trim())
        .filter(Boolean);


      const params: PasswordMutationParams = {
        brand_tokens: tokens.length > 0 ? tokens : ["Sentinel", "Strike"],
        user_handle: userHandle || "admin",
        department: department || "Security",
        year: year || "2026",
        temperature: Number(temperature),
        count: Number(count),
      };

      const res = await generateMutatedPasswords(params);
      setCandidates(res.candidates || []);
    } catch (err) {
      console.error("Password generation failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyToWordlist = async () => {
    if (candidates.length === 0) return;
    setApplying(true);
    try {
      const pwds = candidates.map((c) => c.password);
      const res = await applyWordlist(pwds);
      setApplySuccess(res.message || "Wordlist updated successfully!");
      setTimeout(() => setApplySuccess(null), 5000);
    } catch (err) {
      console.error("Failed to apply wordlist:", err);
    } finally {
      setApplying(false);
    }
  };

  const handleCopy = (pwd: string, index: number) => {
    navigator.clipboard.writeText(pwd);
    setCopiedIndex(index);
    setTimeout(() => setCopiedIndex(null), 2000);
  };

  return (
    <div className="bg-slate-900/60 backdrop-blur-xl border border-slate-700/60 rounded-2xl p-6 shadow-2xl relative overflow-hidden">
      {/* Decorative ambient glow */}
      <div className="absolute top-0 right-0 w-72 h-72 bg-purple-600/10 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-3 mb-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-purple-500/10 border border-purple-500/20 text-purple-400">
            <BrainCircuit size={24} />
          </div>
          <div>
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              Credential AI Mutator
              <span className="text-[10px] font-mono uppercase bg-purple-500/20 border border-purple-500/30 text-purple-300 px-2 py-0.5 rounded-full">
                PassGAN & Char-RNN
              </span>
            </h2>
            <p className="text-xs text-slate-400">
              Probabilistic character transitions & structural pattern synthesis
            </p>
          </div>
        </div>

        {candidates.length > 0 && (
          <button
            onClick={handleApplyToWordlist}
            disabled={applying}
            className="flex items-center gap-2 px-3.5 py-1.5 text-xs font-medium rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 hover:bg-emerald-500/25 transition-all duration-200"
          >
            <Download size={14} className={applying ? "animate-bounce" : ""} />
            {applying ? "Injecting Wordlist..." : "Apply to Live Attack"}
          </button>
        )}
      </div>

      {applySuccess && (
        <div className="mb-4 p-3 bg-emerald-950/60 border border-emerald-500/40 rounded-xl text-xs text-emerald-300 flex items-center gap-2 animate-fadeIn">
          <ShieldCheck size={16} className="text-emerald-400" />
          <span>{applySuccess}</span>
        </div>
      )}

      {/* Input Form Controls */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <div>
          <label className="block text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-1.5">
            Brand / Keywords
          </label>
          <input
            type="text"
            value={brandTokens}
            onChange={(e) => setBrandTokens(e.target.value)}
            placeholder="Sentinel, Strike"
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-1.5">
            User Handle
          </label>
          <input
            type="text"
            value={userHandle}
            onChange={(e) => setUserHandle(e.target.value)}
            placeholder="admin"
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-1.5">
            Department
          </label>
          <input
            type="text"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            placeholder="Security"
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500 transition-colors"
          />
        </div>

        <div>
          <label className="block text-[11px] uppercase tracking-wider font-mono text-slate-400 mb-1.5">
            Target Year
          </label>
          <input
            type="text"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            placeholder="2026"
            className="w-full bg-slate-950/80 border border-slate-700/80 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500 transition-colors"
          />
        </div>
      </div>

      {/* Advanced Mutation Parameters */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-4 rounded-xl bg-slate-950/50 border border-slate-800/80 mb-6">
        <div className="flex-1 min-w-[200px]">
          <div className="flex items-center justify-between text-xs mb-1.5">
            <span className="text-slate-400 flex items-center gap-1.5">
              <Sliders size={13} className="text-purple-400" />
              Mutation Temperature (Creativity)
            </span>
            <span className="font-mono text-purple-300 font-semibold">{temperature}</span>
          </div>
          <input
            type="range"
            min="0.1"
            max="1.0"
            step="0.05"
            value={temperature}
            onChange={(e) => setTemperature(parseFloat(e.target.value))}
            className="w-full accent-purple-500 cursor-pointer h-1.5 bg-slate-800 rounded-lg"
          />
          <div className="flex justify-between text-[10px] text-slate-500 mt-1">
            <span>0.1 (Strict Patterns)</span>
            <span>1.0 (Adversarial Jitter)</span>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div>
            <label className="block text-[11px] text-slate-400 mb-1">Batch Count</label>
            <select
              value={count}
              onChange={(e) => setCount(parseInt(e.target.value))}
              className="bg-slate-900 border border-slate-700 rounded-lg px-2.5 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
            >
              <option value={8}>8 Passwords</option>
              <option value={12}>12 Passwords</option>
              <option value={16}>16 Passwords</option>
              <option value={24}>24 Passwords</option>
            </select>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="group relative self-end py-2 px-5 rounded-xl font-medium text-xs text-white bg-gradient-to-r from-purple-600 via-indigo-600 to-cyan-600 hover:from-purple-500 hover:to-cyan-500 focus:outline-none disabled:opacity-50 transition-all duration-300 shadow-[0_0_20px_rgba(147,51,234,0.3)] hover:shadow-[0_0_25px_rgba(147,51,234,0.5)] overflow-hidden"
          >
            <span className="flex items-center gap-1.5">
              <Sparkles size={15} className={loading ? "animate-spin" : ""} />
              {loading ? "Generating Mutated Tokens..." : "Synthesize Wordlist"}
            </span>
          </button>
        </div>
      </div>

      {/* Generated Candidates Output Grid */}
      {candidates.length > 0 ? (
        <div>
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-xs uppercase font-mono tracking-wider text-slate-400 flex items-center gap-1.5">
              <KeyRound size={14} className="text-purple-400" />
              Generated Candidate Corpus ({candidates.length})
            </h3>
            <span className="text-[10px] text-slate-500 font-mono">
              Entropy & Human Likelihood Scored
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-2.5 max-h-80 overflow-y-auto pr-1 custom-scrollbar">
            {candidates.map((c, idx) => (
              <div
                key={idx}
                className="group p-3 rounded-xl bg-slate-950/70 border border-slate-800 hover:border-purple-500/40 transition-all flex items-center justify-between"
              >
                <div className="flex-1 min-w-0 pr-3">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="font-mono text-sm font-semibold text-purple-200 truncate select-all">
                      {c.password}
                    </span>
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
                      {c.entropy_bits} bits
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-[11px] text-slate-400">
                    <span className="truncate text-slate-500">{c.pattern}</span>
                    <span className="text-slate-600">•</span>
                    <span className="text-emerald-400/90 font-mono text-[10px]">
                      {c.human_likelihood}% match
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => handleCopy(c.password, idx)}
                  className="p-1.5 rounded-lg bg-slate-800/80 hover:bg-purple-600/30 text-slate-400 hover:text-white transition-colors"
                  title="Copy password"
                >
                  {copiedIndex === idx ? (
                    <Check size={14} className="text-emerald-400" />
                  ) : (
                    <Copy size={14} />
                  )}
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className="text-center py-8 border border-dashed border-slate-800 rounded-xl">
          <Terminal size={28} className="mx-auto text-slate-600 mb-2" />
          <p className="text-xs text-slate-400">
            No candidates generated yet. Adjust target metadata and click{" "}
            <span className="text-purple-400 font-semibold">"Synthesize Wordlist"</span>.
          </p>
        </div>
      )}
    </div>
  );
}
