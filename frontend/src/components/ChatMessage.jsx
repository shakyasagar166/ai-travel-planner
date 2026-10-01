import React, { useState } from 'react';
import { User, Sparkles, ChevronDown, ChevronUp, CheckCircle, Clock, MapPin, Hotel, DollarSign } from 'lucide-react';

export default function ChatMessage({ message, onSelectItinerary }) {
  const isUser = message.sender === 'user';
  const [showSteps, setShowSteps] = useState(false);

  return (
    <div className={`flex gap-3 sm:gap-4 ${isUser ? 'justify-end' : 'justify-start'} mb-6`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-500 flex-shrink-0 flex items-center justify-center text-white shadow-md shadow-teal-500/20 mt-1">
          <Sparkles className="w-4 h-4" />
        </div>
      )}

      <div className={`max-w-[88%] sm:max-w-[78%] ${isUser ? 'items-end' : 'items-start'}`}>
        
        {/* Agent Step Execution Chips (Multi-Agent Trace) */}
        {!isUser && message.agent_steps && message.agent_steps.length > 0 && (
          <div className="mb-3">
            <button
              onClick={() => setShowSteps(!showSteps)}
              className="px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/25 text-[11px] font-medium text-teal-300 hover:bg-teal-500/20 transition flex items-center gap-1.5"
            >
              <CheckCircle className="w-3.5 h-3.5 text-teal-400" />
              <span>Multi-Agent Trace ({message.agent_steps.length} Steps Executed)</span>
              {showSteps ? <ChevronUp className="w-3 h-3 ml-1" /> : <ChevronDown className="w-3 h-3 ml-1" />}
            </button>

            {showSteps && (
              <div className="mt-2 p-3 rounded-xl bg-gray-900/90 border border-darkborder space-y-1.5 text-xs text-gray-300 shadow-inner">
                {message.agent_steps.map((step, idx) => (
                  <div key={idx} className="flex items-start gap-2 py-0.5 border-b border-gray-800/60 last:border-none">
                    <span className="font-mono text-[10px] uppercase px-1.5 py-0.5 rounded bg-teal-950 text-teal-400 border border-teal-800/40">
                      {step.agent?.replace('_', ' ')}
                    </span>
                    <span className="text-gray-300 leading-relaxed text-[11px]">{step.output}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Message Bubble */}
        <div
          className={`p-4 rounded-2xl text-sm leading-relaxed ${
            isUser
              ? 'bg-gradient-to-r from-teal-600 to-cyan-600 text-white rounded-br-none shadow-lg shadow-teal-900/20'
              : 'bg-darkcard border border-darkborder text-gray-200 rounded-bl-none shadow-md'
          }`}
        >
          <div className="whitespace-pre-wrap">{message.content}</div>

          {/* Quick Action If Itinerary Present */}
          {!isUser && message.itinerary && onSelectItinerary && (
            <div className="mt-4 pt-3 border-t border-darkborder flex items-center justify-between">
              <div className="text-xs text-teal-300 font-medium flex items-center gap-1.5">
                <MapPin className="w-3.5 h-3.5" />
                <span>{message.itinerary.destination} — {message.itinerary.days} Days Itinerary Ready</span>
              </div>
              <button
                onClick={() => onSelectItinerary(message.itinerary)}
                className="px-3 py-1 rounded-lg text-xs font-semibold bg-teal-500 text-white hover:bg-teal-400 transition shadow-sm"
              >
                View Full Itinerary →
              </button>
            </div>
          )}
        </div>

        <div className={`text-[10px] text-gray-500 mt-1 px-1 ${isUser ? 'text-right' : 'text-left'}`}>
          {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </div>
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-xl bg-gray-700 flex-shrink-0 flex items-center justify-center text-gray-200 mt-1">
          <User className="w-4 h-4" />
        </div>
      )}
    </div>
  );
}
