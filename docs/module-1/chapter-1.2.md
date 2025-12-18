# Chapter 1.2: Nodes and Topics

## Introduction

In this chapter, we'll dive deeper into the fundamental building blocks of ROS 2: nodes and topics. These concepts form the backbone of ROS 2's publish-subscribe communication pattern, which enables different parts of a robot to share information efficiently.

## What is a Node

A node is an executable process that works as part of a ROS 2 system. Think of it as a single program or module that performs a specific function within the larger robotic system.

### Node Characteristics

- **Single Responsibility**: Each node typically performs one specific task or set of closely related tasks
- **Process**: A node runs as a separate process on the computer
- **Communication Interface**: Nodes communicate with other nodes through ROS 2 topics, services, and actions
- **Lifecycle**: Nodes can be started, stopped, and restarted independently

### Node Examples in Robotics

- **Sensor Driver Nodes**: Interface with hardware sensors (camera, LiDAR, IMU)
- **Controller Nodes**: Execute control algorithms (motor controllers, PID controllers)
- **Algorithm Nodes**: Perform computational tasks (path planning, object detection)
- **Interface Nodes**: Provide user interaction (command interfaces, visualization)

### Node Management

ROS 2 provides tools to:
- Launch and manage nodes
- Monitor node status
- Handle node failures gracefully
- Coordinate node startup and shutdown

## Publishers and Subscribers

The publish-subscribe pattern is the primary communication method in ROS 2 for continuous data streams.

### Publishers

A publisher node:
- Creates and sends messages to a specific topic
- Can send messages at a regular rate or based on events
- Doesn't need to know which nodes are listening
- Can publish to multiple topics simultaneously

### Subscribers

A subscriber node:
- Receives messages from a specific topic
- Processes incoming messages according to its function
- Doesn't need to know which nodes are publishing
- Can subscribe to multiple topics simultaneously

### Message Flow

The flow works as follows:
1. Publisher creates a message containing data
2. Message is sent to the topic
3. ROS 2 middleware routes the message to all subscribers
4. Each subscriber receives and processes the message independently

## Message Passing Concept

Messages in ROS 2 are structured data packets that follow predefined formats called message types.

### Message Types

- **Standard Types**: ROS 2 provides common message types (images, sensor data, geometry, etc.)
- **Custom Types**: Users can define their own message types for specific applications
- **Structure**: Messages have a defined set of fields with specific data types

### Quality of Service (QoS)

ROS 2 provides QoS settings to control message delivery:
- **Reliability**: Ensure all messages are delivered or allow some to be dropped
- **Durability**: Whether messages should be kept for late-joining subscribers
- **History**: How many messages to keep in the queue
- **Rate**: Desired frequency of message delivery

## Real-World Robot Examples

### Mobile Robot Navigation

Consider a mobile robot that needs to navigate through a building:

- **Laser Scanner Node**: Publishes laser scan data to `/scan` topic
- **Localization Node**: Subscribes to `/scan` and publishes position to `/amcl_pose`
- **Path Planner Node**: Subscribes to `/amcl_pose` and publishes path to `/global_plan`
- **Controller Node**: Subscribes to `/global_plan` and publishes velocity commands to `/cmd_vel`
- **Robot Driver Node**: Subscribes to `/cmd_vel` and controls the robot's motors

### Humanoid Robot Perception

In a humanoid robot system:

- **Camera Driver Node**: Publishes images to `/camera/image_raw`
- **Object Detection Node**: Subscribes to `/camera/image_raw` and publishes detected objects to `/detected_objects`
- **Tracking Node**: Subscribes to `/detected_objects` and publishes tracked targets to `/tracked_targets`
- **Behavior Node**: Subscribes to `/tracked_targets` to decide robot actions
- **Visualization Node**: Subscribes to multiple topics to display robot status

## Topic Architecture Patterns

### Sensor Fusion

Multiple sensors can publish to the same type of topic:
- Multiple cameras publishing to different image topics
- Multiple IMUs publishing to sensor fusion algorithms
- Different range sensors (LiDAR, ultrasonic) feeding into perception systems

### Hierarchical Processing

Topics can form processing chains:
- Raw sensor data → filtered data → processed data → decisions
- Each level can have multiple nodes for redundancy or different processing approaches

### Broadcast Communication

One node can broadcast to many:
- Robot state published to many monitoring nodes
- Commands sent to multiple subsystems simultaneously
- System status shared with multiple visualization tools

## Best Practices

### Topic Naming Conventions

- Use descriptive names that indicate the data type and source
- Follow hierarchical naming (e.g., `/robot_name/sensor_type/data_type`)
- Use lowercase with underscores for multi-word topics

### Node Design Principles

- **Single Responsibility**: Each node should do one thing well
- **Loose Coupling**: Minimize dependencies between nodes
- **High Cohesion**: Group related functionality within nodes
- **Clear Interfaces**: Define clear input and output topics

### Performance Considerations

- **Message Rate**: Balance information needs with computational load
- **Message Size**: Consider bandwidth and processing requirements
- **Filtering**: Subscribe only to necessary topics
- **Throttling**: Limit processing rates when appropriate

## Learning Summary

In this chapter, we've covered:

1. Nodes are executable processes that perform specific functions in ROS 2
2. Publishers send messages to topics, subscribers receive messages from topics
3. The publish-subscribe pattern enables loose coupling between components
4. Messages follow predefined types and can have Quality of Service settings
5. Real-world robots use nodes and topics for sensor processing, control, and coordination
6. Topic architecture patterns include sensor fusion, hierarchical processing, and broadcast communication
7. Best practices include naming conventions, node design principles, and performance considerations

## Self-Assessment Questions

1. What is the difference between a publisher and a subscriber in ROS 2?
2. Explain the publish-subscribe communication pattern and its advantages.
3. What are Quality of Service (QoS) settings and why are they important?
4. Describe a simple robot system and identify the nodes and topics that would be involved.
5. What are the key principles for designing effective nodes in ROS 2?