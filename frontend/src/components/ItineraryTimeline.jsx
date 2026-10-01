import React, { useState } from 'react';
import { Calendar, Sun, Sunset, Moon, Clock, Tag, IndianRupee, Lightbulb } from 'lucide-react';

export default function ItineraryTimeline({ daysPlan = [] }) {
  const [activeDayIndex, setActiveDayIndex] = useState(0);

  if (!daysPlan || daysPlan.length === 0) {
    return (
      <div className="p-8 text-center text-gray-400 bg-darkcard rounded-2xl border border-darkborder">
        No day-by-day plan available. Ask the agent to plan a trip!
      </div>
    );
  }

  const activeDay = daysPlan[activeDayIndex] || daysPlan[0];

  const renderSlot = (title, icon, slotData, colorClass) => {
    if (!slotData) return null;
    return (
      <div className="p-4 rounded-xl bg-gray-900/70 border border-darkborder hover:border-gray-700 transition">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <div className={`p-1.5 rounded-lg ${colorClass}`}>
              {icon}
            </div>
            <span className="text-xs font-semibold text-gray-300 uppercase tracking-wider">{title}</span>
          </div>
          <span className="text-[11px] font-mono text-gray-400 flex items-center gap-1">
            <Clock className="w-3 h-3" />
            {slotData.time}
          </span>
        </div>

        <h4 className="text-sm font-semibold text-white mb-1.5">{slotData.activity}</h4>

        <div className="flex flex-wrap items-center gap-2 mb-2 text-xs">
          <span className="px-2 py-0.5 rounded-md bg-teal-500/10 text-teal-300 border border-teal-500/20 flex items-center gap-1">
            <Tag className="w-3 h-3" />
            {slotData.category}
          </span>
          <span className="text-gray-400 flex items-center gap-1">
            <Clock className="w-3 h-3 text-gray-500" />
            {slotData.duration_hours} hrs
          </span>
          <span className="text-emerald-400 font-medium flex items-center">
            ₹{slotData.estimated_cost_inr > 0 ? slotData.estimated_cost_inr.toLocaleString() : 'Free Entry'}
          </span>
        </div>

        {slotData.tips && (
          <div className="mt-2 p-2 rounded-lg bg-gray-800/40 border border-gray-800 text-[11px] text-gray-300 flex items-start gap-1.5">
            <Lightbulb className="w-3.5 h-3.5 text-amber-400 flex-shrink-0 mt-0.5" />
            <span className="leading-snug">{slotData.tips}</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="space-y-4">
      {/* Day Selector Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-darkborder">
        {daysPlan.map((d, idx) => (
          <button
            key={idx}
            onClick={() => setActiveDayIndex(idx)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold transition whitespace-nowrap flex items-center gap-1.5 ${
              activeDayIndex === idx
                ? 'bg-gradient-to-r from-teal-500 to-cyan-500 text-white shadow-md shadow-teal-500/20'
                : 'bg-darkcard text-gray-400 hover:text-white border border-darkborder'
            }`}
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>Day {d.day}</span>
          </button>
        ))}
      </div>

      {/* Active Day Header */}
      <div className="flex items-center justify-between px-1">
        <div>
          <h3 className="text-base font-bold text-white">{activeDay.title}</h3>
          <p className="text-xs text-gray-400">Curated Morning, Afternoon & Evening Schedule</p>
        </div>
        <div className="text-right">
          <div className="text-xs text-gray-400">Day Estimated Cost</div>
          <div className="text-sm font-bold text-teal-300">₹{activeDay.day_total_cost_inr?.toLocaleString() || 0}</div>
        </div>
      </div>

      {/* Day Slots */}
      <div className="space-y-3">
        {renderSlot('Morning', <Sun className="w-4 h-4 text-amber-400" />, activeDay.morning, 'bg-amber-500/10 text-amber-400')}
        {renderSlot('Afternoon', <Sun className="w-4 h-4 text-orange-400" />, activeDay.afternoon, 'bg-orange-500/10 text-orange-400')}
        {renderSlot('Evening', <Moon className="w-4 h-4 text-indigo-400" />, activeDay.evening, 'bg-indigo-500/10 text-indigo-400')}
      </div>
    </div>
  );
}
