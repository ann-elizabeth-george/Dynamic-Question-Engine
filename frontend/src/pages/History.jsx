import { useState, useEffect } from 'react';
import { getAssessmentHistory } from '../services/assessment';
import Loader from '../components/Loader';
import './History.css';

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [expandedSessionId, setExpandedSessionId] = useState(null);

  useEffect(() => {
    async function loadHistory() {
      try {
        const res = await getAssessmentHistory();
        setHistory(res.data);
      } catch (err) {
        console.error('Failed to load history', err);
      } finally {
        setLoading(false);
      }
    }
    loadHistory();
  }, []);

  const toggleExpand = (id) => {
    setExpandedSessionId(expandedSessionId === id ? null : id);
  };

  if (loading) return <Loader />;

  return (
    <div className="history-wrapper">
      <div className="history-header">
        <h1 className="gradient-text">Assessment History</h1>
        <p className="history-subtitle">Review your past evaluation sessions and responses</p>
      </div>

      {history.length === 0 ? (
        <div className="empty-state glass-panel">
          <p>You have not started any assessments yet.</p>
        </div>
      ) : (
        <div className="history-list">
          {history.map((item) => {
            const { session, category_name, responses } = item;
            const formattedDate = new Date(session.start_time).toLocaleDateString(undefined, {
              year: 'numeric',
              month: 'long',
              day: 'numeric',
              hour: '2-digit',
              minute: '2-digit',
            });
            const isExpanded = expandedSessionId === session.id;

            return (
              <div key={session.id} className="history-card glass-panel" onClick={() => toggleExpand(session.id)}>
                <div className="history-card-header">
                  <div>
                    <h3>{category_name}</h3>
                    <span className="history-date">{formattedDate}</span>
                  </div>
                  <span className={`status-badge status-${session.status.toLowerCase()}`}>
                    {session.status}
                  </span>
                </div>

                <div className="history-progress">
                  <div className="history-progress-fill" style={{ width: `${session.progress_percentage}%` }}></div>
                </div>

                <div className="history-card-footer">
                  <span>Progress: {session.progress_percentage}%</span>
                  <span className="expand-indicator">{isExpanded ? '▲ Hide Details' : '▼ View Responses'}</span>
                </div>

                {isExpanded && (
                  <div className="history-responses animate-fade-in" onClick={(e) => e.stopPropagation()}>
                    <h4>Detailed Responses:</h4>
                    {responses.length === 0 ? (
                      <p className="no-responses">No answers recorded for this session.</p>
                    ) : (
                      <div className="responses-list">
                        {responses.map((resp) => (
                          <div key={resp.id} className="response-item">
                            <span className="response-question">Q: {resp.question_text}</span>
                            <span className="response-answer">A: {resp.answer_text}</span>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
