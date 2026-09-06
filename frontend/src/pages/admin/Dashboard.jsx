import { useState, useEffect } from 'react';
import { MetricCard, Card, StatusBadge, Spinner } from '../../components/UI';
import { getEnquiryStats, listEnquiries, listVisits, getActivityFeed } from '../../api';
export default function AdminDashboard() {
  const [s, setS] = useState(null); const [enqs, setEnqs] = useState([]); const [vis, setVis] = useState([]); const [act, setAct] = useState([]); const [loading, setLoading] = useState(true);
  const load = () => Promise.all([getEnquiryStats(), listEnquiries(), listVisits(), getActivityFeed()]).then(([a,b,c,d]) => { setS(a.data); setEnqs(b.data.slice(0,5)); setVis(c.data.filter(x=>['scheduled','confirmed'].includes(x.status)).slice(0,5)); setAct(d.data.slice(0,6)); }).finally(()=>setLoading(false));
  useEffect(() => { load(); const id=setInterval(load,30000); return ()=>clearInterval(id); }, []);
  if (loading) return <Spinner />;
  const d = s || {};
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Dashboard</h2>
      <p className="text-sm text-gray-500 mb-5">Live overview — refreshes every 30s</p>
      <div className="flex gap-3 flex-wrap mb-6">
        <MetricCard value={d.total_enquiries||0} label="Total Enquiries" color="text-blue-600" />
        <MetricCard value={d.total_visits||0} label="Total Tours" color="text-indigo-600" />
        <MetricCard value={d.enquiries_by_status?.new||0} label="New Leads" color="text-amber-600" />
        <MetricCard value={d.enquiries_by_status?.escalated||0} label="Escalated" color="text-red-600" />
        <MetricCard value={`${d.conversion_rate||0}%`} label="Conversion" color="text-emerald-600" />
      </div>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div><div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Recent Enquiries</div>
          <Card>{enqs.map((e,i)=><div key={e.id} className={`flex justify-between items-center px-4 py-3 ${i<enqs.length-1?'border-b border-gray-100':''}`}><div className="min-w-0"><div className="text-sm font-semibold text-gray-800 truncate">{e.buyer_name}</div><div className="text-xs text-gray-400 truncate">{e.property_interest} · {e.budget_range}</div></div><StatusBadge status={e.status}/></div>)}</Card></div>
        <div><div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Upcoming Tours</div>
          <Card>{vis.length===0?<div className="p-6 text-center text-sm text-gray-400">No upcoming tours</div>:vis.map((v,i)=><div key={v.id} className={`flex justify-between items-center px-4 py-3 ${i<vis.length-1?'border-b border-gray-100':''}`}><div><div className="text-sm font-semibold text-gray-800">{v.buyer_name}</div><div className="text-xs text-gray-400">{v.property_name} · {new Date(v.scheduled_date).toLocaleDateString('en-US',{weekday:'short',month:'short',day:'numeric'})}</div></div><StatusBadge status={v.status}/></div>)}</Card></div>
        <div><div className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">Activity</div>
          <Card>{act.map((a,i)=><div key={a.id} className={`px-4 py-2.5 ${i<act.length-1?'border-b border-gray-100':''}`}><div className="text-xs text-gray-700">{a.action}</div>{a.details&&<div className="text-xs text-gray-400 truncate">{a.details}</div>}</div>)}</Card></div>
      </div>
    </div>
  );
}
