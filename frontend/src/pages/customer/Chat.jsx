import { useState, useRef, useEffect, useCallback } from 'react';
import { Card } from '../../components/UI';
import { sendMessage, bookVisit } from '../../api';
import { useAuth } from '../../AuthContext';
export default function CustomerChat() {
  const { user } = useAuth();
  const [msgs, setMsgs] = useState([{ id:0, sender:'agent', text:"Hello! 👋 Welcome to HomeConnect AI. I'm here to help you find your perfect home.\n\nWe have properties in Toronto, Austin, and Vancouver. What are you looking for?", time:new Date(), actions:['View Pricing','Check Availability','Schedule Tour'] }]);
  const [input, setInput] = useState(''); const [typing, setTyping] = useState(false); const [eId, setEId] = useState(null);
  const [showBook, setShowBook] = useState(false);
  const [bf, setBf] = useState({ name: user?.full_name||'', phone: user?.phone||'', date: '', time: '10:00 AM', property: 'Sunset Valley Homes' });
  const endRef = useRef(null); const inputRef = useRef(null);
  useEffect(() => { endRef.current?.scrollIntoView({ behavior:'smooth' }); }, [msgs, typing]);

  const send = useCallback(async () => {
    const t = input.trim(); if (!t) return;
    setMsgs(p => [...p, { id:Date.now(), sender:'buyer', text:t, time:new Date() }]); setInput(''); setTyping(true);
    try {
      const r = await sendMessage(t, eId, user?.full_name, user?.phone, user?.email);
      if (r.data.enquiry_id) setEId(r.data.enquiry_id);
      setMsgs(p => [...p, { id:Date.now()+1, sender:'agent', text:r.data.reply, time:new Date(), intent:r.data.intent, actions:r.data.suggested_actions, escalated:r.data.escalated }]);
      if (r.data.intent === 'visit') setShowBook(true);
    } catch { setMsgs(p => [...p, { id:Date.now()+1, sender:'agent', text:'Connection error. Please try again.', time:new Date() }]); }
    finally { setTyping(false); }
  }, [input, eId, user]);

  const doBook = async () => {
    try {
      const r = await bookVisit({ enquiry_id: eId, buyer_name:bf.name, buyer_phone:bf.phone, preferred_date:bf.date, preferred_time:bf.time, property_name:bf.property });
      setMsgs(p => [...p, { id:Date.now(), sender:'agent', text: r.data.conflict ? `⚠ ${r.data.message}` : `✅ ${r.data.message}`, time:new Date() }]);
      if (!r.data.conflict) { setShowBook(false); setBf(p => ({...p, date:'', time:'10:00 AM'})); }
    } catch { setMsgs(p => [...p, { id:Date.now(), sender:'agent', text:'Booking failed. Try again.', time:new Date() }]); }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-7.5rem)] animate-fade-in">
      <div className="flex justify-between items-center mb-3">
        <div><h2 className="text-xl font-bold text-gray-900">AI Assistant</h2><p className="text-xs text-gray-500">Available 24/7 — ask about pricing, availability, tours</p></div>
        <div className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-green-500" /><span className="text-xs text-green-600 font-semibold">Online</span></div>
      </div>
      <Card className="flex-1 overflow-auto p-4 flex flex-col gap-3 min-h-0">
        {msgs.map(m => (
          <div key={m.id} className={`flex ${m.sender==='buyer'?'justify-end':'justify-start'} animate-fade-in`}>
            <div className={`max-w-[75%] px-3.5 py-2.5 rounded-2xl ${m.sender==='buyer'?'bg-blue-600 text-white rounded-br-sm':'bg-gray-100 text-gray-900 rounded-bl-sm'}`}>
              {m.escalated && <div className="text-xs font-bold text-red-600 mb-1">⚠ Transferred to staff</div>}
              <div className="text-sm leading-relaxed whitespace-pre-wrap">{m.text}</div>
              {m.actions?.length > 0 && m.sender==='agent' && (
                <div className="flex flex-wrap gap-1.5 mt-2">{m.actions.map(a => (
                  <button key={a} onClick={() => { if(a.includes('Tour')||a.includes('Visit')||a.includes('Date')) setShowBook(true); else { setInput(a); inputRef.current?.focus(); } }}
                    className="text-xs px-2.5 py-1 rounded-full border border-gray-300 text-blue-600 hover:bg-blue-50 transition">{a}</button>
                ))}</div>)}
              <div className={`text-[10px] mt-1 text-right ${m.sender==='buyer'?'text-blue-200':'text-gray-400'}`}>{m.time.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>
            </div>
          </div>
        ))}
        {typing && <div className="flex justify-start"><div className="px-4 py-3 rounded-2xl bg-gray-100 rounded-bl-sm"><div className="flex gap-1">{[0,1,2].map(i=><div key={i} className="w-1.5 h-1.5 rounded-full bg-gray-400 typing-dot"/>)}</div></div></div>}
        <div ref={endRef}/>
      </Card>
      {showBook && (
        <Card className="mt-3 p-5 border-blue-200 animate-fade-in">
          <div className="flex justify-between items-center mb-3"><span className="text-sm font-bold text-gray-900">📅 Schedule Tour</span><button onClick={()=>setShowBook(false)} className="text-gray-400 hover:text-gray-600 text-lg">×</button></div>
          <div className="grid grid-cols-2 gap-3">
            <div><label className="block text-xs text-gray-500 mb-1">Name</label><input value={bf.name} onChange={e=>setBf(p=>({...p,name:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
            <div><label className="block text-xs text-gray-500 mb-1">Phone</label><input value={bf.phone} onChange={e=>setBf(p=>({...p,phone:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
            <div><label className="block text-xs text-gray-500 mb-1">Date</label><input type="date" value={bf.date} onChange={e=>setBf(p=>({...p,date:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
            <div><label className="block text-xs text-gray-500 mb-1">Time</label><select value={bf.time} onChange={e=>setBf(p=>({...p,time:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none">
              {['9:00 AM','10:00 AM','11:00 AM','1:00 PM','2:00 PM','3:00 PM','4:00 PM','5:00 PM'].map(t=><option key={t}>{t}</option>)}</select></div>
          </div>
          <div className="mt-3"><label className="block text-xs text-gray-500 mb-1">Community</label><select value={bf.property} onChange={e=>setBf(p=>({...p,property:e.target.value}))} className="w-full px-3 py-2 text-sm rounded-lg border border-gray-300 outline-none">
            <option>Maple Ridge Estates</option><option>Sunset Valley Homes</option><option>Pacific Crest Residences</option></select></div>
          <button onClick={doBook} disabled={!bf.name||!bf.phone||!bf.date} className="w-full mt-3 py-2.5 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-40 transition">Confirm Tour</button>
        </Card>
      )}
      <div className="flex gap-2 mt-3">
        <input ref={inputRef} value={input} onChange={e=>setInput(e.target.value)} onKeyDown={e=>e.key==='Enter'&&send()} placeholder="Ask about homes, pricing, tours…"
          className="flex-1 px-4 py-3 text-sm rounded-xl border border-gray-300 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100"/>
        <button onClick={send} disabled={!input.trim()} className="px-5 py-3 text-sm font-semibold rounded-xl bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-40 transition">Send</button>
      </div>
    </div>
  );
}
