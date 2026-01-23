import { useState } from 'react';
import { ChatPanel } from '../components/ChatPanel';
import { SectionsPanel } from '../components/SectionsPanel';
import { FundabilityPanel } from '../components/FundabilityPanel';
import { ExportPanel } from '../components/ExportPanel';
import { createEmptyDraft, sendMessage, scoreDraft } from '../api/coreGateway';
import type { GrantDraft } from '@types';

export default function App() {
    const [draft, setDraft] = useState<GrantDraft>(createEmptyDraft());
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleSend = async () => {
        if (!input.trim()) return;
        setLoading(true);
        setError(null);
        try {
            const updated = await sendMessage(input.trim(), draft);
            setDraft(updated);
            setInput('');
        } catch (e) {
            setError((e as Error).message);
        } finally {
            setLoading(false);
        }
    };

    const refreshScore = async () => {
        setLoading(true);
        setError(null);
        try {
            const newScore = await scoreDraft(draft);
            setDraft({ ...draft, fundability_score: newScore });
        } catch (e) {
            setError((e as Error).message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app-shell">
            <header className="app-header">
                <div>
                    <p className="eyebrow">Quetzal Core</p>
                    <h1>Grant Chat Assistant</h1>
                    <p className="subtitle">Chat-first PWA for team grant drafting (web + mobile).</p>
                </div>
                <div className="pill">MVP shell</div>
            </header>

            <main className="app-main">
                <ChatPanel
                    draft={draft}
                    input={input}
                    setInput={setInput}
                    onSend={handleSend}
                    loading={loading}
                    error={error}
                />
                <SectionsPanel sections={draft.sections} />
                <FundabilityPanel score={draft.fundability_score} />
                <div className="grid two-col">
                    <ExportPanel draft={draft} />
                    <section className="card">
                        <div className="card-header">
                            <h2>Actions</h2>
                        </div>
                        <button type="button" onClick={refreshScore} disabled={loading}>
                            Refresh score
                        </button>
                        <p className="muted">Re-evaluate fundability after edits.</p>
                        {error ? <p className="error-text">{error}</p> : null}
                    </section>
                </div>
            </main>
        </div>
    );
}
