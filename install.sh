#!/bin/bash
#
# Memento Plugin Installer
# "I have to believe in a world outside my own mind."
#

set -e

PLUGIN_DIR="$HOME/.claude/plugins/memento"
REPO_URL="https://github.com/oezguercelebi/memento-plugin.git"

echo ""
echo "  MEMENTO — Context Simulator for Claude Code"
echo "  ============================================"
echo ""

# Check for git
if ! command -v git &> /dev/null; then
    echo "Error: git is required but not installed."
    exit 1
fi

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "Error: python3 is required but not installed."
    exit 1
fi

# Create plugins directory
mkdir -p "$HOME/.claude/plugins"

# Install or update
if [ -d "$PLUGIN_DIR" ]; then
    echo "Updating existing installation..."
    cd "$PLUGIN_DIR"
    git pull --quiet origin main
    echo "Updated to latest version."
else
    echo "Installing Memento plugin..."
    git clone --quiet "$REPO_URL" "$PLUGIN_DIR"
    echo "Installed to $PLUGIN_DIR"
fi

# Check for tiktoken
echo ""
if python3 -c "import tiktoken" 2>/dev/null; then
    echo "tiktoken: installed (accurate token counting)"
else
    echo "tiktoken: not installed (using estimation)"
    echo ""
    read -p "Install tiktoken for accurate counts? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pip install tiktoken
        echo "tiktoken installed."
    fi
fi

echo ""
echo "Installation complete!"
echo ""
echo "Restart Claude Code, then try:"
echo "  /memento"
echo ""
echo "\"Don't believe his lies.\" — But believe your token counter."
echo ""
