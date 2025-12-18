---
sidebar_position: 2
---

# Setup Guide

Before starting with the Physical AI & Humanoid Robotics textbook, you'll need to set up your development environment with the necessary tools and frameworks.

## Prerequisites

- Python 3.8+ installed on your system
- Basic understanding of Python programming concepts
- Git version control system
- Node.js (for Docusaurus development)
- A GitHub account for accessing the repository

## Installing Required Software

### Python Environment

First, ensure you have Python 3.8 or higher installed:

```bash
python --version
# or
python3 --version
```

If Python is not installed or you have an older version, download it from [python.org](https://www.python.org/downloads/).

### Git

Install Git if you don't have it already:
- On Windows: Download from [git-scm.com](https://git-scm.com/)
- On macOS: Install via Homebrew with `brew install git`
- On Linux: Use your package manager (e.g., `sudo apt install git`)

### Node.js

Install Node.js (version 18 or higher) from [nodejs.org](https://nodejs.org/) or via a package manager like nvm.

## Setting Up the Development Environment

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Install Node.js Dependencies

```bash
npm install
```

This command installs all the required dependencies for the Docusaurus documentation platform.

### 3. Install Docusaurus CLI (Optional but Recommended)

```bash
npm install -g @docusaurus/cli
```

### 4. Start the Local Development Server

```bash
npm start
```

This command starts a local development server and opens the textbook in your browser at `http://localhost:3000`.

## Module-Specific Setup

Each module in this textbook introduces different technologies and frameworks. The setup instructions for each will be provided in the respective module introductions:

- **Module 1 (ROS 2)**: Instructions for installing and configuring ROS 2
- **Module 2 (Gazebo & Unity)**: Setup for simulation environments
- **Module 3 (NVIDIA Isaac)**: Installation of NVIDIA Isaac tools
- **Module 4 (VLA)**: Configuration for Vision-Language-Action systems

## Troubleshooting

### Common Issues

1. **Node.js Version**: Ensure you're using Node.js version 18 or higher:
   ```bash
   node --version
   ```

2. **Permission Errors**: If you encounter permission errors during installation, try running the command with appropriate permissions or use a Node.js version manager.

3. **Port Already in Use**: If port 3000 is already in use, Docusaurus will automatically try the next available port.

### Getting Help

- Check the GitHub repository for open issues
- Submit a new issue for problems not covered in documentation
- Join the community discussions for additional support

## Next Steps

After completing the setup, proceed to Module 1 to begin your journey into Physical AI and Humanoid Robotics.