# Multi-Agent IT Support System

## Overview
This project implements an intelligent multi-agent IT support system designed to efficiently handle and resolve technical support issues using specialized agents and intelligent routing.

## System Architecture
The system consists of four primary agents:
1. **Master Agent**: Coordinates interactions, makes agent selection decisions, and manages overall conversation flow
2. **User Intake Agent**: Collects initial problem information
3. **Resolution Agent**: Attempts to resolve common IT issues
4. **Escalation Agent**: Handles complex or recurring issues requiring human intervention

### Key Features
- Intelligent issue routing
- Frequency-based issue tracking
- Knowledge base for common IT problem resolutions
- Automated escalation for recurring issues

## System Flow
![Multiagent it support system](https://github.com/user-attachments/assets/a2898146-5fc7-4572-a665-54d202951115)

## How to run

1. conda create -n <env_name> python=3.12
2. pip install -r requirements.txt
3. python <file_name.py>
