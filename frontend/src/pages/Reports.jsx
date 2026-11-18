import React, { useState, useEffect } from 'react';
import {
  FileText, Download, ShieldCheck, CheckCircle2, AlertCircle,
  Clock, ArrowRight, ExternalLink, RefreshCw
} from 'lucide-react';
import { reportsAPI } from '../services/api';

export default function Reports() {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [loading, setLoading] = useState(true);
  const [loadingDetail, setLoadingDetail] = useState(false);

  useEffect(() => {
    loadReports();
  }, []);

  const loadReports = async () => {
    try {
      setLoading(true);
      const res = await reportsAPI.list();
      setReports(res);
      if (res.length > 0) {
        loadReportDetail(res[0].id);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const loadReportDetail = async (id) => {
    try {
      setLoadingDetail(true);
      const res = await reportsAPI.getDetails(id);
      setSelectedReport(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingDetail(false);
    }
  };

  const handleDownloadPdf = (reportId) => {
    const url = reportsAPI.getDownloadUrl(reportId);
    window.open(url, '_blank');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Header */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileText size={20} color="#38bdf8" />
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Business Intelligence Reports & Audit Repository</h2>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>
            Permanent archive of multi-agent synthesized intelligence, strategic action plans, and verified PDF reports.
          </p>
        </div>

        {selectedReport && (
          <button
            onClick={() => handleDownloadPdf(selectedReport.id)}
            className="btn btn-primary"
            style={{ padding: '9px 16px' }}
          >
            <Download size={16} />
            <span>Download Verified PDF Report</span>
          </button>
        )}
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: '20px' }}>
        {/* Left: Report History List */}
        <div className="card" style={{ padding: '14px', display: 'flex', flexDirection: 'column', gap: '8px', maxHeight: '700px', overflowY: 'auto' }}>
          <div style={{ fontSize: '12px', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '4px', textTransform: 'uppercase' }}>
            Archived Reports ({reports.length})
          </div>

          {loading ? (
            <div style={{ padding: '20px', textAlign: 'center', color: 'var(--text-muted)' }}>
              <RefreshCw className="animate-spin" size={18} style={{ margin: '0 auto 6px auto' }} />
              <span>Loading reports...</span>
            </div>
          ) : reports.length === 0 ? (
            <div style={{ padding: '14px', fontSize: '12px', color: 'var(--text-muted)', fontStyle: 'italic' }}>
              No reports generated yet. Go to Agent Monitoring to run multi-agent analysis.
            </div>
          ) : (
            reports.map((r) => {
              const isSelected = selectedReport?.id === r.id;
              return (
                <button
                  key={r.id}
                  onClick={() => loadReportDetail(r.id)}
                  style={{
                    padding: '12px',
                    borderRadius: 'var(--radius-sm)',
                    border: isSelected ? '1px solid #3b82f6' : '1px solid var(--border-color)',
                    background: isSelected ? 'rgba(59, 130, 246, 0.12)' : 'rgba(15, 23, 42, 0.4)',
                    cursor: 'pointer',
                    textAlign: 'left',
                    color: 'var(--text-main)',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '12px', fontWeight: 700, color: isSelected ? '#60a5fa' : '#f8fafc' }}>
                      Report #{r.id}
                    </span>
                    <span className="badge badge-teal" style={{ fontSize: '9px' }}>
                      {r.verification_status}
                    </span>
                  </div>
                  <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
                    {r.period}
                  </div>
                  <div style={{ fontSize: '10px', color: '#64748b', marginTop: '4px' }}>
                    Created: {new Date(r.created_at).toLocaleDateString()}
                  </div>
                </button>
              );
            })
          )}
        </div>

        {/* Right: Detailed Report Viewer */}
        <div className="card" style={{ maxHeight: '700px', overflowY: 'auto' }}>
          {loadingDetail || !selectedReport ? (
            <div style={{ padding: '40px', textAlign: 'center', color: 'var(--text-muted)' }}>
              <span>Loading full report data...</span>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
              {/* Report Header */}
              <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                  <div>
                    <h3 style={{ fontSize: '18px', fontWeight: 800 }}>{selectedReport.title}</h3>
                    <div style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
                      Operating Window: <span style={{ color: '#f8fafc' }}>{selectedReport.period}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleDownloadPdf(selectedReport.id)}
                    className="btn btn-secondary"
                    style={{ fontSize: '12px' }}
                  >
                    <Download size={14} />
                    <span>Download PDF</span>
                  </button>
                </div>
              </div>

              {/* Verification Seal Box */}
              <div style={{
                padding: '12px 16px',
                background: 'rgba(16, 185, 129, 0.08)',
                border: '1px solid rgba(16, 185, 129, 0.3)',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: '12px'
              }}>
                <ShieldCheck size={24} color="#10b981" style={{ flexShrink: 0, marginTop: '2px' }} />
                <div style={{ fontSize: '12px', lineHeight: '1.4' }}>
                  <div style={{ fontWeight: 700, color: '#34d399' }}>
                    OFFICIAL AUDIT VERIFICATION CERTIFICATE ({selectedReport.verification_status})
                  </div>
                  <div style={{ color: 'var(--text-muted)', marginTop: '2px' }}>
                    {selectedReport.verification_notes}
                  </div>
                </div>
              </div>

              {/* Executive Summary */}
              <div>
                <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#60a5fa', textTransform: 'uppercase', marginBottom: '6px' }}>
                  1. Executive Summary & Synthesis
                </h4>
                <p style={{ fontSize: '12px', lineHeight: '1.6', color: '#e2e8f0' }}>
                  {selectedReport.executive_summary}
                </p>
              </div>

              {/* Agent Findings */}
              <div>
                <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#60a5fa', textTransform: 'uppercase', marginBottom: '8px' }}>
                  2. Agent-by-Agent Findings
                </h4>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                  {Object.entries(selectedReport.agent_findings || {}).map(([key, text]) => {
                    const agentNames = {
                      data_analyst: "Agent 1: Senior Banking Data Analyst Agent",
                      marketing: "Agent 2: Strategic Banking Marketing Agent",
                      finance: "Agent 3: Chief Financial Officer (CFO) Intelligence Agent",
                      operations: "Agent 4: Bank Operations & Process Intelligence Agent",
                      strategy: "Agent 5: Executive Bank Strategy & Decision Intelligence Agent",
                      verification: "Agent 6: Independent Audit & Anti-Hallucination Agent"
                    };
                    return (
                      <div key={key} style={{ padding: '10px 14px', background: 'rgba(15, 23, 42, 0.5)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                        <div style={{ fontSize: '12px', fontWeight: 700, color: '#38bdf8', marginBottom: '4px' }}>
                          {agentNames[key] || key}
                        </div>
                        <p style={{ fontSize: '12px', lineHeight: '1.5', color: 'var(--text-muted)' }}>
                          {text}
                        </p>
                      </div>
                    );
                  })}
                </div>
              </div>

              {/* Strategic Action Plan Table */}
              <div>
                <h4 style={{ fontSize: '13px', fontWeight: 700, color: '#60a5fa', textTransform: 'uppercase', marginBottom: '8px' }}>
                  3. Actionable Business Improvement Roadmap
                </h4>
                <div style={{ overflowX: 'auto' }}>
                  <table className="data-table">
                    <thead>
                      <tr>
                        <th>Phase</th>
                        <th>Strategic Initiative</th>
                        <th>Lead Agent</th>
                        <th>Projected ROI / Impact</th>
                      </tr>
                    </thead>
                    <tbody>
                      {(selectedReport.action_plan || []).map((p, idx) => (
                        <tr key={idx}>
                          <td style={{ fontWeight: 600, color: '#38bdf8' }}>{p.phase}</td>
                          <td>
                            <div style={{ fontWeight: 600 }}>{p.title}</div>
                            <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '2px' }}>{p.description}</div>
                          </td>
                          <td>{p.agent}</td>
                          <td style={{ color: '#34d399', fontWeight: 600 }}>{p.impact}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
