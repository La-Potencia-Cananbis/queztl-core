'use client';

import { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

interface Metric {
    timestamp: string;
    type: string;
    value: number;
    scenario_id: string;
}

export default function MetricsChart() {
    const [metrics, setMetrics] = useState<Metric[]>([]);

    useEffect(() => {
        fetchMetrics();
        const interval = setInterval(fetchMetrics, 5000);
        return () => clearInterval(interval);
    }, []);

    const fetchMetrics = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/metrics/latest');
            if (response.ok) {
                const data = await response.json();
                setMetrics(data.metrics || []);
            }
        } catch (error) {
            console.error('Error fetching metrics:', error);
        }
    };

    // Transform data for chart
    const chartData = metrics
        .filter(m => m.type === 'response_time')
        .slice(-20)
        .map((m, index) => ({
            time: index,
            'Response Time': m.value,
        }));

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Response Time Metrics
            </h3>
            <ResponsiveContainer width="100%" height={300}>
                <LineChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis label={{ value: 'ms', angle: -90, position: 'insideLeft' }} />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Response Time" stroke="#3b82f6" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
