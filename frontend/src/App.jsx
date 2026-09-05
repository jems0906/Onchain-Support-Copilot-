import { useEffect, useState } from 'react';
import { Activity, ArrowUpRight, ClipboardList, Database, Terminal } from 'lucide-react';
import { createCase, getBalance, getCases, getCode, getDashboard, getDraft, getReceipt, reviewCase, runTriage } from './api/client';
import DashboardPage from './pages/DashboardPage';
import KnowledgeBasePage from './pages/KnowledgeBasePage';
import AiDraftReview from './components/AiDraftReview';
import CaseHistory from './components/CaseHistory';
import OpsDashboard from './components/OpsDashboard';
import RpcLookupPanel from './components/RpcLookupPanel';
import SupportForm from './components/SupportForm';
import TriageResults from './components/TriageResults';

const emptyForm = { network: 'base', wallet_address: '', transaction_hash: '', contract_address: '', error_message: '', tool_used: 'Foundry', issue_category: '' };
function App() {
  const [form, setForm] = useState(emptyForm); const [triage, setTriage] = useState(null); const [draft, setDraft] = useState(null); const [cases, setCases] = useState([]); const [dashboard, setDashboard] = useState(null); const [rpc, setRpc] = useState(null); const [loading, setLoading] = useState(false); const [rpcLoading, setRpcLoading] = useState(false); const [currentCase, setCurrentCase] = useState(null); const [message, setMessage] = useState('');
    const [view, setView] = useState('intake'); 
  useEffect(() => { Promise.all([getCases(), getDashboard()]).then(([c, d]) => { setCases(c.items || []); setDashboard(d); }).catch(() => setMessage('Backend offline. Start FastAPI on port 8000 to enable live case saving.')); }, []);
  const update = (key, value) => setForm((old) => ({ ...old, [key]: value }));
  async function diagnose(event) { event.preventDefault(); setLoading(true); setMessage(''); setDraft(null); setRpc(null); setCurrentCase(null); try { const result = await runTriage(form); setTriage(result); if (result.rpc_lookup) setRpc({ receipt: result.rpc_lookup }); const generated = await getDraft(form, result); setDraft(generated); } catch (error) { setMessage(error.message); } finally { setLoading(false); } }
  async function saveCase() { try { const saved = await createCase(form); setCurrentCase(saved); setCases((old) => [saved, ...old]); setMessage('Case saved to the support queue.'); return saved; } catch (error) { setMessage(error.message); return null; } }
  async function lookupRpc() { setRpcLoading(true); setMessage(''); try { const results = await Promise.all([form.transaction_hash ? getReceipt(form.network, form.transaction_hash) : null, form.wallet_address ? getBalance(form.network, form.wallet_address) : null, form.contract_address ? getCode(form.network, form.contract_address) : null]); setRpc({ receipt: results[0], balance: results[1], code: results[2] }); } catch (error) { setMessage(error.message); } finally { setRpcLoading(false); } }
  async function applyReview(status, response) { const saved = currentCase || await saveCase(); if (!saved) return; try { const updated = await reviewCase(saved.id, status, response); setCurrentCase(updated); setCases((old) => old.map((item) => item.id === updated.id ? updated : item)); setDashboard(await getDashboard()); setMessage(`Draft ${status}.`); } catch (error) { setMessage(error.message); } }
  if (view === 'dashboard') return <DashboardPage onBack={() => setView('intake')} />;
  if (view === 'knowledge') return <KnowledgeBasePage onBack={() => setView('intake')} />;
  return <div className="app-shell">
    <aside className="sidebar"><div className="brand"><div className="brand-mark">⌁</div><div><b>support<br/>copilot</b><small>BASE OPERATIONS</small></div></div><nav><a className="active" onClick={() => setView('intake')}><Activity size={17}/>Intake desk</a><a onClick={() => document.getElementById('case-history')?.scrollIntoView({ behavior: 'smooth' })}><ClipboardList size={17}/>Case history <em>{cases.length || 0}</em></a><a onClick={() => setView('knowledge')}><Database size={17}/>Playbooks <em>08</em></a><a onClick={() => setView('dashboard')}><Terminal size={17}/>Dashboard</a></nav><div className="sidebar-foot"><div className="status-dot"/>All systems nominal<div className="version">v1.0 · human-reviewed AI</div></div></aside>
    <main><header><div><div className="eyebrow">OPERATIONS / INTAKE DESK</div><h1>Diagnose the issue.<br/><i>Keep the builder moving.</i></h1></div><div className="header-actions"><span className="live"><span/> Base RPC live</span><button className="outline-btn" onClick={() => setForm(emptyForm)}>New case <ArrowUpRight size={15}/></button></div></header>
      <OpsDashboard dashboard={dashboard} caseCount={cases.length}/>
      <div className="workspace"><SupportForm form={form} update={update} onSubmit={diagnose} loading={loading}/>
        <section className="right-column"><TriageResults triage={triage} onSave={saveCase}/><RpcLookupPanel rpc={rpc} onLookup={lookupRpc} loading={rpcLoading}/><AiDraftReview draft={draft} currentCase={currentCase} onReview={applyReview}/></section></div>
      {message && <div className="toast">{message}</div>}
      <CaseHistory cases={cases}/>
    </main>
  </div>;
}
export default App;
