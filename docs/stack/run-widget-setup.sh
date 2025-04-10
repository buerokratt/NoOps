k#!/bin/bash

set -e  # Exit on error

PROJECT_DIR="widget"
NOOPS_REPO="https://github.com/buerokratt/NoOps"
CHATBOT_REPO="https://github.com/buerokratt/Buerokratt-Chatbot"
NOOPS_COMPOSE_PATH="NoOps/docs/stack"

echo "📁 Creating project directory: $PROJECT_DIR"
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"

# --- Clone and build Ruuter ---
if [ ! -d "Ruuter" ]; then
    echo "🔄 Cloning Ruuter..."
    git clone https://github.com/buerokratt/Ruuter
fi
cd Ruuter
git checkout dev
echo "🐳 Building Ruuter Docker image..."
docker build -t ruuter .
cd ..

# --- Clone and build DataMapper ---
if [ ! -d "DataMapper" ]; then
    echo "🔄 Cloning DataMapper..."
    git clone https://github.com/buerokratt/DataMapper.git
fi
cd DataMapper
git checkout dev
echo "🐳 Building DataMapper Docker image..."
docker build -t data-mapper .
cd ..

# --- Clone and build Resql ---
if [ ! -d "Resql" ]; then
    echo "🔄 Cloning Resql..."
    git clone https://github.com/buerokratt/Resql
fi
cd Resql
git checkout dev
echo "🐳 Building Resql Docker image..."
docker build -f Dockerfile -t resql .
cd ..

# --- Clone and build Chat Widget ---
if [ ! -d "Chat-Widget" ]; then
    echo "🔄 Cloning Chat-Widget..."
    git clone https://github.com/buerokratt/Chat-Widget
fi
cd Chat-Widget
git checkout dev
echo "🐳 Building Chat-Widget Docker image..."
docker build -f Dockerfile.dev -t chat-widget .
cd ..

# --- Clone NoOps for docker-compose ---
if [ ! -d "NoOps" ]; then
    echo "🔄 Cloning NoOps..."
    git clone "$NOOPS_REPO"
fi
cd NoOps
git checkout dev
cd ..

# --- Clone Buerokratt-Chatbot for DSL and constants.ini ---
if [ ! -d "Buerokratt-Chatbot" ]; then
    echo "🔄 Cloning Buerokratt-Chatbot for DSL files and constants.ini..."
    git clone "$CHATBOT_REPO"
fi
cd Buerokratt-Chatbot
git checkout dev
cd ..

# --- Prepare DSL and constants.ini for docker-compose volumes ---
echo "🗂️  Setting up DSL folders and constants.ini..."

mkdir -p NoOps/docs/stack/DSL/Resql
mkdir -p NoOps/docs/stack/DSL/Ruuter.public
mkdir -p NoOps/docs/stack/DSL/DMapper/backoffice/hbs

# Copy DSL files
cp -r Buerokratt-Chatbot/DSL/Resql/backoffice/* NoOps/docs/stack/DSL/Resql/
cp -r Buerokratt-Chatbot/DSL/Ruuter.public/* NoOps/docs/stack/DSL/Ruuter.public/
cp -r Buerokratt-Chatbot/DSL/DMapper/backoffice/hbs/* NoOps/docs/stack/DSL/DMapper/backoffice/hbs/

# Copy constants.ini
cp Buerokratt-Chatbot/constants.ini NoOps/docs/stack/

# --- Run docker-compose ---
echo "🚀 Running docker compose from $NOOPS_COMPOSE_PATH..."
cd "$NOOPS_COMPOSE_PATH"
docker compose up -d

echo "✅ Setup complete!"
