'use client';

import { useState } from 'react';
import { Activity, Zap, Target, Trophy, TrendingUp, Cpu, HardDrive, Wifi } from 'lucide-react';

interface PowerMeasurement {
    timestamp: string;
    cpu: {
        usage_percent: number;
        count: number;
    };
    memory: {
        total_gb: number;
        available_gb: number;
        used_gb: number;
        percent: number;
    };
    disk: {
        total_gb: number;
        used_gb: number;
        free_gb: number;
        percent: number;
    };
    power_score: number;
}

interface StressTestResult {
    intensity: string;
    duration_seconds: number;
    operations_per_second: number;
    error_rate: number;
    grade: string;
    statistics: {
        cpu: { avg: number; max: number };
        memory: { avg: number; max: number };
    };
}

export default function PowerMeter() {
    const [measurement, setMeasurement] = useState<PowerMeasurement | null>(null);
    const [stressResult, setStressResult] = useState<StressTestResult | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isTesting, setIsTesting] = useState(false);

    const measurePower = async () => {
        setIsLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/power/measure');
            const data = await response.json();
            setMeasurement(data);
        } catch (error) {
            console.error('Failed to measure power:', error);
        } finally {
            setIsLoading(false);
        }
    };

    const runStressTest = async (intensity: string, duration: number) => {
        setIsTesting(true);
        try {
            const response = await fetch(
                `http://localhost:8000/api/power/stress-test?duration=${duration}&intensity=${intensity}`,
                { method: 'POST' }
            );
            const data = await response.json();
            setStressResult(data);
        } catch (error) {
            console.error('Failed to run stress test:', error);
        } finally {
            setIsTesting(false);
        }
    };

    const runBenchmark = async () => {
        setIsTesting(true);
        try {
            const response = await fetch('http://localhost:8000/api/power/benchmark', { method: 'POST' });
            const data = await response.json();
            alert(`Benchmark Complete!\nOverall Score: ${data.overall_score.toFixed(2)}/100\nThroughput: ${data.tests.throughput.operations_per_second.toFixed(2)} ops/sec`);
        } catch (error) {
            console.error('Failed to run benchmark:', error);
        } finally {
            setIsTesting(false);
        }
    };

    const getPowerColor = (score: number) => {
        if (score >= 80) return 'text-green-500';
        if (score >= 60) return 'text-yellow-500';
        return 'text-red-500';
    };

    const getGradeColor = (grade: string) => {
        if (grade.startsWith('S') || grade.startsWith('A')) return 'text-green-500';
        if (grade.startsWith('B')) return 'text-blue-500';
        if (grade.startsWith('C')) return 'text-yellow-500';
        return 'text-red-500';
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-6">
                <div className="flex items-center gap-2">
                    <Zap className="w-6 h-6 text-yellow-500" />
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                        Power Meter
                    </h2>
                </div>
                <button
                    onClick={measurePower}
                    disabled={isLoading}
                    className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:opacity-50 flex items-center gap-2"
                >
                    <Activity className="w-4 h-4" />
                    {isLoading ? 'Measuring...' : 'Measure Power'}
                </button>
            </div>

            {measurement && (
                <div className="space-y-4 mb-6">
                    {/* Power Score */}
                    <div className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg p-6 text-white">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-sm opacity-90">Power Score</p>
                                <p className="text-4xl font-bold">{measurement.power_score.toFixed(1)}</p>
                                <p className="text-xs opacity-75 mt-1">Out of 100</p>
                            </div>
                            <Trophy className="w-16 h-16 opacity-50" />
                        </div>
                    </div>

                    {/* System Metrics Grid */}
                    <div className="grid grid-cols-3 gap-4">
                        {/* CPU */}
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                            <div className="flex items-center gap-2 mb-2">
                                <Cpu className="w-5 h-5 text-blue-500" />
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">CPU</p>
                            </div>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                {measurement.cpu.usage_percent.toFixed(1)}%
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                {measurement.cpu.count} cores
                            </p>
                        </div>

                        {/* Memory */}
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                            <div className="flex items-center gap-2 mb-2">
                                <HardDrive className="w-5 h-5 text-green-500" />
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Memory</p>
                            </div>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                {measurement.memory.percent.toFixed(1)}%
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                {measurement.memory.used_gb.toFixed(1)} / {measurement.memory.total_gb.toFixed(1)} GB
                            </p>
                        </div>

                        {/* Disk */}
                        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                            <div className="flex items-center gap-2 mb-2">
                                <TrendingUp className="w-5 h-5 text-purple-500" />
                                <p className="text-sm font-medium text-gray-700 dark:text-gray-300">Disk</p>
                            </div>
                            <p className="text-2xl font-bold text-gray-900 dark:text-white">
                                {measurement.disk.percent.toFixed(1)}%
                            </p>
                            <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                {measurement.disk.used_gb.toFixed(1)} / {measurement.disk.total_gb.toFixed(1)} GB
                            </p>
                        </div>
                    </div>
                </div>
            )}

            {/* Stress Test Controls */}
            <div className="border-t border-gray-200 dark:border-gray-700 pt-6">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
                    <Target className="w-5 h-5 text-red-500" />
                    Stress Testing
                </h3>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-4">
                    <button
                        onClick={() => runStressTest('light', 10)}
                        disabled={isTesting}
                        className="px-4 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 disabled:opacity-50 font-medium"
                    >
                        Light (10s)
                    </button>
                    <button
                        onClick={() => runStressTest('medium', 15)}
                        disabled={isTesting}
                        className="px-4 py-2 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 disabled:opacity-50 font-medium"
                    >
                        Medium (15s)
                    </button>
                    <button
                        onClick={() => runStressTest('heavy', 20)}
                        disabled={isTesting}
                        className="px-4 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 disabled:opacity-50 font-medium"
                    >
                        Heavy (20s)
                    </button>
                    <button
                        onClick={() => runStressTest('extreme', 30)}
                        disabled={isTesting}
                        className="px-4 py-2 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 disabled:opacity-50 font-medium"
                    >
                        Extreme (30s)
                    </button>
                </div>

                <button
                    onClick={runBenchmark}
                    disabled={isTesting}
                    className="w-full px-4 py-3 bg-gradient-to-r from-blue-500 to-purple-500 text-white rounded-lg hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 font-medium flex items-center justify-center gap-2"
                >
                    <Trophy className="w-5 h-5" />
                    {isTesting ? 'Running...' : 'Run Full Benchmark Suite'}
                </button>
            </div>

            {/* Stress Test Results */}
            {stressResult && (
                <div className="mt-6 border-t border-gray-200 dark:border-gray-700 pt-6">
                    <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                        Latest Stress Test Results
                    </h3>

                    <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4 space-y-3">
                        <div className="flex items-center justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Grade</span>
                            <span className={`text-2xl font-bold ${getGradeColor(stressResult.grade)}`}>
                                {stressResult.grade}
                            </span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Operations/sec</span>
                            <span className="text-lg font-semibold text-gray-900 dark:text-white">
                                {stressResult.operations_per_second.toFixed(2)}
                            </span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Error Rate</span>
                            <span className="text-lg font-semibold text-gray-900 dark:text-white">
                                {(stressResult.error_rate * 100).toFixed(2)}%
                            </span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Avg CPU</span>
                            <span className="text-lg font-semibold text-gray-900 dark:text-white">
                                {stressResult.statistics.cpu.avg.toFixed(1)}%
                            </span>
                        </div>

                        <div className="flex items-center justify-between">
                            <span className="text-gray-600 dark:text-gray-400">Avg Memory</span>
                            <span className="text-lg font-semibold text-gray-900 dark:text-white">
                                {stressResult.statistics.memory.avg.toFixed(1)}%
                            </span>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
