import { useState, useEffect } from 'react';
import { Card, StatusBadge, Spinner } from '../../components/UI';
import { listVisits, updateVisitStatus, postponeVisit, submitVisitFeedback } from '../../api';
const FILTERS = ['all','scheduled','confirmed','completed','cancelled','postponed'];
export default function AdminVisits() {
  const [vis, setVis] = useState([]); const [f, setF] = useState('all'); const [loading, setLoading] = useState(true);
  const [ppId, setPpId] = useState(null); const [ppForm, setPpForm] = useState({ new_date:'', new_time:'10:00 AM', reason:'' });
  const [ppErr, setPpErr] = useState('');
  const load = () => { setLoading(true); listVisits(f==='all'?null:f).then(r=>setVis(r.data)).finally(()=>setLoading(false)); };
  useEffect(load, [f]);
  const doPostpone = async () => {
    setPpErr('');
    try { await postponeVisit(ppId, ppForm); setPpId(null); load(); }
    catch(e) { setPpErr(e.response?.data?.detail || 'Failed — time conflict'); }
  };
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Tours</h2>
      <p className="text-sm text-gray-500 mb-4">Manage all scheduled property tours</p>
      <div className="flex gap-1.5 mb-4 flex-wrap">{FILTERS.map(x=><button key={x} onClick={()=>setF(x)} className={`text-xs px-3 py-1.5 rounded-full border capitalize transition ${f===x?'border-blue-300 bg-blue-50 text-blue-700 font-semibold':'border-gray-200 text-gray-500 hover:bg-gray-100'}`}>{x}</button>)}</div>
      {loading?<Spinner/>:<Card><div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="border-b border-gray-200">
        {['Buyer','Property','Date & Time','Agent','Status','Actions'].map(h=><th key={h} className="px-4 py-2.5 text-left text-xs font-semibold text-gray-400">{h}</th>)}</tr></thead>
        <tbody>{vis.map(v=><tr key={v.id} className="border-b border-gray-50 hover:bg-gray-50/50">
          <td className="px-4 py-3"><div className="font-semibold text-gray-800">{v.buyer_name}</div><div className="text-xs text-gray-400">{v.buyer_phone}</div></td>
          <td className="px-4 py-3 text-gray-600">{v.property_name}</td>
          <td className="px-4 py-3 text-gray-600 text-xs font-mono">{new Date(v.scheduled_date).toLocaleDateString('en-US',{month:'short',day:'numeric'})} {new Date(v.scheduled_date).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})}</td>
          <td className="px-4 py-3 text-gray-600">{v.agent_name||'—'}</td>
          <td className="px-4 py-3"><StatusBadge status={v.status}/></td>
          <td className="px-4 py-3"><div className="flex gap-1.5 flex-wrap">
            {v.status==='scheduled'&&<><button onClick={()=>updateVisitStatus(v.id,'confirmed').then(load)} className="text-xs px-2 py-1 rounded border border-green-200 text-green-600 hover:bg-green-50">Confirm</button>
              <button onClick={()=>{setPpId(v.id);setPpErr('');}} className="text-xs px-2 py-1 rounded border border-orange-200 text-orange-600 hover:bg-orange-50">Postpone</button>
              <button onClick={()=>updateVisitStatus(v.id,'cancelled').then(load)} className="text-xs px-2 py-1 rounded border border-red-200 text-red-600 hover:bg-red-50">Cancel</button></>}
            {v.status==='confirmed'&&<><button onClick={()=>updateVisitStatus(v.id,'completed').then(load)} className="text-xs px-2 py-1 rounded border border-green-200 text-green-600 hover:bg-green-50">Complete</button>
              <button onClick={()=>{setPpId(v.id);setPpErr('');}} className="text-xs px-2 py-1 rounded border border-orange-200 text-orange-600 hover:bg-orange-50">Postpone</button></>}
            {v.status==='postponed'&&<button onClick={()=>updateVisitStatus(v.id,'confirmed').then(load)} className="text-xs px-2 py-1 rounded border border-green-200 text-green-600 hover:bg-green-50">Confirm</button>}
            {v.rating&&<span className="text-xs text-amber-500">{'★'.repeat(v.rating)}</span>}
          </div></td></tr>)}
          {vis.length===0&&<tr><td colSpan={6} className="py-10 text-center text-gray-400">No tours</td></tr>}
        </tbody></table></div></Card>}
      {ppId&&<div className="fixed inset-0 bg-black/30 flex items-center justify-center z-50" onClick={()=>setPpId(null)}>
        <div className="bg-white border border-gray-200 rounded-xl p-6 w-96 shadow-xl animate-fade-in" onClick={e=>e.stopPropagation()}>
          <h3 className="text-base font-bold text-gray-900 mb-3">Postpone Tour</h3>
          <p className="text-xs text-gray-500 mb-3">The customer will be automatically notified of the change.</p>
          <div className="grid grid-cols-2 gap-3 mb-3">
            <div><label className="block text-xs text-gray-500 mb-1">New Date</label><input type="date" value={ppForm.new_date} onChange={e=>setPpForm(p=>({...p,new_date:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
            <div><label className="block text-xs text-gray-500 mb-1">New Time</label><select value={ppForm.new_time} onChange={e=>setPpForm(p=>({...p,new_time:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none">
              {['9:00 AM','10:00 AM','11:00 AM','1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM'].map(t=><option key={t}>{t}</option>)}</select></div>
          </div>
          <div className="mb-3"><label className="block text-xs text-gray-500 mb-1">Reason (shown to customer)</label><textarea value={ppForm.reason} onChange={e=>setPpForm(p=>({...p,reason:e.target.value}))} rows={2} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500" placeholder="e.g. Agent unavailable, weather conditions..."/></div>
          {ppErr&&<div className="text-xs text-red-600 mb-2">{ppErr}</div>}
          <button onClick={doPostpone} disabled={!ppForm.new_date||!ppForm.reason} className="w-full py-2 text-sm font-semibold rounded-lg bg-orange-500 text-white hover:bg-orange-600 disabled:opacity-40 transition">Reschedule & Notify Customer</button>
        </div>
      </div>}
    </div>
  );
}
