import React from 'react';
import { MapPin, Calendar, DollarSign, Tag, ArrowRight } from 'lucide-react';

export default function DestinationCard({ destination, onSelectPlan }) {
  return (
    <div className="group rounded-2xl bg-darkcard border border-darkborder overflow-hidden hover:border-teal-500/50 hover:shadow-xl hover:shadow-teal-950/20 transition flex flex-col">
      {/* Cover Image */}
      <div className="relative h-44 w-full overflow-hidden bg-gray-900">
        <img
          src={destination.image_url || 'https://images.unsplash.com/photo-1488646953014-85cb44e25828?w=800'}
          alt={destination.name}
          className="w-full h-full object-cover group-hover:scale-105 transition duration-500"
          loading="lazy"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-darkcard via-transparent to-transparent" />
        <div className="absolute top-3 right-3 px-2.5 py-1 rounded-full bg-black/60 backdrop-blur-md border border-white/10 text-xs font-semibold text-teal-300">
          {destination.continent}
        </div>
      </div>

      {/* Content */}
      <div className="p-4 flex-1 flex flex-col justify-between space-y-3">
        <div>
          <div className="flex items-baseline justify-between mb-1">
            <h3 className="text-lg font-bold text-white group-hover:text-teal-300 transition">
              {destination.name}
            </h3>
            <span className="text-xs text-gray-400">{destination.country}</span>
          </div>

          <p className="text-xs text-gray-300 line-clamp-2 leading-relaxed mb-3">
            {destination.description}
          </p>

          <div className="space-y-1.5 text-xs text-gray-400">
            <div className="flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-amber-400" />
              <span>Best: {destination.best_season}</span>
            </div>
            <div className="flex items-center gap-1.5">
              <DollarSign className="w-3.5 h-3.5 text-emerald-400" />
              <span>Avg Daily: ₹{destination.avg_daily_budget_inr?.toLocaleString()}</span>
            </div>
          </div>
        </div>

        {/* Tags */}
        <div className="pt-2 border-t border-darkborder flex items-center justify-between">
          <div className="flex flex-wrap gap-1">
            {(destination.tags || []).slice(0, 3).map((tag, idx) => (
              <span key={idx} className="px-2 py-0.5 rounded bg-gray-800 text-[10px] text-gray-300">
                #{tag}
              </span>
            ))}
          </div>

          {onSelectPlan && (
            <button
              onClick={() => onSelectPlan(destination)}
              className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-teal-500/10 text-teal-300 hover:bg-teal-500 hover:text-white transition flex items-center gap-1"
            >
              <span>Plan Trip</span>
              <ArrowRight className="w-3 h-3" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
