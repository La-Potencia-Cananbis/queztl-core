'use client'

import { useEffect, useRef, useState } from 'react'

export default function LiveChart({ title, color, data: initialData }: any) {
    const canvasRef = useRef<HTMLCanvasElement>(null)
    const [data, setData] = useState(initialData)

    useEffect(() => {
        const interval = setInterval(() => {
            setData((prev: number[]) => {
                const newData = [...prev.slice(1), prev[prev.length - 1] + (Math.random() * 20 - 10)]
                return newData
            })
        }, 2000)
        return () => clearInterval(interval)
    }, [])

    useEffect(() => {
        const canvas = canvasRef.current
        if (!canvas) return
        const ctx = canvas.getContext('2d')
        if (!ctx) return

        canvas.width = canvas.offsetWidth * 2
        canvas.height = canvas.offsetHeight * 2
        ctx.scale(2, 2)

        ctx.clearRect(0, 0, canvas.width, canvas.height)

        const padding = 20
        const width = canvas.width / 2 - padding * 2
        const height = canvas.height / 2 - padding * 2

        const max = Math.max(...data)
        const min = Math.min(...data)
        const range = max - min || 1

        ctx.beginPath()
        ctx.strokeStyle = color
        ctx.lineWidth = 3
        ctx.lineCap = 'round'
        ctx.lineJoin = 'round'

        data.forEach((value: number, i: number) => {
            const x = padding + (i / (data.length - 1)) * width
            const y = padding + height - ((value - min) / range) * height
            if (i === 0) ctx.moveTo(x, y)
            else ctx.lineTo(x, y)
        })

        ctx.stroke()

        const gradient = ctx.createLinearGradient(0, 0, 0, canvas.height / 2)
        gradient.addColorStop(0, color + '40')
        gradient.addColorStop(1, color + '00')
        ctx.lineTo(width + padding, height + padding)
        ctx.lineTo(padding, height + padding)
        ctx.closePath()
        ctx.fillStyle = gradient
        ctx.fill()
    }, [data, color])

    return (
        <div className="relative overflow-hidden rounded-2xl bg-white/5 backdrop-blur-xl p-6 shadow-2xl border border-white/10 hover:border-white/20 transition-all duration-300">
            <h3 className="text-lg font-semibold text-white mb-4">{title}</h3>
            <canvas ref={canvasRef} className="w-full h-48" />
            <div className="absolute top-4 right-4 text-sm text-white/60">
                {data[data.length - 1].toFixed(1)}
            </div>
        </div>
    )
}