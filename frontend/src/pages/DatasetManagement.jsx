import React, { useState, useEffect } from 'react';
import { Upload, Database, FileSpreadsheet, CheckCircle2, Table as TableIcon, RefreshCw, FileDown } from 'lucide-react';
import { datasetAPI } from '../services/api';

export default function DatasetManagement() {
  const [stats, setStats] = useState(null);
  const [selectedTable, setSelectedTable] = useState('customers');
  const [tableData, setTableData] = useState([]);
  const [loadingPreview, setLoadingPreview] = useState(false);
  const [uploadStatus, setUploadStatus] = useState(null);
  const [uploading, setUploading] = useState(false);

  useEffect(() => {
    loadStats();
    loadPreview('customers');
  }, []);

  const loadStats = async () => {
    try {
      const res = await datasetAPI.getStats();
      setStats(res);
    } catch (e) {
      console.error(e);
    }
  };

  const loadPreview = async (table) => {
    try {
      setLoadingPreview(true);
      setSelectedTable(table);
      const res = await datasetAPI.getPreview(table, 20);
      setTableData(res.data || []);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingPreview(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    try {
      setUploading(true);
      setUploadStatus("Uploading & validating banking schema...");
      const res = await datasetAPI.upload(file);
      setUploadStatus(`Success: ${res.message}`);
      loadStats();
      loadPreview(selectedTable);
    } catch (err) {
      setUploadStatus(`Upload failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setUploading(false);
    }
  };

  const tables = [
    { id: 'customers', label: 'Customers (1,200)', count: stats?.total_customers },
    { id: 'accounts', label: 'Accounts (1,600)', count: stats?.total_accounts },
    { id: 'transactions', label: 'Transactions (3,500)', count: stats?.total_transactions },
    { id: 'loan_applications', label: 'Loan Applications (1,200)', count: stats?.total_loans },
    { id: 'loan_repayments', label: 'Loan Repayments (2,500)', count: stats?.total_repayments },
    { id: 'risk_events', label: 'Risk Events (500)', count: stats?.total_risk_events },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
      {/* Upload and Dataset Status Card */}
      <div className="card" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <FileSpreadsheet size={20} color="#2dd4bf" />
            <h2 style={{ fontSize: '18px', fontWeight: 800 }}>Dataset Management & Processing</h2>
            <span className="badge badge-teal">Coverage: May 1 – Oct 31, 2026</span>
          </div>
          <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '4px' }}>
            Multi-entity synthetic relational database. Ingested and indexed across 6 interconnected banking tables.
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <label className="btn btn-primary" style={{ cursor: 'pointer' }}>
            <Upload size={16} />
            <span>{uploading ? "Validating File..." : "Upload New CSV / Excel"}</span>
            <input
              type="file"
              accept=".csv,.xlsx"
              onChange={handleFileUpload}
              style={{ display: 'none' }}
              disabled={uploading}
            />
          </label>
        </div>
      </div>

      {uploadStatus && (
        <div style={{
          padding: '10px 14px',
          borderRadius: 'var(--radius-sm)',
          fontSize: '12px',
          background: uploadStatus.includes('Success') ? 'rgba(16, 185, 129, 0.15)' : 'rgba(244, 63, 94, 0.15)',
          color: uploadStatus.includes('Success') ? '#34d399' : '#fb7185',
          border: '1px solid currentColor'
        }}>
          {uploadStatus}
        </div>
      )}

      {/* Row Count Metrics */}
      <div className="grid-cols-3">
        {tables.map((t) => (
          <button
            key={t.id}
            onClick={() => loadPreview(t.id)}
            className="card"
            style={{
              cursor: 'pointer',
              textAlign: 'left',
              border: selectedTable === t.id ? '1px solid #3b82f6' : '1px solid var(--border-color)',
              background: selectedTable === t.id ? 'rgba(59, 130, 246, 0.1)' : 'var(--bg-card)'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <span style={{ fontSize: '13px', fontWeight: 600 }}>{t.label}</span>
              <Database size={16} color={selectedTable === t.id ? '#60a5fa' : '#94a3b8'} />
            </div>
            <div style={{ fontSize: '20px', fontWeight: 800, marginTop: '8px', color: '#f8fafc' }}>
              {t.count !== undefined ? t.count.toLocaleString() : '...'}
            </div>
          </button>
        ))}
      </div>

      {/* Data Entity Table Preview */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <TableIcon size={16} color="#60a5fa" />
            <h3 style={{ fontSize: '14px', fontWeight: 700, textTransform: 'capitalize' }}>
              Preview: {selectedTable.replace('_', ' ')} (First 20 Records)
            </h3>
          </div>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            Total in Database: {tables.find(t => t.id === selectedTable)?.count} rows
          </span>
        </div>

        {loadingPreview ? (
          <div style={{ padding: '30px', textAlign: 'center', color: 'var(--text-muted)' }}>
            <RefreshCw className="animate-spin" size={20} style={{ margin: '0 auto 8px auto' }} />
            <span>Loading records from database...</span>
          </div>
        ) : tableData.length === 0 ? (
          <div style={{ padding: '20px', color: 'var(--text-muted)', fontStyle: 'italic' }}>No records found.</div>
        ) : (
          <div style={{ overflowX: 'auto', maxHeight: '420px' }}>
            <table className="data-table">
              <thead>
                <tr>
                  {Object.keys(tableData[0]).map((col) => (
                    <th key={col}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {tableData.map((row, rIdx) => (
                  <tr key={rIdx}>
                    {Object.values(row).map((val, cIdx) => (
                      <td key={cIdx}>{String(val)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
