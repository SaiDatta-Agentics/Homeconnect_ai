import { Outlet, NavLink } from 'react-router-dom';
import { useAuth } from '../../AuthContext';
const NAV = [
  { to: '/browse', label: 'Properties', end: true },
  { to: '/browse/chat', label: 'AI Assistant' },
  { to: '/browse/my-visits', label: 'My Tours' },
];
export default function CustomerLayout() {
  const { user, logout } = useAuth();
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 sticky top-0 z-30">
        <div className="max-w-6xl mx-auto px-5 h-14 flex items-center justify-between">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>
              </div>
              <span className="font-bold text-gray-900">HomeConnect</span>
            </div>
            <nav className="flex gap-1">{NAV.map(n => (
              <NavLink key={n.to} to={n.to} end={n.end} className={({isActive}) => `px-3 py-1.5 rounded-lg text-sm font-medium transition ${isActive ? 'bg-blue-50 text-blue-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'}`}>{n.label}</NavLink>
            ))}</nav>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-sm text-gray-600">Hi, {user?.full_name?.split(' ')[0]}</span>
            <button onClick={logout} className="text-sm text-gray-500 hover:text-gray-700 px-3 py-1 border border-gray-200 rounded-lg">Sign out</button>
          </div>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-5 py-6"><Outlet /></main>
    </div>
  );
}
