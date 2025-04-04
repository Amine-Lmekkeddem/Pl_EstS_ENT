import React, { useState } from "react";
import ChatWindow from "./ChatWindow";
import "../styles/ChatButton.css";

function ChatButton() {
  const [isChatOpen, setIsChatOpen] = useState(false);

  return (
    <>
      <button
        className="chat-button"
        onClick={() => setIsChatOpen(!isChatOpen)}
      >
        💬
      </button>
      {isChatOpen && <ChatWindow onClose={() => setIsChatOpen(false)} />}
    </>
  );
}

export default ChatButton;
