// import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// import HomePage from "./pages/HomePage";
// import LoginPage from "./pages/LoginPage";
// import AccueilPage from "./pages/AccueilPage";
// import "./App.css";
// function App() {
//   return (
//     <Router>
//       <Routes>
//         <Route path="/" element={<HomePage />} />
//         <Route path="/login" element={<LoginPage />} />
//         <Route path="*" element={<HomePage />} />
//         <Route path="/accueil" element={<AccueilPage />} />
//       </Routes>
//     </Router>
//   );
// }

// export default App;

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import AccueilPage from "./pages/AccueilPage";
import ChatPage from "./pages/ChatPage"; // Ajout de la page ChatPage
import SearchPage from "./pages/SearchPage"; // Ajout de la page SearchPage
import CoNavigationPage from "./pages/CoNavigationPage"; // Ajout de la page CoNavigationPage
import ThemeToggle from "./components/ThemeToggle"; // Import du bouton
import "./App.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/accueil" element={<AccueilPage />} />
        <Route path="/chat" element={<ChatPage />} />{" "}
        {/* Route pour la page ChatPage */}
        <Route path="/search" element={<SearchPage />} />{" "}
        {/* Route pour la page SearchPage */}
        <Route path="/co-navigation" element={<CoNavigationPage />} />{" "}
        {/* Route pour la page CoNavigationPage */}
        <Route path="*" element={<HomePage />} />
      </Routes>
      <ThemeToggle /> {/* Bouton ajouté en bas de page */}
    </Router>
  );
}

export default App;
