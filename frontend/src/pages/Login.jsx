import React, { useState } from 'react';
import { ShieldCheck, Lock, User, KeyRound, ArrowRight } from 'lucide-react';
import { authAPI } from '../services/api';

export default function Login({ onLoginSuccess, onSwitchToRegister }) {
  const [username, setUsername] = useState('manager');
  const [password, setPassword] = useState('Manager@12345');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await authAPI.login(username, password);
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify(data.user));
      onLoginSuccess(data.user);
    } catch (err) {
      setError(err.response?.data?.detail || "Authentication failed. Check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickLogin = (u, p) => {
    setUsername(u);
    setPassword(p);
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(ellipse at top, #1e3a8a33, #0b1120 70%)',
      padding: '20px'
    }}>
      <div className="card" style={{ maxWidth: '440px', width: '100%', padding: '32px 28px' }}>
        <div style={{ textAlign: 'center', marginBottom: '24px' }}>
          <div style={{
            width: '48px', height: '48px', margin: '0 auto 12px auto',
            borderRadius: '12px', background: 'linear-gradient(135deg, #1e3a8a, #0d9488)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            boxShadow: '0 0 16px rgba(13, 148, 136, 0.4)'
          }}>
            <ShieldCheck size={28} color="#ffffff" />
          </div>
          <h1 style={{ fontSize: '20px', fontWeight: 800 }}>Apex Trust Intelligence</h1>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Multi-Agent Operations & Decision Intelligence Platform
          </p>
        </div>

        {error && (
          <div style={{
            padding: '10px 14px', borderRadius: '6px', fontSize: '12px',
            background: 'rgba(244, 63, 94, 0.15)', color: '#fb7185',
            border: '1px solid rgba(244, 63, 94, 0.3)', marginBottom: '16px'
          }}>
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Username
            </label>
            <div style={{ position: 'relative' }}>
              <User size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px 10px 36px',
                  backgroundColor: 'var(--bg-secondary)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-main)',
                  fontSize: '13px'
                }}
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <Lock size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{
                  width: '100%',
                  padding: '10px 12px 10px 36px',
                  backgroundColor: 'var(--bg-secondary)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-main)',
                  fontSize: '13px'
                }}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', padding: '11px', marginTop: '6px' }}
          >
            <span>{loading ? "Authenticating..." : "Sign In to Platform"}</span>
            <ArrowRight size={16} />
          </button>
        </form>

        {/* Demo Fast-Login Pill Section */}
        <div style={{ marginTop: '20px', borderTop: '1px solid var(--border-color)', paddingTop: '16px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '8px', textAlign: 'center' }}>
            Quick Demo Access (Select Role):
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '6px' }}>
            <button
              onClick={() => handleQuickLogin('manager', 'Manager@12345')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '6px 8px' }}
            >
              Manager
            </button>
            <button
              onClick={() => handleQuickLogin('analyst', 'Analyst@12345')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '6px 8px' }}
            >
              Analyst
            </button>
            <button
              onClick={() => handleQuickLogin('admin', 'Admin@12345')}
              className="btn btn-secondary"
              style={{ fontSize: '11px', padding: '6px 8px' }}
            >
              Admin
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
