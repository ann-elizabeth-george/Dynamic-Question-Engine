import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser, loginUser, getMe } from '../services/auth';
import { useAuth } from '../context/AuthContext';
import './Register.css';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    setLoading(true);
    try {
      // Register
      await registerUser({ username, email, password });
      
      // Auto Login
      const loginRes = await loginUser(username, password);
      const token = loginRes.data.access_token;
      
      localStorage.setItem('access_token', token);
      const meRes = await getMe();
      login(token, meRes.data);
      
      navigate('/profile');
    } catch (err) {
      setError(err.response?.data?.detail || 'Registration failed. Try another username/email.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="register-card glass-panel animate-fade-in">
      <h2 className="gradient-text">Create Account</h2>
      <p className="register-subtitle">Join the Dynamic Assessment Platform</p>

      {error && <div className="register-error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="input-group">
          <label className="input-label">Username</label>
          <input
            type="text"
            className="input-field"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            placeholder="e.g. johndoe"
          />
        </div>

        <div className="input-group">
          <label className="input-label">Email Address</label>
          <input
            type="email"
            className="input-field"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            placeholder="johndoe@example.com"
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

        <div className="input-group">
          <label className="input-label">Confirm Password</label>
          <input
            type="password"
            className="input-field"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            required
            placeholder="••••••••"
          />
        </div>

        <button type="submit" className={`btn ${loading ? 'btn-disabled' : ''}`} disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
      </form>

      <div className="register-footer">
        Already have an account? <Link to="/login">Login here</Link>
      </div>
    </div>
  );
}
