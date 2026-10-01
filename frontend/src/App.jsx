import React, { useState } from 'react';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import AuthModal from './components/AuthModal';
import PreferencesModal from './components/PreferencesModal';

export default function App() {
  const [authOpen, setAuthOpen] = useState(false);
  const [prefsOpen, setPrefsOpen] = useState(false);
  const [currentView, setCurrentView] = useState('chat'); // 'chat' or 'catalog'

  return (
    <AuthProvider>
      <div className="min-h-screen bg-darkbg text-gray-100 flex flex-col font-sans">
        <Navbar
          onOpenAuth={() => setAuthOpen(true)}
          onOpenPrefs={() => setPrefsOpen(true)}
          onSelectDestinationsView={(view) => setCurrentView(view)}
          currentView={currentView}
        />

        <main className="flex-1">
          <DashboardPage
            currentView={currentView}
            onSwitchView={(view) => setCurrentView(view)}
          />
        </main>

        <AuthModal
          isOpen={authOpen}
          onClose={() => setAuthOpen(false)}
        />

        <PreferencesModal
          isOpen={prefsOpen}
          onClose={() => setPrefsOpen(false)}
        />
      </div>
    </AuthProvider>
  );
}
