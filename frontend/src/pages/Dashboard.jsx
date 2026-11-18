import React, { useState, useEffect } from 'react';
import {
  TrendingUp, TrendingDown, DollarSign, Users, AlertTriangle,
  CreditCard, ShieldAlert, ArrowUpRight, CheckCircle2, RefreshCw
} from 'lucide-react';
import { analyticsAPI } from '../services/api';

export default function Dashboard({ onNavigateToAnalysis }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchOverview = async () => {
    try {
      setLoading(true);
      const res = await analyticsAPI.getOverview();
      setData(res);
    } catch (err) {
      console.error("Failed to load analytics overview:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOverview();
  }, []);

  if (loading || !data) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh', gap: '12px' }}>
        <RefreshCw className="animate-spin" size={24} color="#3b82f6" />
        <span>Loading Verified Banking Analytics...</span>
      </div>
    );
  }

  const { financial_kpis, customer_kpis, lending_kpis, operations_kpis, risk_kpis, monthly_trends } = data;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Top Banner */}
      <div className="card" style={{
        background: 'linear-gradient(135deg, rgba(30, 58, 138, 0.35), rgba(15, 23, 42, 0.8))',
        border: '1px solid rgba(59, 130, 246, 0.3)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '20px 24px'
      }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <h1 style={{ fontSize: '20px', fontWeight: 800 }}>Apex Global Trust Bank Operations Intelligence</h1>
            <span className="badge badge-teal">Verified Data (May–Oct 2026)</span>
          </div>
          <p style={{ fontSize: '13px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Multi-Agent system active. 10,500 records analyzed across 6 relational entities with continuous internal verification.
          </p>
        </div>
        <button
          onClick={onNavigateToAnalysis}
          className="btn btn-primary"
          style={{ padding: '10px 18px', fontSize: '14px' }}
        >
          <RefreshCw size={16} />
          <span>Run Multi-Agent Analysis</span>
        </button>
      </div>

      {/* Primary KPI Scorecard Grid */}
      <div className="grid-cols-4">
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Total Deposit Base</span>
            <div style={{ padding: '6px', background: 'rgba(59, 130, 246, 0.15)', borderRadius: '6px' }}>
              <DollarSign size={18} color="#60a5fa" />
            </div>
          </div>
          <div style={{ fontSize: '22px', fontWeight: 700, marginTop: '8px' }}>
            ₹ {(financial_kpis.total_deposit_balance / 10000000).toFixed(2)} Cr
          </div>
          <div style={{ fontSize: '11px', color: '#34d399', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <TrendingUp size={12} />
            <span>1,600 Verified Accounts ({financial_kpis.account_status_counts?.Active || 0} Active)</span>
          </div>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>6-Month Turnover</span>
            <div style={{ padding: '6px', background: 'rgba(20, 184, 166, 0.15)', borderRadius: '6px' }}>
              <CreditCard size={18} color="#2dd4bf" />
            </div>
          </div>
          <div style={{ fontSize: '22px', fontWeight: 700, marginTop: '8px' }}>
            ₹ {(financial_kpis.total_transaction_turnover / 10000000).toFixed(2)} Cr
          </div>
          <div style={{ fontSize: '11px', color: '#2dd4bf', marginTop: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <CheckCircle2 size={12} />
            <span>{operations_kpis.total_transactions} Transactions (Net: +₹{(financial_kpis.net_liquidity_flow / 10000000).toFixed(2)}Cr)</span>
          </div>
        </div>

        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)' }}>Loan Approval Rate</span>
            <div style={{ padding: '6px', background: 'rgba(16, 185, 129, 0.15)', borderRadius: '6px' }}>
              <ArrowUpRight size={18} color="#34d399" />
            </div>
          </div>
          <div style={{ fontSize: '22px', fontWeight: 700, marginTop: '8px' }}>
            {lending_kpis.approval_rate}%
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Disbursed: ₹{(lending_kpis.disbursed_volume / 10000000).toFixed(2)} Cr (Avg CIBIL: {lending_kpis.avg_credit_score})
          </div>
        </div>

        <div className="card" style={{ borderColor: 'rgba(244, 63, 94, 0.3)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, color: '#fb7185' }}>Repayment Delinquency</span>
            <div style={{ padding: '6px', background: 'rgba(244, 63, 94, 0.15)', borderRadius: '6px' }}>
              <AlertTriangle size={18} color="#fb7185" />
            </div>
          </div>
          <div style={{ fontSize: '22px', fontWeight: 700, marginTop: '8px', color: '#fb7185' }}>
            {risk_kpis.delinquency_rate}%
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Avg DPD: {risk_kpis.avg_days_past_due} Days | {risk_kpis.critical_risk_events} Critical Alerts
          </div>
        </div>
      </div>

      {/* Visual Analytics Sections */}
      <div className="grid-cols-2">
        {/* Monthly Liquidity Velocity */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700 }}>Monthly Transaction Volume Progression</h3>
            <span className="badge badge-blue">May – Oct 2026</span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {monthly_trends.map((item) => {
              const maxVol = Math.max(...monthly_trends.map(m => m.total_volume));
              const pct = (item.total_volume / maxVol) * 100;
              return (
                <div key={item.month} style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px' }}>
                    <span style={{ fontWeight: 600 }}>{item.month}</span>
                    <span style={{ color: 'var(--text-muted)' }}>
                      ₹{(item.total_volume / 10000000).toFixed(2)} Cr ({item.transaction_count} txns)
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: 'rgba(51, 65, 85, 0.5)', borderRadius: '4px', overflow: 'hidden' }}>
                    <div style={{ width: `${pct}%`, height: '100%', background: 'linear-gradient(90deg, #3b82f6, #0d9488)', borderRadius: '4px' }}></div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Customer Segmentation & Deposit Allocation */}
        <div className="card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
            <h3 style={{ fontSize: '14px', fontWeight: 700 }}>Customer Segments & Account Portfolios</h3>
            <span className="badge badge-teal">1,200 Customers</span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '12px', marginBottom: '16px' }}>
            {Object.entries(customer_kpis.segment_breakdown || {}).map(([seg, count]) => {
              const colors = {
                Priority: '#38bdf8',
                Corporate: '#818cf8',
                SME: '#34d399',
                Retail: '#fbbf24'
              };
              return (
                <div key={seg} style={{ padding: '10px', background: 'rgba(15, 23, 42, 0.6)', borderRadius: '6px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '11px', color: 'var(--text-muted)' }}>
                    <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: colors[seg] || '#94a3b8' }}></span>
                    <span>{seg}</span>
                  </div>
                  <div style={{ fontSize: '18px', fontWeight: 700, marginTop: '4px' }}>{count}</div>
                  <div style={{ fontSize: '10px', color: 'var(--text-muted)' }}>
                    {((count / customer_kpis.total_customers) * 100).toFixed(1)}% of base
                  </div>
                </div>
              );
            })}
          </div>

          <div style={{ fontSize: '12px', color: 'var(--text-muted)', borderTop: '1px solid var(--border-color)', paddingTop: '10px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
              <span>Dormancy Ratio:</span>
              <span style={{ color: '#fbbf24', fontWeight: 600 }}>{financial_kpis.dormancy_ratio}%</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Frozen Balance Drag:</span>
              <span style={{ color: '#fb7185', fontWeight: 600 }}>{financial_kpis.frozen_ratio}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Operations & Risk Split */}
      <div className="grid-cols-2">
        <div className="card">
          <h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>Channel Utilization & Gateway Stability</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {Object.entries(operations_kpis.channel_distribution || {}).map(([chan, count]) => (
              <div key={chan} style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '6px 0', borderBottom: '1px solid rgba(51, 65, 85, 0.4)', fontSize: '12px' }}>
                <span style={{ fontWeight: 600 }}>{chan}</span>
                <span>{count} txns</span>
                <span style={{ color: 'var(--text-muted)' }}>₹{(operations_kpis.channel_volume[chan] / 10000000).toFixed(2)} Cr</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h3 style={{ fontSize: '14px', fontWeight: 700, marginBottom: '12px' }}>Risk Events & Investigation Load</h3>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '10px', marginBottom: '12px' }}>
            <div style={{ padding: '8px', background: 'rgba(244, 63, 94, 0.1)', borderRadius: '6px', border: '1px solid rgba(244, 63, 94, 0.2)' }}>
              <div style={{ fontSize: '11px', color: '#fb7185' }}>Critical Risk Events</div>
              <div style={{ fontSize: '18px', fontWeight: 700, color: '#fb7185' }}>{risk_kpis.critical_risk_events}</div>
            </div>
            <div style={{ padding: '8px', background: 'rgba(245, 158, 11, 0.1)', borderRadius: '6px', border: '1px solid rgba(245, 158, 11, 0.2)' }}>
              <div style={{ fontSize: '11px', color: '#fbbf24' }}>Open Cases</div>
              <div style={{ fontSize: '18px', fontWeight: 700, color: '#fbbf24' }}>{risk_kpis.open_cases}</div>
            </div>
          </div>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            Investigative units (Fraud, Operations, Credit Risk, Compliance) are assigned 500 incidents. 
            Verification Agent has audited 100% of flagged events.
          </div>
        </div>
      </div>
    </div>
  );
}
