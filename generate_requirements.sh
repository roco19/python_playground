#!/bin/bash
# generate_requirements.sh

echo "🔍 Analyzing code imports..."
pipreqs . --force --encoding utf-8 --mode no-pin --ignore .venv,__pycache__,.git --savepath requirements.in

if [ $? -eq 0 ]; then
    echo "✅ Generated requirements.in"

    echo "🔒 Compiling locked requirements..."
    pip-compile --strip-extras --quiet requirements.in

    if [ $? -eq 0 ]; then
        echo "📝 Adding CUDA support warning..."

        # Add CUDA warning after the pip-compile header
        sed -i "1i\
# CUDA SUPPORT: If you have an NVIDIA GPU, install PyTorch with CUDA support:\n\
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118\n\
# For other CUDA versions: https://pytorch.org/get-started/locally/" requirements.txt

        echo "✅ Generated requirements.txt with CUDA warning"
        echo "Summary:"
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