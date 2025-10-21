import React, { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";
import { Send, Bot, User, Loader2 } from "lucide-react";
import "./App.css";

interface Message {
  id: string;
  type: "user" | "bot";
  content: string;
  timestamp: Date;
}

const App = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: "user",
      content: input.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      // Use environment variable for API URL
      // For Render: VITE_API_URL should be set in render.yaml
      // For local dev with docker-compose: use relative path (nginx proxy)
      const apiUrl = import.meta.env.VITE_API_URL || "";
      const endpoint = apiUrl ? `${apiUrl}/api/ask` : "/api/ask";

      console.log("API Endpoint:", endpoint); // Debug log

      const response = await fetch(endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: userMessage.content }),
      });

      if (!response.ok) {
        throw new Error("Failed to get response");
      }

      const data = await response.json();

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content: data.answer || "Sorry, couldn't get a response.",
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: "bot",
        content:
          "An error occurred while getting the response. Please check the server connection.",
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app">
      <div className="chat-header">
        <div className="header-content">
          <Bot className="header-icon" />
          <h1>Scientific Search</h1>
          <span className="header-subtitle">Powered by Gemini AI</span>
        </div>
      </div>

      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <Bot className="welcome-icon" />
              <h2>Welcome!</h2>
              <p>
                Ask any scientific question and I'll help you find an answer.
              </p>
              <div className="examples">
                <div className="example-category">
                  <span>Example questions:</span>
                  <div className="example-tags">
                    <span className="example-tag">
                      What is machine learning?
                    </span>
                    <span className="example-tag">Explain quantum physics</span>
                    <span className="example-tag">How does DNA work?</span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id} className={`message ${message.type}`}>
              <div className="message-icon">
                {message.type === "user" ? <User /> : <Bot />}
              </div>
              <div className="message-content">
                {message.type === "user" ? (
                  <p>{message.content}</p>
                ) : (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    rehypePlugins={[rehypeHighlight]}
                    components={{
                      code: ({
                        className,
                        children,
                        ...props
                      }: React.ComponentPropsWithoutRef<"code">) => {
                        const match = /language-(\w+)/.exec(className || "");
                        const isInline = !match;
                        return isInline ? (
                          <code className="inline-code" {...props}>
                            {children}
                          </code>
                        ) : (
                          <pre className={className}>
                            <code {...props}>{children}</code>
                          </pre>
                        );
                      },
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                )}
                <div className="message-time">
                  {message.timestamp.toLocaleTimeString("en-US", {
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="message bot loading">
              <div className="message-icon">
                <Bot />
              </div>
              <div className="message-content">
                <div className="loading-content">
                  <Loader2 className="spinner" />
                  <span>Generating response...</span>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter your question..."
            className="input"
            rows={1}
            disabled={isLoading}
          />
          <button
            onClick={sendMessage}
            disabled={!input.trim() || isLoading}
            className="send-button"
          >
            <Send />
          </button>
        </div>
      </div>
    </div>
  );
};

export default App;
