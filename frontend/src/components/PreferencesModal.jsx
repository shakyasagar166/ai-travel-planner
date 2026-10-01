import React, { useState, useEffect } from 'react';
import { X, Sliders, Check, Compass, Shield } from 'lucide-react';
import { getUserPreferences, updateUserPreferences } from '../api/endpoints';

export default function PreferencesModal({ isOpen, onClose }) {
  const [style, setStyle] = useState('Balanced');
  const [tier, setTier] = useState('Moderate');
  const [diet, setDiet] = useState('Any');
  const [pace, setPace] = useState('Moderate');
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);

  useEffect(() => {
    if (isOpen) {
      getUserPreferences()
        .then((data) => {
          if (data) {
            setStyle(data.preferred_travel_style || 'Balanced');
            setTier(data.budget_tier || 'Moderate');
            setDiet(data.dietary_preferences || 'Any');
            setPace(data.pace_preference || 'Moderate');
          }
        })
        .catch((err) => console.log('Could not load preferences', err));
    }
  }, [isOpen]);

  if (!isOpen) return null;

  const handleSave = async () => {
    setLoading(true);
    try {
      await updateUserPreferences({
        preferred_travel_style: style,
        budget_tier: tier,
        dietary_preferences: diet,
        pace_preference: pace,
      });
      setSuccess(true);
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1000);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-sm">
      <div className="relative w-full max-w-md rounded-2xl bg-darkcard border border-darkborder shadow-2xl p-6">
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-1.5 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition"
        >
          <X className="w-5 h-5" />
        </button>

        <div className="flex items-center gap-2.5 mb-5">
          <div className="p-2 rounded-xl bg-teal-500/10 text-teal-400 border border-teal-500/25">
            <Sliders className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-base font-bold text-white">Traveler Preferences</h2>
            <p className="text-xs text-gray-400">Personalize AI itinerary and recommendations</p>
          </div>
        </div>

        {success && (
          <div className="mb-4 p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-xs text-emerald-400 flex items-center gap-2">
            <Check className="w-4 h-4" />
            <span>Preferences saved successfully!</span>
          </div>
        )}

        <div className="space-y-4 text-xs">
          {/* Travel Style */}
          <div>
            <label className="block font-medium text-gray-300 mb-1.5">Travel Style</label>
            <div className="grid grid-cols-2 gap-2">
              {['Balanced', 'Adventure', 'Relaxed', 'Cultural', 'Foodie'].map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => setStyle(opt)}
                  className={`p-2 rounded-xl border text-center transition font-medium ${
                    style === opt
                      ? 'bg-teal-500/20 border-teal-500 text-teal-300'
                      : 'bg-gray-900 border-darkborder text-gray-400 hover:text-white'
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          {/* Budget Tier */}
          <div>
            <label className="block font-medium text-gray-300 mb-1.5">Default Budget Tier</label>
            <div className="grid grid-cols-3 gap-2">
              {['Budget', 'Moderate', 'Luxury'].map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => setTier(opt)}
                  className={`p-2 rounded-xl border text-center transition font-medium ${
                    tier === opt
                      ? 'bg-teal-500/20 border-teal-500 text-teal-300'
                      : 'bg-gray-900 border-darkborder text-gray-400 hover:text-white'
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          {/* Pace */}
          <div>
            <label className="block font-medium text-gray-300 mb-1.5">Itinerary Pacing</label>
            <div className="grid grid-cols-3 gap-2">
              {['Relaxed', 'Moderate', 'Fast-paced'].map((opt) => (
                <button
                  key={opt}
                  type="button"
                  onClick={() => setPace(opt)}
                  className={`p-2 rounded-xl border text-center transition font-medium ${
                    pace === opt
                      ? 'bg-teal-500/20 border-teal-500 text-teal-300'
                      : 'bg-gray-900 border-darkborder text-gray-400 hover:text-white'
                  }`}
                >
                  {opt}
                </button>
              ))}
            </div>
          </div>

          {/* Diet */}
          <div>
            <label className="block font-medium text-gray-300 mb-1.5">Dietary & Food Habits</label>
            <input
              type="text"
              value={diet}
              onChange={(e) => setDiet(e.target.value)}
              placeholder="e.g. Vegetarian, Street food, Halal"
              className="w-full px-3 py-2 rounded-xl bg-gray-900 border border-darkborder text-white text-xs placeholder-gray-500 focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        <button
          onClick={handleSave}
          disabled={loading}
          className="w-full mt-6 py-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-cyan-500 text-white text-xs font-bold shadow-md shadow-teal-500/25 hover:brightness-110 transition"
        >
          {loading ? 'Saving...' : 'Apply & Save Preferences'}
        </button>
      </div>
    </div>
  );
}
