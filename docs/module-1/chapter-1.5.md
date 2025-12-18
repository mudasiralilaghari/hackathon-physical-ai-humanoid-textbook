# Chapter 1.5: Debugging and Monitoring ROS 2

## Introduction

In this final chapter of Module 1, we'll explore the essential tools and techniques for debugging and monitoring ROS 2 systems. As robotic systems become more complex, the ability to understand system behavior, identify problems, and verify correct operation becomes critical for successful deployment.

## Common Problems in ROS 2 Systems

Working with ROS 2 systems can present various challenges that require debugging:

### Communication Issues

- **Topic Connection Problems**: Publishers and subscribers not connecting properly
- **Message Rate Issues**: Too fast or too slow message publishing
- **Message Content Problems**: Incorrect data types or malformed messages
- **Network Issues**: Problems with distributed systems across multiple computers

### Performance Problems

- **Timing Issues**: Real-time constraints not being met
- **Resource Usage**: High CPU or memory consumption
- **Communication Bottlenecks**: System slowed by message passing
- **Synchronization Problems**: Components not operating in the expected sequence

### Behavioral Issues

- **Incorrect Logic**: Algorithms producing unexpected results
- **Parameter Problems**: Wrong parameter values causing poor performance
- **State Management**: Components in unexpected states
- **Integration Issues**: Multiple components not working together as expected

## Logging

Logging is the practice of recording system events and states for later analysis.

### Log Levels

ROS 2 supports different log levels for different types of information:

- **DEBUG**: Detailed information for diagnosing problems during development
- **INFO**: General information about system operation
- **WARN**: Warning messages about potential issues
- **ERROR**: Error conditions that don't stop system operation
- **FATAL**: Critical errors that require system shutdown

### Effective Logging Practices

#### Be Descriptive

```cpp
// Good logging
RCLCPP_INFO(this->get_logger(), "Received goal: position=(%f, %f), orientation=%f",
            goal.x, goal.y, goal.theta);

// Less helpful
RCLCPP_INFO(this->get_logger(), "Got goal");
```

#### Include Context

- **Node Information**: Which node generated the log
- **Timestamps**: When the event occurred
- **Parameter Values**: Important values that affect behavior
- **State Information**: Current state of the system

#### Avoid Excessive Logging

- **Performance Impact**: Too much logging can slow the system
- **Signal-to-Noise Ratio**: Too many logs make important issues hard to find
- **Storage Considerations**: Large log files consume disk space

### Log Management

- **Log Rotation**: Automatically create new log files to manage size
- **Log Filtering**: Focus on relevant information during analysis
- **Remote Logging**: Collect logs from distributed systems

## Visualization Concepts

Visualization tools help you understand system behavior by displaying information graphically.

### RViz (ROS Visualization)

RViz is the standard visualization tool for ROS 2:

- **Topic Display**: Show sensor data like laser scans, images, and point clouds
- **Robot Models**: Display robot URDF models in 3D
- **Paths and Trajectories**: Visualize planned and executed paths
- **Markers**: Display custom visualization elements
- **Coordinate Frames**: Show TF (transform) relationships

### Common Visualization Types

#### Sensor Data Visualization

- **Laser Scans**: Show obstacles and free space
- **Camera Images**: Display what the robot sees
- **Point Clouds**: 3D representation of the environment
- **Range Sensors**: Show sensor coverage areas

#### State Visualization

- **Robot Position**: Show current location and orientation
- **Path Planning**: Display planned and executed paths
- **System Status**: Indicate operational state of different components
- **Safety Zones**: Show areas where robot should not go

## System Introspection

System introspection tools allow you to examine the internal state of your ROS 2 system.

### Command-Line Tools

#### ros2 node

- `ros2 node list`: Show all active nodes
- `ros2 node info <node_name>`: Show detailed information about a specific node
- `ros2 node ping <node_name>`: Test connectivity to a node

#### ros2 topic

- `ros2 topic list`: Show all active topics
- `ros2 topic echo <topic_name>`: Display messages on a topic in real-time
- `ros2 topic info <topic_name>`: Show information about topic publishers/subscribers
- `ros2 topic hz <topic_name>`: Measure message publication rate

#### ros2 service

- `ros2 service list`: Show all available services
- `ros2 service call <service_name>`: Call a service with specific parameters

#### ros2 action

- `ros2 action list`: Show all available actions
- `ros2 action info <action_name>`: Show information about an action server/client

#### ros2 param

- `ros2 param list`: Show parameters for a node
- `ros2 param get <node_name> <param_name>`: Get parameter value
- `ros2 param set <node_name> <param_name> <value>`: Set parameter value

### Graphical Tools

#### rqt

rqt is a framework for ROS GUI tools with many plugins:

- **rqt_graph**: Show node and topic connections visually
- **rqt_console**: Display and filter log messages
- **rqt_plot**: Plot numeric values over time
- **rqt_bag**: View and play back recorded data

#### ros2doctor

A diagnostic tool that checks the health of your ROS 2 system:
- **ros2 doctor**: Analyze system configuration and connectivity
- **ros2 doctor --report**: Generate detailed system report

## Debugging Strategies

### Systematic Approach

1. **Reproduce the Problem**: Ensure you can consistently reproduce the issue
2. **Isolate the Component**: Determine which node or subsystem is causing the problem
3. **Check Communication**: Verify that nodes are properly connected
4. **Examine Parameters**: Check that all parameters have correct values
5. **Review Logs**: Look for error messages or warnings
6. **Test Incrementally**: Add components back one by one to identify the issue

### Common Debugging Patterns

#### Communication Debugging

```bash
# Check if nodes are running
ros2 node list

# Check topic connections
ros2 topic info /my_topic

# Monitor messages in real-time
ros2 topic echo /my_topic
```

#### Parameter Verification

```bash
# Check parameter values
ros2 param list /my_node
ros2 param get /my_node my_parameter

# Update parameters at runtime
ros2 param set /my_node my_parameter new_value
```

#### Performance Monitoring

```bash
# Monitor CPU usage
htop

# Check message rates
ros2 topic hz /my_topic

# Monitor system resources
ros2 doctor
```

## Monitoring Best Practices

### Proactive Monitoring

- **Health Checks**: Regularly verify system operation
- **Performance Metrics**: Monitor CPU, memory, and communication performance
- **Safety Checks**: Ensure safety systems are operational
- **Log Analysis**: Regular review of system logs

### Dashboard Creation

- **Key Metrics**: Display critical system parameters
- **Status Indicators**: Show operational status of key components
- **Alert Systems**: Generate warnings when parameters exceed thresholds
- **Historical Data**: Track performance over time

### Automated Testing

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **Regression Tests**: Ensure new changes don't break existing functionality
- **Continuous Integration**: Automated testing of system changes

## Learning Summary

In this chapter, we've covered:

1. Common problems in ROS 2 systems include communication, performance, and behavioral issues
2. Logging provides information about system operation at different severity levels
3. Visualization tools like RViz help understand system behavior graphically
4. System introspection tools allow examination of node, topic, and parameter states
5. Debugging strategies involve systematic problem isolation and verification
6. Monitoring best practices include proactive checks and automated testing
7. Effective debugging requires both command-line and graphical tools

## Self-Assessment Questions

1. What are the different log levels in ROS 2 and when should each be used?
2. How can you use ros2 topic echo to debug communication issues?
3. What is the purpose of rqt_graph and how does it help with debugging?
4. Explain the systematic approach to debugging ROS 2 systems.
5. What are the advantages of proactive monitoring compared to reactive debugging?