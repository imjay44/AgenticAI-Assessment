import React from 'react';
import {
  LayoutDashboard,
  Cpu,
  MessageSquare,
  Database,
  FileText,
  CheckCircle,
  Building,
  Users
} from 'lucide-react';

export default function Sidebar({ currentTab, onSelectTab, user }) {
  const navItems = [
    { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
    { id: 'monitoring', label: 'Agent Monitoring', icon: Cpu, badge: '6 Agents' },
    { id: 'chat', label: 'AI Business Copilot', icon: MessageSquare },
    { id: 'dataset', label: 'Dataset Management', icon: Database },
    { id: 'reports', label: 'Reports & PDF Export', icon: FileText },
    { id: 'approvals', label: 'Human-in-the-Loop', icon: CheckCircle, badge: 'Required' },
    { id: 'profile', label: 'Business Profile', icon: Building },
  ];

  if (user && user.role === 'admin') {
    navItems.push({ id: 'admin', label: 'Admin Governance', icon: Users });
  }

  return (
    <aside style={{
      width: '240px',
      backgroundColor: 'var(--bg-secondary)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      padding: '16px 12px',
      gap: '4px'
    }}>
      <div style={{ padding: '0 8px 12px 8px', fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.8px' }}>
        Operations Console
      </div>

      {navItems.map((item) => {
        const Icon = item.icon;
        const isActive = currentTab === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onSelectTab(item.id)}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '10px 12px',
              borderRadius: 'var(--radius-sm)',
              border: 'none',
              cursor: 'pointer',
              backgroundColor: isActive ? 'rgba(59, 130, 246, 0.15)' : 'transparent',
              color: isActive ? '#60a5fa' : 'var(--text-muted)',
              fontWeight: isActive ? 600 : 500,
              fontSize: '13px',
              textAlign: 'left',
              transition: 'all 0.15s ease'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
              <Icon size={18} color={isActive ? '#60a5fa' : '#94a3b8'} />
              <span>{item.label}</span>
            </div>
            {item.badge && (
              <span className={`badge ${isActive ? 'badge-blue' : 'badge-teal'}`} style={{ fontSize: '9px', padding: '1px 6px' }}>
                {item.badge}
              </span>
            )}
          </button>
        );
      })}

      <div style={{ marginTop: 'auto', padding: '12px', background: 'rgba(30, 41, 59, 0.5)', borderRadius: 'var(--radius-sm)', border: '1px solid var(--border-color)' }}>
        <div style={{ fontSize: '11px', fontWeight: 600, color: '#38bdf8' }}>Audit Protection Active</div>
        <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
          Verification Agent enforces 0% discrepancy tolerance against source ledgers.
        </div>
      </div>
    </aside>
  );
}
