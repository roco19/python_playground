#!/bin/bash
# generate_requirements.sh

echo "🔍 Analyzing code imports..."
pipreqs . --force --encoding utf-8 --mode no-pin --ignore .venv,__pycache__,.git --savepath requirements.in

if [ $? -eq 0 ]; then
    echo "✅ Generated requirements.in"
    
    echo "🔒 Compiling locked requirements..."
    pip-compile requirements.in
    
    if [ $? -eq 0 ]; then
        echo "✅ Generated requirements.txt"
        echo "📊 Summary:"
        echo "   requirements.in:  $(wc -l < requirements.in) packages"
        echo "   requirements.txt: $(grep -c '^[^#]' requirements.txt) packages"
    else
        echo "❌ Failed to compile requirements"
        exit 1
    fi
else
    echo "❌ Failed to analyze imports"
    exit 1
fi
