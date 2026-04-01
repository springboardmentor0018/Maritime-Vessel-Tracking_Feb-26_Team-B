import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/login.css";

function Login({ setIsLoggedIn }) {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("");

  const handleLogin = () => {
    if (!email || !password || !role) {
      alert("Please fill all fields");
      return;
    }

    // ✅ ONLY THIS LINE IS IMPORTANT
    setIsLoggedIn(true);

    navigate("/dashboard");
  };

  return (
    <div className="login-container">

      <div className="login-card">

        <div className="login-header">
          <div className="icon">🚢</div>
          <h2>Maritime Risk Intelligence</h2>
          <p>Access real-time vessel tracking and risk analysis</p>
        </div>

        <div className="login-form">

          <label>Email</label>
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <label>Password</label>
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <label>Select Role</label>
          <select
            value={role}
            onChange={(e) => setRole(e.target.value)}
          >
            <option value="">Choose your role</option>
            <option>Admin</option>
            <option>Operator</option>
            <option>Analyst</option>
          </select>

          <button onClick={handleLogin}>Login</button>

        </div>
      </div>

    </div>
  );
}

export default Login;