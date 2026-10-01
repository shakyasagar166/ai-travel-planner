import React from 'react';
import { DollarSign, CheckCircle2, AlertTriangle, Hotel, Utensils, Navigation, Compass } from 'lucide-react';

export default function BudgetBreakdownCard({ breakdown, accommodation, destination }) {
  if (!breakdown) return null;

  const total = breakdown.total_estimated_cost_inr || 1;
  const stayPct = Math.round((breakdown.stay_cost_inr / total) * 100);
  const foodPct = Math.round((breakdown.food_cost_inr / total) * 100);
  const transitPct = Math.round((breakdown.transit_cost_inr / total) * 100);
  const activitiesPct = Math.round((breakdown.activities_cost_inr / total) * 100);

  const isWithin = breakdown.is_within_budget;
  const budgetLimit = breakdown.budget_limit_inr;

  return (
    <div className="p-5 rounded-2xl bg-darkcard border border-darkborder shadow-md space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
            <DollarSign className="w-4 h-4 text-teal-400" />
            Budget & Expense Breakdown
          </h3>
          <p className="text-xs text-gray-400">Deterministic calculation based on travel tier</p>
        </div>

        {budgetLimit > 0 && (
          <div
            className={`px-3 py-1 rounded-full text-xs font-semibold flex items-center gap-1.5 ${
              isWithin
                ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                : 'bg-amber-500/10 text-amber-400 border border-amber-500/30'
            }`}
          >
            {isWithin ? (
              <>
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Within Budget (Save ₹{Math.abs(breakdown.savings_or_excess_inr).toLocaleString()})</span>
              </>
            ) : (
              <>
                <AlertTriangle className="w-3.5 h-3.5" />
                <span>Exceeds by ₹{Math.abs(breakdown.savings_or_excess_inr).toLocaleString()}</span>
              </>
            )}
          </div>
        )}
      </div>

      {/* Total Display */}
      <div className="flex items-baseline justify-between p-3 rounded-xl bg-gray-900/60 border border-gray-800">
        <div>
          <span className="text-xs text-gray-400">Total Estimated Trip Cost</span>
          <div className="text-2xl font-black text-teal-300">
            ₹{breakdown.total_estimated_cost_inr?.toLocaleString() || 0}
          </div>
        </div>
        {budgetLimit > 0 && (
          <div className="text-right">
            <span className="text-xs text-gray-400">Your Target Budget</span>
            <div className="text-lg font-bold text-gray-300">₹{budgetLimit.toLocaleString()}</div>
          </div>
        )}
      </div>

      {/* Progress Bar */}
      <div className="space-y-1">
        <div className="h-3 w-full bg-gray-800 rounded-full overflow-hidden flex">
          <div style={{ width: `${stayPct}%` }} title={`Stay: ${stayPct}%`} className="bg-teal-500 transition-all duration-500" />
          <div style={{ width: `${foodPct}%` }} title={`Food: ${foodPct}%`} className="bg-amber-500 transition-all duration-500" />
          <div style={{ width: `${transitPct}%` }} title={`Transit: ${transitPct}%`} className="bg-blue-500 transition-all duration-500" />
          <div style={{ width: `${activitiesPct}%` }} title={`Activities: ${activitiesPct}%`} className="bg-purple-500 transition-all duration-500" />
        </div>
        <div className="flex justify-between text-[10px] text-gray-400 px-0.5">
          <span>Hotel: {stayPct}%</span>
          <span>Food: {foodPct}%</span>
          <span>Transit: {transitPct}%</span>
          <span>Activities: {activitiesPct}%</span>
        </div>
      </div>

      {/* Details Grid */}
      <div className="grid grid-cols-2 gap-2 text-xs">
        <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-gray-300">
            <Hotel className="w-3.5 h-3.5 text-teal-400" />
            <span>Stay / Hotel</span>
          </div>
          <span className="font-semibold text-white">₹{breakdown.stay_cost_inr?.toLocaleString()}</span>
        </div>

        <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-gray-300">
            <Utensils className="w-3.5 h-3.5 text-amber-400" />
            <span>Food & Dining</span>
          </div>
          <span className="font-semibold text-white">₹{breakdown.food_cost_inr?.toLocaleString()}</span>
        </div>

        <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-gray-300">
            <Navigation className="w-3.5 h-3.5 text-blue-400" />
            <span>Local Transit</span>
          </div>
          <span className="font-semibold text-white">₹{breakdown.transit_cost_inr?.toLocaleString()}</span>
        </div>

        <div className="p-2.5 rounded-lg bg-gray-900/40 border border-gray-800/80 flex items-center justify-between">
          <div className="flex items-center gap-1.5 text-gray-300">
            <Compass className="w-3.5 h-3.5 text-purple-400" />
            <span>Activities</span>
          </div>
          <span className="font-semibold text-white">₹{breakdown.activities_cost_inr?.toLocaleString()}</span>
        </div>
      </div>

      {/* Hotel Recommendation */}
      {accommodation && (
        <div className="pt-3 border-t border-darkborder flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-300">
              <Hotel className="w-4 h-4" />
            </div>
            <div>
              <div className="text-xs font-semibold text-white">{accommodation.name}</div>
              <div className="text-[10px] text-gray-400">{accommodation.tier} Tier • Rating {accommodation.rating}/5</div>
            </div>
          </div>
          <div className="text-right">
            <div className="text-xs font-bold text-teal-300">₹{accommodation.price_per_night_inr?.toLocaleString()}/night</div>
          </div>
        </div>
      )}
    </div>
  );
}
