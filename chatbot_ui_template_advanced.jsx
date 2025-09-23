import { useState, useEffect, useRef } from "react";
import { Send, Bot, User, Moon, Sun, ArrowUp } from "lucide-react";
import { motion } from "framer-motion";

export default function ChatbotUI() {
  const [messages, setMessages] = useState(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("chatMessages");
      return saved
        ? JSON.parse(saved)
        : [
            {
              id: 1,
              sender: "bot",
              text: "Hello! How can I help you today?",
              time: new Date().toLocaleTimeString(),
            },
          ];
    }
    return [];
  });

  const [input, setInput] = useState("");
  const [darkMode, setDarkMode] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      localStorage.setItem("chatMessages", JSON.stringify(messages));
    }
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  const scrollToTop = () => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTo({ top: 0, behavior: "smooth" });
    }
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessage = {
      id: messages.length + 1,
      sender: "user",
      text: input,
      time: new Date().toLocaleTimeString(),
    };

    setMessages([...messages, newMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch("https://tyageshparmar-hr-policy-backend.hf.space/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query: input }),
      });

      const data = await res.json();

      const botReply = {
        id: newMessage.id + 1,
        sender: "bot",
        text: data.answer || "I couldn't understand that.",
        time: new Date().toLocaleTimeString(),
      };

      setMessages((prev) => [...prev, botReply]);

      // Optional: Add source snippets below the answer
      data.sources?.forEach((src, i) => {
        setMessages((prev) => [
          ...prev,
          {
            id: botReply.id + i + 1,
            sender: "bot",
            text: `📄 [Page ${src.page}]: ${src.snippet}`,
            time: new Date().toLocaleTimeString(),
          },
        ]);
      });
    } catch (error) {
      console.error("Error fetching from backend:", error);
      setMessages((prev) => [
        ...prev,
        {
          id: newMessage.id + 1,
          sender: "bot",
          text: "⚠️ Something went wrong. Try again later.",
          time: new Date().toLocaleTimeString(),
        },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div
      className={`${
        darkMode ? "bg-gray-900 text-white" : "bg-white text-black"
      } flex flex-col h-screen w-full max-w-2xl mx-auto shadow-2xl rounded-2xl overflow-hidden relative`}
    >
      {/* Header */}
      <div
        className={`flex items-center justify-between p-4 ${
          darkMode
            ? "bg-gray-800"
            : "bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
        }`}
      >
        <div className="flex items-center gap-2 text-lg font-semibold">
          <Bot size={24} /> ChatBot Assistant
        </div>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="p-2 rounded-xl hover:bg-gray-700 transition"
        >
          {darkMode ? <Sun size={20} /> : <Moon size={20} />}
        </button>
      </div>

      {/* Chat Area */}
      <div
        ref={chatContainerRef}
        className={`flex-1 overflow-y-auto p-4 space-y-3 ${
          darkMode ? "bg-gray-900" : "bg-gray-50"
        }`}
      >
        {messages.map((msg) => (
          <motion.div
            key={msg.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.2 }}
            className={`flex items-end gap-2 max-w-[80%] ${
              msg.sender === "user" ? "ml-auto flex-row-reverse" : ""
            }`}
          >
            <div
              className={`p-3 rounded-2xl shadow text-sm ${
                msg.sender === "user"
                  ? "bg-indigo-500 text-white"
                  : darkMode
                  ? "bg-gray-800 border border-gray-700"
                  : "bg-white border border-gray-200"
              }`}
            >
              <div>{msg.text}</div>
              <div className="text-[10px] mt-1 opacity-70 text-right">
                {msg.time}
              </div>
            </div>
            {msg.sender === "user" ? (
              <User className="text-indigo-500" size={20} />
            ) : (
              <Bot
                className={`${darkMode ? "text-gray-400" : "text-gray-500"}`}
                size={20}
              />
            )}
          </motion.div>
        ))}

        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{
              repeat: Infinity,
              duration: 0.8,
              repeatType: "reverse",
            }}
            className="flex items-center gap-2 text-sm text-gray-400"
          >
            <Bot size={18} /> Typing...
          </motion.div>
        )}
        <div ref={chatEndRef} />
      </div>

      {/* Scroll to Top Button */}
      <button
        onClick={scrollToTop}
        className="absolute bottom-20 right-4 p-3 rounded-full shadow-lg bg-indigo-500 hover:bg-indigo-600 text-white transition"
      >
        <ArrowUp size={20} />
      </button>

      {/* Input Box */}
      <div
        className={`p-3 border-t flex items-center gap-2 ${
          darkMode
            ? "bg-gray-800 border-gray-700"
            : "bg-white border-gray-200"
        }`}
      >
        <input
          type="text"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className={`flex-1 px-4 py-2 rounded-xl border focus:outline-none focus:ring-2 ${
            darkMode
              ? "bg-gray-700 border-gray-600 focus:ring-purple-400"
              : "border-gray-300 focus:ring-indigo-400"
          }`}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
        />
        <button
          onClick={handleSend}
          className={`p-2 rounded-xl transition ${
            darkMode
              ? "bg-purple-500 hover:bg-purple-600"
              : "bg-indigo-500 hover:bg-indigo-600"
          } text-white`}
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}