import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import "../styles/auth.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await API.post("login/", {
        username,
        password,
      });
      localStorage.setItem("token", res.data.access);
      navigate("/profile");
    } catch (error) {
      alert("Invalid username or password");
    }
  };

  return (
  <div className="auth-container">
    <div className="auth-card">
      {/* Heading */}
      <h1 className="auth-title">Maritime Vessel Tracking</h1>

      <form onSubmit={handleLogin}>
        <input
          type="text"
          placeholder="Email"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />

        <button type="submit">Login</button>
      </form>

      {/* Forgot password */}
      <p className="forgot-link">Forgot Password?</p>

      {/* Register link */}
      <p className="auth-link" onClick={() => navigate("/register")}>
        New user? Register
      </p>
    </div>
  </div>
);

}

export default Login;
