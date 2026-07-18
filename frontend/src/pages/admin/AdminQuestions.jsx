import { useState } from 'react';
import { createQuestion } from '../../services/questions';
import './AdminQuestions.css';

export default function AdminQuestions() {
  const [code, setCode] = useState('');
  const [text, setText] = useState('');
  const [type, setType] = useState('SINGLE_CHOICE');
  const [answers, setAnswers] = useState([
    { answer_text: '', display_order: 1 },
    { answer_text: '', display_order: 2 },
  ]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleAnswerChange = (index, value) => {
    const updated = [...answers];
    updated[index].answer_text = value;
    setAnswers(updated);
  };

  const handleOrderChange = (index, value) => {
    const updated = [...answers];
    updated[index].display_order = parseInt(value) || 0;
    setAnswers(updated);
  };

  const addAnswerField = () => {
    setAnswers([...answers, { answer_text: '', display_order: answers.length + 1 }]);
  };

  const removeAnswerField = (index) => {
    if (answers.length <= 1) return;
    setAnswers(answers.filter((_, idx) => idx !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSubmitting(true);
    setError('');
    setSuccess('');

    // Filter empty options
    const filteredAnswers = answers.filter((a) => a.answer_text.trim() !== '');
    if (filteredAnswers.length === 0) {
      setError('Please add at least one answer option.');
      setSubmitting(false);
      return;
    }

    try {
      const res = await createQuestion({
        code,
        question_text: text,
        question_type: type,
        status: 'ACTIVE',
        answers: filteredAnswers,
      });

      setSuccess(`Question Created Successfully! Question ID is: ${res.data.id}`);
      setCode('');
      setText('');
      setAnswers([
        { answer_text: '', display_order: 1 },
        { answer_text: '', display_order: 2 },
      ]);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create question.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="admin-questions-wrapper animate-fade-in">
      <h2>Question Library</h2>

      {error && <div className="q-error">{error}</div>}
      {success && <div className="q-success">{success}</div>}

      <div className="admin-form glass-panel">
        <h3 className="form-title">Create New Question</h3>
        <form onSubmit={handleSubmit}>
          <div className="q-details-grid">
            <div className="input-group">
              <label className="input-label">Question Code (Unique)</label>
              <input
                type="text"
                className="input-field"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                required
                placeholder="e.g. Q001"
              />
            </div>

            <div className="input-group">
              <label className="input-label">Question Type</label>
              <select
                className="input-field select-field"
                value={type}
                onChange={(e) => setType(e.target.value)}
              >
                <option value="SINGLE_CHOICE">Single Choice (Radio)</option>
                <option value="MULTI_CHOICE">Multiple Choice (Checkbox)</option>
              </select>
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Question Text</label>
            <textarea
              className="input-field textarea-field"
              value={text}
              onChange={(e) => setText(e.target.value)}
              required
              rows="3"
              placeholder="Enter question text here..."
            />
          </div>

          <div className="answers-section">
            <h4>Predefined Answer Options</h4>
            {answers.map((ans, idx) => (
              <div key={idx} className="answer-row">
                <span className="row-index">#{idx + 1}</span>
                <input
                  type="text"
                  className="input-field"
                  value={ans.answer_text}
                  onChange={(e) => handleAnswerChange(idx, e.target.value)}
                  placeholder={`Option ${idx + 1} text`}
                  required
                />
                <input
                  type="number"
                  className="input-field order-input"
                  value={ans.display_order}
                  onChange={(e) => handleOrderChange(idx, e.target.value)}
                  placeholder="Order"
                  required
                />
                <button
                  type="button"
                  className="btn-remove"
                  onClick={() => removeAnswerField(idx)}
                  disabled={answers.length <= 1}
                >
                  ✕
                </button>
              </div>
            ))}

            <button type="button" className="btn btn-secondary btn-small" onClick={addAnswerField}>
              + Add Option
            </button>
          </div>

          <button type="submit" className={`btn submit-btn ${submitting ? 'btn-disabled' : ''}`} disabled={submitting}>
            {submitting ? 'Creating Question...' : 'Create Question'}
          </button>
        </form>
      </div>
    </div>
  );
}
