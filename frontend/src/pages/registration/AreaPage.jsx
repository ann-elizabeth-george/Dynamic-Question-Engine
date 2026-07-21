import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";


export default function AreaPage() {

  const navigate = useNavigate();


  const districtId = localStorage.getItem("districtId");
  const districtName = localStorage.getItem("districtName");


  const [areas, setAreas] = useState([]);
  const [area, setArea] = useState("");


  useEffect(() => {

    loadAreas();

  }, []);



  const loadAreas = async () => {

    try {

      const res = await axios.get(
        `http://127.0.0.1:8000/api/v1/areas/${districtId}`
      );


      setAreas(res.data);


    } catch (error) {

      console.error(error);

      alert("Failed to load areas");

    }

  };



  const handleNext = () => {


    if (!area) {

      alert("Please select your Area");

      return;

    }



    const selected = areas.find(
      (a) => a.id === Number(area)
    );



    if (!selected) {

      alert("Invalid area selected");

      return;

    }



    localStorage.setItem(
      "areaId",
      selected.id
    );


    localStorage.setItem(
      "areaCode",
      selected.code
    );


    localStorage.setItem(
      "areaName",
      selected.name
    );



    navigate("/register/age");

  };



  return (

    <div style={styles.container}>


      <div style={styles.card}>


        <h2>Basic Registration</h2>


        <p>Question 4 of 5</p>


        <h3>
          Select your Area / Post Office
        </h3>


        <h4>
          {districtName}
        </h4>



        <select

          style={styles.select}

          value={area}

          onChange={(e)=>setArea(e.target.value)}

        >


          <option value="">

            Select Area

          </option>



          {areas.map((a)=>(


            <option

              key={a.id}

              value={a.id}

            >

              {a.name}

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


  select:{

    width:"100%",

    padding:"12px",

    marginTop:"20px",

    fontSize:"16px"

  },


  button:{

    width:"100%",

    padding:"12px",

    marginTop:"25px",

    background:"#2563eb",

    color:"#fff",

    border:"none",

    borderRadius:"6px",

    cursor:"pointer"

  }


};