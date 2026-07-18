import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createProfile } from '../services/auth';
import { useAuth } from '../context/AuthContext';
import './Profile.css';

export default function Profile() {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [phone, setPhone] = useState('');
  const [districtCode, setDistrictCode] = useState('');
  const [areaCode, setAreaCode] = useState('');
  const [categoryCode, setCategoryCode] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [regNumber, setRegNumber] = useState('');
  const { loadUser } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const res = await createProfile({
        first_name: firstName,
        last_name: lastName,
        phone,
        district_code: districtCode,
        area_code: areaCode,
        category_code: categoryCode,
      });
      setRegNumber(res.data.registration_number);
      await loadUser(); // Reload user state to fetch profile links
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to complete profile. Verify your codes.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="profile-wrapper">
      <div className="profile-card glass-panel animate-fade-in">
        <h2 className="gradient-text">Complete Your Profile</h2>
        <p className="profile-subtitle">
          Fill in details below to generate your unique, future-ready Registration Number.
        </p>

        {error && <div className="profile-error">{error}</div>}

        {!regNumber ? (
          <form onSubmit={handleSubmit}>
            <div className="profile-grid">
              <div className="input-group">
                <label className="input-label">First Name</label>
                <input
                  type="text"
                  className="input-field"
                  value={firstName}
                  onChange={(e) => setFirstName(e.target.value)}
                  required
                  placeholder="John"
                />
              </div>

              <div className="input-group">
                <label className="input-label">Last Name</label>
                <input
                  type="text"
                  className="input-field"
                  value={lastName}
                  onChange={(e) => setLastName(e.target.value)}
                  required
                  placeholder="Doe"
                />
              </div>
            </div>

            <div className="input-group">
              <label className="input-label">Phone Number</label>
              <input
                type="tel"
                className="input-field"
                value={phone}
                onChange={(e) => setPhone(e.target.value)}
                required
                placeholder="+1 (555) 000-0000"
              />
            </div>

            <div className="profile-grid-three">
              <div className="input-group">
                <label className="input-label">District Code</label>
                <input
                  type="text"
                  className="input-field"
                  value={districtCode}
                  onChange={(e) => setDistrictCode(e.target.value)}
                  required
                  maxLength="4"
                  placeholder="e.g. 04"
                />
              </div>

              <div className="input-group">
                <label className="input-label">Area Code</label>
                <input
                  type="text"
                  className="input-field"
                  value={areaCode}
                  onChange={(e) => setAreaCode(e.target.value)}
                  required
                  maxLength="4"
                  placeholder="e.g. 123"
                />
              </div>

              <div className="input-group">
                <label className="input-label">Category Code</label>
                <input
                  type="text"
                  className="input-field"
                  value={categoryCode}
                  onChange={(e) => setCategoryCode(e.target.value)}
                  required
                  maxLength="4"
                  placeholder="e.g. 02"
                />
              </div>
            </div>

            <button type="submit" className={`btn ${loading ? 'btn-disabled' : ''}`} disabled={loading}>
              {loading ? 'Generating...' : 'Complete & Generate'}
            </button>
          </form>
        ) : (
          <div className="profile-success animate-fade-in">
            <div className="success-icon">✓</div>
            <h3>Profile Completed!</h3>
            <p>Your unique registration number has been successfully generated:</p>
            <div className="reg-number">{regNumber}</div>
            <button className="btn" onClick={() => navigate('/')}>
              Go to Dashboard
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
