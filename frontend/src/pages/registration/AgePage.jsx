import { useState } from "react";
import { useNavigate } from "react-router-dom";


export default function AgePage() {

  const navigate = useNavigate();


  const [age, setAge] = useState(
    localStorage.getItem("age") || ""
  );


  const handleNext = () => {


    if (!age) {

      alert("Please enter your age");
      return;

    }


    const ageNumber = Number(age);


    if (ageNumber < 5 || ageNumber > 100) {

      alert("Please enter a valid age");
      return;

    }


    localStorage.setItem(
      "age",
      ageNumber
    );


    // Temporary next step
    navigate("/register/complete");

  };



  return (

    <div style={styles.container}>


      <div style={styles.card}>


        <h2>Basic Registration</h2>


        <p>Question 5 of 5</p>


        <h3>
          Enter Your Age
        </h3>



        <input

          type="number"

          placeholder="Age"

          value={age}

          onChange={(e)=>setAge(e.target.value)}

          style={styles.input}

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


  container:{
    height:"100vh",
    display:"flex",
    justifyContent:"center",
    alignItems:"center",
    background:"#f5f5f5"
  },


  card:{
    width:"500px",
    background:"#fff",
    padding:"40px",
    borderRadius:"10px",
    boxShadow:"0 5px 15px rgba(0,0,0,.1)",
    textAlign:"center"
  },


  input:{
    width:"100%",
    padding:"12px",
    marginTop:"20px",
    fontSize:"16px",
    boxSizing:"border-box"
  },


  button:{
    width:"100%",
    padding:"12px",
    marginTop:"25px",
    background:"#2563eb",
    color:"#fff",
    border:"none",
    borderRadius:"6px",
    cursor:"pointer",
    fontSize:"16px"
  }

};