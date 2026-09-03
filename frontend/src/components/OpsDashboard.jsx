function Metric({ label, value, note, tone = '' }) {
  return <div className="metric"><span>{label}</span><strong className={tone}>{value}</strong><small>{note}</small></div>;
}

export default function OpsDashboard({ dashboard, caseCount }) {
  return <section className="metrics"><Metric label="Open cases" value={dashboard?.total_cases ?? caseCount} note="Current queue"/><Metric label="Playbook reuse" value={dashboard ? `${Math.round(dashboard.response_reuse_rate * 100)}%` : '82%'} note="Last 30 days" tone="teal"/><Metric label="Avg. time saved" value={`${dashboard?.avg_minutes_saved ?? 7.5}m`} note="Per AI-assisted response" tone="orange"/><Metric label="RPC network" value="99.98%" note="Base endpoints" tone="teal"/></section>;
}