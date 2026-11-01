"use client";

import { useEffect, useState } from "react";
import { createWebSocketConnection } from "../../lib/wsClient";
import { RadioReceiver, AlertTriangle, Info, Skull } from "lucide-react";

export default function EventFeed() {
  const [events, setEvents] = useState<any[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = createWebSocketConnection((data) => {
      setEvents((prev) => [data, ...prev].slice(0, 50)); // Keep last 50 events
    });

    ws.onopen = () => setConnected(true);
    ws.onclose = () => setConnected(false);

    return () => {
      ws.close();
    };
  }, []);

  const getSeverityIcon = (severity: string) => {
    switch (severity?.toUpperCase()) {
      case "HIGH":
        return <Skull className="text-red-500 shrink-0" size={20} />;
      case "MEDIUM":
        return <AlertTriangle className="text-amber-500 shrink-0" size={20} />;
      default:
        return <Info className="text-blue-500 shrink-0" size={20} />;
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity?.toUpperCase()) {
      case "HIGH":
        return "border-red-500/50 bg-red-500/10 text-red-200";
      case "MEDIUM":
        return "border-amber-500/50 bg-amber-500/10 text-amber-200";
      default:
        return "border-blue-500/50 bg-blue-500/10 text-blue-200";
    }
  };

  return (
    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl h-[500px] flex flex-col">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <RadioReceiver className="text-fuchsia-400" size={24} />
          Live Threat Feed
        </h2>
        <div className="flex items-center gap-2">
          <span className="relative flex h-3 w-3">
            {connected && (
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            )}
            <span className={`relative inline-flex rounded-full h-3 w-3 ${connected ? 'bg-emerald-500' : 'bg-rose-500'}`}></span>
          </span>
          <span className="text-sm text-slate-400">
            {connected ? "IDS Active" : "Disconnected"}
          </span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2 custom-scrollbar">
        {events.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-slate-500 gap-3">
            <RadioReceiver size={48} className="opacity-20" />
            <p>Listening for malicious traffic...</p>
          </div>
        ) : (
          events.map((event, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl border ${getSeverityColor(event.severity)} animate-[slideIn_0.3s_ease-out_forwards] backdrop-blur-sm`}
            >
              <div className="flex items-start gap-3">
                {getSeverityIcon(event.severity)}
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start">
                    <p className="text-sm font-bold truncate">
                      {event.type}
                    </p>
                    <span className="text-xs opacity-60 shrink-0">
                      {new Date(event.detected_at).toLocaleTimeString()}
                    </span>
                  </div>
                  <p className="text-xs mt-1 opacity-80">
                    <span className="font-mono text-cyan-300">{event.src_ip}</span> 
                    {" → "} 
                    <span className="font-mono text-fuchsia-300">{event.dst_ip}</span>
                    {event.dst_port && `:${event.dst_port}`}
                  </p>
                  <p className="text-xs mt-2 opacity-90">
                    {event.details}
                  </p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
