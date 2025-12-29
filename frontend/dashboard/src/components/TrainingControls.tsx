'use client';

import { useState } from 'react';
import { Play, Square, RefreshCw } from 'lucide-react';

interface TrainingControlsProps {
    trainingStatus: any;
    onStatusChange: () => void;
}

export default function TrainingControls({ trainingStatus, onStatusChange }: TrainingControlsProps) {
    const [loading, setLoading] = useState(false);

    const startTraining = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/training/start', {
                method: 'POST',
            });
            if (response.ok) {
                onStatusChange();
            }
        } catch (error) {
            console.error('Error starting training:', error);
        } finally {
            setLoading(false);
        }
    };

    const stopTraining = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/training/stop', {
                method: 'POST',
            });
            if (response.ok) {
                onStatusChange();
            }
        } catch (error) {
            console.error('Error stopping training:', error);
        } finally {
            setLoading(false);
        }
    };

    const generateScenario = async () => {
        setLoading(true);
        try {
            const response = await fetch('http://localhost:8000/api/scenarios/generate', {
                method: 'POST',
            });
            if (response.ok) {
                const scenario = await response.json();
                console.log('Generated scenario:', scenario);

                // Execute the scenario
                await fetch(`http://localhost:8000/api/scenarios/${scenario.id}/execute`, {
                    method: 'POST',
                });

                onStatusChange();
            }
        } catch (error) {
            console.error('Error generating scenario:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Training Controls
            </h3>
            <div className="flex gap-4">
                {!trainingStatus?.is_running ? (
                    <button
                        onClick={startTraining}
                        disabled={loading}
                        className="flex items-center gap-2 px-6 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                        <Play className="h-5 w-5" />
                        Start Continuous Training
                    </button>
                ) : (
                    <button
                        onClick={stopTraining}
                        disabled={loading}
                        className="flex items-center gap-2 px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                    >
                        <Square className="h-5 w-5" />
                        Stop Training
                    </button>
                )}

                <button
                    onClick={generateScenario}
                    disabled={loading}
                    className="flex items-center gap-2 px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium transition-colors disabled:opacity-50"
                >
                    <RefreshCw className="h-5 w-5" />
                    Generate & Execute Scenario
                </button>
            </div>
        </div>
    );
}
