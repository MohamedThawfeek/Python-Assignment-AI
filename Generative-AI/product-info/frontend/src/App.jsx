import { useEffect, useRef, useState } from "react";
import { normalizeResponse } from "./utils/response.js";

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
).replace(/\/$/, "");

function SendIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="m5 12 7-7 7 7M12 5v14" />
    </svg>
  );
}

function SparkIcon() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 3.5 13.7 8a3.7 3.7 0 0 0 2.3 2.3l4.5 1.7-4.5 1.7a3.7 3.7 0 0 0-2.3 2.3L12 20.5 10.3 16A3.7 3.7 0 0 0 8 13.7L3.5 12 8 10.3A3.7 3.7 0 0 0 10.3 8L12 3.5Z" />
    </svg>
  );
}

function ProductCard({ product }) {
  if (!product || typeof product !== "object") {
    return <p className="product-raw">{String(product)}</p>;
  }

  return (
    <article className="product-card">
      <div className="product-card__topline">
        <span>{product.category || "Product"}</span>
        {product.rating != null && <span>★ {product.rating}</span>}
      </div>
      <h3>{product.name || "Recommended product"}</h3>
      {product.brand && <p className="product-brand">by {product.brand}</p>}
      {product.description && <p>{product.description}</p>}
      {Array.isArray(product.features) && product.features.length > 0 && (
        <div className="feature-list">
          {product.features.slice(0, 4).map((feature) => (
            <span key={feature}>{feature}</span>
          ))}
        </div>
      )}
      <div className="product-card__footer">
        <div>
          {product.model_number && <span>{product.model_number}</span>}
          {product.warranty && <span>{product.warranty} warranty</span>}
        </div>
        {product.price != null && (
          <strong>
            {new Intl.NumberFormat("en-US", {
              style: "currency",
              currency: "USD",
            }).format(Number(product.price))}
          </strong>
        )}
      </div>
    </article>
  );
}

function Message({ item }) {
  const isUser = item.role === "user";
  const hasProducts =
    !isUser && Array.isArray(item.data) && item.data.length > 0;

  return (
    <div className={`message-row ${isUser ? "message-row--user" : ""}`}>
      {!isUser && (
        <div className="assistant-avatar" aria-hidden="true">
          <SparkIcon />
        </div>
      )}
      <div
        className={`message ${
          isUser
            ? "message--user"
            : `message--assistant ${hasProducts ? "" : "message--text-answer"}`
        }`}
      >
        {!isUser && !hasProducts && <span className="answer-label">ANSWER</span>}
        <p>{item.text}</p>
        {hasProducts && (
          <section className="results" aria-label="Products returned by the assistant">
            <div className="results__header">
              <span>PRODUCTS</span>
              <strong>{item.data.length} found</strong>
            </div>
            <div className="product-grid">
              {item.data.map((product, index) => (
                <ProductCard
                  key={product?.model_number || product?.name || index}
                  product={product}
                />
              ))}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

function TypingIndicator() {
  return (
    <div className="message-row" role="status" aria-label="Assistant is thinking">
      <div className="assistant-avatar" aria-hidden="true">
        <SparkIcon />
      </div>
      <div className="typing-indicator">
        <span />
        <span />
        <span />
      </div>
    </div>
  );
}

export default function App() {
  const [prompt, setPrompt] = useState("");
  const [messages, setMessages] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  const resizeTextarea = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 152)}px`;
  };

  const sendMessage = async () => {
    const text = prompt.trim();
    if (!text || isLoading) return;

    setMessages((current) => [...current, { role: "user", text }]);
    setPrompt("");
    setIsLoading(true);
    requestAnimationFrame(resizeTextarea);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/ask-ollama`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: text }),
      });

      let payload;
      try {
        payload = await response.json();
      } catch {
        payload = null;
      }

      if (!response.ok) {
        throw new Error(
          payload?.detail || `The server returned an error (${response.status}).`,
        );
      }

      const normalizedResponse = normalizeResponse(payload);

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          text: normalizedResponse.message,
          data: normalizedResponse.products,
          status: normalizedResponse.status,
        },
      ]);
    } catch (error) {
      const isNetworkError = error instanceof TypeError;
      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          status: "failed",
          text: isNetworkError
            ? "I couldn't reach the server. Make sure the API is running on port 8000 and try again."
            : error.message || "Something went wrong. Please try again.",
          data: [],
        },
      ]);
    } finally {
      setIsLoading(false);
      textareaRef.current?.focus();
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    sendMessage();
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-shell">
      <header className="app-header">
        <a className="brand" href="/" aria-label="Product Assistant home">
          <span className="brand-mark">
            <SparkIcon />
          </span>
          <span>Product Assistant</span>
        </a>
        <div className="status-pill">
          <span /> Ready to help
        </div>
      </header>

      <main className={`chat ${messages.length === 0 ? "chat--empty" : ""}`}>
        {messages.length === 0 ? (
          <section className="empty-state">
            <div className="empty-state__icon">
              <SparkIcon />
            </div>
            <p className="eyebrow">AI PRODUCT GUIDE</p>
            <h1>What can I help you find?</h1>
            <p className="empty-state__copy">
              Ask about products, features, prices, or recommendations.
            </p>
          </section>
        ) : (
          <section className="messages" aria-live="polite">
            {messages.map((item, index) => (
              <Message key={`${item.role}-${index}`} item={item} />
            ))}
            {isLoading && <TypingIndicator />}
            <div ref={messagesEndRef} />
          </section>
        )}
      </main>

      <div className="composer-wrap">
        <form className="composer" onSubmit={handleSubmit}>
          <label className="sr-only" htmlFor="prompt">
            Ask about a product
          </label>
          <textarea
            ref={textareaRef}
            id="prompt"
            name="prompt"
            rows="1"
            value={prompt}
            onChange={(event) => {
              setPrompt(event.target.value);
              resizeTextarea();
            }}
            onKeyDown={handleKeyDown}
            placeholder="Ask about a product..."
            disabled={isLoading}
          />
          <button
            className="send-button"
            type="submit"
            disabled={!prompt.trim() || isLoading}
            aria-label="Send message"
          >
            <SendIcon />
          </button>
        </form>
        <p className="composer-hint">Press Enter to send · Shift + Enter for a new line</p>
      </div>
    </div>
  );
}
