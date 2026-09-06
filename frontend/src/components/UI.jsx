export function StatusBadge({ status }) {
  const m = { new:'bg-blue-100 text-blue-700', contacted:'bg-amber-100 text-amber-700', qualified:'bg-yellow-100 text-yellow-700',
    visit_booked:'bg-green-100 text-green-700', escalated:'bg-red-100 text-red-700', converted:'bg-emerald-100 text-emerald-800',
    lost:'bg-gray-100 text-gray-500', scheduled:'bg-blue-100 text-blue-700', confirmed:'bg-green-100 text-green-700',
    completed:'bg-gray-200 text-gray-600', cancelled:'bg-red-100 text-red-700', postponed:'bg-orange-100 text-orange-700',
    available:'bg-green-100 text-green-700', reserved:'bg-yellow-100 text-yellow-700', sold:'bg-gray-200 text-gray-600', conflict:'bg-red-100 text-red-700' };
  return <span className={`text-[11px] font-semibold px-2.5 py-0.5 rounded-full capitalize whitespace-nowrap ${m[status]||'bg-gray-100 text-gray-500'}`}>{(status||'').replace('_',' ')}</span>;
}
export function Card({ children, className = '' }) { return <div className={`bg-white border border-gray-200 rounded-xl shadow-sm ${className}`}>{children}</div>; }
export function MetricCard({ value, label, icon, color = 'text-blue-600' }) {
  return <Card className="p-5 flex-1 min-w-[150px]"><div className={`text-[28px] font-bold font-mono tracking-tight ${color}`}>{value}</div><div className="text-[12px] text-gray-500 mt-1">{label}</div></Card>;
}
export function Spinner() { return <div className="flex items-center justify-center py-12"><div className="w-6 h-6 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin"/></div>; }
