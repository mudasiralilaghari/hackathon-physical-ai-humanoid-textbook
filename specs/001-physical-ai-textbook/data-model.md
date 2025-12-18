# Data Model: Physical AI & Humanoid Robotics Textbook

## Entities

### Module
- **name**: String (e.g., "ROS 2", "Gazebo & Unity", "NVIDIA Isaac", "Vision-Language-Action")
- **description**: String - Brief overview of the module's purpose
- **learning_objectives**: Array of strings - Specific skills/knowledge students will gain
- **chapters**: Array of Chapter entities
- **prerequisites**: Array of strings - Knowledge required before starting
- **duration**: Number - Estimated hours to complete

### Chapter
- **id**: String (e.g., "module-1-chapter-1")
- **title**: String - Descriptive name of the chapter
- **module_id**: String - Reference to parent module
- **content**: String - Main educational content in Markdown
- **learning_objectives**: Array of strings - Specific goals for the chapter
- **examples**: Array of Example entities
- **exercises**: Array of Exercise entities
- **duration**: Number - Estimated hours to complete

### Example
- **id**: String
- **chapter_id**: String - Reference to parent chapter
- **title**: String - Brief description
- **description**: String - Detailed explanation of the example
- **code_snippet**: String - Code to demonstrate the concept
- **expected_outcome**: String - What the example should demonstrate

### Exercise
- **id**: String
- **chapter_id**: String - Reference to parent chapter
- **title**: String - Brief description
- **description**: String - Detailed instructions
- **difficulty**: String (e.g., "beginner", "intermediate", "advanced")
- **solution**: String - Suggested approach or answer
- **validation_criteria**: Array of strings - How to verify completion

### TechnologyStack
- **name**: String (e.g., "ROS 2", "Gazebo", "Unity", "NVIDIA Isaac")
- **version**: String - Recommended version
- **installation_guide**: String - Steps to set up the technology
- **compatibility**: String - Platform and system requirements
- **modules_used_in**: Array of Module entities - Which modules use this technology

## Relationships
- Module contains multiple Chapters
- Chapter contains multiple Examples and Exercises
- Module uses multiple TechnologyStack items
- Exercise belongs to one Chapter
- Example belongs to one Chapter

## Validation Rules
- Each Module must have 4-6 Chapters
- Each Chapter must have at least 1 Learning Objective
- Each Chapter must have at least 1 Example
- Each Chapter must have at least 1 Exercise
- Module duration must be between 8-12 hours
- Chapter duration must be between 1-3 hours
- Difficulty must be one of: "beginner", "intermediate", "advanced"