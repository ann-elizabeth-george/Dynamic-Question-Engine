import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Welcome() {
  const navigate = useNavigate();
  const [category, setCategory] = useState("");

  const handleContinue = () => {
    if (!category) {
      alert("Please select who you are.");
      return;
    }

    // Save selected category
    localStorage.setItem("category", category);

    // Start Basic Registration
    navigate("/register/name");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h1>Dynamic Assessment Platform</h1>

        <h2>Welcome</h2>

        <p>Question 1</p>

        <h3>Who are you?</h3>

        <div style={styles.option}>
          <input
            type="radio"
            value="student"
            checked={category === "student"}
            onChange={(e) => setCategory(e.target.value)}
          />
          <label>Student</label>
        </div>

        <div style={styles.option}>
          <input
            type="radio"
            value="teacher"
            checked={category === "teacher"}
            onChange={(e) => setCategory(e.target.value)}
          />
          <label>Teacher</label>
        </div>

        <div style={styles.option}>
          <input
            type="radio"
            value="farmer"
            checked={category === "farmer"}
            onChange={(e) => setCategory(e.target.value)}
          />
          <label>Farmer</label>
        </div>

<div style={styles.option}>
  <input
    type="radio"
    value="business"
    checked={category === "business"}
    onChange={(e) => setCategory(e.target.value)}
  />
  <label>Business</label>
</div>

<div style={styles.option}>
  <input
    type="radio"
    value="employee"
    checked={category === "employee"}
    onChange={(e) => setCategory(e.target.value)}
  />
  <label>Employee</label>
</div>

<div style={styles.option}>
  <input
    type="radio"
    value="homemaker"
    checked={category === "homemaker"}
    onChange={(e) => setCategory(e.target.value)}
  />
  <label>Homemaker</label>
</div>

<div style={styles.option}>
  <input
    type="radio"
    value="other"
    checked={category === "other"}
    onChange={(e) => setCategory(e.target.value)}
  />
  <label>Other</label>
</div>
        <button style={styles.button} onClick={handleContinue}>
          Continue
        </button>

        <hr style={{ margin: "25px 0" }} />

        <button
          style={styles.loginButton}
          onClick={() => navigate("/login")}
        >
          Already Registered? Login
        </button>

      </div>
    </div>
  );
}

const styles = {
  container: {
    height: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "center",
    background: "#f5f5f5",
  },

  card: {
    width: "450px",
    background: "#fff",
    padding: "40px",
    borderRadius: "12px",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
    textAlign: "center",
  },

  option: {
    display: "flex",
    alignItems: "center",
    gap: "10px",
    margin: "15px 0",
    fontSize: "18px",
  },

  button: {
    marginTop: "25px",
    width: "100%",
    padding: "12px",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
  },

  loginButton: {
    width: "100%",
    padding: "12px",
    background: "#16a34a",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
  },
};