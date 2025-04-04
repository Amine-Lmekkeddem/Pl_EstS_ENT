import React, { useState, useEffect } from "react";
import Layout from "../components/Layout";
import "../styles/ChatPage.css"; // S'assurer que ce fichier existe

function ChatPage() {
  const [role, setRole] = useState(null);

  useEffect(() => {
    const userRole = localStorage.getItem("role"); // Récupérer le rôle stocké
    setRole(userRole);
  }, []);

  return (
    <Layout>
      <div className="chat-content">
        <div className="main-content-titre">
          <h1>Page de Chat</h1>
          <p>
            Bienvenue sur la page de chat. Vous pouvez discuter avec notre
            équipe ici.
          </p>
        </div>

        {/* 🔹 Zone de chat */}
        <div className="chat-box">
          <p>Zone de discussion...</p>
        </div>
      </div>
    </Layout>
  );
}

export default ChatPage;
