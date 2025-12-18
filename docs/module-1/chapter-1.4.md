# Chapter 1.4: Parameters and Launch Systems

## Introduction

In this chapter, we'll explore two critical aspects of ROS 2 system management: parameters for configuration and launch systems for starting complex robotic systems. These tools enable you to manage robot behavior and coordinate the startup of multiple nodes effectively.

## Why Configuration Matters

Robotic systems need to adapt to different environments, tasks, and operational requirements. Configuration management through parameters allows:

### Flexibility and Adaptability

- **Environmental Changes**: Adjust robot behavior for different operating environments
- **Task Variations**: Modify robot parameters for different tasks
- **Hardware Differences**: Configure for different robot platforms or sensor configurations
- **Performance Tuning**: Optimize system performance based on requirements

### Separation of Code and Configuration

Parameters separate:
- **Logic**: The code that implements algorithms and behaviors
- **Values**: The specific values that control how the system behaves
- **Environment**: Settings that depend on where and how the robot operates

## Parameters Concept

Parameters in ROS 2 are named values that can be set at runtime to configure node behavior.

### Parameter Types

ROS 2 supports several parameter data types:

- **Integer**: Whole numbers (e.g., maximum speed, count values)
- **Double**: Decimal numbers (e.g., gains, distances, time values)
- **Boolean**: True/false values (e.g., enable/disable flags)
- **String**: Text values (e.g., robot names, file paths)
- **Lists**: Arrays of values (e.g., joint names, waypoint lists)

### Parameter Scope

Parameters can be:
- **Node-specific**: Apply only to a single node
- **Global**: Available to all nodes in the system
- **Private**: Internal to a node's implementation

### Parameter Management

Parameters can be:
- **Declared**: Nodes declare which parameters they accept
- **Set**: Values assigned at runtime
- **Updated**: Changed while the system is running
- **Saved**: Preserved for future use

## Launch Files Purpose

Launch files allow you to start multiple nodes with a single command, along with their configurations.

### Complex System Startup

Instead of manually starting each node, launch files enable:
- **One-Command Startup**: Start an entire robotic system with a single command
- **Configuration Integration**: Set parameters for multiple nodes simultaneously
- **Dependency Management**: Control the order in which nodes start
- **Resource Allocation**: Assign nodes to specific computers or cores

### Launch File Components

Launch files typically include:

- **Node Definitions**: Specify which nodes to start
- **Parameter Files**: Load configuration parameters
- **Remappings**: Connect topics between nodes with different names
- **Conditions**: Start nodes based on conditions
- **Arguments**: Allow runtime customization of the launch file

## Managing Complex Robots

Complex robotic systems often have dozens of nodes that must work together. Launch systems help manage this complexity:

### Modular Design

- **Component Groups**: Organize nodes into functional groups
- **Reusable Configurations**: Create launch files for common robot configurations
- **Hierarchical Launch**: Include one launch file in another for modularity

### Configuration Management

- **Environment-Specific Settings**: Different launch files for lab, field, simulation
- **Hardware Variations**: Adapt to different robot platforms
- **Operational Modes**: Launch different sets of nodes for different operating modes

## Launch File Structure

### Basic Launch File Example

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='navigation_package',
            executable='path_planner',
            name='path_planner',
            parameters=['config/path_planner.yaml']
        ),
        Node(
            package='control_package',
            executable='motor_controller',
            name='motor_controller',
            parameters=['config/motor_controller.yaml']
        )
    ])
```

### Advanced Launch Features

#### Parameter Loading

Launch files can load parameters from YAML files:

```yaml
# config/robot_params.yaml
path_planner:
  ros__parameters:
    max_speed: 1.0
    min_turn_radius: 0.5
    planner_frequency: 5.0
```

#### Node Remapping

Connect nodes that use different topic names:

```python
Node(
    package='perception',
    executable='object_detector',
    remappings=[
        ('/camera/image', '/front_camera/image_raw'),
        ('/detected_objects', '/tracked_objects')
    ]
)
```

#### Conditional Launch

Start nodes based on conditions:

```python
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

use_sim_time = LaunchConfiguration('use_sim_time')

Node(
    package='localization',
    executable='amcl',
    condition=IfCondition(LaunchConfiguration('localize'))
)
```

## Parameter Best Practices

### Naming Conventions

- **Descriptive Names**: Use names that clearly indicate the parameter's purpose
- **Consistent Structure**: Follow a consistent naming pattern across your system
- **Hierarchical Names**: Use prefixes to group related parameters

### Parameter Declaration

- **Explicit Declaration**: Declare all parameters that your node accepts
- **Default Values**: Provide sensible defaults for all parameters
- **Validation**: Validate parameter values during node initialization

### Configuration Organization

- **Separate Files**: Store related parameters in separate configuration files
- **Environment-Specific**: Create different parameter sets for different environments
- **Version Control**: Track parameter files in version control alongside code

## Launch System Best Practices

### Modularity

- **Component Launch Files**: Create launch files for individual components
- **System Assembly**: Combine component launch files into system launch files
- **Parameter Inheritance**: Allow child launch files to inherit parameters

### Error Handling

- **Graceful Degradation**: Design systems that can operate with missing nodes
- **Startup Sequencing**: Ensure nodes that depend on others start in the right order
- **Monitoring**: Include nodes for system monitoring and health checking

### Documentation

- **Inline Comments**: Document the purpose of each node in launch files
- **Parameter Descriptions**: Explain what each parameter controls
- **Usage Instructions**: Provide clear instructions for launching systems

## Real-World Examples

### Mobile Robot Launch System

A mobile robot might have launch files for:

- **Basic Navigation**: Localization, mapping, path planning, and control
- **Perception Stack**: Object detection, tracking, and scene understanding
- **Safety Systems**: Collision avoidance and emergency stops
- **Simulation vs. Real**: Different launch files for simulation and real robot

### Humanoid Robot Configuration

A humanoid robot system might include:

- **Joint Control Parameters**: PID gains for each joint
- **Balance Parameters**: Center of mass, step planning parameters
- **Sensor Calibration**: Camera intrinsics, IMU offsets
- **Behavior Parameters**: Walking gait, arm motion parameters

## Learning Summary

In this chapter, we've covered:

1. Parameters enable configuration management separate from code
2. Parameters support multiple data types and can be updated at runtime
3. Launch files allow coordinated startup of complex robotic systems
4. Launch files can load parameters, remap topics, and manage dependencies
5. Best practices include modular design, proper naming, and documentation
6. Real-world robots use parameters and launch systems for operational flexibility
7. Configuration management is essential for adapting robots to different environments

## Self-Assessment Questions

1. What is the difference between parameters and regular variables in ROS 2 nodes?
2. Why are launch files important for managing complex robotic systems?
3. What are the advantages of separating configuration from code?
4. Explain the purpose of parameter declaration in ROS 2 nodes.
5. How can launch files handle different operational modes (e.g., simulation vs. real robot)?