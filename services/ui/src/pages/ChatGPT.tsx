import React from "react";
import { ChatView } from "@/features/chat";

/**
 * ChatGPT page component
 * Acts as a simple container for the chat feature view
 */
const ChatGPT: React.FC = () => (
  <div className="h-full w-full">
    <ChatView />
  </div>
);

export default ChatGPT;