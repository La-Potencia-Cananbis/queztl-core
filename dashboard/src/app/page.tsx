'use client';

import { useEffect, useState } from 'react';
import MetricsChart from '@/components/MetricsChart';
import StatusCard from '@/components/StatusCard';
import TrainingControls from '@/components/TrainingControls';
import RecentProblems from '@/components/RecentProblems';
import PowerMeter from '@/components/PowerMeter';
import CreativeTraining from '@/components/CreativeTraining';
import { Activity, Zap, AlertCircle, TrendingUp } from 'lucide-react';

interface MetricsSummary {
    total_scenarios: number;
    average_response_time: number;
    average_throughput: number;
    average_success_rate: number;
    total_errors: number;
    uptime: number;
}

interface TrainingStatus {
    is_running: boolean;
    current_scenario: string | null;
    scenarios_completed: number;
    total_runtime: number;
    average_success_rate: number;
    current_difficulty: string;
}

export default function Home() {
    const [summary, setSummary] = useState<MetricsSummary | null>(null);
    const [trainingStatus, setTrainingStatus] = useState<TrainingStatus | null>(null);
    const [isConnected, setIsConnected] = useState(false);

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 5000);

        // WebSocket connection
        connectWebSocket();

        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [summaryRes, statusRes] = await Promise.all([
                fetch('http://localhost:8000/api/metrics/summary'),
                fetch('http://localhost:8000/api/training/status')
            ]);

            if (summaryRes.ok) {
                const data = await summaryRes.json();
                setSummary(data);
            }

            if (statusRes.ok) {
                const data = await statusRes.json();
                setTrainingStatus(data);
            }
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const connectWebSocket = () => {
        const ws = new WebSocket('ws://localhost:8000/ws/metrics');

        ws.onopen = () => {
            console.log('WebSocket connected');
            setIsConnected(true);

            // Send periodic ping
            const pingInterval = setInterval(() => {
                if (ws.readyState === WebSocket.OPEN) {
                    ws.send('ping');
                }
            }, 30000);

            ws.onclose = () => {
                clearInterval(pingInterval);
            };
        };

        ws.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log('Received:', message);

            if (message.type === 'training_update' || message.type === 'scenario_completed') {
                fetchData();
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            setIsConnected(false);
        };

        ws.onclose = () => {
            console.log('WebSocket disconnected');
            setIsConnected(false);

            // Reconnect after 5 seconds
            setTimeout(connectWebSocket, 5000);
        };
    };

    const formatUptime = (seconds: number) => {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = Math.floor(seconds % 60);
        return `${hours}h ${minutes}m ${secs}s`;
    };

    return (
        <main className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
            <div className="container mx-auto p-6">
                {/* Header */}
                <div className="mb-8">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
                                🦅 Queztl-Core Testing & Monitoring
                            </h1>
                            <p className="text-gray-600 dark:text-gray-400">
                                Real-time performance monitoring and adaptive learning system
                            </p>
                        </div>
                        <div className="flex items-center gap-2">
                            <div className={`h-3 w-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                                {isConnected ? 'Connected' : 'Disconnected'}
                            </span>
                        </div>
                    </div>
                </div>

                {/* Status Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                    <StatusCard
                        title="Total Scenarios"
                        value={summary?.total_scenarios.toString() || '0'}
                        icon={<Activity className="h-5 w-5" />}
                        trend="+12%"
                        trendUp={true}
                    />
                    <StatusCard
                        title="Avg Response Time"
                        value={`${summary?.average_response_time.toFixed(0) || '0'}ms`}
                        icon={<Zap className="h-5 w-5" />}
                        trend="-8%"
                        trendUp={true}
                    />
                    <StatusCard
                        title="Success Rate"
                        value={`${((summary?.average_success_rate || 0) * 100).toFixed(1)}%`}
                        icon={<TrendingUp className="h-5 w-5" />}
                        trend="+2.5%"
                        trendUp={true}
                    />
                    <StatusCard
                        title="Total Errors"
                        value={summary?.total_errors.toString() || '0'}
                        icon={<AlertCircle className="h-5 w-5" />}
                        trend="-15%"
                        trendUp={true}
                    />
                </div>

                {/* Training Controls */}
                <div className="mb-8">
                    <TrainingControls
                        trainingStatus={trainingStatus}
                        onStatusChange={fetchData}
                    />
                </div>

                {/* Charts */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
                    <MetricsChart />
                    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
                        <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                            Training Progress
                        </h3>
                        {trainingStatus && (
                            <div className="space-y-4">
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 dark:text-gray-400">Status</span>
                                    <span className={`px-3 py-1 rounded-full text-sm font-medium ${trainingStatus.is_running
                                        ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                                        : 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
                                        }`}>
                                        {trainingStatus.is_running ? 'Running' : 'Stopped'}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 dark:text-gray-400">Scenarios Completed</span>
                                    <span className="font-semibold text-gray-900 dark:text-white">
                                        {trainingStatus.scenarios_completed}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 dark:text-gray-400">Current Difficulty</span>
                                    <span className="px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200">
                                        {trainingStatus.current_difficulty}
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 dark:text-gray-400">Average Success Rate</span>
                                    <span className="font-semibold text-gray-900 dark:text-white">
                                        {(trainingStatus.average_success_rate * 100).toFixed(1)}%
                                    </span>
                                </div>
                                <div className="flex justify-between items-center">
                                    <span className="text-gray-600 dark:text-gray-400">Runtime</span>
                                    <span className="font-semibold text-gray-900 dark:text-white">
                                        {formatUptime(trainingStatus.total_runtime)}
                                    </span>
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                {/* Recent Problems */}
                <RecentProblems />

                {/* Power Measurement & Benchmarking */}
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <PowerMeter />
                    <CreativeTraining />
                </div>
            </div>
        </main>
    );
}
