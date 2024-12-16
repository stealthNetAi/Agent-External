# StealthNet AI - External Penetration Testing AI Agent

The **StealthNet AI Agent** is a cutting-edge tool designed for automating external penetration testing. Built to run on Kali Linux, this AI-driven agent simplifies and enhances pentesting workflows by intelligently leveraging popular security tools.

---

## Features
- Fully automated external penetration testing powered by AI.
- Seamlessly integrates with the StealthNet platform.
- Utilizes a wide range of pre-installed pentesting tools on Kali Linux.
- Customizable with your API key for secure connectivity.

---

## Requirements
- **Operating System**: Kali Linux (required).
- **API Key**: Obtainable from the StealthNet platform (see instructions below).

---

## Installation and Setup

### Step 1: Clone the Repository
Download the project files by cloning the GitHub repository:
- git clone https://github.com/stealthNetAi/Agent-External.git
- CD into the directory

### Step 2: Install Required Tools
Run the `install_tools.sh` script to download and install all required pentesting tools:
- chmod +x install_tools.sh ./install_tools.sh
**Note**: This process may take some time depending on your network speed. Ensure all tools are properly added to your `PATH` environment variable so they are callable from any directory.

### Step 3: Verify Tool Installation
Check that the installed tools are accessible from the command line:
- nuclei --help
- nikto --help
- gobuster --help

### Step 4: Configure API Key
1. Log in to the **StealthNet AI Platform**.
2. Navigate to the **Settings** tab after creating a pentest.
3. Copy your API key.
4. Open the `stealthnet-external.py` script and paste your API key into the designated section:
   ```python
   API_KEY = "your-api-key-here"
   ```
### Step 5: Run the Agent
- python3 stealthnet-external.py

### Troubleshooting
- Ensure you are using Kali Linux, as the agent may not work on other operating systems.
- Make sure you are using python3
- Verify that all required tools are installed and callable from the terminal.
- Double-check the API key is correctly configured in stealthnet-external.py




