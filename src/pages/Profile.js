import { useNavigate } from "react-router-dom";
import "../styles/auth.css";

function Profile() {
  const navigate = useNavigate();

  // Temporary static data (for Milestone-1 UI)
  const name = "Ramya";
  const role = "Operator";

  return (
    <div className="auth-container">
      <div className="auth-card">
        <h2>Profile</h2>

        {/* Avatar */}
        <div className="profile-avatar"></div>

        {/* Name */}
        <h3>{name}</h3>

        {/* Role */}
        <p>Role: {role}</p>

        <button
          onClick={() => {
            localStorage.removeItem("token");
            navigate("/");
          }}
        >
          Logout
        </button>
      </div>
    </div>
  );
}

export default Profile;
