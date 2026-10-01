import React from 'react';
import { Compass, User, LogOut, Sliders, MapPin, Sparkles } from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export default function Navbar({ onOpenAuth, onOpenPrefs, onSelectDestinationsView, currentView }) {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 bg-darkcard/80 backdrop-blur-md border-b border-darkborder">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => onSelectDestinationsView('chat')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-500 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <Compass className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center gap-1.5">
              <span className="font-bold text-lg text-white tracking-tight">ShopAgent</span>
              <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-teal-500/20 text-teal-300 border border-teal-500/30">TRAVEL</span>
            </div>
            <p className="text-xs text-gray-400">Agentic AI Travel Planner</p>
          </div>
        </div>

        {/* Navigation Actions */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => onSelectDestinationsView(currentView === 'catalog' ? 'chat' : 'catalog')}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition flex items-center gap-1.5 border ${
              currentView === 'catalog'
                ? 'bg-teal-500/20 text-teal-300 border-teal-500/40'
                : 'text-gray-300 hover:text-white border-darkborder hover:bg-gray-800'
            }`}
          >
            <MapPin className="w-3.5 h-3.5" />
            <span>Destinations Catalog</span>
          </button>

          {user && (
            <button
              onClick={onOpenPrefs}
              className="px-3 py-1.5 rounded-lg text-xs font-medium text-gray-300 hover:text-white border border-darkborder hover:bg-gray-800 transition flex items-center gap-1.5"
            >
              <Sliders className="w-3.5 h-3.5 text-teal-400" />
              <span>Preferences</span>
            </button>
          )}

          {user ? (
            <div className="flex items-center gap-3 pl-2 border-l border-darkborder">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-teal-500/20 border border-teal-500/40 flex items-center justify-center text-teal-300 font-semibold text-xs">
                  {user.full_name?.charAt(0) || 'U'}
                </div>
                <div className="hidden sm:block text-left">
                  <div className="text-xs font-semibold text-white leading-tight">{user.full_name}</div>
                  <div className="text-[10px] text-gray-400">{user.email}</div>
                </div>
              </div>
              <button
                onClick={logout}
                title="Logout"
                className="p-1.5 rounded-lg text-gray-400 hover:text-red-400 hover:bg-red-500/10 transition"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <button
              onClick={onOpenAuth}
              className="px-4 py-2 rounded-lg text-xs font-semibold bg-gradient-to-r from-teal-500 to-cyan-500 text-white shadow-md shadow-teal-500/20 hover:brightness-110 transition flex items-center gap-1.5"
            >
              <User className="w-3.5 h-3.5" />
              <span>Sign In / Demo</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
}
