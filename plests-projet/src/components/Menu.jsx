import React from "react";
import { Link } from "react-router-dom";
import "../styles/Menu.css";
import ChatButton from "./ChatButton";

const Menu = ({ role }) => {
  return (
    <nav className="menu">
      <Link to="/accueil">Accueil</Link>
      <Link to="/scolarite">Scolarité</Link>
      <Link to="/examens">Examens</Link>
      <Link to="/outils-pedagogiques">Outils Pédagogiques</Link>
      <Link to="/outils-collaboratifs">Outils Collaboratifs</Link>
      <Link to="/assistance">Assistance</Link>

      {role === "etudiant" && (
        <>
          <Link to="/scolarite">Scolarité</Link>
          <Link to="/examens">Examens</Link>
          <Link to="/outils-pedagogiques">Outils Pédagogiques</Link>
          <Link to="/outils-collaboratifs">Outils Collaboratifs</Link>
          <Link to="/assistance">Assistance</Link>
        </>
      )}

      {role === "enseignant" && (
        <>
          <Link to="/cours">Mes Cours</Link>
          <Link to="/examens">Examens</Link>
          <Link to="/corrections">Corrections</Link>
          <Link to="/assistance">Assistance</Link>
        </>
      )}

      {role === "admin" && (
        <>
          <Link to="/gestion-etudiants">Gestion des Étudiants</Link>
          <Link to="/gestion-enseignants">Gestion des Enseignants</Link>
          <Link to="/gestion-cours">Gestion des Cours</Link>
        </>
      )}
      {/* Affichage du bouton de chat flottant */}
      <ChatButton />
    </nav>
  );
};

export default Menu;
