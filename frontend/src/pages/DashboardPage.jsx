import React, { useState, useEffect, useRef } from 'react';
import {
  Send, Sparkles, Compass, MapPin, Calendar, DollarSign,
  CheckCircle, AlertCircle, RefreshCw, Luggage, Lightbulb,
  Search, Filter, ChevronRight
} from 'lucide-react';
import { sendChatMessage, getDestinations } from '../api/endpoints';
import ChatMessage from '../components/ChatMessage';
import ItineraryTimeline from '../components/ItineraryTimeline';
import BudgetBreakdownCard from '../components/BudgetBreakdownCard';
import DestinationCard from '../components/DestinationCard';

export default function DashboardPage({ currentView, onSwitchView }) {
  // Chat State
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'assistant',
      content: "👋 Hello! I am your **Autonomous AI Travel Planner**. Tell me your dream trip in plain words:\n\n*Example:* *\"Plan a 4-day budget trip to Goa for 2 people with ₹35,000 budget. We love beaches, water sports, and sunset shacks.\"*",
      agent_steps: [],
      itinerary: null,
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeItinerary, setActiveItinerary] = useState(null);
  const [activeSideTab, setActiveSideTab] = useState('schedule'); // schedule, budget, tips

  // Catalog State
  const [destinations, setDestinations] = useState([]);
  const [catalogSearch, setCatalogSearch] = useState('');
  const [selectedContinent, setSelectedContinent] = useState('All');
  const [catalogLoading, setCatalogLoading] = useState(false);

  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Load destinations catalog
  useEffect(() => {
    setCatalogLoading(true);
    getDestinations()
      .then((data) => setDestinations(data))
      .catch((err) => console.error("Could not load destinations", err))
      .finally(() => setCatalogLoading(false));
  }, []);

  const handleSend = async (textToSend) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = {
      id: Date.now().toString(),
      sender: 'user',
      content: query,
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await sendChatMessage(query);
      const asstMsg = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        content: res.response,
        agent_steps: res.agent_steps || [],
        itinerary: res.itinerary || null,
      };

      setMessages((prev) => [...prev, asstMsg]);
      if (res.itinerary) {
        setActiveItinerary(res.itinerary);
      }
    } catch (err) {
      console.error(err);
      setMessages((prev) => [
        ...prev,
        {
          id: (Date.now() + 1).toString(),
          sender: 'assistant',
          content: "❌ Sorry, I encountered an issue processing your travel request. Please make sure the backend server is running and try again.",
          agent_steps: [],
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handlePromptPillClick = (promptText) => {
    if (currentView === 'catalog') {
      onSwitchView('chat');
    }
    handleSend(promptText);
  };

  const handlePlanFromCard = (dest) => {
    onSwitchView('chat');
    handleSend(`Plan a 4-day balanced trip to ${dest.name} with sightseeing, famous food, and comfortable hotel stay.`);
  };

  // Filtered destinations
  const filteredDestinations = destinations.filter((d) => {
    const matchesSearch =
      d.name.toLowerCase().includes(catalogSearch.toLowerCase()) ||
      d.city.toLowerCase().includes(catalogSearch.toLowerCase()) ||
      d.country.toLowerCase().includes(catalogSearch.toLowerCase());
    const matchesContinent =
      selectedContinent === 'All' || d.continent.toLowerCase() === selectedContinent.toLowerCase();
    return matchesSearch && matchesContinent;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      
      {/* ===================== VIEW 1: DESTINATION CATALOG ===================== */}
      {currentView === 'catalog' ? (
        <div className="space-y-6">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div>
              <h1 className="text-2xl font-black text-white flex items-center gap-2">
                <Compass className="w-7 h-7 text-teal-400" />
                Explore Global & Indian Destinations
              </h1>
              <p className="text-xs text-gray-400 mt-0.5">
                Browse our curated catalog of destinations powered by vector RAG knowledge and local insights
              </p>
            </div>

            {/* Search & Continent Filters */}
            <div className="flex flex-wrap items-center gap-3">
              <div className="relative">
                <Search className="w-4 h-4 text-gray-500 absolute left-3 top-3" />
                <input
                  type="text"
                  value={catalogSearch}
                  onChange={(e) => setCatalogSearch(e.target.value)}
                  placeholder="Search city, country..."
                  className="pl-9 pr-3 py-2 rounded-xl bg-darkcard border border-darkborder text-xs text-white placeholder-gray-500 focus:outline-none focus:border-teal-500 w-52"
                />
              </div>

              <div className="flex items-center gap-1.5 p-1 rounded-xl bg-darkcard border border-darkborder text-xs">
                {['All', 'Asia', 'Europe'].map((cont) => (
                  <button
                    key={cont}
                    onClick={() => setSelectedContinent(cont)}
                    className={`px-3 py-1 rounded-lg font-medium transition ${
                      selectedContinent === cont
                        ? 'bg-teal-500 text-white shadow-sm'
                        : 'text-gray-400 hover:text-white'
                    }`}
                  >
                    {cont}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Grid */}
          {catalogLoading ? (
            <div className="text-center py-16 text-gray-400 flex items-center justify-center gap-2">
              <RefreshCw className="w-5 h-5 animate-spin text-teal-400" />
              <span>Loading destinations catalog...</span>
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
              {filteredDestinations.map((dest) => (
                <DestinationCard
                  key={dest.id}
                  destination={dest}
                  onSelectPlan={handlePlanFromCard}
                />
              ))}
            </div>
          )}
        </div>
      ) : (
        /* ===================== VIEW 2: AI CHAT & INTERACTIVE WORKSPACE ===================== */
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* Left Column: Chat Assistant (5 cols on lg) */}
          <div className="lg:col-span-6 flex flex-col h-[calc(100vh-130px)] rounded-2xl bg-darkcard/50 border border-darkborder overflow-hidden">
            
            {/* Header with Quick Suggestion Pills */}
            <div className="p-4 border-b border-darkborder bg-darkcard/80 space-y-2.5">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-teal-400" />
                  <span className="text-xs font-bold text-white tracking-wide uppercase">AI Travel Assistant</span>
                </div>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                  LangGraph Active
                </span>
              </div>

              {/* Quick Pills */}
              <div className="flex items-center gap-2 overflow-x-auto pb-1">
                {[
                  "🏖️ 4-day Goa trip under ₹35,000 for 2",
                  "🏔️ 5-day snow & adventure in Manali",
                  "🌸 4 days in Tokyo for foodie & anime",
                  "🗼 3 romantic days in Paris",
                  "🏝️ 5 days in Bali for relaxation"
                ].map((pill, idx) => (
                  <button
                    key={idx}
                    onClick={() => handlePromptPillClick(pill.replace(/^[^\s]+\s/, ''))}
                    className="px-2.5 py-1 rounded-full bg-gray-800/80 hover:bg-teal-500/20 hover:border-teal-500/40 border border-gray-700/60 text-[11px] text-gray-300 hover:text-teal-300 transition whitespace-nowrap flex-shrink-0"
                  >
                    {pill}
                  </button>
                ))}
              </div>
            </div>

            {/* Chat Messages Feed */}
            <div className="flex-1 p-4 overflow-y-auto space-y-1">
              {messages.map((msg) => (
                <ChatMessage
                  key={msg.id}
                  message={msg}
                  onSelectItinerary={(itinerary) => setActiveItinerary(itinerary)}
                />
              ))}

              {loading && (
                <div className="flex items-center gap-3 p-4 rounded-2xl bg-darkcard border border-darkborder max-w-[85%] text-xs text-gray-300">
                  <div className="w-6 h-6 rounded-lg bg-teal-500/20 flex items-center justify-center text-teal-400 animate-spin">
                    <RefreshCw className="w-3.5 h-3.5" />
                  </div>
                  <div>
                    <div className="font-semibold text-white">Agentic Orchestration in Progress...</div>
                    <div className="text-[11px] text-teal-400 animate-pulse">
                      Analyzing specs • Querying catalog • Running RAG knowledge • Scheduling days
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Chat Input Bar */}
            <div className="p-3 border-t border-darkborder bg-darkcard">
              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleSend();
                }}
                className="flex items-center gap-2"
              >
                <input
                  type="text"
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Describe your trip: destination, days, budget, interests..."
                  disabled={loading}
                  className="flex-1 px-4 py-2.5 rounded-xl bg-gray-900 border border-darkborder text-xs text-white placeholder-gray-500 focus:outline-none focus:border-teal-500 transition disabled:opacity-50"
                />
                <button
                  type="submit"
                  disabled={loading || !input.trim()}
                  className="p-2.5 rounded-xl bg-gradient-to-r from-teal-500 to-cyan-500 text-white hover:brightness-110 transition shadow-md shadow-teal-500/20 disabled:opacity-40"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>
          </div>

          {/* Right Column: Interactive Itinerary Workspace (6 cols on lg) */}
          <div className="lg:col-span-6 flex flex-col h-[calc(100vh-130px)] rounded-2xl bg-darkcard/50 border border-darkborder overflow-hidden">
            
            {activeItinerary ? (
              <div className="flex-1 flex flex-col overflow-hidden">
                
                {/* Destination Hero Header */}
                <div className="p-4 border-b border-darkborder bg-gradient-to-r from-teal-950/40 via-darkcard to-darkcard">
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-xl font-black text-white tracking-tight">
                          {activeItinerary.destination}
                        </span>
                        <span className="px-2 py-0.5 rounded-md bg-teal-500/20 text-teal-300 text-[10px] font-bold border border-teal-500/30">
                          {activeItinerary.days} DAYS
                        </span>
                      </div>
                      <p className="text-xs text-gray-400 mt-0.5">
                        Style: <span className="text-gray-300">{activeItinerary.travel_style}</span> • {activeItinerary.travelers_count} Traveler{activeItinerary.travelers_count > 1 ? 's' : ''} • Pacing: {activeItinerary.pace}
                      </p>
                    </div>

                    <div className="text-right">
                      <div className="text-[10px] text-gray-400 uppercase">Estimated Budget</div>
                      <div className="text-base font-black text-teal-300">
                        ₹{activeItinerary.cost_breakdown?.total_estimated_cost_inr?.toLocaleString() || 0}
                      </div>
                    </div>
                  </div>

                  {/* Sub-tabs: Schedule, Budget, Tips */}
                  <div className="flex items-center gap-2 mt-3 pt-3 border-t border-darkborder/70 text-xs">
                    <button
                      onClick={() => setActiveSideTab('schedule')}
                      className={`px-3 py-1 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                        activeSideTab === 'schedule'
                          ? 'bg-teal-500 text-white shadow-sm'
                          : 'text-gray-400 hover:text-white bg-gray-900 border border-darkborder'
                      }`}
                    >
                      <Calendar className="w-3.5 h-3.5" />
                      <span>Day Schedule</span>
                    </button>

                    <button
                      onClick={() => setActiveSideTab('budget')}
                      className={`px-3 py-1 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                        activeSideTab === 'budget'
                          ? 'bg-teal-500 text-white shadow-sm'
                          : 'text-gray-400 hover:text-white bg-gray-900 border border-darkborder'
                      }`}
                    >
                      <DollarSign className="w-3.5 h-3.5" />
                      <span>Budget Breakdown</span>
                    </button>

                    <button
                      onClick={() => setActiveSideTab('tips')}
                      className={`px-3 py-1 rounded-lg font-semibold transition flex items-center gap-1.5 ${
                        activeSideTab === 'tips'
                          ? 'bg-teal-500 text-white shadow-sm'
                          : 'text-gray-400 hover:text-white bg-gray-900 border border-darkborder'
                      }`}
                    >
                      <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                      <span>Insider Tips & Packing</span>
                    </button>
                  </div>
                </div>

                {/* Sub-tab Contents */}
                <div className="flex-1 p-4 overflow-y-auto space-y-4">
                  {activeSideTab === 'schedule' && (
                    <ItineraryTimeline daysPlan={activeItinerary.days_plan} />
                  )}

                  {activeSideTab === 'budget' && (
                    <BudgetBreakdownCard
                      breakdown={activeItinerary.cost_breakdown}
                      accommodation={activeItinerary.accommodation}
                      destination={activeItinerary.destination}
                    />
                  )}

                  {activeSideTab === 'tips' && (
                    <div className="space-y-4">
                      {/* Insider Tips */}
                      <div className="p-4 rounded-xl bg-darkcard border border-darkborder space-y-2.5">
                        <div className="flex items-center gap-2 text-amber-400 text-xs font-bold uppercase tracking-wider">
                          <Lightbulb className="w-4 h-4" />
                          <span>Local Insights & Advisories</span>
                        </div>
                        <ul className="space-y-2 text-xs text-gray-300">
                          {(activeItinerary.insider_tips || []).map((tip, idx) => (
                            <li key={idx} className="flex items-start gap-2">
                              <span className="text-teal-400 font-bold">•</span>
                              <span className="leading-relaxed">{tip}</span>
                            </li>
                          ))}
                        </ul>
                      </div>

                      {/* Packing Checklist */}
                      <div className="p-4 rounded-xl bg-darkcard border border-darkborder space-y-2.5">
                        <div className="flex items-center gap-2 text-teal-400 text-xs font-bold uppercase tracking-wider">
                          <Luggage className="w-4 h-4" />
                          <span>Smart Packing Checklist</span>
                        </div>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
                          {(activeItinerary.packing_checklist || []).map((item, idx) => (
                            <div key={idx} className="p-2.5 rounded-lg bg-gray-900/60 border border-gray-800 flex items-center gap-2 text-gray-300">
                              <CheckCircle className="w-3.5 h-3.5 text-teal-400 flex-shrink-0" />
                              <span>{item}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              /* Empty State */
              <div className="flex-1 flex flex-col items-center justify-center p-8 text-center space-y-4">
                <div className="w-16 h-16 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400 shadow-inner">
                  <Compass className="w-8 h-8" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white">Your Itinerary Workspace is Ready</h3>
                  <p className="text-xs text-gray-400 max-w-sm mt-1 leading-relaxed">
                    Chat with the AI travel agent on the left or click any prompt pill to generate a day-by-day schedule, budget breakdown, and local guide.
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
