#!/bin/bash
# Docker Container Management Script for CSE_proj_12

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "======================================================================"
echo "🐳 Phishing Detection - Docker Container Manager"
echo "======================================================================"

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker Desktop.${NC}"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker is running${NC}"
}

# Function to build the image
build_image() {
    echo ""
    echo "======================================================================"
    echo "🔨 Building Docker Image..."
    echo "======================================================================"
    docker build -t phishing-detection-api -f .devcontainer/Dockerfile .
    echo -e "${GREEN}✓ Image built successfully${NC}"
}

# Function to run the container
run_container() {
    echo ""
    echo "======================================================================"
    echo "🚀 Starting Container..."
    echo "======================================================================"
    
    # Stop existing container if running
    if docker ps -a | grep -q phishing-api; then
        echo "Stopping existing container..."
        docker stop phishing-api 2>/dev/null || true
        docker rm phishing-api 2>/dev/null || true
    fi
    
    # Run new container
    docker run -d \
        --name phishing-api \
        -p 8000:8000 \
        -v "$(pwd)":/workspace \
        -w /workspace \
        phishing-detection-api \
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    
    echo -e "${GREEN}✓ Container started successfully${NC}"
    echo ""
    echo "📍 API available at:"
    echo "   • http://localhost:8000"
    echo "   • http://localhost:8000/docs (Swagger UI)"
    echo ""
    echo "📋 Useful commands:"
    echo "   • View logs:    docker logs -f phishing-api"
    echo "   • Stop:         docker stop phishing-api"
    echo "   • Restart:      docker restart phishing-api"
    echo "   • Shell access: docker exec -it phishing-api bash"
}

# Function to stop the container
stop_container() {
    echo ""
    echo "======================================================================"
    echo "🛑 Stopping Container..."
    echo "======================================================================"
    docker stop phishing-api 2>/dev/null || echo "Container not running"
    docker rm phishing-api 2>/dev/null || echo "Container not found"
    echo -e "${GREEN}✓ Container stopped${NC}"
}

# Function to view logs
view_logs() {
    echo ""
    echo "======================================================================"
    echo "📋 Container Logs (Press Ctrl+C to exit)"
    echo "======================================================================"
    docker logs -f phishing-api
}

# Function to access shell
access_shell() {
    echo ""
    echo "======================================================================"
    echo "🖥️  Accessing Container Shell"
    echo "======================================================================"
    docker exec -it phishing-api bash
}

# Function to use docker-compose
use_compose() {
    echo ""
    echo "======================================================================"
    echo "🐳 Using Docker Compose..."
    echo "======================================================================"
    docker-compose up --build
}

# Main menu
show_menu() {
    echo ""
    echo "======================================================================"
    echo "Select an option:"
    echo "======================================================================"
    echo "1. Build and Run (Full Setup)"
    echo "2. Build Image Only"
    echo "3. Run Container"
    echo "4. Stop Container"
    echo "5. View Logs"
    echo "6. Access Shell"
    echo "7. Use Docker Compose"
    echo "8. Exit"
    echo "======================================================================"
}

# Check Docker first
check_docker

# If arguments provided, use them
if [ $# -gt 0 ]; then
    case $1 in
        build)
            build_image
            ;;
        run)
            run_container
            ;;
        stop)
            stop_container
            ;;
        logs)
            view_logs
            ;;
        shell)
            access_shell
            ;;
        compose)
            use_compose
            ;;
        full)
            build_image
            run_container
            ;;
        *)
            echo "Usage: $0 {build|run|stop|logs|shell|compose|full}"
            exit 1
            ;;
    esac
else
    # Interactive menu
    while true; do
        show_menu
        read -p "Enter choice [1-8]: " choice
        case $choice in
            1)
                build_image
                run_container
                ;;
            2)
                build_image
                ;;
            3)
                run_container
                ;;
            4)
                stop_container
                ;;
            5)
                view_logs
                ;;
            6)
                access_shell
                ;;
            7)
                use_compose
                ;;
            8)
                echo "Goodbye!"
                exit 0
                ;;
            *)
                echo -e "${RED}Invalid option${NC}"
                ;;
        esac
    done
fi
