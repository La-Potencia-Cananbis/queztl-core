"use client";

import { useState } from 'react';

interface WorkloadResult {
    workload: string;
    emoji: string;
    duration: number;
    grade: string;
    description: string;
    [key: string]: any;
}

export default function AdvancedWorkloads() {
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<WorkloadResult | null>(null);
    const [workloadType, setWorkloadType] = useState<'3d' | 'mining' | 'extreme' | null>(null);

    const run3DWorkload = async (preset: 'light' | 'medium' | 'heavy') => {
        setLoading(true);
        setWorkloadType('3d');

        const configs = {
            light: { matrix_size: 256, num_iterations: 50, ray_count: 5000 },
            medium: { matrix_size: 512, num_iterations: 100, ray_count: 10000 },
            heavy: { matrix_size: 1024, num_iterations: 150, ray_count: 20000 }
        };

        const config = configs[preset];

        try {
            const response = await fetch(
                `http://localhost:8000/api/workload/3d?matrix_size=${config.matrix_size}&num_iterations=${config.num_iterations}&ray_count=${config.ray_count}`,
                { method: 'POST' }
            );
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('3D workload error:', error);
            setResult({ workload: 'Error', emoji: '❌', duration: 0, grade: 'F', description: 'Failed to run 3D workload' });
        } finally {
            setLoading(false);
        }
    };

    const runMiningWorkload = async (preset: 'easy' | 'medium' | 'hard') => {
        setLoading(true);
        setWorkloadType('mining');

        const configs = {
            easy: { difficulty: 3, num_blocks: 3, num_workers: 2 },
            medium: { difficulty: 4, num_blocks: 5, num_workers: 4 },
            hard: { difficulty: 5, num_blocks: 8, num_workers: 8 }
        };

        const config = configs[preset];

        try {
            const response = await fetch(
                `http://localhost:8000/api/workload/mining?difficulty=${config.difficulty}&num_blocks=${config.num_blocks}&parallel=true&num_workers=${config.num_workers}`,
                { method: 'POST' }
            );
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Mining workload error:', error);
            setResult({ workload: 'Error', emoji: '❌', duration: 0, grade: 'F', description: 'Failed to run mining workload' });
        } finally {
            setLoading(false);
        }
    };

    const runExtremeWorkload = async () => {
        setLoading(true);
        setWorkloadType('extreme');

        try {
            const response = await fetch(
                'http://localhost:8000/api/workload/extreme?duration_seconds=30',
                { method: 'POST' }
            );
            const data = await response.json();
            setResult(data);
        } catch (error) {
            console.error('Extreme workload error:', error);
            setResult({ workload: 'Error', emoji: '❌', duration: 0, grade: 'F', description: 'Failed to run extreme workload' });
        } finally {
            setLoading(false);
        }
    };

    const getGradeColor = (grade: string) => {
        if (grade.startsWith('S')) return 'text-purple-400';
        if (grade.startsWith('A')) return 'text-green-400';
        if (grade.startsWith('B')) return 'text-blue-400';
        if (grade.startsWith('C')) return 'text-yellow-400';
        if (grade.startsWith('D')) return 'text-orange-400';
        return 'text-red-400';
    };

    const getGradeBg = (grade: string) => {
        if (grade.startsWith('S')) return 'bg-purple-500/10 border-purple-500/30';
        if (grade.startsWith('A')) return 'bg-green-500/10 border-green-500/30';
        if (grade.startsWith('B')) return 'bg-blue-500/10 border-blue-500/30';
        if (grade.startsWith('C')) return 'bg-yellow-500/10 border-yellow-500/30';
        if (grade.startsWith('D')) return 'bg-orange-500/10 border-orange-500/30';
        return 'bg-red-500/10 border-red-500/30';
    };

    return (
        <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
            <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-bold text-white flex items-center gap-2">
                    <span>🔥</span>
                    Advanced Workloads
                </h2>
            </div>

            {/* 3D Graphics Workload */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                    <span>🎮</span>
                    3D Graphics & Ray Tracing
                </h3>
                <div className="flex gap-2">
                    <button
                        onClick={() => run3DWorkload('light')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Light
                    </button>
                    <button
                        onClick={() => run3DWorkload('medium')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Medium
                    </button>
                    <button
                        onClick={() => run3DWorkload('heavy')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-purple-600 hover:bg-purple-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Heavy
                    </button>
                </div>
                <p className="text-gray-400 text-sm mt-2">
                    Matrix transformations, ray-sphere intersections, GFLOPS benchmark
                </p>
            </div>

            {/* Crypto Mining Workload */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                    <span>⛏️</span>
                    Cryptocurrency Mining Simulation
                </h3>
                <div className="flex gap-2">
                    <button
                        onClick={() => runMiningWorkload('easy')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-yellow-600 hover:bg-yellow-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Easy
                    </button>
                    <button
                        onClick={() => runMiningWorkload('medium')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-orange-600 hover:bg-orange-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Medium
                    </button>
                    <button
                        onClick={() => runMiningWorkload('hard')}
                        disabled={loading}
                        className="flex-1 px-4 py-2 bg-red-600 hover:bg-red-700 disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors"
                    >
                        Hard
                    </button>
                </div>
                <p className="text-gray-400 text-sm mt-2">
                    SHA-256 hashing, proof-of-work, parallel mining workers
                </p>
            </div>

            {/* EXTREME Combined Workload */}
            <div className="mb-6">
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                    <span>🔥</span>
                    BEAST MODE - Combined Extreme
                </h3>
                <button
                    onClick={runExtremeWorkload}
                    disabled={loading}
                    className="w-full px-6 py-4 bg-gradient-to-r from-red-600 via-purple-600 to-pink-600 hover:from-red-700 hover:via-purple-700 hover:to-pink-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed text-white rounded-lg font-bold text-lg transition-all transform hover:scale-105"
                >
                    {loading && workloadType === 'extreme' ? '🔥 UNLEASHING BEAST...' : '🔥 UNLEASH THE BEAST'}
                </button>
                <p className="text-gray-400 text-sm mt-2">
                    Runs 3D graphics + crypto mining simultaneously for 30 seconds. Maximum stress!
                </p>
            </div>

            {/* Loading State */}
            {loading && (
                <div className="mb-6 p-4 bg-gray-700 rounded-lg border border-gray-600">
                    <div className="flex items-center gap-3">
                        <div className="animate-spin h-6 w-6 border-4 border-blue-500 border-t-transparent rounded-full"></div>
                        <div>
                            <p className="text-white font-semibold">Running {workloadType?.toUpperCase()} workload...</p>
                            <p className="text-gray-400 text-sm">Pushing your system to the limits</p>
                        </div>
                    </div>
                </div>
            )}

            {/* Results Display */}
            {result && !loading && (
                <div className={`p-6 rounded-lg border-2 ${getGradeBg(result.grade)}`}>
                    <div className="flex items-center justify-between mb-4">
                        <h3 className="text-2xl font-bold text-white flex items-center gap-2">
                            <span className="text-4xl">{result.emoji}</span>
                            {result.workload}
                        </h3>
                        <div className={`text-3xl font-bold ${getGradeColor(result.grade)}`}>
                            {result.grade}
                        </div>
                    </div>

                    <p className="text-gray-300 mb-4">{result.description}</p>

                    <div className="grid grid-cols-2 gap-4 mb-4">
                        <div>
                            <p className="text-gray-400 text-sm">Duration</p>
                            <p className="text-white font-semibold">{result.duration.toFixed(2)}s</p>
                        </div>

                        {/* 3D Workload Specific */}
                        {result.gflops !== undefined && (
                            <>
                                <div>
                                    <p className="text-gray-400 text-sm">GFLOPS</p>
                                    <p className="text-white font-semibold">{result.gflops.toFixed(2)}</p>
                                </div>
                                {result.metrics && (
                                    <>
                                        <div>
                                            <p className="text-gray-400 text-sm">Matrix Operations</p>
                                            <p className="text-white font-semibold">{result.metrics.matrix_operations.toLocaleString()}</p>
                                        </div>
                                        <div>
                                            <p className="text-gray-400 text-sm">Ray Intersections</p>
                                            <p className="text-white font-semibold">{result.metrics.ray_intersections.toLocaleString()}</p>
                                        </div>
                                    </>
                                )}
                            </>
                        )}

                        {/* Mining Workload Specific */}
                        {result.hash_rate !== undefined && (
                            <>
                                <div>
                                    <p className="text-gray-400 text-sm">Hash Rate</p>
                                    <p className="text-white font-semibold">{result.hash_rate_display}</p>
                                </div>
                                <div>
                                    <p className="text-gray-400 text-sm">Blocks Mined</p>
                                    <p className="text-white font-semibold">{result.blocks_mined}</p>
                                </div>
                                <div>
                                    <p className="text-gray-400 text-sm">Total Hashes</p>
                                    <p className="text-white font-semibold">{result.total_hashes.toLocaleString()}</p>
                                </div>
                                <div>
                                    <p className="text-gray-400 text-sm">Workers</p>
                                    <p className="text-white font-semibold">{result.workers}</p>
                                </div>
                            </>
                        )}

                        {/* Extreme Workload Specific */}
                        {result.combined_score !== undefined && (
                            <>
                                <div>
                                    <p className="text-gray-400 text-sm">Combined Score</p>
                                    <p className="text-white font-semibold">{result.combined_score.toFixed(2)}/100</p>
                                </div>
                                <div>
                                    <p className="text-gray-400 text-sm">Beast Level</p>
                                    <p className="text-white font-semibold">{result.beast_level}</p>
                                </div>
                            </>
                        )}
                    </div>

                    {/* Comparison Section */}
                    {result.comparison && (
                        <div className="mt-4 pt-4 border-t border-gray-600">
                            <p className="text-gray-400 text-sm mb-2">Industry Comparison:</p>
                            <div className="grid grid-cols-3 gap-2">
                                {Object.entries(result.comparison).map(([key, value]) => (
                                    <div key={key} className="bg-gray-700/50 rounded p-2">
                                        <p className="text-gray-400 text-xs">{key.replace(/_/g, ' ').toUpperCase()}</p>
                                        <p className="text-white font-semibold text-sm">{String(value)}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Extreme Workload Details */}
                    {result.system_metrics && (
                        <div className="mt-4 pt-4 border-t border-gray-600">
                            <p className="text-gray-400 text-sm mb-2">System Metrics:</p>
                            <div className="grid grid-cols-2 gap-2 text-sm">
                                <div>
                                    <p className="text-gray-400">Peak CPU</p>
                                    <p className="text-white">{result.system_metrics.peak_cpu_percent.toFixed(1)}%</p>
                                </div>
                                <div>
                                    <p className="text-gray-400">Memory Used</p>
                                    <p className="text-white">{result.system_metrics.memory_used_mb.toFixed(1)} MB</p>
                                </div>
                                <div>
                                    <p className="text-gray-400">CPU Cores</p>
                                    <p className="text-white">{result.system_metrics.cpu_cores}</p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
