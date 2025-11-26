// Task Manager with TypeScript - Demonstrates interfaces, enums, and type safety

// Enums for task priority and status
enum Priority {
  LOW = "low",
  MEDIUM = "medium",
  HIGH = "high",
  URGENT = "urgent"
}

enum Status {
  TODO = "todo",
  IN_PROGRESS = "in_progress",
  COMPLETED = "completed",
  CANCELLED = "cancelled"
}

// Interface for Task object
interface Task {
  id: string;
  title: string;
  description: string;
  priority: Priority;
  status: Status;
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  tags: string[];
}

// Interface for Task statistics
interface TaskStats {
  total: number;
  completed: number;
  inProgress: number;
  todo: number;
  byPriority: Record<Priority, number>;
}

// Type for filter options
type FilterOptions = {
  status?: Status;
  priority?: Priority;
  tag?: string;
};

class TaskManager {
  private tasks: Task[] = [];
  private nextId: number = 1;

  // Create a new task
  createTask(
    title: string,
    description: string,
    priority: Priority,
    dueDate?: Date,
    tags: string[] = []
  ): Task {
    const task: Task = {
      id: `TASK-${this.nextId++}`,
      title,
      description,
      priority,
      status: Status.TODO,
      createdAt: new Date(),
      updatedAt: new Date(),
      dueDate,
      tags
    };

    this.tasks.push(task);
    console.log(` Task created: ${task.id} - ${task.title}`);
    return task;
  }

  // Update task status
  updateStatus(taskId: string, newStatus: Status): Task | null {
    const task = this.findTaskById(taskId);
    if (task) {
      task.status = newStatus;
      task.updatedAt = new Date();
      console.log(` Task ${taskId} status updated to: ${newStatus}`);
      return task;
    }
    console.log(` Task ${taskId} not found`);
    return null;
  }

  // Update task priority
  updatePriority(taskId: string, newPriority: Priority): Task | null {
    const task = this.findTaskById(taskId);
    if (task) {
      task.priority = newPriority;
      task.updatedAt = new Date();
      console.log(` Task ${taskId} priority updated to: ${newPriority}`);
      return task;
    }
    console.log(` Task ${taskId} not found`);
    return null;
  }

  // Find task by ID
  private findTaskById(taskId: string): Task | undefined {
    return this.tasks.find(task => task.id === taskId);
  }

  // Get all tasks
  getAllTasks(): Task[] {
    return [...this.tasks];
  }

  // Filter tasks based on criteria
  filterTasks(options: FilterOptions): Task[] {
    return this.tasks.filter(task => {
      if (options.status && task.status !== options.status) return false;
      if (options.priority && task.priority !== options.priority) return false;
      if (options.tag && !task.tags.includes(options.tag)) return false;
      return true;
    });
  }

  // Get tasks by status
  getTasksByStatus(status: Status): Task[] {
    return this.tasks.filter(task => task.status === status);
  }

  // Get overdue tasks
  getOverdueTasks(): Task[] {
    const now = new Date();
    return this.tasks.filter(
      task => 
        task.dueDate && 
        task.dueDate < now && 
        task.status !== Status.COMPLETED &&
        task.status !== Status.CANCELLED
    );
  }

  // Delete a task
  deleteTask(taskId: string): boolean {
    const index = this.tasks.findIndex(task => task.id === taskId);
    if (index !== -1) {
      this.tasks.splice(index, 1);
      console.log(`  Task ${taskId} deleted`);
      return true;
    }
    console.log(`X Task ${taskId} not found`);
    return false;
  }

  // Get task statistics
  getStats(): TaskStats {
    const stats: TaskStats = {
      total: this.tasks.length,
      completed: 0,
      inProgress: 0,
      todo: 0,
      byPriority: {
        [Priority.LOW]: 0,
        [Priority.MEDIUM]: 0,
        [Priority.HIGH]: 0,
        [Priority.URGENT]: 0
      }
    };

    this.tasks.forEach(task => {
      // Count by status
      switch (task.status) {
        case Status.COMPLETED:
          stats.completed++;
          break;
        case Status.IN_PROGRESS:
          stats.inProgress++;
          break;
        case Status.TODO:
          stats.todo++;
          break;
      }

      // Count by priority
      stats.byPriority[task.priority]++;
    });

    return stats;
  }

