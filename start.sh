#!/bin/bash

echo "=========================================="
echo "  MindPulse - ML Production Platform"
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "   Please start Docker Desktop and try again"
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Create necessary directories
echo "📁 Creating required directories..."
mkdir -p data artifacts reports
echo "   ✅ data/ artifacts/ reports/ created"
echo ""

# Check if artifacts exist
if [ ! -f "artifacts/model.pickle" ]; then
    echo "⚠️  Warning: Model artifacts not found in artifacts/"
    echo "   Please run the training script first:"
    echo "   python scripts/students_scripts.py"
    echo ""
fi

# Check if ref_data exists
if [ ! -f "data/ref_data.csv" ]; then
    echo "⚠️  Warning: Reference data not found in data/"
    echo "   The training script will generate it"
    echo ""
fi

echo "🚀 Starting all services..."
echo ""
echo "   Services:"
echo "   - serving-api:  http://localhost:8080"
echo "   - webapp:       http://localhost:8081"
echo "   - reporting:    generates reports in reports/"
echo ""

# Start services
docker compose up --build

echo ""
echo "✅ Services started!"
