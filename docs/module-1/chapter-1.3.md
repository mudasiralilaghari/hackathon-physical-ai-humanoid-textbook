# Chapter 1.3: Services and Actions

## Introduction

In this chapter, we'll explore two other fundamental communication patterns in ROS 2: services and actions. While topics provide asynchronous, continuous communication, services and actions enable synchronous requests and long-running tasks with feedback, respectively. Understanding when to use each pattern is crucial for effective robotic system design.

## Request-Response vs Long-Running Actions

The key difference between services and actions lies in their duration and communication patterns:

### Services: Immediate Request-Response

Services are designed for operations that:
- Complete relatively quickly
- Return a result immediately upon completion
- Don't need to provide feedback during execution
- Follow a simple request-response pattern

### Actions: Long-Running Operations with Feedback

Actions are designed for operations that:
- Take significant time to complete
- Benefit from providing feedback during execution
- May need to be canceled during execution
- Require more complex goal-result-feedback communication

## When to Use Services

Services are appropriate for tasks that fit the following criteria:

### Query-Based Operations

- **Information Requests**: Asking for the current state of the robot
- **Simple Computations**: Calculating a path between two points
- **Configuration Queries**: Getting current parameter values
- **Status Checks**: Checking if a subsystem is ready

### Example Service Interactions

```
Client: "What is your current position?"
Server: "I am at coordinates (2.5, 3.0, 0.0)"
```

```
Client: "Plan a path from A to B"
Server: "Here is the path: [waypoints...]"
```

### Service Characteristics

- **Synchronous**: Client waits for the response
- **One Request, One Response**: Simple exchange pattern
- **Fast Execution**: Should complete quickly (typically milliseconds to seconds)
- **No Feedback**: No status updates during processing

## When to Use Actions

Actions are appropriate for tasks that are:

### Long-Running Operations

- **Navigation**: Moving to a distant location
- **Manipulation**: Grasping an object or performing complex tasks
- **Calibration**: Running lengthy sensor calibration procedures
- **Learning**: Training or adaptation processes

### Operations Requiring Feedback

- **Progress Monitoring**: Wanting to know how far along a task is
- **Adjustment**: Needing to modify parameters during execution
- **User Interaction**: Allowing user input during execution

### Example Action Interactions

```
Client: "Move to location (5, 5)"
Server: "Starting navigation" → "50% complete" → "Arrived at destination"
```

```
Client: "Grasp the red cup"
Server: "Approaching cup" → "Grasping" → "Lifted cup successfully"
```

### Action Characteristics

- **Asynchronous**: Client doesn't block waiting for completion
- **Goal-Result-Feedback**: Complex three-part communication
- **Cancel Capability**: Actions can be interrupted
- **Progress Updates**: Continuous feedback during execution

## Examples in Robotics

### Service Examples

#### Get Robot State Service

A service that returns the current state of the robot:

- **Request**: No specific parameters needed
- **Response**: Robot's current position, battery level, system status
- **Use Case**: A user interface requesting current robot status

#### Plan Path Service

A service that calculates a path between two points:

- **Request**: Start coordinates and goal coordinates
- **Response**: Sequence of waypoints forming a path
- **Use Case**: Path planning when the robot needs to navigate

#### Transform Service

A service that provides coordinate transformations:

- **Request**: Source frame, target frame, timestamp
- **Response**: Transformation matrix between frames
- **Use Case**: Converting coordinates between different reference frames

### Action Examples

#### Navigation Action

An action for moving the robot to a goal location:

- **Goal**: Target pose (position and orientation)
- **Feedback**: Current progress, distance remaining, estimated time
- **Result**: Success/failure status, final pose
- **Use Case**: Autonomous navigation to a specified location

#### Manipulation Action

An action for grasping and moving objects:

- **Goal**: Object to grasp, destination location
- **Feedback**: Current phase (approaching, grasping, lifting, moving)
- **Result**: Success/failure status, final object location
- **Use Case**: Object manipulation tasks

#### Calibration Action

An action for calibrating sensors:

- **Goal**: Calibration parameters and targets
- **Feedback**: Calibration progress, intermediate results
- **Result**: Calibration success status, new parameters
- **Use Case**: Sensor calibration procedures

## Service Architecture

### Service Client and Server

- **Service Client**: Node that sends requests and receives responses
- **Service Server**: Node that receives requests and sends responses
- **Service Interface**: Defines the request and response message types

### Service Communication Flow

1. Service server advertises the service
2. Service client calls the service with a request
3. Service server processes the request
4. Service server sends the response back to the client

### Service Reliability

- **Blocking Call**: Client waits for response (synchronous)
- **Timeout**: Client can specify maximum wait time
- **Error Handling**: Server can return error codes in responses

## Action Architecture

### Action Client and Server

- **Action Client**: Node that sends goals and receives feedback/results
- **Action Server**: Node that processes goals and sends feedback/results
- **Action Interface**: Defines goal, feedback, and result message types

### Action Communication Flow

1. Action server advertises the action
2. Action client sends a goal to the server
3. Action server sends feedback messages during execution
4. Action server sends the final result when complete
5. Action client can cancel the goal during execution

### Action States

Actions can be in various states:
- **Pending**: Goal received but not yet started
- **Active**: Goal is being processed
- **Succeeded**: Goal completed successfully
- **Aborted**: Goal failed to complete
- **Canceled**: Goal was canceled by client

## Choosing Between Services and Actions

### Use Services When:

- The operation completes quickly (under a few seconds)
- You need an immediate response
- The operation doesn't require feedback during execution
- The operation is idempotent (same result regardless of timing)

### Use Actions When:

- The operation takes significant time (seconds to minutes)
- You need feedback during execution
- The operation might need to be canceled
- The operation involves multiple phases with different statuses

### Hybrid Approaches

Sometimes, a system might use both patterns:
- A service to initiate a quick check before starting a long action
- A service to query the status of ongoing actions
- A service to configure parameters used by actions

## Learning Summary

In this chapter, we've covered:

1. Services provide synchronous request-response communication for quick operations
2. Actions provide asynchronous goal-result-feedback communication for long-running tasks
3. Services are appropriate for queries and quick computations
4. Actions are appropriate for navigation, manipulation, and other long-running operations
5. Services block the client until completion, while actions run asynchronously
6. Actions can be canceled and provide feedback during execution
7. Choosing between services and actions depends on duration and feedback requirements

## Self-Assessment Questions

1. What is the main difference between services and actions in ROS 2?
2. When would you use a service instead of a topic for communication?
3. What are the three components of action communication?
4. Provide an example of a robotic task that would be better implemented as an action rather than a service.
5. Explain the different states an action can be in during its lifecycle.