// import React, { useState } from "react";
// import api from "../services/api";
// import "../styles/RegisterForm.css";

// function RegisterForm() {
//   const [username, setUsername] = useState("");
//   const [password, setPassword] = useState("");
//   const [email, setEmail] = useState("");

//   const handleRegister = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await api.post("/auth/register", {
//         username,
//         email,
//         password,
//       });
//       alert("Inscription réussie !");
//     } catch (error) {
//       alert("Échec de l'inscription !");
//     }
//   };

//   return (
//     <form onSubmit={handleRegister}>
//       <input
//         type="text"
//         placeholder="Nom d'utilisateur"
//         value={username}
//         onChange={(e) => setUsername(e.target.value)}
//       />
//       <input
//         type="email"
//         placeholder="Email"
//         value={email}
//         onChange={(e) => setEmail(e.target.value)}
//       />
//       <input
//         type="password"
//         placeholder="Mot de passe"
//         value={password}
//         onChange={(e) => setPassword(e.target.value)}
//       />
//       <button type="submit">S'inscrire</button>
//     </form>
//   );
// }

// export default RegisterForm;

import React, { useState } from "react";
import api from "../services/api";
import "../styles/RegisterForm.css";

function RegisterForm() {
  const [nom, setNom] = useState("");
  const [prenom, setPrenom] = useState("");
  const [codeUniversitaire, setCodeUniversitaire] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await api.post("/auth/register", { nom, prenom, codeUniversitaire });
      alert("Inscription réussie !");
    } catch (error) {
      alert("Échec de l'inscription !");
    }
  };

  return (
    <form className="register-form" onSubmit={handleRegister}>
      <input
        type="text"
        placeholder="Nom"
        value={nom}
        onChange={(e) => setNom(e.target.value)}
      />
      <input
        type="text"
        placeholder="Prénom"
        value={prenom}
        onChange={(e) => setPrenom(e.target.value)}
      />
      <input
        type="text"
        placeholder="Code universitaire"
        value={codeUniversitaire}
        onChange={(e) => setCodeUniversitaire(e.target.value)}
      />
      <button type="submit">Valider</button>
    </form>
  );
}

export default RegisterForm;
