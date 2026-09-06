import { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, register as apiRegister, getMe } from './api';
const Ctx = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => { const s = localStorage.getItem('user'); return s ? JSON.parse(s) : null; });
  const [loading, setLoading] = useState(true);
  useEffect(() => { const t = localStorage.getItem('token'); if (t) getMe().then(r => { setUser(r.data); localStorage.setItem('user', JSON.stringify(r.data)); }).catch(() => { localStorage.clear(); setUser(null); }).finally(() => setLoading(false)); else setLoading(false); }, []);
  const login = async (email, password) => { const r = await apiLogin(email, password); localStorage.setItem('token', r.data.access_token); localStorage.setItem('user', JSON.stringify(r.data.user)); setUser(r.data.user); return r.data; };
  const signup = async (data) => { const r = await apiRegister(data); localStorage.setItem('token', r.data.access_token); localStorage.setItem('user', JSON.stringify(r.data.user)); setUser(r.data.user); return r.data; };
  const logout = () => { localStorage.clear(); setUser(null); };
  return <Ctx.Provider value={{ user, login, signup, logout, loading }}>{children}</Ctx.Provider>;
}
export const useAuth = () => useContext(Ctx);
