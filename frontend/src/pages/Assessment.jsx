import { useState, useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { startAssessment, getCurrentQuestion, submitAnswer } from '../services/assessment';
import Loader from '../components/Loader';
import './Assessment.css';

export default function Assessment() {
  const [searchParams] = useSearchParams();
  const categoryId = searchParams.get('category');
  const navigate = useNavigate();

  const [session, setSession] = useState(null);
  const [question, setQuestion] = useState(null);
  const [selectedAnswerId, setSelectedAnswerId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!categoryId) {
      navigate('/');
      return;
    }

    async function initSession() {
      try {
        const startRes = await startAssessment(parseInt(categoryId));
        const activeSession = startRes.data;
        setSession(activeSession);

        const qRes = await getCurrentQuestion(activeSession.id);
        setQuestion(qRes.data);
      } catch (err) {
        setError(err.response?.data?.detail || 'Failed to initialize session. Make sure questions are mapped.');
      } finally {
        setLoading(false);
      }
    }

    initSession();
  }, [categoryId, navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedAnswerId || submitting) return;

    setSubmitting(true);
    setError('');

    try {
      const res = await submitAnswer({
        session_id: session.id,
        question_id: question.id,
        answer_id: selectedAnswerId,
      });

      if (res.data.is_completed) {
        navigate(`/completion?session_id=${session.id}`);
      } else {
        // Load next question from return directly
        setQuestion(res.data.next_question);
        setSelectedAnswerId(null);
        setSession((prev) => ({
          ...prev,
          current_question_index: prev.current_question_index + 1,
          progress_percentage: res.data.progress_percentage,
        }));
      }
    } catch (err) {
      setError('Failed to submit answer. Try again.');
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader />;

  if (error) {
    return (
      <div className="assessment-error-wrapper animate-fade-in">
        <div className="glass-panel text-center">
          <h3 className="text-danger">Evaluation Error</h3>
          <p>{error}</p>
          <button className="btn mt-4" onClick={() => navigate('/')}>
            Back to Dashboard
          </button>
        </div>
      </div>
    );
  }

  const currentProgress = session?.progress_percentage || 0;

  return (
    <div className="assessment-wrapper animate-fade-in">
      <div className="progress-container">
        <div className="progress-bar-container">
          <div className="progress-bar-fill" style={{ width: `${currentProgress}%` }}></div>
        </div>
        <div className="progress-labels">
          <span>Question {session?.current_question_index + 1}</span>
          <span>{currentProgress}% Progress</span>
        </div>
      </div>

      {question && (
        <div className="glass-panel question-card">
          <div className="question-badge">QUESTION {question.code}</div>
          <h2 className="question-text">{question.question_text}</h2>

          <form onSubmit={handleSubmit}>
            <div className="options-list">
              {question.answers.map((opt) => (
                <div
                  key={opt.id}
                  className={`option-card ${selectedAnswerId === opt.id ? 'selected' : ''}`}
                  onClick={() => setSelectedAnswerId(opt.id)}
                >
                  <div className="option-indicator"></div>
                  <span className="option-text">{opt.answer_text}</span>
                </div>
              ))}
            </div>

            <button
              type="submit"
              className={`btn ${!selectedAnswerId || submitting ? 'btn-disabled' : ''}`}
              disabled={!selectedAnswerId || submitting}
            >
              {submitting ? 'Submitting...' : 'Submit & Next'}
            </button>
          </form>
        </div>
      )}
    </div>
  );
}
