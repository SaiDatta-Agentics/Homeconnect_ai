import { useState, useEffect } from 'react';
import { Card, StatusBadge, Spinner } from '../../components/UI';
import { listProperties } from '../../api';
export default function CustomerHome() {
  const [props, setProps] = useState([]); const [loading, setLoading] = useState(true);
  useEffect(() => { listProperties().then(r => setProps(r.data)).finally(() => setLoading(false)); }, []);
  if (loading) return <Spinner />;
  return (
    <div className="animate-fade-in">
      <h2 className="text-xl font-bold text-gray-900">Browse Properties</h2>
      <p className="text-sm text-gray-500 mb-5">Find your perfect home across our premium communities</p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {props.map(p => (
          <Card key={p.id} className="overflow-hidden hover:shadow-md transition-shadow">
            <div className="h-36 bg-gradient-to-br from-blue-100 to-blue-50 flex items-center justify-center">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#93c5fd" strokeWidth="1.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
            </div>
            <div className="p-4">
              <div className="flex justify-between items-start mb-2">
                <div><div className="text-[15px] font-bold text-gray-900">{p.name}</div><div className="text-xs text-gray-500">{p.city}, {p.state}</div></div>
                <StatusBadge status={p.status} />
              </div>
              <div className="text-xl font-bold text-blue-600 mb-3">${p.price_usd.toLocaleString()}</div>
              <div className="grid grid-cols-3 gap-2 text-xs text-gray-600">
                <div className="text-center bg-gray-50 rounded-lg py-1.5"><div className="font-bold text-gray-900">{p.bedrooms}</div>Beds</div>
                <div className="text-center bg-gray-50 rounded-lg py-1.5"><div className="font-bold text-gray-900">{p.bathrooms}</div>Baths</div>
                <div className="text-center bg-gray-50 rounded-lg py-1.5"><div className="font-bold text-gray-900">{p.total_area_sqft.toLocaleString()}</div>Sqft</div>
              </div>
              {p.description && <p className="text-xs text-gray-500 mt-2.5 line-clamp-2">{p.description}</p>}
              {p.mls_id && <div className="text-[10px] text-gray-400 mt-2 font-mono">MLS: {p.mls_id}</div>}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
