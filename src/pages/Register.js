import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/register.css";
import registerImage from "../assets/images/register.png";

function Register() {
  const navigate = useNavigate();

  const [form, setForm] = useState({
    name: "",
    email: "",
    mobile: "",
    password: "",
    confirmPassword: "",
    role: ""
  });

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm({
      ...form,
      [name]: value
    });
  };

  const handleSubmit = () => {

    if (!form.name || !form.email || !form.mobile || !form.password || !form.confirmPassword || !form.role) {
      alert("Please fill all fields");
      return;
    }

    if (form.password.length < 6) {
      alert("Password must be at least 6 characters");
      return;
    }

    if (form.password !== form.confirmPassword) {
      alert("Passwords do not match");
      return;
    }

    console.log("Register Data:", form);

    navigate("/profile", { state: form });
  };

  return (
    <div className="container">
      <div className="left">
        <img src={registerImage} alt="register" />
      </div>

      <div className="right">
        <h2>Register</h2>

        <input name="name" placeholder="Name" onChange={handleChange} />
        <input name="email" placeholder="Email Address" onChange={handleChange} />
        <input name="mobile" placeholder="Mobile Number" onChange={handleChange} />

        <input
          type="password"
          name="password"
          placeholder="Password"
          onChange={handleChange}
        />

        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          onChange={handleChange}
        />

        <select name="role" onChange={handleChange}>
          <option value="">Select Role</option>
          <option>User</option>
          <option>Admin</option>
        </select>

        <button onClick={handleSubmit}>Next</button>
      </div>
    </div>
  );
}

export default Register;