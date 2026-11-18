import React, { useState, useEffect } from 'react';
import { Building, Save, CheckCircle2, ShieldCheck } from 'lucide-react';
import { businessAPI } from '../services/api';

export default function BusinessProfile() {
  const [profile, setProfile] = useState({
    company_name: '',
    industry: '',
    team_size: '',
    business_goals: '',
    risk_tolerance: '',
    target_period: ''
  });
  const [loading, setLoading] = useState(true);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      setLoading(true);
      const res = await businessAPI.getProfile();
      setProfile(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await businessAPI.updateProfile(profile);
      setProfile(res);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
    } catch (err) {
      alert("Failed to update profile: " + err.message);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '800px' }}>
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '16px' }}>
          <Building size={20} color="#38bdf8" />
          <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Institution & Business Profile</h2>
        </div>

        {saved && (
          <div style={{ padding: '10px 14px', background: 'rgba(16, 185, 129, 0.15)', color: '#34d399', borderRadius: '6px', fontSize: '12px', marginBottom: '14px', display: 'flex', alignItems: 'center', gap: '6px' }}>
            <CheckCircle2 size={16} />
            <span>Business Profile & Objectives updated successfully.</span>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
              Institution Name
            </label>
            <input
              type="text"
              value={profile.company_name}
              onChange={(e) => setProfile({ ...profile, company_name: e.target.value })}
              style={{
                width: '100%',
                padding: '9px 12px',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                color: 'var(--text-main)',
                fontSize: '13px'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
                Industry Sector
              </label>
              <input
                type="text"
                value={profile.industry}
                disabled
                style={{
                  width: '100%',
                  padding: '9px 12px',
                  background: 'rgba(15, 23, 42, 0.5)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-muted)',
                  fontSize: '13px'
                }}
              />
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
                Organization Team Size
              </label>
              <input
                type="text"
                value={profile.team_size}
                onChange={(e) => setProfile({ ...profile, team_size: e.target.value })}
                style={{
                  width: '100%',
                  padding: '9px 12px',
                  background: 'var(--bg-secondary)',
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
              Strategic Business Goals
            </label>
            <textarea
              rows={3}
              value={profile.business_goals}
              onChange={(e) => setProfile({ ...profile, business_goals: e.target.value })}
              style={{
                width: '100%',
                padding: '9px 12px',
                background: 'var(--bg-secondary)',
                border: '1px solid var(--border-color)',
                borderRadius: 'var(--radius-sm)',
                color: 'var(--text-main)',
                fontSize: '13px',
                lineHeight: '1.5'
              }}
            />
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
                Risk Tolerance
              </label>
              <select
                value={profile.risk_tolerance}
                onChange={(e) => setProfile({ ...profile, risk_tolerance: e.target.value })}
                style={{
                  width: '100%',
                  padding: '9px 12px',
                  background: 'var(--bg-secondary)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-main)',
                  fontSize: '13px'
                }}
              >
                <option value="Conservative">Conservative</option>
                <option value="Moderate-Conservative">Moderate-Conservative</option>
                <option value="Moderate">Moderate</option>
                <option value="Aggressive">Aggressive</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
                Audited Dataset Window
              </label>
              <input
                type="text"
                value={profile.target_period}
                disabled
                style={{
                  width: '100%',
                  padding: '9px 12px',
                  background: 'rgba(15, 23, 42, 0.5)',
                  border: '1px solid var(--border-color)',
                  borderRadius: 'var(--radius-sm)',
                  color: 'var(--text-muted)',
                  fontSize: '13px'
                }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '10px' }}>
            <button type="submit" className="btn btn-primary">
              <Save size={16} />
              <span>Save Business Profile</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
