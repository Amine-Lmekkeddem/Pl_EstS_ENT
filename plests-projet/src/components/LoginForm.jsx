// import React, { useState } from "react";
// import { useNavigate } from "react-router-dom"; // Importer useNavigate pour la redirection
// import api from "../services/api";
// import "../styles/LoginForm.css";

// function LoginForm() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const navigate = useNavigate(); // Initialiser useNavigate

//   const handleLogin = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await api.post("/auth/login", { username, password });
//       localStorage.setItem("token", response.data.access_token);
//       alert("Connexion réussie !");

//       // Rediriger vers la page AccueilPage après une connexion réussie
//       navigate("/accueil"); // Redirection vers /accueil
//     } catch (error) {
//       alert("Échec de la connexion !");
//     }
//   };

//   return (
//     <form onSubmit={handleLogin}>
//       <input
//         type="text"
//         placeholder="Nom d'utilisateur"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//       />
//       <input
//         type="password"
//         placeholder="Mot de passe"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//       />
//       <button type="submit">Se connecter</button>
//     </form>
//   );
// }

// export default LoginForm;

import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import "../styles/LoginForm.css";

function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", response.data.access_token);
      alert("Connexion réussie !");
      navigate("/accueil");
    } catch (error) {
      alert("Échec de la connexion !");
    }
  };

  return (
    <form className="login-form" onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Email académique"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="password"
        placeholder="Mot de passe"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Se connecter</button>
      <a href="/forgot-password" className="forgot-password">
        Oublier votre mot de passe ?
      </a>
    </form>
  );
}

export default LoginForm;
