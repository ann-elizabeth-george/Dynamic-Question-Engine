import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { loginUser, getMe } from '../services/auth';
import './Login.css';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await loginUser(username, password);
      const token = res.data.access_token;
      
      // Load user profile details
      localStorage.setItem('access_token', token);
      const meRes = await getMe();
      login(token, meRes.data);
      
      navigate('/');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid username or password');
      localStorage.removeItem('access_token');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-card glass-panel animate-fade-in">
      <h2 className="gradient-text">Welcome Back</h2>
      <p className="login-subtitle">Sign in to your assessment account</p>

      {error && <div className="login-error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label className="input-label">Username or Email</label>
          <input
            type="text"
            className="input-field"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="Enter username or email"
          />
        </div>

        <div className="input-group">
          <label className="input-label">Password</label>
          <input
            type="password"
            className="input-field"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            placeholder="••••••••"
          />
        </div>

        <button type="submit" className={`btn ${loading ? 'btn-disabled' : ''}`} disabled={loading}>
          {loading ? 'Signing in...' : 'Sign In'}
        </button>
      </form>

      <div className="login-footer">
        Don't have an account? <Link to="/register">Register here</Link>
      </div>
    </div>
  );
}
