import { useState, useEffect } from 'react';
import { getCategories, createCategory } from '../../services/categories';
import Loader from '../../components/Loader';
import './AdminCategories.css';

export default function AdminCategories() {
  const [categories, setCategories] = useState([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  async function loadCategories() {
    try {
      const res = await getCategories();
      setCategories(res.data);
    } catch (err) {
      setError('Failed to load categories');
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadCategories();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');

    try {
      await createCategory({ name, description, is_active: isActive });
      setName('');
      setDescription('');
      setIsActive(true);
      await loadCategories();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create category');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="admin-categories-wrapper animate-fade-in">
      <h2>Manage Categories</h2>
      
      {error && <div className="category-error">{error}</div>}

      <div className="admin-form glass-panel">
        <h3 className="form-title">Create New Category</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-row">
            <div className="input-group">
              <label className="input-label">Category Name</label>
              <input
                type="text"
                className="input-field"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="e.g. Student"
              />
            </div>
            
            <div className="input-group flex-2">
              <label className="input-label">Description</label>
              <input
                type="text"
                className="input-field"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Description of target group"
              />
            </div>
          </div>

          <div className="form-bottom-row">
            <label className="checkbox-container">
              <input
                type="checkbox"
                checked={isActive}
                onChange={(e) => setIsActive(e.target.checked)}
              />
              <span className="checkbox-label">Active / Available</span>
            </label>

            <button type="submit" className={`btn ${submitting ? 'btn-disabled' : ''}`} disabled={submitting}>
              {submitting ? 'Adding...' : 'Add Category'}
            </button>
          </div>
        </form>
      </div>

      <div className="admin-list glass-panel">
        <h3>Existing Categories</h3>
        <table className="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Description</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {categories.map((cat) => (
              <tr key={cat.id}>
                <td>{cat.id}</td>
                <td><strong>{cat.name}</strong></td>
                <td>{cat.description || '-'}</td>
                <td>
                  <span className={`status-badge status-${cat.is_active ? 'completed' : 'abandoned'}`}>
                    {cat.is_active ? 'Active' : 'Inactive'}
                  </span>
                </td>
              </tr>
            ))}
            {categories.length === 0 && (
              <tr>
                <td colSpan="4" className="text-center">No categories created yet.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
