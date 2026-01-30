#!/bin/bash

# AI Interview Backend - Quick Verification Script
# Run this after activating venv: source venv/Scripts/activate

echo "=================================================="
echo "  AI INTERVIEW BACKEND - QUICK VERIFICATION"
echo "=================================================="
echo ""

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment not activated!"
    echo "Run: source venv/Scripts/activate"
    echo ""
    exit 1
fi

echo "✅ Virtual environment: ACTIVE"
echo "   Path: $VIRTUAL_ENV"
echo ""

# Run the comprehensive verification
echo "Running comprehensive tests..."
echo ""

python verify_backend.py

echo ""
echo "=================================================="
echo "   Verification Complete"
echo "=================================================="
