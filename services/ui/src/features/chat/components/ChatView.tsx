import React, { useState, useRef, useEffect } from "react";
import { ChevronRight, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

interface Message {
  role: "user" | "assistant";
  content: string;
}

const ChatView: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLTextAreaElement>(null);

  // Scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Focus input field when component mounts
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = { role: "user", content: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Simulate API call
      setTimeout(() => {
        // Add assistant message
        const assistantMessage: Message = {
          role: "assistant",
          content: `This is a simulated response to: "${input}". In a real implementation, this would come from the agent API.`,
        };
        setMessages((prev) => [...prev, assistantMessage]);
        setIsLoading(false);
      }, 1000);
    } catch (error) {
      console.error("Error sending message:", error);
      setIsLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="flex flex-col h-full w-full">
      {/* Chat header */}
      <div className="p-4 border-b border-border">
        <div className="w-full px-4 md:px-8 lg:px-12">
          <h1 className="text-xl font-bold text-primary">AI Foundation Chat</h1>
        </div>
      </div>
      
      {/* Chat messages container */}
      <div className="flex-1 overflow-y-auto">
        <div className="w-full px-4 md:px-8 lg:px-12 py-6 space-y-6">
          {messages.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center py-20">
              <h2 className="text-2xl font-bold text-gray-700 dark:text-gray-300 mb-2">
                AI Foundation Chat
              </h2>
              <p className="text-gray-500 dark:text-gray-400 max-w-md">
                Ask me anything, and I'll do my best to help you. This is a demo
                of the AI Foundation chat interface.
              </p>
            </div>
          ) : (
            messages.map((message, index) => (
              <div
                key={index}
                className={`flex ${
                  message.role === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <Card
                  className={`max-w-[80%] p-4 ${
                    message.role === "user"
                      ? "bg-primary text-primary-foreground"
                      : "bg-accent text-accent-foreground"
                  }`}
                >
                  {message.role === "user" ? (
                    <div className="flex items-start">
                      <div className="mr-2 whitespace-pre-wrap">{message.content}</div>
                    </div>
                  ) : (
                    <div className="flex items-start">
                      <div className="ml-2 whitespace-pre-wrap">{message.content}</div>
                    </div>
                  )}
                </Card>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <Card className="max-w-[80%] p-4 bg-gray-100 dark:bg-slate-800">
                <div className="flex items-center space-x-2">
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.2s" }}></div>
                  <div className="h-2 w-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0.4s" }}></div>
                </div>
              </Card>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input area - fixed at the bottom */}
      <div className="sticky bottom-0 w-full border-t border-border bg-card p-4">
        <div className="w-full px-4 md:px-8 lg:px-12">
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <div className="flex-1 relative">
              <textarea
                ref={inputRef}
                value={input}
                onChange={handleInputChange}
                onKeyDown={handleKeyDown}
                placeholder="Type a message..."
                className="w-full p-3 border border-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary bg-background resize-none min-h-[50px] max-h-[200px] overflow-y-auto"
                rows={1}
              />
            </div>
            <Button
              type="submit"
              disabled={!input.trim() || isLoading}
              className={`h-[50px] w-[50px] rounded-full flex items-center justify-center ${
                !input.trim() || isLoading
                  ? "bg-gray-300 dark:bg-gray-700"
                  : "bg-primary hover:bg-primary/80"
              }`}
            >
              <Send className="h-5 w-5" />
            </Button>
          </form>
          <p className="text-xs text-center text-gray-500 mt-2">
            AI Foundation Chat may produce inaccurate information about people, places, or facts.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatView;