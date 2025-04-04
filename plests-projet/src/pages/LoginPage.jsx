// import React, { useState } from "react";
// import { Link } from "react-router-dom";
// import LoginForm from "../components/LoginForm";
// import RegisterForm from "../components/RegisterForm";
// import "../styles/LoginPage.css";

// function LoginPage() {
//   const [isLogin, setIsLogin] = useState(true);

//   return (
//     <div className="login-container">
//       <h2>{isLogin ? "Connexion" : "Inscription"}</h2>

//       {isLogin ? <LoginForm /> : <RegisterForm />}

//       {/* Bouton pour basculer entre Login et Register */}
//       <button className="toggle-button" onClick={() => setIsLogin(!isLogin)}>
//         {isLogin ? "Créer un compte" : "Déjà un compte ? Se connecter"}
//       </button>

//       <p>
//         <Link to="/">Retour à l'accueil</Link>
//       </p>
//     </div>
//   );
// }

// export default LoginPage;

// import React, { useState } from "react";
// import { Link } from "react-router-dom";
// import LoginForm from "../components/LoginForm";
// import RegisterForm from "../components/RegisterForm";
// import "../styles/LoginPage.css";
// import estLogo from "../assets/OIP.jpg";

// function LoginPage() {
//   const [activeTab, setActiveTab] = useState("login");

//   return (
//     <div className="login-infer-container">
//       <div className="login-container">
//         <div className="logo">
//           <img src={estLogo} alt="EST Salé Logo" />
//         </div>

//         {/* Onglets */}
//         <div className="tabs">
//           <button
//             className={activeTab === "login" ? "tab active" : "tab"}
//             onClick={() => setActiveTab("login")}
//           >
//             Connexion
//           </button>
//           <button
//             className={activeTab === "register" ? "tab active" : "tab"}
//             onClick={() => setActiveTab("register")}
//           >
//             Inscription
//           </button>
//           <button
//             className={activeTab === "help" ? "tab active" : "tab"}
//             onClick={() => setActiveTab("help")}
//           >
//             Besoin d’aide ?
//           </button>
//         </div>

//         {/* Contenu des onglets */}
//         <div className="tab-content">
//           {activeTab === "login" && <LoginForm />}
//           {activeTab === "register" && <RegisterForm />}
//           {activeTab === "help" && (
//             <p className="help-text">
//               Si vous avez besoin d’aide, contactez l’administration.
//             </p>
//           )}
//         </div>

//         <p>
//           <Link to="/">Retour à l'accueil</Link>
//         </p>
//       </div>
//     </div>
//   );
// }

// export default LoginPage;

import React, { useState } from "react";
import { Link } from "react-router-dom";
import LoginForm from "../components/LoginForm";
import RegisterForm from "../components/RegisterForm";
import "../styles/LoginPage.css";
import estLogo from "../assets/OIP.jpg";

function LoginPage() {
  const [activeTab, setActiveTab] = useState("login");

  return (
    <div className="login-infer-container">
      <div className="login-container">
        <div className="logo">
          <img src={estLogo} alt="EST Salé Logo" />
        </div>

        {/* Onglets */}
        <div className="tabs">
          <button
            className={activeTab === "login" ? "tab active" : "tab"}
            onClick={() => setActiveTab("login")}
          >
            Connexion
          </button>
          <button
            className={activeTab === "register" ? "tab active" : "tab"}
            onClick={() => setActiveTab("register")}
          >
            Nouveau à l'université
            <span className="tooltip">Validez votre compte ?</span>
          </button>

          <button
            className={activeTab === "help" ? "tab active" : "tab"}
            onClick={() => setActiveTab("help")}
          >
            Besoin d’aide ?
          </button>
        </div>

        {/* Contenu des onglets */}
        <div className="tab-content">
          {activeTab === "login" && <LoginForm />}
          {activeTab === "register" && <RegisterForm />}
          {activeTab === "help" && (
            <p className="help-text">
              Si vous avez besoin d’aide, contactez l’administration.
            </p>
          )}
        </div>

        <p>
          <Link to="/">Retour à l'accueil</Link>
        </p>
      </div>
    </div>
  );
}

export default LoginPage;
