import { Link } from 'react-router-dom';
import './AdminDashboard.css';

export default function AdminDashboard() {
  return (
    <div className="admin-dashboard-wrapper">
      <div className="admin-header">
        <h1 className="gradient-text">Admin Control Panel</h1>
        <p className="admin-subtitle">Configure, seed and manage the core assessment data structures</p>
      </div>

      <div className="admin-grid">
        <Link to="/admin/categories" className="admin-card glass-panel animate-fade-in">
          <div className="admin-card-icon">📋</div>
          <h3>Manage Categories</h3>
          <p>Create evaluation categories like Students, Farmers, Teachers or Businesses.</p>
        </Link>

        <Link to="/admin/questions" className="admin-card glass-panel animate-fade-in">
          <div className="admin-card-icon">❓</div>
          <h3>Question Library</h3>
          <p>Create assessment questions with multiple order-based choice options.</p>
        </Link>

        <Link to="/admin/mappings" className="admin-card glass-panel animate-fade-in">
          <div className="admin-card-icon">🔗</div>
          <h3>Category Mappings</h3>
          <p>Map questions to categories and configure display orders.</p>
        </Link>
      </div>
    </div>
  );
}
