import React, { useState, useEffect } from 'react';
import { Users, UserPlus, Trash2, Shield, Activity, Database, CheckCircle2 } from 'lucide-react';
import { adminAPI } from '../services/api';

export default function AdminDashboard({ currentAdminUser }) {
  const [users, setUsers] = useState([]);
  const [health, setHealth] = useState(null);
  const [showAddUser, setShowAddUser] = useState(false);
  const [newUser, setNewUser] = useState({
    username: '',
    email: '',
    full_name: '',
    password: '',
    role: 'business_manager'
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      const [uList, hStatus] = await Promise.all([
        adminAPI.getUsers(),
        adminAPI.getSystemHealth()
      ]);
      setUsers(uList);
      setHealth(hStatus);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      await adminAPI.createUser(newUser);
      setShowAddUser(false);
      setNewUser({ username: '', email: '', full_name: '', password: '', role: 'business_manager' });
      loadData();
    } catch (err) {
      alert("Failed to create user: " + (err.response?.data?.detail || err.message));
    }
  };

  const handleDeleteUser = async (id, uname) => {
    if (!confirm(`Are you sure you want to revoke access for ${uname}?`)) return;
    try {
      await adminAPI.deleteUser(id);
      loadData();
    } catch (err) {
      alert("Failed to delete user: " + (err.response?.data?.detail || err.message));
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <Shield size={20} color="#60a5fa" />
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Admin System Governance & Access Control</h2>
            <span className="badge badge-blue">Role-Based Access (RBAC)</span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            User provisioning, audit trail supervision, and operational infrastructure metrics.
          </p>
        </div>

        <button
          onClick={() => setShowAddUser(true)}
          className="btn btn-primary"
        >
          <UserPlus size={16} />
          <span>Provision New User</span>
        </button>
      </div>

      {/* System Health Scorecard */}
      {health && (
        <div className="grid-cols-3">
          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
              <Activity size={16} color="#34d399" />
              <span>System Health</span>
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, marginTop: '8px', color: '#34d399' }}>
              {health.status}
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
              Version {health.platform_version} | DB: {health.database_type}
            </div>
          </div>

          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
              <Database size={16} color="#38bdf8" />
              <span>Relational Records</span>
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, marginTop: '8px', color: '#f8fafc' }}>
              10,500 Ingested Records
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
              {health.records.customers} Customers, {health.records.accounts} Accounts, {health.records.transactions} Transactions
            </div>
          </div>

          <div className="card">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>
              <CheckCircle2 size={16} color="#14b8a6" />
              <span>Multi-Agent Engine</span>
            </div>
            <div style={{ fontSize: '16px', fontWeight: 700, marginTop: '8px', color: '#14b8a6' }}>
              CrewAI 6-Agent Pipeline
            </div>
            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
              Anti-Hallucination & Human-in-the-Loop Enforced
            </div>
          </div>
        </div>
      )}

      {/* User Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <h3 style={{ fontSize: '14px', fontWeight: 700 }}>Authorized System Users</h3>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{users.length} Active Accounts</span>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table className="data-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Full Name</th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Created Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id}>
                  <td>#{u.id}</td>
                  <td style={{ fontWeight: 600 }}>{u.full_name}</td>
                  <td><code>{u.username}</code></td>
                  <td>{u.email}</td>
                  <td>
                    <span className={`badge ${u.role === 'admin' ? 'badge-rose' : u.role === 'business_manager' ? 'badge-blue' : 'badge-teal'}`}>
                      {u.role.replace('_', ' ')}
                    </span>
                  </td>
                  <td style={{ color: 'var(--text-muted)' }}>{new Date(u.created_at).toLocaleDateString()}</td>
                  <td>
                    {u.username !== 'admin' && (
                      <button
                        onClick={() => handleDeleteUser(u.id, u.username)}
                        style={{ background: 'none', border: 'none', color: '#f43f5e', cursor: 'pointer' }}
                        title="Delete user"
                      >
                        <Trash2 size={14} />
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Add User Modal */}
      {showAddUser && (
        <div style={{
          position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.7)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          zIndex: 100, padding: '20px'
        }}>
          <div className="card" style={{ maxWidth: '480px', width: '100%' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700, marginBottom: '14px' }}>Provision New Platform User</h3>
            <form onSubmit={handleCreateUser} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <div>
                <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>Full Name</label>
                <input
                  type="text" required
                  value={newUser.full_name}
                  onChange={(e) => setNewUser({ ...newUser, full_name: e.target.value })}
                  style={{ width: '100%', padding: '8px 12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>Username</label>
                <input
                  type="text" required
                  value={newUser.username}
                  onChange={(e) => setNewUser({ ...newUser, username: e.target.value })}
                  style={{ width: '100%', padding: '8px 12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>Email</label>
                <input
                  type="email" required
                  value={newUser.email}
                  onChange={(e) => setNewUser({ ...newUser, email: e.target.value })}
                  style={{ width: '100%', padding: '8px 12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>Password</label>
                <input
                  type="password" required
                  value={newUser.password}
                  onChange={(e) => setNewUser({ ...newUser, password: e.target.value })}
                  style={{ width: '100%', padding: '8px 12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: '#fff' }}
                />
              </div>

              <div>
                <label style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>System Role</label>
                <select
                  value={newUser.role}
                  onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}
                  style={{ width: '100%', padding: '8px 12px', background: 'var(--bg-secondary)', border: '1px solid var(--border-color)', borderRadius: '4px', color: '#fff' }}
                >
                  <option value="business_manager">Business Manager (Executive / Approver)</option>
                  <option value="analyst">Data Analyst (Read & Query Access)</option>
                  <option value="admin">System Administrator (Full Control)</option>
                </select>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '12px' }}>
                <button type="button" onClick={() => setShowAddUser(false)} className="btn btn-secondary">Cancel</button>
                <button type="submit" className="btn btn-primary">Create User</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
