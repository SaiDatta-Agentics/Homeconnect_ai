import { useState, useEffect } from 'react';
import { Card, Spinner } from '../../components/UI';
import { getEnquiryStats } from '../../api';
function Bar({ label, value, max, color='bg-blue-500' }) {
  const pct = max>0?(value/max)*100:0;
  return <div className="mb-2.5"><div className="flex justify-between text-xs mb-1"><span className="text-gray-500 capitalize">{label}</span><span className="text-gray-800 font-semibold font-mono">{value}</span></div><div className="h-2 bg-gray-100 rounded-full overflow-hidden"><div className={`h-full ${color} rounded-full transition-all duration-500`} style={{width:`${pct}%`}}/></div></div>;
}
export default function AdminAnalytics() {
  const [s, setS] = useState(null); const [loading, setLoading] = useState(true);
  useEffect(() => { getEnquiryStats().then(r=>setS(r.data)).finally(()=>setLoading(false)); }, []);
  if (loading) return <Spinner />;
  const d = s||{}; const sm = Math.max(...Object.values(d.enquiries_by_status||{}),1); const vm = Math.max(...Object.values(d.visits_by_status||{}),1);
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Analytics</h2>
      <p className="text-sm text-gray-500 mb-5">Performance breakdown</p>
      <div className="grid grid-cols-4 gap-3 mb-6">
        <Card className="p-4 text-center"><div className="text-2xl font-bold text-gray-900">{d.total_enquiries}</div><div className="text-xs text-gray-400">Enquiries</div></Card>
        <Card className="p-4 text-center"><div className="text-2xl font-bold text-gray-900">{d.total_visits}</div><div className="text-xs text-gray-400">Tours</div></Card>
        <Card className="p-4 text-center"><div className="text-2xl font-bold text-emerald-600">{d.conversion_rate}%</div><div className="text-xs text-gray-400">Conversion</div></Card>
        <Card className="p-4 text-center"><div className="text-2xl font-bold text-blue-600">{d.total_properties}</div><div className="text-xs text-gray-400">Listings</div></Card>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div><div className="text-xs font-semibold text-gray-400 uppercase mb-2">Enquiry Pipeline</div><Card className="p-5">{Object.entries(d.enquiries_by_status||{}).map(([k,v])=><Bar key={k} label={k.replace('_',' ')} value={v} max={sm}/>)}</Card></div>
        <div><div className="text-xs font-semibold text-gray-400 uppercase mb-2">Tour Status</div><Card className="p-5">{Object.entries(d.visits_by_status||{}).map(([k,v])=><Bar key={k} label={k.replace('_',' ')} value={v} max={vm} color="bg-indigo-500"/>)}</Card></div>
        <div><div className="text-xs font-semibold text-gray-400 uppercase mb-2">Agent Performance</div><Card className="p-5">{(d.agent_performance||[]).map(a=><div key={a.name} className="mb-3 pb-3 border-b border-gray-100 last:border-0"><div className="text-sm font-semibold text-gray-800">{a.name}</div><div className="flex gap-4 mt-1 text-xs text-gray-500"><span>Assigned: <span className="font-semibold text-gray-700">{a.assigned}</span></span><span>Completed: <span className="font-semibold text-emerald-600">{a.visits_completed}</span></span></div></div>)}</Card></div>
      </div>
      <div className="mt-5"><div className="text-xs font-semibold text-gray-400 uppercase mb-2">Daily Enquiries (14 days)</div><Card className="p-5"><div className="flex items-end gap-1.5 h-32">{(d.daily_enquiries||[]).map((x,i)=>{const mx=Math.max(...(d.daily_enquiries||[]).map(z=>z.count),1);const h=x.count>0?Math.max((x.count/mx)*100,8):4;return<div key={i} className="flex-1 flex flex-col items-center gap-1"><span className="text-[10px] text-gray-400 font-mono">{x.count||''}</span><div className="w-full bg-blue-400 rounded-t transition-all" style={{height:`${h}%`}}/><span className="text-[9px] text-gray-400">{new Date(x.date).getDate()}</span></div>})}</div></Card></div>
    </div>
  );
}
