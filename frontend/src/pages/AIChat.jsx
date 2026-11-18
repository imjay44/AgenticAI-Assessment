import React, { useState } from 'react';
import { Send, Bot, User, Sparkles, Database, HelpCircle } from 'lucide-react';
import { chatAPI } from '../services/api';

export default function AIChat() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      agent: 'Strategy Agent',
      content: 'Welcome to the Apex Trust Bank Decision Intelligence Copilot. I have access to our audited May–October 2026 operations dataset across all 10,500 records. How can I assist your executive decisions today?'
    }
  ]);
  const [input, setInput] = useState('');
  const [targetAgent, setTargetAgent] = useState('Strategy Agent');
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  const suggestedPrompts = [
    "What is our total deposit volume and dormancy ratio?",
    "Explain the root cause of our 53% loan delinquency rate.",
    "Which payment channels have the highest transaction failure rates?",
    "How should we monetize our Priority and SME customer segments?",
    "What are the Verification Agent's audit findings?"
  ];

  const handleSend = async (textToSend = null) => {
    const query = textToSend || input;
    if (!query.trim() || loading) return;

    const userMsg = { role: 'user', content: query };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await chatAPI.ask(query, sessionId, targetAgent);
      if (res.session_id) setSessionId(res.session_id);

      const botMsg = {
        role: 'assistant',
        agent: res.agent_name,
        content: res.response,
        kpis: res.context_kpis
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [
        ...prev,
        { role: 'assistant', agent: 'System', content: 'Apologies, failed to process query: ' + err.message }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: 'calc(100vh - 120px)', gap: '16px' }}>
      {/* Header Controls */}
      <div className="card" style={{ padding: '12px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles size={18} color="#38bdf8" />
          <span style={{ fontWeight: 700, fontSize: '14px' }}>AI Business Operations Copilot</span>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '12px' }}>
          <span style={{ color: 'var(--text-muted)' }}>Addressing Agent:</span>
          <select
            value={targetAgent}
            onChange={(e) => setTargetAgent(e.target.value)}
            style={{
              padding: '6px 10px',
              backgroundColor: 'var(--bg-secondary)',
              color: 'var(--text-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              fontSize: '12px'
            }}
          >
            <option value="Strategy Agent">Strategy Agent (Consolidated)</option>
            <option value="Data Analyst Agent">Data Analyst Agent (Metrics & Trends)</option>
            <option value="Finance Agent">Finance Agent (Liquidity & Margins)</option>
            <option value="Marketing Agent">Marketing Agent (Customers & Retention)</option>
            <option value="Operations Agent">Operations Agent (Gateways & Channels)</option>
            <option value="Verification Agent">Verification Agent (Audits & Accuracy)</option>
          </select>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="card" style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px', padding: '16px 20px' }}>
        {messages.map((m, idx) => {
          const isUser = m.role === 'user';
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                gap: '10px',
                alignSelf: isUser ? 'flex-end' : 'flex-start',
                maxWidth: '80%'
              }}
            >
              {!isUser && (
                <div style={{
                  width: '32px', height: '32px', borderRadius: '50%',
                  background: 'linear-gradient(135deg, #1e3a8a, #0d9488)',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
                }}>
                  <Bot size={18} color="#ffffff" />
                </div>
              )}

              <div style={{
                background: isUser ? '#2563eb' : 'var(--bg-secondary)',
                border: isUser ? 'none' : '1px solid var(--border-color)',
                borderRadius: '10px',
                padding: '10px 14px',
                color: '#f8fafc',
                fontSize: '13px',
                lineHeight: '1.5'
              }}>
                {!isUser && m.agent && (
                  <div style={{ fontSize: '11px', fontWeight: 700, color: '#38bdf8', marginBottom: '4px' }}>
                    [{m.agent}]
                  </div>
                )}
                <div>{m.content}</div>
              </div>

              {isUser && (
                <div style={{
                  width: '32px', height: '32px', borderRadius: '50%',
                  background: '#334155',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
                }}>
                  <User size={18} color="#ffffff" />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div style={{ display: 'flex', gap: '10px', alignItems: 'center', color: 'var(--text-muted)', fontSize: '12px' }}>
            <div className="animate-spin" style={{ width: '16px', height: '16px', border: '2px solid #3b82f6', borderTopColor: 'transparent', borderRadius: '50%' }}></div>
            <span>{targetAgent} is analyzing dataset records...</span>
          </div>
        )}
      </div>

      {/* Suggested Prompts */}
      <div style={{ display: 'flex', gap: '8px', overflowX: 'auto', paddingBottom: '4px' }}>
        {suggestedPrompts.map((p, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(p)}
            style={{
              padding: '6px 12px',
              backgroundColor: 'rgba(30, 41, 59, 0.6)',
              border: '1px solid var(--border-color)',
              borderRadius: '9999px',
              color: 'var(--text-muted)',
              fontSize: '11px',
              cursor: 'pointer',
              whiteSpace: 'nowrap'
            }}
          >
            {p}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{ display: 'flex', gap: '10px' }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={`Ask the ${targetAgent} about KPIs, customer behavior, liquidity, or risk events...`}
          style={{
            flex: 1,
            padding: '12px 16px',
            backgroundColor: 'var(--bg-card)',
            border: '1px solid var(--border-color)',
            borderRadius: 'var(--radius-sm)',
            color: 'var(--text-main)',
            fontSize: '13px'
          }}
        />
        <button
          type="submit"
          className="btn btn-primary"
          disabled={loading || !input.trim()}
          style={{ padding: '0 20px' }}
        >
          <Send size={16} />
          <span>Ask Agent</span>
        </button>
      </form>
    </div>
  );
}
