'use client';

import { useState, useEffect } from 'react';
import { Brain, Skull, AlertTriangle, TrendingUp, Zap, Clock, Shield, Swords } from 'lucide-react';

interface CreativeScenario {
    name: string;
    description: string;
    mode: string;
    parameters: Record<string, any>;
    objectives: string[];
    created_at: string;
}

export default function CreativeTraining() {
    const [modes, setModes] = useState<any>(null);
    const [currentScenario, setCurrentScenario] = useState<CreativeScenario | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        fetchModes();
    }, []);

    const fetchModes = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/training/creative/modes');
            const data = await response.json();
            setModes(data);
        } catch (error) {
            console.error('Failed to fetch modes:', error);
        }
    };

    const startCreativeTraining = async (mode?: string) => {
        setIsLoading(true);
        try {
            const url = mode
                ? `http://localhost:8000/api/training/creative?mode=${mode}`
                : 'http://localhost:8000/api/training/creative';

            const response = await fetch(url, { method: 'POST' });
            const data = await response.json();
            setCurrentScenario(data);
        } catch (error) {
            console.error('Failed to start training:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const getModeIcon = (mode: string) => {
        const icons: Record<string, any> = {
            chaos_monkey: Skull,
            resource_starving: AlertTriangle,
            cascade_failure: TrendingUp,
            traffic_spike: Zap,
            adaptive_adversary: Brain,
            time_pressure: Clock,
            multi_attack: Swords,
            data_corruption: Shield,
        };
        return icons[mode] || Brain;
    };

    const getModeColor = (mode: string) => {
        const colors: Record<string, string> = {
            chaos_monkey: 'from-purple-500 to-pink-500',
            resource_starving: 'from-yellow-500 to-orange-500',
            cascade_failure: 'from-red-500 to-pink-500',
            traffic_spike: 'from-blue-500 to-cyan-500',
            adaptive_adversary: 'from-green-500 to-teal-500',
            time_pressure: 'from-orange-500 to-red-500',
            multi_attack: 'from-indigo-500 to-purple-500',
            data_corruption: 'from-gray-500 to-slate-500',
        };
        return colors[mode] || 'from-gray-500 to-gray-700';
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                    <Brain className="w-6 h-6 text-purple-500" />
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                        Creative Training
                    </h2>
                </div>
                <button
                    onClick={() => startCreativeTraining()}
                    disabled={isLoading}
                    className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-lg hover:from-purple-600 hover:to-pink-600 disabled:opacity-50"
                >
                    {isLoading ? 'Generating...' : 'Random Scenario'}
                </button>
            </div>

            {/* Training Modes Grid */}
            {modes && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                    {modes.modes.map((mode: string) => {
                        const Icon = getModeIcon(mode);
                        const colorClass = getModeColor(mode);

                        return (
                            <button
                                key={mode}
                                onClick={() => startCreativeTraining(mode)}
                                disabled={isLoading}
                                className={`relative overflow-hidden rounded-lg p-4 text-white bg-gradient-to-br ${colorClass} hover:scale-105 transition-transform disabled:opacity-50`}
                            >
                                <Icon className="w-8 h-8 mb-2 opacity-90" />
                                <p className="text-sm font-medium">
                                    {mode.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                                </p>
                                <div className="absolute top-0 right-0 w-20 h-20 bg-white opacity-10 rounded-full -translate-y-8 translate-x-8" />
                            </button>
                        );
                    })}
                </div>
            )}

            {/* Current Scenario Display */}
            {currentScenario && (
                <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                    <div className={`bg-gradient-to-br ${getModeColor(currentScenario.mode)} rounded-lg p-6 text-white mb-4`}>
                        <div className="flex items-start justify-between mb-4">
                            <div>
                                <h3 className="text-2xl font-bold mb-2">{currentScenario.name}</h3>
                                <p className="text-sm opacity-90">{currentScenario.description}</p>
                            </div>
                            {(() => {
                                const Icon = getModeIcon(currentScenario.mode);
                                return <Icon className="w-12 h-12 opacity-50" />;
                            })()}
                        </div>

                        {/* Parameters */}
                        <div className="bg-white bg-opacity-20 rounded-lg p-4 mb-4">
                            <p className="text-xs font-semibold uppercase tracking-wide mb-2 opacity-90">
                                Parameters
                            </p>
                            <div className="grid grid-cols-2 gap-3">
                                {Object.entries(currentScenario.parameters).map(([key, value]) => (
                                    <div key={key} className="bg-white bg-opacity-10 rounded px-3 py-2">
                                        <p className="text-xs opacity-75 capitalize">
                                            {key.replace(/_/g, ' ')}
                                        </p>
                                        <p className="text-sm font-semibold">
                                            {typeof value === 'object' ? JSON.stringify(value) : String(value)}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        {/* Objectives */}
                        <div>
                            <p className="text-xs font-semibold uppercase tracking-wide mb-2 opacity-90">
                                Objectives
                            </p>
                            <ul className="space-y-2">
                                {currentScenario.objectives.map((objective, idx) => (
                                    <li key={idx} className="flex items-start gap-2">
                                        <span className="text-yellow-300 mt-0.5">✓</span>
                                        <span className="text-sm">{objective}</span>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="grid grid-cols-2 gap-3">
                        <button className="px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 font-medium">
                            ▶ Start Scenario
                        </button>
                        <button
                            onClick={() => startCreativeTraining()}
                            className="px-4 py-3 bg-gray-500 text-white rounded-lg hover:bg-gray-600 font-medium"
                        >
                            🔄 New Scenario
                        </button>
                    </div>
                </div>
            )}

            {/* Mode Descriptions */}
            {modes && !currentScenario && (
                <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Training Modes
                    </h3>
                    <div className="space-y-3">
                        {Object.entries(modes.descriptions).map(([mode, description]: [string, any]) => (
                            <div key={mode} className="bg-gray-50 dark:bg-gray-700 rounded-lg p-3">
                                <div className="flex items-center gap-2 mb-1">
                                    {(() => {
                                        const Icon = getModeIcon(mode);
                                        return <Icon className="w-4 h-4 text-gray-600 dark:text-gray-400" />;
                                    })()}
                                    <p className="font-medium text-gray-900 dark:text-white capitalize">
                                        {mode.split('_').join(' ')}
                                    </p>
                                </div>
                                <p className="text-sm text-gray-600 dark:text-gray-400 ml-6">
                                    {description}
                                </p>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}
