import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import AgentMonitoring from './pages/AgentMonitoring';
import AIChat from './pages/AIChat';
import DatasetManagement from './pages/DatasetManagement';
import Reports from './pages/Reports';
import Approvals from './pages/Approvals';
import BusinessProfile from './pages/BusinessProfile';
import AdminDashboard from './pages/AdminDashboard';
import Login from './pages/Login';
import { authAPI } from './services/api';

export default function App() {
  const [user, setUser] = useState(null);
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [checkingAuth, setCheckingAuth] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    const token = localStorage.getItem('token');
    if (savedUser && token) {
      setUser(JSON.parse(savedUser));
    }
    setCheckingAuth(false);
  }, []);

  const handleLoginSuccess = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setUser(null);
  };

  if (checkingAuth) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)' }}>
        <span>Initializing Platform...</span>
      </div>
    );
  }

  if (!user) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar user={user} onLogout={handleLogout} />

      <div style={{ display: 'flex', flex: 1 }}>
        <Sidebar currentTab={currentTab} onSelectTab={setCurrentTab} user={user} />

        <main style={{ flex: 1, padding: '24px 32px', overflowY: 'auto' }}>
          {currentTab === 'dashboard' && (
            <Dashboard onNavigateToAnalysis={() => setCurrentTab('monitoring')} />
          )}
          {currentTab === 'monitoring' && <AgentMonitoring />}
          {currentTab === 'chat' && <AIChat />}
          {currentTab === 'dataset' && <DatasetManagement />}
          {currentTab === 'reports' && <Reports />}
          {currentTab === 'approvals' && <Approvals user={user} />}
          {currentTab === 'profile' && <BusinessProfile />}
          {currentTab === 'admin' && <AdminDashboard currentAdminUser={user} />}
        </main>
      </div>
    </div>
  );
}
