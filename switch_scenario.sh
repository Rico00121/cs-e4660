#!/bin/bash

# Simulator URL
SIMULATOR_URL="http://localhost:8081"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display usage
show_usage() {
    echo -e "${BLUE}=== Simulator Scenario Switcher ===${NC}"
    echo ""
    echo "Usage: $0 [scenario]"
    echo ""
    echo "Available scenarios:"
    echo -e "  ${GREEN}normal${NC}           - Switch to normal operation"
    echo -e "  ${RED}cooling-failure${NC}  - Switch to cooling failure scenario"
    echo -e "  ${YELLOW}current${NC}          - Show current scenario"
    echo ""
    echo "Examples:"
    echo "  $0 normal"
    echo "  $0 cooling-failure"
    echo "  $0 current"
}

# Function to check if simulator is running
check_simulator() {
    if ! curl -s "$SIMULATOR_URL/scenario/current" > /dev/null 2>&1; then
        echo -e "${RED}Error: Simulator is not running on $SIMULATOR_URL${NC}"
        echo "Please start the simulator first with: python simulator.py"
        exit 1
    fi
}

# Function to switch scenario
switch_scenario() {
    local scenario=$1
    echo -e "${BLUE}Switching to scenario: ${YELLOW}$scenario${NC}"
    
    response=$(curl -s "$SIMULATOR_URL/scenario/$scenario")
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Success!${NC}"
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo -e "${RED}✗ Failed to switch scenario${NC}"
        exit 1
    fi
}

# Function to show current scenario
show_current() {
    echo -e "${BLUE}Current scenario:${NC}"
    response=$(curl -s "$SIMULATOR_URL/scenario/current")
    
    if [ $? -eq 0 ]; then
        echo "$response" | python3 -m json.tool 2>/dev/null || echo "$response"
    else
        echo -e "${RED}✗ Failed to get current scenario${NC}"
        exit 1
    fi
}

# Main logic
if [ $# -eq 0 ]; then
    show_usage
    exit 0
fi

# Check if simulator is running
check_simulator

# Process command
case "$1" in
    normal)
        switch_scenario "normal"
        ;;
    cooling-failure|failure)
        switch_scenario "cooling-failure"
        ;;
    current|status)
        show_current
        ;;
    -h|--help|help)
        show_usage
        ;;
    *)
        echo -e "${RED}Error: Unknown scenario '$1'${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac

