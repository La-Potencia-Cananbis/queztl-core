import type { FundabilityScore } from '@types';

interface FundabilityPanelProps {
    score?: FundabilityScore;
}

export function FundabilityPanel({ score }: FundabilityPanelProps) {
    const rows = [
        { label: 'Alignment', value: score?.alignment },
        { label: 'Readiness', value: score?.readiness },
        { label: 'Budget Fit', value: score?.budget_fit },
        { label: 'Timing', value: score?.timing },
        { label: 'Narrative Fit', value: score?.narrative_fit },
    ];

    return (
        <section className="card">
            <div className="card-header">
                <h2>Fundability</h2>
                <span className="pill">{score?.total ?? 0}/100</span>
            </div>
            <div className="grid two-col">
                {rows.map((row) => (
                    <div key={row.label} className="score-row">
                        <span className="muted">{row.label}</span>
                        <strong>{row.value ?? '—'}</strong>
                    </div>
                ))}
            </div>
            {score?.warnings?.length ? (
                <div className="warning-box">
                    <p className="eyebrow">Warnings</p>
                    <ul>
                        {score.warnings.map((w, idx) => (
                            <li key={idx}>{w}</li>
                        ))}
                    </ul>
                </div>
            ) : null}
        </section>
    );
}
