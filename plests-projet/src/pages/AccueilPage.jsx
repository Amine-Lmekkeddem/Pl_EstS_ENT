import React, { useState, useEffect } from "react";
import Layout from "../components/Layout";
import Card from "../components/Card";
import "../styles/AccueilPage.css";

const AccueilPage = () => {
  const [role, setRole] = useState(null);

  useEffect(() => {
    const userRole = localStorage.getItem("role"); // Récupérer le rôle stocké
    setRole(userRole);
  }, []);

  return (
    <Layout>
      <div className="main-content-titre">
        <h1>Bienvenue sur votre page d'accueil</h1>
        <p>Sélectionnez un rôle ci-dessous pour accéder à vos options.</p>
      </div>

      {/* 🔹 Section Cartes */}
      <div className="main-content-carte">
        {role === "etudiant" && (
          <>
            <Card title="Mes Cours" description="Voici vos cours en ligne." />
            <Card
              title="Mes Examens"
              description="Consultez vos examens à venir."
            />
          </>
        )}
        {role === "enseignant" && (
          <>
            <Card
              title="Mes Cours à Enseigner"
              description="Voici vos cours à enseigner."
            />
            <Card
              title="Mes Examens"
              description="Consultez les examens à préparer."
            />
          </>
        )}
        {role === "admin" && (
          <>
            <Card
              title="Gestion des Étudiants"
              description="Gérez les informations des étudiants."
            />
            <Card
              title="Gestion des Enseignants"
              description="Gérez les informations des enseignants."
            />
          </>
        )}
        {!role && (
          <>
            <Card
              title="Bienvenue"
              description="Veuillez vous connecter pour voir le contenu."
            />
            <Card
              title="Gestion des Étudiants"
              description="Gérez les informations des étudiants."
            />
            <Card
              title="Gestion des Enseignants"
              description="Gérez les informations des enseignants."
            />
          </>
        )}
      </div>
    </Layout>
  );
};

export default AccueilPage;
