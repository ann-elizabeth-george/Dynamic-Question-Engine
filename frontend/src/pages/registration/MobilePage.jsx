import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function MobilePage() {

  const navigate = useNavigate();

  const [mobile, setMobile] = useState(
    localStorage.getItem("mobile") || ""
  );

  const handleNext = () => {

    if (!/^[0-9]{10}$/.test(mobile)) {
      alert("Please enter a valid 10 digit mobile number");
      return;
    }

    localStorage.setItem("mobile", mobile);

    navigate("/register/district");
  };

  return (
    <div style={styles.container}>
      <div style={styles.card}>

        <h2>Basic Registration</h2>

        <p>Question 2 of 5</p>

        <h3>Please enter your Mobile Number</h3>

        <input
          style={styles.input}
          type="tel"
          placeholder="Mobile Number"
          value={mobile}
          maxLength={10}
          onChange={(e) => setMobile(e.target.value)}
        />

        <button
          style={styles.button}
          onClick={handleNext}
        >
          Next
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
    width: "500px",
    background: "#fff",
    padding: "40px",
    borderRadius: "10px",
    boxShadow: "0 5px 15px rgba(0,0,0,.1)",
    textAlign: "center",
  },

  input: {
    width: "100%",
    padding: "12px",
    marginTop: "20px",
    borderRadius: "6px",
    border: "1px solid #ccc",
    fontSize: "16px",
    boxSizing: "border-box",
  },

  button: {
    width: "100%",
    padding: "12px",
    marginTop: "25px",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    fontSize: "16px",
  },
};