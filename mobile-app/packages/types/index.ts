export interface GrantSectionBundle {
    executive_summary?: string;
    need?: string;
    methods?: string;
    staffing?: string;
    budget?: string;
    evaluation?: string;
    attachments?: string;
}

export interface GrantProfile {
    study_type?: string;
    scope?: string;
    duration_months?: number;
    geography?: string;
}

export interface BudgetProfile {
    max_funds?: number;
    median_funds?: number;
    target_funds?: number;
    constraints?: string;
}

export interface StaffingProfile {
    field_workers?: number;
    notes?: string;
}

export interface FundabilityScore {
    total?: number;
    alignment?: number;
    readiness?: number;
    budget_fit?: number;
    timing?: number;
    narrative_fit?: number;
    warnings?: string[];
}

export interface GrantMessage {
    role: 'user' | 'assistant' | 'system';
    content: string;
    timestamp?: string;
}

export interface GrantDraft {
    messages: GrantMessage[];
    grant_profile: GrantProfile;
    budget_profile: BudgetProfile;
    staffing_profile: StaffingProfile;
    sections: GrantSectionBundle;
    fundability_score?: FundabilityScore;
    version_snapshots?: GrantSectionBundle[];
}