  // Display all tasks in a formatted way
  displayTasks(): void {
    console.log("\n ALL TASKS:");
    console.log("=".repeat(80));
    
    if (this.tasks.length === 0) {
      console.log("No tasks available.");
      return;
    }

    this.tasks.forEach(task => {
      const dueStr = task.dueDate ? ` | Due: ${task.dueDate.toLocaleDateString()}` : '';
      const tagsStr = task.tags.length > 0 ? ` | Tags: ${task.tags.join(', ')}` : '';
      
      console.log(`
ID: ${task.id}
Title: ${task.title}
Description: ${task.description}
Priority: ${task.priority.toUpperCase()} | Status: ${task.status}${dueStr}${tagsStr}
Created: ${task.createdAt.toLocaleString()}
${"-".repeat(80)}`);
    });
  }

  // Display statistics
  displayStats(): void {
    const stats = this.getStats();
    console.log("\n| TASK STATISTICS:");
    console.log("=".repeat(50));
    console.log(`Total Tasks: ${stats.total}`);
    console.log(`  Completed: ${stats.completed}`);
    console.log(`  In Progress: ${stats.inProgress}`);
    console.log(`  To Do: ${stats.todo}`);
    console.log("\nBy Priority:");
    console.log(`  🔴 Urgent: ${stats.byPriority[Priority.URGENT]}`);
    console.log(`  [high] High: ${stats.byPriority[Priority.HIGH]}`);
    console.log(`  [mid] Medium: ${stats.byPriority[Priority.MEDIUM]}`);
    console.log(`  [low] Low: ${stats.byPriority[Priority.LOW]}`);
    console.log("=".repeat(50));
  }
}

// ===== DEMO USAGE =====

const manager = new TaskManager();

// Create some tasks
manager.createTask(
  "Implement user authentication",
  "Add JWT-based authentication to the API",
  Priority.HIGH,
  new Date("2024-12-15"),
  ["backend", "security"]
);

manager.createTask(
  "Design landing page",
  "Create mockups for the new landing page",
  Priority.MEDIUM,
  new Date("2024-12-10"),
  ["frontend", "design"]
);

manager.createTask(
  "Fix bug in payment module",
  "Users report payment failures on checkout",
  Priority.URGENT,
  new Date("2024-12-01"),
  ["backend", "bugfix", "urgent"]
);

manager.createTask(
  "Write documentation",
  "Document the new API endpoints",
  Priority.LOW,
  undefined,
  ["documentation"]
);

manager.createTask(
  "Optimize database queries",
  "Improve performance of user dashboard queries",
  Priority.MEDIUM,
  new Date("2024-12-20"),
  ["backend", "performance"]
);

// Update some tasks
manager.updateStatus("TASK-1", Status.IN_PROGRESS);
manager.updateStatus("TASK-2", Status.COMPLETED);
manager.updatePriority("TASK-4", Priority.MEDIUM);

// Display all tasks
manager.displayTasks();

// Display statistics
manager.displayStats();

// Filter tasks
console.log("\n HIGH PRIORITY TASKS:");
const highPriorityTasks = manager.filterTasks({ priority: Priority.HIGH });
highPriorityTasks.forEach(task => console.log(`  - ${task.title} (${task.status})`));

console.log("\n IN PROGRESS TASKS:");
const inProgressTasks = manager.getTasksByStatus(Status.IN_PROGRESS);
inProgressTasks.forEach(task => console.log(`  - ${task.title}`));

console.log("\n  OVERDUE TASKS:");
const overdueTasks = manager.getOverdueTasks();
if (overdueTasks.length === 0) {
  console.log("  No overdue tasks!");
} else {
  overdueTasks.forEach(task => console.log(`  - ${task.title} (Due: ${task.dueDate?.toLocaleDateString()})`));
}

// To run this file:
// 1. Install TypeScript: npm install -g typescript
// 2. Compile: tsc task-manager.ts
// 3. Run: node task-manager.js
// OR use ts-node: npx ts-node task-manager.ts