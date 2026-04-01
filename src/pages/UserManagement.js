import React, { useEffect, useState } from "react";
import "../styles/user.css";

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");
  const [showForm, setShowForm] = useState(false);

  const [newUser, setNewUser] = useState({
    name: "",
    email: "",
    role: "",
  });

  useEffect(() => {
    const storedUsers = JSON.parse(localStorage.getItem("users")) || [];
    setUsers(storedUsers);
  }, []);

  const handleAddUser = () => {
    if (!newUser.name || !newUser.email || !newUser.role) {
      alert("Fill all fields");
      return;
    }

    const user = {
      ...newUser,
      status: "Active",
      lastLogin: new Date().toLocaleString(),
    };

    const updatedUsers = [...users, user];
    setUsers(updatedUsers);
    localStorage.setItem("users", JSON.stringify(updatedUsers));

    setNewUser({ name: "", email: "", role: "" });
    setShowForm(false);
  };

  const filteredUsers = users.filter(
    (u) =>
      u.name.toLowerCase().includes(search.toLowerCase()) ||
      u.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="user-page">

      <div className="user-header">
        <div>
          <h2>User Management</h2>
          <p>Manage system users and permissions</p>
        </div>

        <button className="add-btn" onClick={() => setShowForm(true)}>
          + Add User
        </button>
      </div>

      {/* SEARCH */}
      <input
        className="search-box"
        type="text"
        placeholder="Search users by name or email..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />

      {/* FORM */}
      {showForm && (
        <div className="form-card">
          <input
            placeholder="Name"
            value={newUser.name}
            onChange={(e) =>
              setNewUser({ ...newUser, name: e.target.value })
            }
          />
          <input
            placeholder="Email"
            value={newUser.email}
            onChange={(e) =>
              setNewUser({ ...newUser, email: e.target.value })
            }
          />
          <select
            value={newUser.role}
            onChange={(e) =>
              setNewUser({ ...newUser, role: e.target.value })
            }
          >
            <option value="">Select Role</option>
            <option>Admin</option>
            <option>Operator</option>
            <option>Analyst</option>
          </select>

          <button onClick={handleAddUser}>Save</button>
        </div>
      )}

      {/* TABLE CARD */}
      <div className="table-card">

        <div className="table-header">
          <span>Name</span>
          <span>Email</span>
          <span>Role</span>
          <span>Status</span>
          <span>Last Login</span>
        </div>

        {filteredUsers.length === 0 ? (
          <p className="no-users">No users found</p>
        ) : (
          filteredUsers.map((user, i) => (
            <div key={i} className="table-row">
              <span>{user.name}</span>
              <span>{user.email}</span>

              <span className={`badge role ${user.role.toLowerCase()}`}>
                {user.role}
              </span>

              <span className="badge status">{user.status}</span>

              <span>{user.lastLogin}</span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default UserManagement;