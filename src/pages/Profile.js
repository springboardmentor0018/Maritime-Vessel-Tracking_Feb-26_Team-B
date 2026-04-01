import React from "react";
import { useLocation } from "react-router-dom";
import "../styles/profile.css";

import profileImage from "../assets/images/profile.png";
import profileIcon from "../assets/images/profile_icon.jpg";

function Profile() {
  const location = useLocation();
  const data = location.state || {};

  return (
    <div className="container">

      <div className="left">
        <img src={profileImage} alt="profile" />
      </div>

      <div className="right">
        <h2>Profile</h2>

        <div className="profile-header">
          <img src={profileIcon} alt="icon" className="avatar-img" />
          <h3>{data.name || "User"}</h3>
        </div>

        <p><strong>Email:</strong> {data.email || "Not Provided"}</p>
        <p><strong>Phone:</strong> {data.mobile || "Not Provided"}</p>
        <p><strong>Role:</strong> {data.role || "User"}</p>

      </div>
    </div>
  );
}

export default Profile;