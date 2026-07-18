import { useState, useEffect } from 'react';
import { getCategories, mapQuestionToCategory } from '../../services/categories';
import { getQuestionsByCategory } from '../../services/questions';
import Loader from '../../components/Loader';
import './AdminMappings.css';

export default function AdminMappings() {
  const [categories, setCategories] = useState([]);
  const [selectedCategoryId, setSelectedCategoryId] = useState('');
  const [questionId, setQuestionId] = useState('');
  const [displayOrder, setDisplayOrder] = useState('');
  
  const [mappedQuestions, setMappedQuestions] = useState([]);
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  useEffect(() => {
    async function loadData() {
      try {
        const catRes = await getCategories();
        setCategories(catRes.data);
        if (catRes.data.length > 0) {
          setSelectedCategoryId(catRes.data[0].id.toString());
        }
      } catch (err) {
        setError('Failed to load categories');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  // Reload mappings when category selection changes
  useEffect(() => {
    if (!selectedCategoryId) return;

    async function loadMappings() {
      try {
        const res = await getQuestionsByCategory(parseInt(selectedCategoryId));
        setMappedQuestions(res.data);
      } catch (err) {
        console.error('Failed to load category mappings');
      }
    }
    loadMappings();
  }, [selectedCategoryId]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');

    try {
      await mapQuestionToCategory({
        category_id: parseInt(selectedCategoryId),
        question_id: parseInt(questionId),
        display_order: parseInt(displayOrder),
      });

      setSuccess('Question mapped successfully!');
      setQuestionId('');
      setDisplayOrder('');
      
      // Reload mapped list
      const res = await getQuestionsByCategory(parseInt(selectedCategoryId));
      setMappedQuestions(res.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to map question. Verify Question ID exists.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;

  return (
    <div className="admin-mappings-wrapper animate-fade-in">
      <h2>Category-Question Mappings</h2>

      {error && <div className="mapping-error">{error}</div>}
      {success && <div className="mapping-success">{success}</div>}

      <div className="admin-form glass-panel">
        <h3 className="form-title">Assign Question to Category</h3>
        <form onSubmit={handleSubmit}>
          <div className="mapping-grid">
            <div className="input-group">
              <label className="input-label">Select Category</label>
              <select
                className="input-field select-field"
                value={selectedCategoryId}
                onChange={(e) => setSelectedCategoryId(e.target.value)}
                required
              >
                {categories.map((cat) => (
                  <option key={cat.id} value={cat.id}>
                    {cat.name}
                  </option>
                ))}
              </select>
            </div>

            <div className="input-group">
              <label className="input-label">Question ID (Numeric Reference)</label>
              <input
                type="number"
                className="input-field"
                value={questionId}
                onChange={(e) => setQuestionId(e.target.value)}
                required
                placeholder="e.g. 5"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Display Order</label>
              <input
                type="number"
                className="input-field"
                value={displayOrder}
                onChange={(e) => setDisplayOrder(e.target.value)}
                required
                placeholder="e.g. 1"
              />
            </div>
          </div>

          <button type="submit" className={`btn submit-btn ${submitting ? 'btn-disabled' : ''}`} disabled={submitting}>
            {submitting ? 'Mapping...' : 'Assign Question'}
          </button>
        </form>
      </div>

      <div className="admin-list glass-panel">
        <h3>Mapped Questions Preview</h3>
        {mappedQuestions.length === 0 ? (
          <p className="no-mappings">No questions mapped to this category yet.</p>
        ) : (
          <div className="mappings-timeline">
            {mappedQuestions.map((q, idx) => (
              <div key={q.id} className="mapping-item">
                <span className="mapping-order">#{idx + 1}</span>
                <div className="mapping-info">
                  <span className="mapping-code">Question ID: {q.id} | Code: {q.code}</span>
                  <p className="mapping-text">{q.question_text}</p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
