import { useEffect, useRef, useState } from 'react'
import { ArrowUp, Bot, ChevronDown, LoaderCircle } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api/v1'
).replace(/\/$/, '')

const MODEL_OPTIONS = [
  { value: 'gpt', label: 'GPT', endpoint: 'ask-gpt' },
  { value: 'gemini', label: 'Gemini', endpoint: 'ask-gemini' },
  { value: 'ollama', label: 'Ollama', endpoint: 'ask-ollama' },
]

function getModel(model) {
  return MODEL_OPTIONS.find((option) => option.value === model) ?? MODEL_OPTIONS[0]
}

function rehypeLineBreaks() {
  return (tree) => {
    function replaceBreaks(node) {
      if (!Array.isArray(node.children)) return

      node.children = node.children.map((child) => {
        if (
          child.type === 'raw' &&
          /^<br\s*\/?\s*>$/i.test(child.value.trim())
        ) {
          return {
            type: 'element',
            tagName: 'br',
            properties: {},
            children: [],
          }
        }

        replaceBreaks(child)
        return child
      })
    }

    replaceBreaks(tree)
  }
}

function getReply(data) {
  if (typeof data === 'string') return data

  const reply =
    data?.response ??
    data?.answer ??
    data?.message ??
    data?.content ??
    data?.data

  if (typeof reply === 'string') return reply
  if (reply != null) return JSON.stringify(reply, null, 2)

  return 'The API returned an empty response.'
}

function AssistantMessage({ content, model, pending }) {
  return (
    <article className="message-row assistant-row">
      <div className="assistant-avatar" aria-hidden="true">
        <Bot size={17} strokeWidth={2.1} />
      </div>
      <div className="assistant-content">
        <p className="message-label">Financial AI · {getModel(model).label}</p>
        {pending ? (
          <div className="thinking" role="status" aria-label="Generating response">
            <span />
            <span />
            <span />
          </div>
        ) : (
          <div className="markdown">
            <ReactMarkdown
              remarkPlugins={[remarkGfm]}
              rehypePlugins={[rehypeLineBreaks]}
            >
              {content}
            </ReactMarkdown>
          </div>
        )}
      </div>
    </article>
  )
}

function UserMessage({ content }) {
  return (
    <article className="message-row user-row">
      <div className="user-bubble">{content}</div>
    </article>
  )
}

function App() {
  const [prompt, setPrompt] = useState('')
  const [messages, setMessages] = useState([])
  const [selectedModel, setSelectedModel] = useState('gpt')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading, error])

  function resizeTextarea() {
    const textarea = textareaRef.current
    if (!textarea) return

    textarea.style.height = 'auto'
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`
  }

  async function handleSubmit(event) {
    event?.preventDefault()

    const cleanPrompt = prompt.trim()
    if (!cleanPrompt || isLoading) return

    const requestModel = getModel(selectedModel)

    setMessages((current) => [
      ...current,
      { id: crypto.randomUUID(), role: 'user', content: cleanPrompt },
    ])
    setPrompt('')
    setError('')
    setIsLoading(true)

    if (textareaRef.current) textareaRef.current.style.height = 'auto'

    try {
      const response = await fetch(`${API_BASE_URL}/${requestModel.endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: cleanPrompt }),
      })

      const contentType = response.headers.get('content-type') ?? ''
      const data = contentType.includes('application/json')
        ? await response.json()
        : await response.text()

      if (!response.ok) {
        throw new Error(
          data?.detail ?? data?.message ?? `Request failed (${response.status})`,
        )
      }

      setMessages((current) => [
        ...current,
        {
          id: crypto.randomUUID(),
          role: 'assistant',
          content: getReply(data),
          model: requestModel.value,
        },
      ])
    } catch (requestError) {
      const message =
        requestError instanceof TypeError
          ? 'Could not reach the API. Make sure FastAPI is running on port 8000.'
          : requestError.message
      setError(message)
    } finally {
      setIsLoading(false)
      textareaRef.current?.focus()
    }
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault()
      handleSubmit()
    }
  }

  const isEmpty = messages.length === 0 && !isLoading

  return (
    <main className="app-shell">
      <section
        className={`conversation ${isEmpty ? 'conversation-empty' : ''}`}
        aria-live="polite"
      >
        {messages.map((message) =>
          message.role === 'user' ? (
            <UserMessage key={message.id} content={message.content} />
          ) : (
            <AssistantMessage
              key={message.id}
              content={message.content}
              model={message.model}
            />
          ),
        )}

        {isLoading && (
          <AssistantMessage pending content="" model={selectedModel} />
        )}

        {error && (
          <div className="error-message" role="alert">
            {error}
          </div>
        )}
        <div ref={bottomRef} />
      </section>

      <div className="composer-wrap">
        <form className="composer" onSubmit={handleSubmit}>
          <label className="sr-only" htmlFor="prompt">
            Ask Financial AI
          </label>
          <textarea
            ref={textareaRef}
            id="prompt"
            rows="1"
            value={prompt}
            onChange={(event) => {
              setPrompt(event.target.value)
              requestAnimationFrame(resizeTextarea)
            }}
            onKeyDown={handleKeyDown}
            placeholder="Ask Financial AI"
          />
          <div className="composer-footer">
            <label className="model-select-wrap">
              <span className="sr-only">Choose AI model</span>
              <select
                value={selectedModel}
                onChange={(event) => setSelectedModel(event.target.value)}
                disabled={isLoading}
                aria-label="Choose AI model"
              >
                {MODEL_OPTIONS.map((model) => (
                  <option key={model.value} value={model.value}>
                    {model.label}
                  </option>
                ))}
              </select>
              <ChevronDown size={15} aria-hidden="true" />
            </label>
            <button
              type="submit"
              className="send-button"
              disabled={!prompt.trim() || isLoading}
              aria-label={isLoading ? 'Sending message' : 'Send message'}
            >
              {isLoading ? (
                <LoaderCircle size={20} className="spin" />
              ) : (
                <ArrowUp size={21} strokeWidth={2.5} />
              )}
            </button>
          </div>
        </form>
      </div>
    </main>
  )
}

export default App
