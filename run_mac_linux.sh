#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null
then
    echo "Python 3 não foi encontrado. Por favor, instala o Python 3 antes de continuar."
    exit
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "A criar ambiente virtual..."
    python3 -m venv venv
fi

# Activate virtual environment (optional but good practice)
source venv/bin/activate 2>/dev/null

# Install requirements using the venv's python directly
echo "A instalar dependências (isto pode demorar um pouco na primeira vez)..."
./venv/bin/python3 -m pip install -r requirements.txt --quiet

# Run the app using the venv's streamlit module directly
echo "A iniciar o simulador..."
./venv/bin/python3 -m streamlit run app.py
