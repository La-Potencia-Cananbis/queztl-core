import { downloadBlob } from '../lib/download';
import { exportDocx } from '../api/coreGateway';
import type { GrantDraft } from '@types';
import { useState } from 'react';

interface ExportPanelProps {
    draft: GrantDraft;
}

export function ExportPanel({ draft }: ExportPanelProps) {
    const [exporting, setExporting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const handleExport = async () => {
        try {
            setExporting(true);
            setError(null);
            const blob = await exportDocx(draft);
            downloadBlob(blob, 'grant-draft.docx');
        } catch (e) {
            setError((e as Error).message);
        } finally {
            setExporting(false);
        }
    };

    return (
        <section className="card">
            <div className="card-header">
                <h2>Export</h2>
            </div>
            <p className="muted">Download the latest draft as DOCX.</p>
            <button type="button" onClick={handleExport} disabled={exporting}>
                {exporting ? 'Exporting…' : 'Export DOCX'}
            </button>
            {error ? <p className="error-text">{error}</p> : null}
        </section>
    );
}
