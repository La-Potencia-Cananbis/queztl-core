import type { Dispatch, SetStateAction } from 'react';

interface PlaceholderChatProps {
    value: string;
    onChange: Dispatch<SetStateAction<string>>;
    onSend: () => void;
}

export function PlaceholderChat({ value, onChange, onSend }: PlaceholderChatProps) {
    return (
        <div className="chat-card">
            <div className="chat-window">
                <div className="chat-message incoming">AI: Describe your grant and I’ll draft structured sections.</div>
                {value ? <div className="chat-message outgoing">You: {value}</div> : null}
            </div>
            <div className="chat-input">
                <input
                    value={value}
                    placeholder="Type a grant ask…"
                    onChange={(e) => onChange(e.target.value)}
                />
                <button type="button" onClick={onSend}>
                    Send
                </button>
            </div>
        </div>
    );
}
