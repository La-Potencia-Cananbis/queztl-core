'use client';

import { useEffect, useState } from 'react';

interface Problem {
    id: string;
    type: string;
    difficulty: string;
    description: string;
    created_at: string;
}

export default function RecentProblems() {
    const [problems, setProblems] = useState<Problem[]>([]);

    useEffect(() => {
        fetchProblems();
        const interval = setInterval(fetchProblems, 10000);
        return () => clearInterval(interval);
    }, []);

    const fetchProblems = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/problems/recent');
            if (response.ok) {
                const data = await response.json();
                setProblems(data.problems || []);
            }
        } catch (error) {
            console.error('Error fetching problems:', error);
        }
    };

    const getDifficultyColor = (difficulty: string) => {
        switch (difficulty.toLowerCase()) {
            case 'easy':
                return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
            case 'medium':
                return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
            case 'hard':
                return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
            case 'extreme':
                return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
            default:
                return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200';
        }
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 text-gray-900 dark:text-white">
                Recent Training Problems
            </h3>
            <div className="space-y-3">
                {problems.length === 0 ? (
                    <p className="text-gray-500 dark:text-gray-400 text-center py-8">
                        No problems generated yet. Start training to see scenarios.
                    </p>
                ) : (
                    problems.map((problem) => (
                        <div
                            key={problem.id}
                            className="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                        >
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className="font-medium text-gray-900 dark:text-white">
                                        {problem.type.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                                    </span>
                                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getDifficultyColor(problem.difficulty)}`}>
                                        {problem.difficulty}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                    {problem.description}
                                </p>
                            </div>
                            <div className="text-xs text-gray-500 dark:text-gray-500 ml-4">
                                {new Date(problem.created_at).toLocaleTimeString()}
                            </div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}
