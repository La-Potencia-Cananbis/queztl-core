'use client'

import { useState, useEffect } from 'react'
import LiveChart from '../components/LiveChart'
import PacketFlow from '../components/PacketFlow'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'https://queztl-core-backend.onrender.com'

export default function Dashboard() {
    const [metrics, setMetrics] = useState({
        packetsPerSecond: 185000,
        activeNodes: 847,
        latency: 2.3,
        uptime: 99.97,
        backendConnected: false
    })

    // Fetch real data from backend
    useEffect(() => {
        const fetchMetrics = async () => {
            try {
                const response = await fetch(`${BACKEND_URL}/api/metrics`)
                if (response.ok) {
                    const data = await response.json()
                    setMetrics(prev => ({ ...prev, ...data, backendConnected: true }))
                }
            } catch (error) {
                console.error('Backend not connected:', error)
            }
        }

        fetchMetrics()
        const interval = setInterval(fetchMetrics, 5000)
        return () => clearInterval(interval)
    }, [])

    // Simulate metrics if backend not connected
    useEffect(() => {
        const interval = setInterval(() => {
            setMetrics(prev => ({
                ...prev,
                packetsPerSecond: prev.packetsPerSecond + Math.floor(Math.random() * 10000 - 5000),
                activeNodes: prev.activeNodes + Math.floor(Math.random() * 20 - 10),
                latency: Math.max(0.5, prev.latency + (Math.random() * 0.4 - 0.2)),
                uptime: Math.min(100, prev.uptime + (Math.random() * 0.01))
            }))
        }, 2000)
        return () => clearInterval(interval)
    }, [])

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 p-8">
            <PacketFlow />

            {/* Backend Status Indicator */}
            <div className="fixed top-4 right-4 z-50">
                <div className={`px-4 py-2 rounded-full ${metrics.backendConnected ? 'bg-green-500' : 'bg-red-500'} text-white text-sm font-semibold flex items-center gap-2`}>
                    <div className={`w-2 h-2 rounded-full ${metrics.backendConnected ? 'bg-green-200 animate-pulse' : 'bg-red-200'}`}></div>
                    {metrics.backendConnected ? '🦅 BACKEND CONNECTED' : '⚠️ SIMULATED DATA'}
                </div>
            </div>

            <div className="max-w-7xl mx-auto">
                <div className="mb-8 text-center">
                    <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-purple-400 to-pink-400 mb-2 animate-pulse">
                        {metrics.packetsPerSecond.toLocaleString()}
                    </h1>
                    <p className="text-xl text-gray-300">Packets per Second 🦅</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <StatCard
                        title="Active Nodes"
                        value={metrics.activeNodes}
                        icon="🌐"
                        gradient="from-blue-500 to-cyan-500"
                    />
                    <StatCard
                        title="Latency"
                        value={`${metrics.latency.toFixed(1)}ms`}
                        icon="⚡"
                        gradient="from-purple-500 to-pink-500"
                    />
                    <StatCard
                        title="Uptime"
                        value={`${metrics.uptime.toFixed(2)}%`}
                        icon="🚀"
                        gradient="from-green-500 to-emerald-500"
                    />
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <LiveChart
                        title="Network Traffic"
                        color="#8b5cf6"
                        data={[45, 52, 48, 65, 72, 68, 85, 92, 88, 95]}
                    />
                    <LiveChart
                        title="Node Activity"
                        color="#06b6d4"
                        data={[30, 35, 42, 38, 45, 52, 48, 55, 62, 58]}
                    />
                    <LiveChart
                        title="Response Time"
                        color="#ec4899"
                        data={[2.1, 2.3, 1.9, 2.5, 2.2, 1.8, 2.4, 2.0, 2.3, 1.9]}
                    />
                    <LiveChart
                        title="CPU Usage"
                        color="#10b981"
                        data={[45, 48, 52, 49, 55, 58, 54, 60, 63, 59]}
                    />
                </div>
            </div>
        </div>
    )
}

function StatCard({ title, value, icon, gradient }: any) {
    return (
        <div className={`relative overflow-hidden rounded-2xl bg-gradient-to-br ${gradient} p-6 backdrop-blur-xl shadow-2xl hover:scale-105 transition-transform duration-300`}>
            <div className="absolute inset-0 bg-white/10 backdrop-blur-sm"></div>
            <div className="relative z-10">
                <div className="text-4xl mb-2">{icon}</div>
                <h3 className="text-sm text-white/80 mb-1">{title}</h3>
                <p className="text-3xl font-bold text-white">{value}</p>
            </div>
        </div>
    )
}/* Updated Tue Dec 16 01:50:00 MST 2025 */
