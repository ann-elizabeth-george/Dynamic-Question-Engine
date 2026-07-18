import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getCategories } from '../services/categories';
import { useAuth } from '../context/AuthContext';
import Loader from '../components/Loader';
import './Dashboard.css';

export default function Dashboard() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to profile if profile is missing
    if (user && !user.profile) {
      navigate('/profile');
      return;
    }

    async function loadCategories() {
      try {
        const res = await getCategories();
        setCategories(res.data);
      } catch (err) {
        setError('Failed to load categories.');
      } finally {
        setLoading(false);
      }
    }
    loadCategories();
  }, [user, navigate]);

  if (loading) return <Loader />;

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-header">
        <h1 className="gradient-text">Select Assessment</h1>
        <p className="dashboard-subtitle">Choose a category below to start your evaluation session</p>
      </div>

      {error && <div className="dashboard-error">{error}</div>}

      {categories.length === 0 ? (
        <div className="empty-state glass-panel">
          <p>No active categories available at the moment. Please contact the administrator.</p>
        </div>
      ) : (
        <div className="category-grid">
          {categories.map((cat) => (
            <div key={cat.id} className="category-card glass-panel">
              <h3>{cat.name}</h3>
              <p>{cat.description || 'No description provided.'}</p>
              <button
                className="btn"
                onClick={() => navigate(`/assessment?category=${cat.id}`)}
              >
                Start Assessment
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
