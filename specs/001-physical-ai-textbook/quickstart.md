# Quickstart Guide: Physical AI & Humanoid Robotics Textbook

## Prerequisites

Before starting with the Physical AI & Humanoid Robotics textbook, ensure you have:

- Python 3.8+ installed on your system
- Basic understanding of Python programming concepts
- Git version control system
- Node.js (for Docusaurus development)
- A GitHub account for accessing the repository

## Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/your-org/physical-ai-textbook.git
cd physical-ai-textbook
```

### 2. Set Up the Development Environment
```bash
# Install Node.js dependencies
npm install

# Install Docusaurus CLI globally (if not already installed)
npm install -g @docusaurus/cli
```

### 3. Start the Local Development Server
```bash
npm start
```

This command starts a local development server and opens the textbook in your browser at `http://localhost:3000`.

### 4. Navigate the Textbook Structure
The textbook is organized into 4 core modules:

1. **Module 1**: ROS 2 (Robotic Nervous System)
2. **Module 2**: Gazebo & Unity (Digital Twin)
3. **Module 3**: NVIDIA Isaac (AI-Robot Brain)
4. **Module 4**: Vision-Language-Action (VLA)

Each module contains 5 chapters with practical examples and exercises.

## Contributing to the Textbook

### Adding New Content
1. Create a new Markdown file in the appropriate module directory
2. Follow the existing chapter template structure
3. Include learning objectives, content, examples, and exercises
4. Add links to the sidebar in `sidebars.js`

### Running the Build Process
```bash
# Build the static files
npm run build

# Serve the built files locally
npm run serve
```

### Deployment
The textbook is automatically deployed to GitHub Pages when changes are pushed to the main branch.

## Textbook Navigation

### For Students
1. Start with Module 1 if you're new to robotics
2. Complete each chapter sequentially for best learning outcomes
3. Follow the practical examples in each chapter
4. Complete the exercises to reinforce your learning

### For Educators
1. Use the modular structure to customize course content
2. Each module can be taught independently
3. Exercises can be used for assignments or in-class activities
4. Examples provide practical implementation guidance

## Troubleshooting

### Common Issues
- **Page not loading**: Ensure you're running `npm start` and accessing the correct URL
- **Links not working**: Check that all internal links use Docusaurus's link syntax
- **Build errors**: Verify all Markdown files follow proper syntax

### Getting Help
- Check the GitHub repository for open issues
- Submit a new issue for problems not covered in documentation
- Join the community discussions for additional support

## Next Steps

1. Begin with [Module 1: ROS 2](./docs/textbook/module-1-ros2/index.md) if you're starting from the beginning
2. Review the [setup guide](./docs/setup-guide.md) for detailed environment configuration
3. Explore the [exercises section](./docs/textbook/exercises/) for additional practice