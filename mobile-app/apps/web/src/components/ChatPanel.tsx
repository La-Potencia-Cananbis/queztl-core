import type { Dispatch, SetStateAction } from 'react';
import type { GrantDraft } from '@types';

interface ChatPanelProps {
    draft: GrantDraft;
    input: string;
    setInput: Dispatch<SetStateAction<string>>;
    onSend: () => void;
    loading: boolean;
    error?: string | null;
}

export function ChatPanel({ draft, input, setInput, onSend, loading, error }: ChatPanelProps) {
    return (
        <section className="card">
            <div className="card-header">
                <h2>Chat</h2>
                {loading ? <span className="pill pill-quiet">Generating…</span> : null}
            </div>
            <div className="chat-window">
                {draft.messages.length === 0 && (
                    <div className="chat-message incoming">
                        AI: Describe your grant (scope, study type, funds, timeline). I’ll draft sections.
                    </div>
                )}
                {draft.messages.map((m, idx) => (
                    <div key={idx} className={`chat-message ${m.role === 'user' ? 'outgoing' : 'incoming'}`}>
                        <strong>{m.role === 'user' ? 'You' : 'AI'}:</strong> {m.content}
                    </div>
                ))}
            </div>
            <div className="chat-input">
                <input
                    value={input}
                    placeholder="Type a grant ask…"
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter' && !e.shiftKey) {
                            e.preventDefault();
                            onSend();
                        }
                    }}
                    disabled={loading}
                />
                <button type="button" onClick={onSend} disabled={loading || !input.trim()}>
                    Send
                </button>
            </div>
            {error ? <p className="error-text">{error}</p> : null}
        </section>
    );
}
