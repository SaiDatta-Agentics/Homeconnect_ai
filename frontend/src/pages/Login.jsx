import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../AuthContext';
export default function LoginPage() {
  const { user, login } = useAuth(); const nav = useNavigate();
  const [email, setEmail] = useState(''); const [pw, setPw] = useState(''); const [err, setErr] = useState(''); const [loading, setLoading] = useState(false);
  useEffect(() => { if (user) nav(user.role === 'customer' ? '/browse' : '/admin'); }, [user]);
  const submit = async () => { setErr(''); setLoading(true); try { const d = await login(email, pw); nav(d.user.role === 'customer' ? '/browse' : '/admin'); } catch { setErr('Invalid credentials'); } finally { setLoading(false); } };
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-gray-100 px-5">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-14 h-14 rounded-2xl bg-blue-600 inline-flex items-center justify-center mb-4">
            <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          </div>
          <h1 className="text-2xl font-bold text-gray-900">HomeConnect AI</h1>
          <p className="text-sm text-gray-500 mt-1">AI-Powered Real Estate Agent</p>
        </div>
        <div className="bg-white border border-gray-200 rounded-xl shadow-sm p-8">
          <div className="mb-4"><label className="block text-sm text-gray-600 mb-1">Email</label>
            <input type="email" value={email} onChange={e=>setEmail(e.target.value)} onKeyDown={e=>e.key==='Enter'&&submit()} placeholder="you@email.com" className="w-full px-3 py-2.5 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" /></div>
          <div className="mb-5"><label className="block text-sm text-gray-600 mb-1">Password</label>
            <input type="password" value={pw} onChange={e=>setPw(e.target.value)} onKeyDown={e=>e.key==='Enter'&&submit()} placeholder="••••••••" className="w-full px-3 py-2.5 text-sm rounded-lg border border-gray-300 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-100" /></div>
          {err && <div className="text-sm text-red-600 mb-3">{err}</div>}
          <button onClick={submit} disabled={loading} className="w-full py-2.5 text-sm font-semibold rounded-lg bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 transition">{loading ? 'Signing in…' : 'Sign in'}</button>
          <div className="text-center mt-4"><Link to="/register" className="text-sm text-blue-600 hover:underline">Don't have an account? Sign up</Link></div>
        </div>
        <div className="mt-5 text-center text-xs text-gray-400 space-y-1">
          <p>Customer: john@example.com / customer1</p>
          <p>Admin: admin@homeconnect.ai / admin123</p>
        </div>
      </div>
    </div>
  );
}
