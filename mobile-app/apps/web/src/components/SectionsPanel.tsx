import type { GrantSectionBundle } from '@types';

interface SectionsPanelProps {
    sections: GrantSectionBundle;
}

const sectionOrder: Array<keyof GrantSectionBundle> = [
    'executive_summary',
    'need',
    'methods',
    'staffing',
    'budget',
    'evaluation',
    'attachments',
];

const labelMap: Record<keyof GrantSectionBundle, string> = {
    executive_summary: 'Executive Summary',
    need: 'Need',
    methods: 'Methods',
    staffing: 'Staffing',
    budget: 'Budget',
    evaluation: 'Evaluation',
    attachments: 'Attachments',
};

export function SectionsPanel({ sections }: SectionsPanelProps) {
    return (
        <section className="card">
            <h2>Sections</h2>
            <div className="grid">
                {sectionOrder.map((key) => (
                    <div key={key} className="section-tile">
                        <p className="eyebrow">{labelMap[key]}</p>
                        <p className="muted">{sections[key] || '—'}</p>
                    </div>
                ))}
            </div>
        </section>
    );
}
