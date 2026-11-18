import React, { useState, useEffect } from 'react';
import {
  Cpu, Play, CheckCircle2, Clock, AlertTriangle, ShieldCheck,
  Terminal, ArrowRight, RefreshCw, Eye
} from 'lucide-react';
import { agentsAPI } from '../services/api';

export default function AgentMonitoring() {
  const [specs, setSpecs] = useState({});
  const [running, setRunning] = useState(false);
  const [currentSessionId, setCurrentSessionId] = useState(null);
  const [executionState, setExecutionState] = useState(null);
  const [logs, setLogs] = useState([]);
  const [executionMode, setExecutionMode] = useState('sequential');
  const [selectedAgentDetail, setSelectedAgentDetail] = useState(null);

  useEffect(() => {
    loadSpecs();
    loadLatestLogs();
  }, []);

  const loadSpecs = async () => {
    try {
      const res = await agentsAPI.getSpecs();
      setSpecs(res);
    } catch (e) {
      console.error(e);
    }
  };

  const loadLatestLogs = async () => {
    try {
      const res = await agentsAPI.getLogs();
      setLogs(res);
    } catch (e) {
      console.error(e);
    }
  };

  const triggerWorkflow = async () => {
    try {
      setRunning(true);
      const res = await agentsAPI.runWorkflow({ execution_mode: executionMode });
      setCurrentSessionId(res.session_id);
    } catch (e) {
      alert("Failed to start workflow: " + e.message);
      setRunning(false);
    }
  };

  // Poll status while running
  useEffect(() => {
    if (!currentSessionId || !running) return;

    const interval = setInterval(async () => {
      try {
        const status = await agentsAPI.getStatus(currentSessionId);
        setExecutionState(status);
        if (status.status === 'Completed' || status.status === 'Failed') {
          setRunning(false);
          loadLatestLogs();
        }
      } catch (err) {
        console.error(err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [currentSessionId, running]);

  const agentKeys = [
    { key: "Data Analyst Agent", id: "data_analyst", color: "#38bdf8" },
    { key: "Marketing Agent", id: "marketing", color: "#818cf8" },
    { key: "Finance Agent", id: "finance", color: "#34d399" },
    { key: "Operations Agent", id: "operations", color: "#fbbf24" },
    { key: "Strategy Agent", id: "strategy", color: "#f43f5e" },
    { key: "Verification Agent", id: "verification", color: "#14b8a6" }
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Control Header */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h2 style={{ fontSize: '18px', fontWeight: 800 }}>CrewAI Multi-Agent Execution Monitor</h2>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Orchestrates 6 autonomous agents collaborating sequentially to synthesize business intelligence and audit numerical claims.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <select
            value={executionMode}
            onChange={(e) => setExecutionMode(e.target.value)}
            style={{
              padding: '8px 12px',
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              fontSize: '12px'
            }}
          >
            <option value="sequential">Sequential Pipeline (Recommended)</option>
            <option value="hierarchical">Hierarchical Crew Orchestration</option>
          </select>

          <button
            onClick={triggerWorkflow}
            disabled={running}
            className="btn btn-primary"
            style={{ opacity: running ? 0.7 : 1 }}
          >
            {running ? <RefreshCw className="animate-spin" size={16} /> : <Play size={16} />}
            <span>{running ? "Agents Executing..." : "Trigger Multi-Agent Analysis"}</span>
          </button>
        </div>
      </div>

      {/* Progress Bar */}
      {executionState && (
        <div className="card" style={{ background: 'rgba(15, 23, 42, 0.7)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px' }}>
            <span style={{ fontWeight: 600 }}>Execution Status: {executionState.status}</span>
            <span style={{ color: '#38bdf8', fontWeight: 700 }}>{executionState.progress_percentage}%</span>
          </div>
          <div style={{ width: '100%', height: '8px', background: 'var(--bg-card)', borderRadius: '4px', overflow: 'hidden' }}>
            <div style={{
              width: `${executionState.progress_percentage}%`,
              height: '100%',
              background: 'linear-gradient(90deg, #3b82f6, #14b8a6)',
              transition: 'width 0.4s ease'
            }}></div>
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px' }}>
            Current Focus: <span style={{ color: '#f8fafc', fontWeight: 600 }}>{executionState.current_agent || 'Waiting'}</span>
          </div>
        </div>
      )}

      {/* 6 Specialized Agent Cards */}
      <div className="grid-cols-3">
        {agentKeys.map((agent, idx) => {
          const spec = specs[agent.id] || {};
          const liveStatus = executionState?.agent_statuses?.[agent.key] || { status: 'Pending', time_ms: 0, summary: '' };
          
          let badgeClass = 'badge-blue';
          if (liveStatus.status === 'Completed') badgeClass = 'badge-green';
          if (liveStatus.status === 'Running') badgeClass = 'badge-amber';
          if (liveStatus.status === 'Pending') badgeClass = 'badge-teal';

          return (
            <div
              key={agent.key}
              className="card"
              style={{
                borderLeft: `4px solid ${agent.color}`,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between'
              }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div style={{ fontSize: '11px', fontWeight: 700, color: agent.color }}>
                    STEP {idx + 1}
                  </div>
                  <span className={`badge ${badgeClass}`}>
                    {liveStatus.status === 'Completed' && <CheckCircle2 size={10} />}
                    {liveStatus.status === 'Running' && <RefreshCw className="animate-spin" size={10} />}
                    <span>{liveStatus.status}</span>
                  </span>
                </div>

                <div style={{ fontSize: '14px', fontWeight: 700, marginTop: '4px' }}>
                  {agent.key}
                </div>

                <p style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '6px', lineHeight: '1.4' }}>
                  {spec.goal?.slice(0, 140)}...
                </p>
              </div>

              <div style={{ marginTop: '12px', borderTop: '1px solid var(--border-color)', paddingTop: '8px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: 'var(--text-muted)' }}>
                  <span>Time: {liveStatus.time_ms}ms</span>
                  <button
                    onClick={() => setSelectedAgentDetail({ agent: agent.key, spec, status: liveStatus })}
                    style={{ background: 'none', border: 'none', color: '#60a5fa', cursor: 'pointer', fontSize: '11px', display: 'flex', alignItems: 'center', gap: '3px' }}
                  >
                    <Eye size={12} />
                    <span>View Role</span>
                  </button>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Live Agent Terminal Logs */}
      <div className="card" style={{ background: '#090d16', border: '1px solid #1e293b' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '12px', borderBottom: '1px solid #1e293b', paddingBottom: '8px' }}>
          <Terminal size={16} color="#38bdf8" />
          <h3 style={{ fontSize: '13px', fontWeight: 700, color: '#38bdf8' }}>Agent Collaboration Stream & Verification Audit Logs</h3>
        </div>

        <div style={{ maxHeight: '280px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '12px' }}>
          {logs.length === 0 ? (
            <div style={{ color: 'var(--text-muted)', fontStyle: 'italic', padding: '12px' }}>
              No execution logs recorded yet. Click "Trigger Multi-Agent Analysis" above to initiate workflow.
            </div>
          ) : (
            logs.map((log) => (
              <div key={log.id} style={{ padding: '8px 12px', background: 'rgba(30, 41, 59, 0.4)', borderRadius: '4px', borderLeft: '3px solid #3b82f6' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', color: '#94a3b8', fontSize: '11px' }}>
                  <span style={{ fontWeight: 600, color: '#f8fafc' }}>[{log.agent_name}]</span>
                  <span>{log.step_name} ({log.execution_time_ms}ms)</span>
                </div>
                <div style={{ marginTop: '4px', color: '#e2e8f0', lineHeight: '1.4' }}>
                  {log.output_content}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Modal for Agent Specs */}
      {selectedAgentDetail && (
        <div style={{
          position: 'fixed',
          top: 0, left: 0, right: 0, bottom: 0,
          background: 'rgba(0, 0, 0, 0.75)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 100,
          padding: '20px'
        }}>
          <div className="card" style={{ maxWidth: '600px', width: '100%' }}>
            <h3 style={{ fontSize: '16px', fontWeight: 700, color: '#38bdf8' }}>{selectedAgentDetail.agent}</h3>
            <div style={{ marginTop: '10px', fontSize: '12px', lineHeight: '1.5' }}>
              <div style={{ fontWeight: 600, color: '#cbd5e1' }}>Role:</div>
              <div style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>{selectedAgentDetail.spec.role}</div>

              <div style={{ fontWeight: 600, color: '#cbd5e1' }}>Goal:</div>
              <div style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>{selectedAgentDetail.spec.goal}</div>

              <div style={{ fontWeight: 600, color: '#cbd5e1' }}>Backstory:</div>
              <div style={{ color: 'var(--text-muted)', marginBottom: '8px' }}>{selectedAgentDetail.spec.backstory}</div>
            </div>
            <button
              onClick={() => setSelectedAgentDetail(null)}
              className="btn btn-secondary"
              style={{ marginTop: '14px', width: '100%' }}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
