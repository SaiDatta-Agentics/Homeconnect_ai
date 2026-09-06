import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';
export default function RegisterPage() {
  const { signup } = useAuth(); const nav = useNavigate();
  const [f, setF] = useState({ full_name: '', email: '', phone: '', password: '' });
  const [err, setErr] = useState(''); const [loading, setLoading] = useState(false);
  const submit = async () => { setErr(''); setLoading(true); try { await signup(f); nav('/browse'); } catch(e) { setErr(e.response?.data?.detail || 'Registration failed'); } finally { setLoading(false); } };
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 px-5">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-blue-600 inline-flex items-center justify-center mb-4">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-sm text-gray-500 mt-1">Start your home search with HomeConnect AI</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8">
          {['full_name','email','phone','password'].map(k => (
            <div key={k} className="mb-4"><label className="block text-sm text-gray-600 mb-1 capitalize">{k.replace('_',' ')}</label>
              <input type={k==='password'?'password':k==='email'?'email':'text'} value={f[k]} onChange={e=>setF(p=>({...p,[k]:e.target.value}))}
                onKeyDown={e=>e.key==='Enter'&&submit()} className="w-full px-3 py-2.5 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" /></div>
          ))}
          {err && <div className="text-sm text-red-600 mb-3">{err}</div>}
          <button onClick={submit} disabled={loading || !f.full_name || !f.email || !f.password}
            className="w-full py-2.5 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition">{loading ? 'Creating…' : 'Create Account'}</button>
          <div className="text-center mt-4"><Link to="/login" className="text-sm text-blue-600 hover:underline">Already have an account? Sign in</Link></div>
        </div>
      </div>
    </div>
  );
}
