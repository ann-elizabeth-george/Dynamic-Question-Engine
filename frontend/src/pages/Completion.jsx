import { useNavigate } from 'react-router-dom';
import './Completion.css';

export default function Completion() {
  const navigate = useNavigate();

  return (
    <div className="completion-wrapper">
      <div className="completion-card glass-panel animate-fade-in">
        <div className="completion-icon">✓</div>
        <h1 className="gradient-text">Assessment Completed!</h1>
        <p className="completion-subtitle">
          Great job! Your responses have been processed and recorded successfully.
        </p>

        <div className="completion-actions">
          <button className="btn" onClick={() => navigate('/history')}>
            View History
          </button>
          <button className="btn btn-secondary" onClick={() => navigate('/')}>
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}
