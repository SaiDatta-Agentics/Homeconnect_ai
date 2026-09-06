import { useState, useEffect } from 'react';
import { Card, Spinner } from '../../components/UI';
import { getActivityFeed } from '../../api';
const COLORS = { agent:'bg-blue-100 text-blue-700', staff:'bg-emerald-100 text-emerald-700', system:'bg-gray-100 text-gray-500' };
export default function AdminActivity() {
  const [items, setItems] = useState([]); const [loading, setLoading] = useState(true);
  useEffect(() => { const l=()=>getActivityFeed().then(r=>setItems(r.data)).finally(()=>setLoading(false)); l(); const id=setInterval(l,15000); return ()=>clearInterval(id); }, []);
  if (loading) return <Spinner />;
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Activity Feed</h2>
      <p className="text-sm text-gray-500 mb-5">Real-time log — auto-refreshes every 15s</p>
      <Card>{items.map((a,i)=><div key={a.id} className={`flex gap-4 px-5 py-3.5 ${i<items.length-1?'border-b border-gray-100':''}`}>
        <div className="flex flex-col items-center pt-0.5"><div className={`w-2.5 h-2.5 rounded-full ${a.actor==='agent'?'bg-blue-500':a.actor==='staff'?'bg-emerald-500':'bg-gray-400'}`}/>{i<items.length-1&&<div className="w-px flex-1 bg-gray-200 mt-1"/>}</div>
        <div className="flex-1"><div className="flex items-center gap-2"><span className={`text-[11px] font-semibold px-2 py-0.5 rounded-full ${COLORS[a.actor]||COLORS.system}`}>{a.actor==='agent'?'AI Agent':a.actor==='staff'?'Staff':'System'}</span><span className="text-sm text-gray-800">{a.action}</span></div>
          {a.details&&<div className="text-xs text-gray-500 mt-0.5">{a.details}</div>}
          <div className="text-[10px] text-gray-400 mt-1 font-mono">{new Date(a.created_at).toLocaleString('en-US',{month:'short',day:'numeric',hour:'2-digit',minute:'2-digit'})}</div>
        </div></div>)}{items.length===0&&<div className="py-10 text-center text-gray-400 text-sm">No activity</div>}</Card>
    </div>
  );
}
