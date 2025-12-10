#!/bin/bash
echo "🚀 Launching QuetzalCore Dashboard"
echo "URL: http://localhost:8080"
python3 -m http.server 8080 --directory dashboard &
echo "✅ Dashboard running on http://localhost:8080"
