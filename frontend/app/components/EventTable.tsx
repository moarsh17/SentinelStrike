"use client";

import { useEffect, useState } from "react";
import { fetchEvents } from "../../lib/apiClient";
import { Database, RefreshCw, AlertCircle } from "lucide-react";

export default function EventTable() {
  const [events, setEvents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadEvents = async () => {
    setLoading(true);
    try {
      const data = await fetchEvents();
      setEvents(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadEvents();
  }, []);

  return (
    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-2xl p-6 shadow-2xl overflow-hidden flex flex-col h-[500px]">
      <div className="flex justify-between items-center mb-6 shrink-0">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <Database className="text-blue-400" size={24} />
          Historical Event Log
        </h2>
        <button
          onClick={loadEvents}
          disabled={loading}
          className="p-2 hover:bg-slate-800 rounded-full transition-colors disabled:opacity-50 text-slate-300"
          title="Refresh Events"
        >
          <RefreshCw size={20} className={loading ? "animate-spin text-blue-400" : ""} />
        </button>
      </div>

      <div className="flex-1 overflow-auto rounded-xl border border-slate-700/50 custom-scrollbar">
        <table className="w-full text-left border-collapse">
          <thead className="bg-slate-800/80 sticky top-0 z-10 backdrop-blur-md">
            <tr>
              <th className="p-4 text-xs font-medium text-slate-400 uppercase tracking-wider">Time</th>
              <th className="p-4 text-xs font-medium text-slate-400 uppercase tracking-wider">Type</th>
              <th className="p-4 text-xs font-medium text-slate-400 uppercase tracking-wider">Source IP</th>
              <th className="p-4 text-xs font-medium text-slate-400 uppercase tracking-wider">Target IP</th>
              <th className="p-4 text-xs font-medium text-slate-400 uppercase tracking-wider">Severity</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {events.length === 0 && !loading && (
              <tr>
                <td colSpan={5} className="p-8 text-center text-slate-500">
                  <div className="flex flex-col items-center justify-center gap-2">
                    <AlertCircle size={32} className="opacity-50" />
                    <p>No historical events found in the database.</p>
                  </div>
                </td>
              </tr>
            )}
            {events.map((event) => (
              <tr key={event.id} className="hover:bg-slate-800/50 transition-colors">
                <td className="p-4 text-sm text-slate-300 whitespace-nowrap">
                  {new Date(event.detected_at).toLocaleString()}
                </td>
                <td className="p-4 text-sm font-medium text-white whitespace-nowrap">
                  {event.type}
                </td>
                <td className="p-4 text-sm font-mono text-cyan-400 whitespace-nowrap">
                  {event.src_ip}
                </td>
                <td className="p-4 text-sm font-mono text-fuchsia-400 whitespace-nowrap">
                  {event.dst_ip}{event.dst_port ? `:${event.dst_port}` : ''}
                </td>
                <td className="p-4 text-sm whitespace-nowrap">
                  <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                    event.severity === 'HIGH' ? 'bg-red-500/20 text-red-400' :
                    event.severity === 'MEDIUM' ? 'bg-amber-500/20 text-amber-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>
                    {event.severity}
                  </span>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
