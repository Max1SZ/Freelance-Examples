 TypeScript Projects Showcase
Demonstrating Object-Oriented Design, Type Safety & Event-Driven Architecture

This repository contains two independent TypeScript projects that highlight best practices in object-oriented programming, strong typing, modular design, and event-driven architecture.

 1. Task Manager – TypeScript OOP Example

File: task-manager.ts

 Overview

A fully typed Task Management System built with TypeScript that demonstrates:

Use of Enums, Interfaces, and Custom Types

Principles of Abstraction, Encapsulation, and Code Reusability

Filtering, statistics, and full CRUD task operations

Perfect as an example of clean and maintainable OOP in TypeScript.

* Key Features

* Create, update, filter, and delete tasks

* Automatically detect overdue tasks

* Generate global statistics by priority and status

* Flexible task filtering using FilterOptions

* Clean and structured console output

 Core Components
Component	Description
Priority & Status	Enums defining task priority and workflow status
Task	Interface describing the structure of a task
TaskManager	Main class handling all task logic
TaskStats	Interface defining aggregated statistics
 How to Run
# Compile
tsc task-manager.ts

# Run
node task-manager.js

# Or directly (no compilation needed)
npx ts-node task-manager.ts

 Example Output
Task created: TASK-1 - Implement user authentication
Task TASK-1 status updated to: in_progress

ALL TASKS:
================================================================================
ID: TASK-1
Title: Implement user authentication
Description: Add JWT-based authentication to the API
Priority: HIGH | Status: IN_PROGRESS | Due: 12/15/2024 | Tags: backend, security
Created: 11/26/2025, 1:00:00 PM
--------------------------------------------------------------------------------
...
| TASK STATISTICS:
==================================================
Total Tasks: 5
  Completed: 1
  In Progress: 1
  To Do: 3

By Priority:
  🔴 Urgent: 1
  [high] High: 1
  [mid] Medium: 2
  [low] Low: 1
==================================================

 2. Event System – Event-Driven Architecture Example

File: event-system.ts

 Overview

A type-safe event system simulating interaction between different services (users, orders, notifications, analytics, and email).

Demonstrates:

Classic Observer / Pub-Sub design pattern

Asynchronous programming using Promises and async/await

Loose coupling between modules via generic events

Subscription management, event history, and one-time handlers

* Key Features

* Fully generic and strongly typed event system

* Built-in event history tracking

* Methods on, once, off, and emit for flexible event control

* Simulated real-world services (Email, Notifications, Analytics)

* Concurrent asynchronous handlers

 Core Components
Component	Description
EventEmitter	Core class managing event subscriptions and emissions
Logger, EmailService, AnalyticsService, NotificationService	Simulated service modules responding to events
Event<T>	Generic interface defining event type, payload, and metadata
Subscription	Interface for unsubscribing from events
EventTypes	Constants defining all system event types
 How to Run
# Compile
tsc event-system.ts

# Run
node event-system.js

# Or directly:
npx ts-node event-system.ts

 Example Output
TypeScript Event System Demo
======================================================================
Setting up event handlers...

Event handlers registered
======================================================================

Simulating user actions...

|¡| [2025-11-26T16:01:00Z] User created: johndoe
|¡| [2025-11-26T16:01:00Z] Welcome email sent to john@example.com (johndoe)
|¡| [2025-11-26T16:01:00Z] Analytics: User johndoe (101) created
|¡| [2025-11-26T16:01:01Z] User logged in: johndoe from 192.168.1.100
|¡| [2025-11-26T16:01:01Z] Push notification sent to user 101: New login detected from local network
...
System Statistics:
Total event types registered: 7
User 101 login count: 1

 Technologies Used

TypeScript – Strong typing & OOP structure

Node.js – Execution environment

ts-node – Run TypeScript files directly without compiling

 What These Projects Demonstrate

 Practical application of SOLID principles
 Modular and scalable architecture
 Strong type safety and data consistency
 Professional console-based debugging and output formatting

 Run Both Projects

Install TypeScript (if you don’t have it yet):

npm install -g typescript ts-node


Clone or download this repository.

Run each demo:

npx ts-node task-manager.ts
npx ts-node event-system.ts

Author

Max1SZ
Developer with experience in TypeScript, Python, Javascript, Arduino, HTML, PHP, and SQL.
Passionate about creating structured, readable, and visually engaging software.