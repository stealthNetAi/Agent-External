#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Arrays to track tool status
installed_tool=()
is_available=()

# Declaring Go tools and their installation commands
declare -A gotools
gotools["amass"]="go install -v github.com/owasp-amass/amass/v4/...@master"
gotools["nuclei"]="go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest"
gotools["gau"]="go install -v github.com/lc/gau/v2/cmd/gau@latest"
gotools["gobuster"]="go install github.com/OJ/gobuster/v3@latest"
gotools["ffuf"]="go install github.com/ffuf/ffuf/v2@latest"
gotools["assetfinder"]="go get -u github.com/tomnomnom/assetfinder"
gotools["subfinder"]="go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
gotools["naabu"]="go install -v github.com/projectdiscovery/naabu/v2/cmd/naabu@latest"
gotools["waybackurls"]="go install github.com/tomnomnom/waybackurls@latest"
gotools["httpx"]="go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest"
gotools["gxss"]="go install github.com/KathanP19/Gxss@latest"
gotools["github-subdomains"]="go install github.com/gwen001/github-subdomains@latest"
gotools["gf"]="go install -v github.com/tomnomnom/gf@latest"
gotools["jaeles"]="go install github.com/jaeles-project/jaeles@latest"

# Non-Go tools
tools=(
    "git"
    "golang"
    "nmap"
    "dirb"
    "nikto"
    "whatweb"
    "sqlmap"
    "sublist3r"
    "masscan"
    "wfuzz"
    "msfconsole"
    "theharvester"
    "eyewitness"
    "shodan"
    "hydra"
    "zap-cli"
    "trufflehog"
    "cewl"
    "dnsenum"
    "sn1per"
    "aquatone"
    "paramspider"
    "corsy"
    "gitgraber"
    "findomain"
    "kiterunner"
    "smuggler"
    "lazyrecon"
    "pwnxss"
    "xsstrike"
    "linkfinder"
    "photon"
    "subjack"
    "subover"
    "wpscan"
    "joomscan"
    "droopescan"
    "cmsmap"
    "aem-hacker"
)

# Function to check for apt/apt-get support and install
function install_with_apt() {
    local tool=$1
    if command -v apt &>/dev/null; then
        sudo apt install "$tool" -y
    elif command -v apt-get &>/dev/null; then
        sudo apt-get install "$tool" -y
    else
        echo -e "${RED}Neither apt nor apt-get is available for installing $tool.${NC}"
        return 1
    fi
}

# Install non-Go tools
function install_tools() {
    for tool in "${tools[@]}"; do
        if command -v "$tool" &>/dev/null; then
         echo -e "${GREEN}$tool is already installed.${NC}"
            is_available+=("$tool")
        else
            echo -e "\n${BLUE} Installing $tool${NC}"
            if install_with_apt "$tool"; then
                installed_tool+=("$tool")
            else
                echo -e "${RED}Failed to install $tool.${NC}"
            fi
        fi
    done
}

# Install Go tools
function install_go_tools() {
    for tool in "${!gotools[@]}"; do
        if command -v "$tool" &>/dev/null; then
            echo -e "${GREEN}$tool is already installed.${NC}"
            is_available+=("$tool")
        else
           echo -e "\n${BLUE} Installing $tool${NC}"
            eval "${gotools[$tool]}" && installed_tool+=("$tool") || echo "Failed to install $tool."
        fi
    done
}

# Main execution
echo -e "${YELLOW}Starting tool installation process...${NC}"
install_tools
install_go_tools

# Print results
echo -e "${GREEN}\nTools available on the system:${NC}"
printf "%s\n" "${is_available[@]}"

echo -e "${YELLOW}\nTools installed during this run:${NC}"
printf "%s\n" "${installed_tool[@]}"

echo -e '\nexport GOPATH=$HOME/go\nexport GOBIN=$GOPATH/bin\nexport PATH=$PATH:$GOBIN' | tee -a ~/.bashrc ~/.zshrc > /dev/null
