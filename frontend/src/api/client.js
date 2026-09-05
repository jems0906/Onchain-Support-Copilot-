const API_BASE = import.meta.env.VITE_API_URL || '/api';
export async function api(path, options = {}) {
  const reviewerId = import.meta.env.VITE_REVIEWER_ID || 'local-reviewer';
  const response = await fetch(`${API_BASE}${path}`, { headers: { 'Content-Type': 'application/json', 'X-Reviewer-ID': reviewerId, ...(options.headers || {}) }, ...options });
  if (!response.ok) throw new Error((await response.json().catch(() => ({}))).detail || 'Request failed');
  return response.json();
}
export const runTriage = (data) => api('/triage', { method: 'POST', body: JSON.stringify(data) });
export const createCase = (data) => api('/cases', { method: 'POST', body: JSON.stringify(data) });
export const getDashboard = () => api('/dashboards/overview');
export const getCases = () => api('/cases');
export const getDraft = (caseData, triage) => api('/ai/draft', { method: 'POST', body: JSON.stringify({ case: caseData, triage }) });
export const getReceipt = (network, value) => api('/rpc/tx-receipt', { method: 'POST', body: JSON.stringify({ network, value }) });
export const getBalance = (network, value) => api('/rpc/balance', { method: 'POST', body: JSON.stringify({ network, value }) });
export const getCode = (network, value) => api('/rpc/code', { method: 'POST', body: JSON.stringify({ network, value }) });
export const reviewCase = (caseId, status, response, source, timeSavedMinutes) => api(`/cases/${caseId}/review`, { method: 'POST', body: JSON.stringify({ case_id: caseId, status, response, source, reviewer_id: import.meta.env.VITE_REVIEWER_ID || 'local-reviewer', time_saved_minutes: timeSavedMinutes }) });
export const getKnowledgeBase = () => api('/kb');
