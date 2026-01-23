import type { GrantDraft, GrantMessage, GrantSectionBundle, FundabilityScore } from '@types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';
const USE_MOCK = !API_BASE_URL;

const mockSection = (title: string, prompt: string) => `${title}: ${prompt.slice(0, 140)}…`;

const mockScore = (messages: GrantMessage[]): FundabilityScore => {
    const hasContent = messages.length > 0;
    return {
        total: hasContent ? 72 : 0,
        alignment: hasContent ? 4 : 0,
        readiness: hasContent ? 3 : 0,
        budget_fit: hasContent ? 3 : 0,
        timing: hasContent ? 3 : 0,
        narrative_fit: hasContent ? 4 : 0,
        warnings: hasContent ? [] : ['No content yet. Start with a brief description.'],
    };
};

const emptySections: GrantSectionBundle = {
    executive_summary: '',
    need: '',
    methods: '',
    staffing: '',
    budget: '',
    evaluation: '',
    attachments: '',
};

export const createEmptyDraft = (): GrantDraft => ({
    messages: [],
    grant_profile: {},
    budget_profile: {},
    staffing_profile: {},
    sections: { ...emptySections },
    fundability_score: mockScore([]),
    version_snapshots: [],
});

async function callApi<T>(path: string, body: unknown): Promise<T> {
    if (USE_MOCK) {
        return Promise.reject(new Error('API_BASE_URL not configured; using mock only.'));
    }

    const res = await fetch(`${API_BASE_URL}${path}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`API ${path} failed: ${res.status} ${res.statusText} — ${text}`);
    }

    return res.json();
}

export async function sendMessage(input: string, draft: GrantDraft): Promise<GrantDraft> {
    const userMessage: GrantMessage = {
        role: 'user',
        content: input,
        timestamp: new Date().toISOString(),
    };

    if (USE_MOCK) {
        const assistantMessage: GrantMessage = {
            role: 'assistant',
            content: 'Drafted sections and score (mock).',
            timestamp: new Date().toISOString(),
        };

        const messages: GrantMessage[] = [...draft.messages, userMessage, assistantMessage];

        const sections: GrantSectionBundle = {
            executive_summary: mockSection('Executive Summary', input),
            need: mockSection('Need', input),
            methods: mockSection('Methods', input),
            staffing: mockSection('Staffing', input),
            budget: mockSection('Budget', input),
            evaluation: mockSection('Evaluation', input),
            attachments: 'Checklist: LOI, budget, letters, data mgmt plan.',
        };

        return {
            ...draft,
            messages,
            sections,
            fundability_score: mockScore(messages),
            version_snapshots: [...(draft.version_snapshots || []), sections],
        };
    }

    const updated: GrantDraft = await callApi('/core/update_section', {
        message: input,
        draft,
    });

    return updated;
}

export async function scoreDraft(draft: GrantDraft): Promise<FundabilityScore> {
    if (USE_MOCK) {
        return mockScore(draft.messages);
    }
    return callApi('/core/score', { draft });
}

export async function exportDocx(draft: GrantDraft): Promise<Blob> {
    if (USE_MOCK) {
        const content = `Grant Draft (mock)\n\n${draft.sections.executive_summary || ''}`;
        return new Blob([content], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' });
    }

    const res = await fetch(`${API_BASE_URL}/core/export_docx`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ draft }),
    });

    if (!res.ok) {
        const text = await res.text();
        throw new Error(`Export failed: ${res.status} ${res.statusText} — ${text}`);
    }

    const blob = await res.blob();
    return blob;
}
