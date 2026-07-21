import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

export default function DistrictPage() {
  const navigate = useNavigate();

  const [districts, setDistricts] = useState([]);
  const [district, setDistrict] = useState("");

  useEffect(() => {
    loadDistricts();
  }, []);

  const loadDistricts = async () => {
    try {
      const res = await axios.get(
        "http://127.0.0.1:8000/api/v1/districts"
      );

      setDistricts(res.data);

    } catch (error) {
      console.error(error);
      alert("Failed to load districts");
    }
  };


  const handleNext = () => {

    if (!district) {
      alert("Please select your district");
      return;
    }


    const selected = districts.find(
      (d) => d.id === Number(district)
    );


    if (!selected) {
      alert("Invalid district selected");
      return;
    }


    localStorage.setItem(
      "districtId",
      selected.id
    );

    localStorage.setItem(
      "districtCode",
      selected.code
    );

    localStorage.setItem(
      "districtName",
      selected.name
    );


    navigate("/register/area");
  };


  return (
    <div style={styles.container}>

      <div style={styles.card}>

        <h2>Basic Registration</h2>

        <p>Question 3 of 5</p>

        <h3>Select Your District</h3>


        <select
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
          style={styles.select}
        >

          <option value="">
            Select District
          </option>


          {districts.map((d) => (

            <option
              key={d.id}
              value={d.id}
            >
              {d.name}
            </option>

          ))}


        </select>


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
    background: "#f4f6f8",
  },


  card: {
    width: "450px",
    background: "#fff",
    padding: "40px",
    borderRadius: "12px",
    boxShadow: "0 5px 15px rgba(0,0,0,0.1)",
    textAlign: "center",
  },


  select: {
    width: "100%",
    padding: "12px",
    marginTop: "20px",
    marginBottom: "25px",
    fontSize: "16px",
    borderRadius: "6px",
  },


  button: {
    width: "100%",
    padding: "12px",
    background: "#2563eb",
    color: "#fff",
    border: "none",
    borderRadius: "8px",
    cursor: "pointer",
    fontSize: "16px",
  },

};