import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import './Navbar.css';

export default function Navbar() {
  const { user, logout, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  if (!isAuthenticated) return null;

  const isAdmin = user?.role?.name === 'Admin' || user?.role_id === 1;

  return (
    <nav className="navbar">
      <div className="navbar-inner">
        <Link to="/" className="navbar-brand">
          <span className="brand-icon">◆</span>
          <span className="brand-text">DAP</span>
        </Link>

        <div className="navbar-links">
          <Link to="/" className="nav-link">Dashboard</Link>
          {isAdmin && <Link to="/admin" className="nav-link">Admin Panel</Link>}
          <Link to="/history" className="nav-link">History</Link>
        </div>

        <div className="navbar-user">
          <span className="user-greeting">Hi, {user?.username}</span>
          <button className="btn-logout" onClick={handleLogout}>Logout</button>
        </div>
      </div>
    </nav>
  );
}
