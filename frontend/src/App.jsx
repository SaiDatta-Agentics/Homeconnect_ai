import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './AuthContext';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';
import CustomerLayout from './pages/customer/Layout';
import CustomerHome from './pages/customer/Home';
import CustomerChat from './pages/customer/Chat';
import CustomerVisits from './pages/customer/MyVisits';
import AdminLayout from './pages/admin/Layout';
import AdminDashboard from './pages/admin/Dashboard';
import AdminVisits from './pages/admin/Visits';
import AdminEnquiries from './pages/admin/Enquiries';
import AdminProperties from './pages/admin/Properties';
import AdminAnalytics from './pages/admin/Analytics';
import AdminActivity from './pages/admin/Activity';

function Protected({ children, roles }) {
  const { user, loading } = useAuth();
  if (loading) return <div className="min-h-screen flex items-center justify-center"><div className="w-6 h-6 border-2 border-gray-300 border-t-blue-600 rounded-full animate-spin"/></div>;
  if (!user) return <Navigate to="/login" />;
  if (roles && !roles.includes(user.role)) return <Navigate to="/" />;
  return children;
}

function RoleRedirect() {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (user.role === 'customer') return <Navigate to="/browse" />;
  return <Navigate to="/admin" />;
}

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/" element={<RoleRedirect />} />
        {/* Customer portal */}
        <Route path="/browse" element={<Protected roles={['customer']}><CustomerLayout /></Protected>}>
          <Route index element={<CustomerHome />} />
          <Route path="chat" element={<CustomerChat />} />
          <Route path="my-visits" element={<CustomerVisits />} />
        </Route>
        {/* Admin portal */}
        <Route path="/admin" element={<Protected roles={['admin','sales_manager','sales_agent']}><AdminLayout /></Protected>}>
          <Route index element={<AdminDashboard />} />
          <Route path="visits" element={<AdminVisits />} />
          <Route path="enquiries" element={<AdminEnquiries />} />
          <Route path="properties" element={<AdminProperties />} />
          <Route path="analytics" element={<AdminAnalytics />} />
          <Route path="activity" element={<AdminActivity />} />
        </Route>
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </AuthProvider>
  );
}
