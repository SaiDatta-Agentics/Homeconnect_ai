import { useState, useEffect } from 'react';
import { Card, StatusBadge, Spinner } from '../../components/UI';
import { listProperties, createProperty, deleteProperty } from '../../api';
export default function AdminProperties() {
  const [props, setProps] = useState([]); const [loading, setLoading] = useState(true); const [show, setShow] = useState(false);
  const blank = { name:'', project_name:'', property_type:'Condo', total_area_sqft:0, price_usd:0, bedrooms:3, bathrooms:2, floor_number:null, total_floors:0, facing:'', parking:1, amenities:'', completion_date:'', description:'', location:'', address:'', city:'', state:'', country:'USA', zip_code:'', mls_id:'', year_built:2025, lot_size_sqft:0, hoa_monthly:0 };
  const [f, setF] = useState({...blank});
  const load = () => { setLoading(true); listProperties().then(r=>setProps(r.data)).finally(()=>setLoading(false)); };
  useEffect(load, []);
  const submit = async () => { await createProperty(f); setShow(false); setF({...blank}); load(); };
  const del = async (id) => { if(confirm('Delete this property?')) { await deleteProperty(id); load(); } };
  return (
    <div className="animate-fade-in">
      <div className="flex justify-between items-center mb-4"><div><h2 className="text-xl font-bold text-gray-900">Properties</h2><p className="text-sm text-gray-500">Manage listings — add, edit, remove</p></div>
        <button onClick={()=>setShow(!show)} className="px-4 py-2 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition">+ Add Property</button></div>
      {show&&<Card className="p-5 mb-4 border-blue-200 animate-fade-in">
        <div className="text-sm font-bold text-gray-800 mb-3">New Property (saved to database)</div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
          {[['name','Name'],['project_name','Community'],['city','City'],['state','State/Province'],['address','Address'],['zip_code','Zip'],['mls_id','MLS ID']].map(([k,l])=>
            <div key={k}><label className="block text-xs text-gray-500 mb-1">{l}</label><input value={f[k]} onChange={e=>setF(p=>({...p,[k]:e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>)}
          <div><label className="block text-xs text-gray-500 mb-1">Type</label><select value={f.property_type} onChange={e=>setF(p=>({...p,property_type:e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none">
            {['Condo','Townhome','Detached','Semi-Detached','Ranch','Colonial','Custom Build','Penthouse','Villa'].map(t=><option key={t}>{t}</option>)}</select></div>
          <div><label className="block text-xs text-gray-500 mb-1">Price ($)</label><input type="number" value={f.price_usd||''} onChange={e=>setF(p=>({...p,price_usd:+e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
          <div><label className="block text-xs text-gray-500 mb-1">Area (sqft)</label><input type="number" value={f.total_area_sqft||''} onChange={e=>setF(p=>({...p,total_area_sqft:+e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
          <div><label className="block text-xs text-gray-500 mb-1">Beds</label><input type="number" value={f.bedrooms} onChange={e=>setF(p=>({...p,bedrooms:+e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
          <div><label className="block text-xs text-gray-500 mb-1">Baths</label><input type="number" value={f.bathrooms} onChange={e=>setF(p=>({...p,bathrooms:+e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
          <div><label className="block text-xs text-gray-500 mb-1">Country</label><select value={f.country} onChange={e=>setF(p=>({...p,country:e.target.value}))} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none"><option>USA</option><option>Canada</option></select></div>
        </div>
        <div className="mt-3"><label className="block text-xs text-gray-500 mb-1">Description</label><textarea value={f.description} onChange={e=>setF(p=>({...p,description:e.target.value}))} rows={2} className="w-full px-2.5 py-2 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500"/></div>
        <button onClick={submit} disabled={!f.name||!f.project_name} className="mt-3 px-6 py-2 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-40 transition">Save Property</button>
      </Card>}
      {loading?<Spinner/>:<div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">{props.map(p=>(
        <Card key={p.id} className="p-5">
          <div className="flex justify-between items-start mb-2"><div><div className="text-sm font-bold text-gray-900">{p.name}</div><div className="text-xs text-gray-400">{p.city}, {p.state}</div></div><StatusBadge status={p.status}/></div>
          <div className="text-lg font-bold text-blue-600 mb-2">${p.price_usd.toLocaleString()}</div>
          <div className="grid grid-cols-3 gap-2 text-xs text-gray-500 mb-2">
            <div>{p.bedrooms} bed</div><div>{p.bathrooms} bath</div><div>{p.total_area_sqft.toLocaleString()} sqft</div>
          </div>
          {p.mls_id&&<div className="text-[10px] text-gray-400 font-mono">MLS: {p.mls_id}</div>}
          <button onClick={()=>del(p.id)} className="mt-2 text-xs text-red-500 hover:text-red-700">Delete</button>
        </Card>
      ))}</div>}
    </div>
  );
}
