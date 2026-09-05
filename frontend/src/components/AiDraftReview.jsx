import { useEffect, useState } from 'react';
import { Check, Sparkles, Terminal, X } from 'lucide-react';

export default function AiDraftReview({ draft, currentCase, onReview }) {
  const [response, setResponse] = useState('');
  useEffect(() => setResponse(draft?.draft || ''), [draft]);
  return <div className="panel draft-panel"><div className="panel-heading"><div><span className="kicker">03 / HUMAN REVIEW</span><h2>Response draft</h2></div>{draft && <span className="pending">{currentCase?.review_status || 'Pending approval'}</span>}</div>{draft ? <><textarea className="draft-copy" value={response} onChange={(event) => setResponse(event.target.value)} aria-label="Editable response draft"/><div className="citation"><Sparkles size={14}/><span>Grounded in <b>{draft.citation}</b> · {draft.provider}</span></div><div className="review-actions"><button className="approve" onClick={() => onReview('accepted', response)}><Check size={15}/> Approve</button><button className="edit" onClick={() => onReview('edited', response)}><Terminal size={15}/> Save edit</button><button className="reject" onClick={() => onReview('rejected', response)}><X size={15}/> Reject</button></div></> : <div className="draft-empty"><Sparkles size={18}/><span>Run a diagnosis to generate a playbook-grounded draft.</span></div>}</div>;
}