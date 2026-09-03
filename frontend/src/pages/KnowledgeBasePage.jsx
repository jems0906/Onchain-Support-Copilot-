import { useEffect, useState } from 'react';
import { getKnowledgeBase } from '../api/client';

export default function KnowledgeBasePage({ onBack }) {
  const [items, setItems] = useState([]);
  useEffect(() => { getKnowledgeBase().then((result) => setItems(result.items || [])).catch(() => setItems([])); }, []);
  return <main><button className="text-btn" onClick={onBack}>Back to intake</button><div className="eyebrow">OPERATIONS / PLAYBOOKS</div><h1>Approved guidance.</h1><p className="page-intro">Reusable troubleshooting paths for Base builder support.</p><section className="kb-grid">{items.map((item) => <article className="panel page-panel" key={item.citation}><span className="kicker">PLAYBOOK</span><h2>{item.title}</h2><p>{item.summary}</p><div className="playbook-steps">{item.steps.map((step) => <div key={step}>{step}</div>)}</div><small className="muted">Source: {item.citation}</small></article>)}{!items.length && <p>Knowledge base unavailable.</p>}</section></main>;
}
