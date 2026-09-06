import { useState, useEffect } from 'react';
import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../../AuthContext';
import { getUnreadCount, listNotifications, markAllRead } from '../../api';
const NAV = [
  { to:'/admin', label:'Dashboard', end:true }, { to:'/admin/visits', label:'Tours' },
  { to:'/admin/enquiries', label:'Enquiries' }, { to:'/admin/properties', label:'Properties' },
  { to:'/admin/analytics', label:'Analytics' }, { to:'/admin/activity', label:'Activity' },
];
export default function AdminLayout() {
  const { user, logout } = useAuth();
  const [unread, setUnread] = useState(0); const [showN, setShowN] = useState(false); const [notifs, setNotifs] = useState([]);
  useEffect(() => { const p = () => getUnreadCount().then(r=>setUnread(r.data.count)).catch(()=>{}); p(); const id=setInterval(p,15000); return ()=>clearInterval(id); }, []);
  const openN = async () => { setShowN(!showN); if (!showN) { const r = await listNotifications(); setNotifs(r.data); } };
  const readAll = async () => { await markAllRead(); setUnread(0); setNotifs(n=>n.map(x=>({...x,is_read:true}))); };
  return (
    <div className="flex h-screen bg-gray-50">
      <aside className="w-56 bg-white border-r border-gray-200 flex flex-col flex-shrink-0">
        <div className="px-5 py-4 border-b border-gray-100"><div className="flex items-center gap-2"><div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg></div><span className="font-bold text-gray-900 text-sm">HomeConnect</span></div><div className="text-[10px] text-gray-400 mt-0.5">Admin Panel</div></div>
        <nav className="flex-1 px-3 py-2 space-y-0.5">{NAV.map(n=>(
          <NavLink key={n.to} to={n.to} end={n.end} className={({isActive})=>`block px-3 py-2 rounded-lg text-sm transition ${isActive?'bg-blue-50 text-blue-700 font-semibold':'text-gray-600 hover:bg-gray-100'}`}>{n.label}</NavLink>
        ))}</nav>
        <div className="px-4 py-3 border-t border-gray-100"><div className="text-sm font-semibold text-gray-800 truncate">{user?.full_name}</div><div className="text-xs text-gray-400">{user?.role}</div>
          <button onClick={logout} className="w-full mt-2 py-1.5 text-xs text-gray-500 border border-gray-200 rounded-lg hover:bg-gray-50 transition">Sign out</button></div>
      </aside>
      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="h-12 bg-white border-b border-gray-200 flex items-center justify-end px-5 gap-3 flex-shrink-0">
          <div className="flex items-center gap-1.5 mr-auto"><div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"/><span className="text-xs text-green-600 font-semibold">Agent Online 24/7</span></div>
          <div className="relative">
            <button onClick={openN} className="relative text-gray-500 hover:text-gray-700 p-1">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"><path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0"/></svg>
              {unread>0&&<span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-white text-[10px] flex items-center justify-center font-bold">{unread}</span>}
            </button>
            {showN&&<div className="absolute right-0 top-9 w-80 max-h-96 overflow-auto bg-white border border-gray-200 rounded-xl shadow-lg z-50 animate-fade-in">
              <div className="flex justify-between items-center px-4 py-2.5 border-b border-gray-100"><span className="text-sm font-semibold">Notifications</span>{unread>0&&<button onClick={readAll} className="text-xs text-blue-600 hover:underline">Mark all read</button>}</div>
              {notifs.map(n=><div key={n.id} className={`px-4 py-3 border-b border-gray-50 ${n.is_read?'opacity-60':''}`}><div className="text-xs font-semibold text-gray-800">{n.title}</div>{n.body&&<div className="text-xs text-gray-500 mt-0.5">{n.body}</div>}</div>)}
              {notifs.length===0&&<div className="px-4 py-6 text-center text-gray-400 text-sm">No notifications</div>}
            </div>}
          </div>
        </div>
        <main className="flex-1 overflow-auto p-6"><Outlet /></main>
      </div>
    </div>
  );
}
