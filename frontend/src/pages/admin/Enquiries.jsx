import { useState, useEffect } from 'react';
import { Card, StatusBadge, Spinner } from '../../components/UI';
import { listEnquiries, updateEnquiry } from '../../api';
const FILTERS = ['all','new','contacted','qualified','visit_booked','escalated','converted','lost'];
export default function AdminEnquiries() {
  const [data, setData] = useState([]); const [f, setF] = useState('all'); const [loading, setLoading] = useState(true);
  const load = () => { setLoading(true); listEnquiries(f==='all'?null:f).then(r=>setData(r.data)).finally(()=>setLoading(false)); };
  useEffect(load, [f]);
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Enquiries</h2>
      <p className="text-sm text-gray-500 mb-4">All buyer enquiries captured by the AI agent</p>
      <div className="flex gap-1.5 mb-4 flex-wrap">{FILTERS.map(x=><button key={x} onClick={()=>setF(x)} className={`text-xs px-3 py-1.5 rounded-full border capitalize transition ${f===x?'border-blue-300 bg-blue-50 text-blue-700 font-semibold':'border-gray-200 text-gray-500 hover:bg-gray-100'}`}>{x.replace('_',' ')}</button>)}</div>
      {loading?<Spinner/>:<Card><div className="overflow-x-auto"><table className="w-full text-sm"><thead><tr className="border-b border-gray-200">
        {['Buyer','Interest','Budget','Source','Msgs','Status','Update'].map(h=><th key={h} className="px-4 py-2.5 text-left text-xs font-semibold text-gray-400">{h}</th>)}</tr></thead>
        <tbody>{data.map(e=><tr key={e.id} className="border-b border-gray-50 hover:bg-gray-50/50">
          <td className="px-4 py-3"><div className="font-semibold text-gray-800">{e.buyer_name}</div><div className="text-xs text-gray-400">{e.buyer_phone}</div></td>
          <td className="px-4 py-3 text-gray-600">{e.property_interest||'—'}</td>
          <td className="px-4 py-3 text-gray-600 font-mono text-xs">{e.budget_range||'—'}</td>
          <td className="px-4 py-3"><span className="text-xs px-2 py-0.5 rounded-full bg-blue-50 text-blue-600 capitalize">{e.source}</span></td>
          <td className="px-4 py-3 text-gray-500 font-mono">{e.message_count}</td>
          <td className="px-4 py-3"><StatusBadge status={e.status}/></td>
          <td className="px-4 py-3"><select value={e.status} onChange={ev=>updateEnquiry(e.id,{status:ev.target.value}).then(load)} className="text-xs px-2 py-1 rounded border border-gray-200 text-gray-600 outline-none">
            {['new','contacted','qualified','visit_booked','escalated','converted','lost'].map(s=><option key={s} value={s}>{s.replace('_',' ')}</option>)}</select></td>
        </tr>)}</tbody></table></div></Card>}
    </div>
  );
}
