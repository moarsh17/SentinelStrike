import AttackControls from "./components/AttackControls";
import EventFeed from "./components/EventFeed";
import EventTable from "./components/EventTable";
import { ShieldCheck } from "lucide-react";

export default function Home() {
  return (
    <main className="min-h-screen bg-[#050B14] text-slate-200 p-4 md:p-8 font-sans selection:bg-cyan-500/30">
      <div className="max-w-7xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center gap-4 border-b border-slate-800 pb-6">
          <div className="relative">
            <div className="absolute inset-0 bg-cyan-500 blur-xl opacity-20 rounded-full animate-pulse"></div>
            <div className="bg-slate-900 border border-slate-700 p-3 rounded-2xl relative shadow-lg">
              <ShieldCheck className="text-cyan-400" size={32} />
            </div>
          </div>
          <div>
            <h1 className="text-3xl font-extrabold tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
              SentinelStrike
            </h1>
            <p className="text-slate-400 text-sm mt-1">
              Automated Network Attack Simulation & Real-Time IDS
            </p>
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Left Column: Controls & Feed */}
          <div className="lg:col-span-1 space-y-8 flex flex-col">
            <AttackControls />
            <EventFeed />
          </div>

          {/* Right Column: Historical Table */}
          <div className="lg:col-span-2 flex flex-col">
            <EventTable />
          </div>

        </div>
      </div>

      {/* Global custom styles for scrollbar and animations */}
      <style dangerouslySetInnerHTML={{__html: `
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
          height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(30, 41, 59, 0.5);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(71, 85, 105, 0.8);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(100, 116, 139, 1);
        }
        @keyframes slideIn {
          from { opacity: 0; transform: translateY(-10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        @keyframes shimmer {
          100% { transform: translateX(100%); }
        }
      `}} />
    </main>
  );
}
