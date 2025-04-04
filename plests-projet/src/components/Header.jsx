import React, { useState, useEffect } from "react";
import { Link, useNavigate } from "react-router-dom";
import estLogo from "../assets/OIP.jpg"; // Assurez-vous d'ajouter une image
import "../styles/Header.css";

function Header() {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  // Simulation de l'utilisateur connecté dans localStorage
  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem("user"));
    if (userData) {
      setUser(userData);
    } else {
      // Utilisateur fictif pour simulation
      const simulatedUser = {
        firstName: "Jean",
        lastName: "Dupont",
        role: "étudiant", // Choisir entre 'admin', 'enseignant', 'étudiant'
        profileImage: "path/to/default-profile-image.jpg", // Image par défaut
      };
      localStorage.setItem("user", JSON.stringify(simulatedUser));
      setUser(simulatedUser);
    }
  }, []);

  // Déconnexion
  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null); // Réinitialiser l'état de l'utilisateur
    navigate("/login");
  };

  return (
    <header>
      <div className="left-header">
        <img src={estLogo} alt="EST Salé Logo" />
      </div>

      {user ? (
        // Header pour l'utilisateur connecté
        <div className="user-info">
          <img
            src={user.profileImage || "path/to/default-image.jpg"} // Image de profil (par défaut si non disponible)
            alt={user.firstName}
            className="profile-image"
          />
          <div className="user-details">
            <span className="user-name">
              {user.firstName} {user.lastName}
            </span>
            <span className="user-role">{user.role}</span>{" "}
            {/* Affiche le rôle de l'utilisateur */}
          </div>
          <div className="header-actions">
            <button className="notification-button">
              <i className="fas fa-bell"></i> {/* Icône de notification */}
            </button>
            <button className="logout-button" onClick={handleLogout}>
              <i className="fas fa-sign-out-alt"></i>{" "}
              {/* Icône de déconnexion */}
            </button>
          </div>
        </div>
      ) : (
        // Header pour l'utilisateur non connecté
        <div className="login-section">
          <span className="email">ests@um5.ac.ma</span>
          <Link to="/login">
            <button className="button">Se connecter</button>
          </Link>
        </div>
      )}
    </header>
  );
}

export default Header;
