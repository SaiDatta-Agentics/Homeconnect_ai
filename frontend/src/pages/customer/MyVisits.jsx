import { useState, useEffect } from 'react';
import { Card, StatusBadge, Spinner } from '../../components/UI';
import { myVisits, listNotifications } from '../../api';
export default function MyVisits() {
  const [visits, setVisits] = useState([]); const [notifs, setNotifs] = useState([]); const [loading, setLoading] = useState(true);
  useEffect(() => { Promise.all([myVisits(), listNotifications()]).then(([v,n]) => { setVisits(v.data); setNotifs(n.data); }).finally(() => setLoading(false)); }, []);
  if (loading) return <Spinner />;
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">My Tours</h2>
      <p className="text-sm text-gray-500 mb-5">Your scheduled property tours and notifications</p>
      {notifs.length > 0 && (
        <div className="mb-5 space-y-2">{notifs.filter(n => !n.is_read).slice(0,3).map(n => (
          <div key={n.id} className="bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
            <div className="text-sm font-semibold text-blue-800">{n.title}</div>
            {n.body && <div className="text-xs text-blue-600 mt-0.5">{n.body}</div>}
          </div>
        ))}</div>
      )}
      {visits.length === 0 ? (
        <Card className="p-10 text-center"><div className="text-gray-400 text-lg mb-2">No tours yet</div><p className="text-sm text-gray-500">Chat with our AI assistant to schedule a tour!</p></Card>
      ) : (
        <div className="space-y-3">{visits.map(v => (
          <Card key={v.id} className="p-5">
            <div className="flex justify-between items-start">
              <div><div className="text-[15px] font-bold text-gray-900">{v.property_name}</div>
                <div className="text-sm text-gray-500 mt-1">{new Date(v.scheduled_date).toLocaleDateString('en-US',{weekday:'long',month:'long',day:'numeric',year:'numeric'})} at {new Date(v.scheduled_date).toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit'})}</div>
                {v.agent_name && <div className="text-xs text-gray-400 mt-1">Agent: {v.agent_name}</div>}
                {v.postpone_reason && <div className="text-xs text-orange-600 mt-1 bg-orange-50 px-2 py-1 rounded inline-block">Rescheduled: {v.postpone_reason}</div>}
              </div>
              <StatusBadge status={v.status} />
            </div>
          </Card>
        ))}</div>
      )}
    </div>
  );
}
