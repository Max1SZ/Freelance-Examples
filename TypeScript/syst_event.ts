// Event System with TypeScript - Demonstrates design patterns, type safety, and event-driven architecture

// Generic event interface
interface Event<T = any> {
  type: string;
  payload: T;
  timestamp: Date;
  source: string;
}

// Event handler type
type EventHandler<T = any> = (event: Event<T>) => void | Promise<void>;

// Subscription interface
interface Subscription {
  unsubscribe(): void;
}

// Event emitter class
class EventEmitter {
  private handlers: Map<string, Set<EventHandler>> = new Map();
  private eventHistory: Event[] = [];
  private maxHistorySize: number = 100;

  // Subscribe to an event
  on<T = any>(eventType: string, handler: EventHandler<T>): Subscription {
    if (!this.handlers.has(eventType)) {
      this.handlers.set(eventType, new Set());
    }

    this.handlers.get(eventType)!.add(handler as EventHandler);

    // Return subscription object
    return {
      unsubscribe: () => {
        this.off(eventType, handler);
      }
    };
  }

  // Subscribe to an event (fires only once)
  once<T = any>(eventType: string, handler: EventHandler<T>): Subscription {
    const wrappedHandler: EventHandler<T> = (event) => {
      handler(event);
      this.off(eventType, wrappedHandler);
    };

    return this.on(eventType, wrappedHandler);
  }

  // Unsubscribe from an event
  off<T = any>(eventType: string, handler: EventHandler<T>): void {
    const handlers = this.handlers.get(eventType);
    if (handlers) {
      handlers.delete(handler as EventHandler);
      if (handlers.size === 0) {
        this.handlers.delete(eventType);
      }
    }
  }

  // Emit an event
  async emit<T = any>(eventType: string, payload: T, source: string = 'system'): Promise<void> {
    const event: Event<T> = {
      type: eventType,
      payload,
      timestamp: new Date(),
      source
    };

    // Add to history
    this.addToHistory(event);

    // Get handlers for this event type
    const handlers = this.handlers.get(eventType);
    if (!handlers || handlers.size === 0) {
      console.log(`  No handlers for event: ${eventType}`);
      return;
    }

    console.log(` Emitting event: ${eventType} (${handlers.size} handlers)`);

    // Execute all handlers
    const promises = Array.from(handlers).map(handler => 
      Promise.resolve(handler(event))
    );

    await Promise.all(promises);
  }

  // Get event history
  getHistory(eventType?: string): Event[] {
    if (eventType) {
      return this.eventHistory.filter(e => e.type === eventType);
    }
    return [...this.eventHistory];
  }

  // Clear event history
  clearHistory(): void {
    this.eventHistory = [];
  }

  // Add event to history
  private addToHistory(event: Event): void {
    this.eventHistory.push(event);
    if (this.eventHistory.length > this.maxHistorySize) {
      this.eventHistory.shift();
    }
  }

  // Get all registered event types
  getEventTypes(): string[] {
    return Array.from(this.handlers.keys());
  }

  // Get handler count for an event
  getHandlerCount(eventType: string): number {
    return this.handlers.get(eventType)?.size || 0;
  }
}

// ===== Example Application: User Management System =====

// Event payload types
interface UserCreatedPayload {
  userId: number;
  username: string;
  email: string;
}

interface UserLoggedInPayload {
  userId: number;
  username: string;
  timestamp: Date;
  ipAddress: string;
}

interface UserUpdatedPayload {
  userId: number;
  changes: Record<string, any>;
}

interface OrderPlacedPayload {
  orderId: string;
  userId: number;
  amount: number;
  items: string[];
}

// Event type constants
const EventTypes = {
  USER_CREATED: 'user:created',
  USER_LOGGED_IN: 'user:logged-in',
  USER_UPDATED: 'user:updated',
  USER_DELETED: 'user:deleted',
  ORDER_PLACED: 'order:placed',
  ORDER_SHIPPED: 'order:shipped',
  PAYMENT_PROCESSED: 'payment:processed'
} as const;

// Logger service
class Logger {
  log(message: string, level: 'info' | 'warn' | 'error' = 'info'): void {
    const prefix = level === 'error' ? 'X' : level === 'warn' ? '!!' : '|¡|';
    console.log(`${prefix} [${new Date().toISOString()}] ${message}`);
  }
}

// Email service
class EmailService {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  async sendWelcomeEmail(email: string, username: string): Promise<void> {
    // Simulate email sending
    await this.delay(300);
    this.logger.log(` Welcome email sent to ${email} (${username})`, 'info');
  }

  async sendOrderConfirmation(email: string, orderId: string): Promise<void> {
    await this.delay(300);
    this.logger.log(` Order confirmation sent for order ${orderId}`, 'info');
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// Analytics service
class AnalyticsService {
  private logger: Logger;
  private userLogins: Map<number, number> = new Map();

  constructor(logger: Logger) {
    this.logger = logger;
  }

  trackUserCreated(userId: number, username: string): void {
    this.logger.log(` Analytics: User ${username} (${userId}) created`, 'info');
  }

  trackUserLogin(userId: number): void {
    const count = (this.userLogins.get(userId) || 0) + 1;
    this.userLogins.set(userId, count);
    this.logger.log(` Analytics: User ${userId} logged in (total: ${count})`, 'info');
  }

  trackOrderPlaced(orderId: string, amount: number): void {
    this.logger.log(` Analytics: Order ${orderId} placed ($${amount})`, 'info');
  }

  getLoginCount(userId: number): number {
    return this.userLogins.get(userId) || 0;
  }
}

// Notification service
class NotificationService {
  private logger: Logger;

  constructor(logger: Logger) {
    this.logger = logger;
  }

  async sendPushNotification(userId: number, message: string): Promise<void> {
    await this.delay(200);
    this.logger.log(` Push notification sent to user ${userId}: ${message}`, 'info');
  }

  private delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

// ===== DEMO APPLICATION =====

async function runDemo() {
  console.log(" TypeScript Event System Demo\n");
  console.log("=".repeat(70));

  // Initialize services
  const eventEmitter = new EventEmitter();
  const logger = new Logger();
  const emailService = new EmailService(logger);
  const analyticsService = new AnalyticsService(logger);
  const notificationService = new NotificationService(logger);

  console.log("\n Setting up event handlers...\n");

  // Subscribe to USER_CREATED event
  eventEmitter.on<UserCreatedPayload>(EventTypes.USER_CREATED, async (event) => {
    logger.log(`User created: ${event.payload.username}`, 'info');
    await emailService.sendWelcomeEmail(event.payload.email, event.payload.username);
    analyticsService.trackUserCreated(event.payload.userId, event.payload.username);
  });

  // Subscribe to USER_LOGGED_IN event
  eventEmitter.on<UserLoggedInPayload>(EventTypes.USER_LOGGED_IN, async (event) => {
    logger.log(`User logged in: ${event.payload.username} from ${event.payload.ipAddress}`, 'info');
    analyticsService.trackUserLogin(event.payload.userId);
    
    // Send notification for suspicious login if from new IP
    if (event.payload.ipAddress.startsWith('192.')) {
      await notificationService.sendPushNotification(
        event.payload.userId,
        'New login detected from local network'
      );
    }
  });

  // Subscribe to ORDER_PLACED event
  eventEmitter.on<OrderPlacedPayload>(EventTypes.ORDER_PLACED, async (event) => {
    logger.log(`Order placed: ${event.payload.orderId} by user ${event.payload.userId}`, 'info');
    analyticsService.trackOrderPlaced(event.payload.orderId, event.payload.amount);
    
    // Send order confirmation
    await emailService.sendOrderConfirmation('user@example.com', event.payload.orderId);
    
    // Send push notification
    await notificationService.sendPushNotification(
      event.payload.userId,
      `Order ${event.payload.orderId} confirmed!`
    );
  });

  // Subscribe to USER_UPDATED event (one-time handler)
  eventEmitter.once<UserUpdatedPayload>(EventTypes.USER_UPDATED, (event) => {
    logger.log(`User ${event.payload.userId} updated (one-time handler)`, 'info');
  });

  console.log(" Event handlers registered\n");
  console.log("=".repeat(70));

  // Emit events
  console.log("\n Simulating user actions...\n");

  // Create a user
  await eventEmitter.emit<UserCreatedPayload>(
    EventTypes.USER_CREATED,
    {
      userId: 101,
      username: 'johndoe',
      email: 'john@example.com'
    },
    'UserService'
  );

  await delay(500);

  // User logs in
  await eventEmitter.emit<UserLoggedInPayload>(
    EventTypes.USER_LOGGED_IN,
    {
      userId: 101,
      username: 'johndoe',
      timestamp: new Date(),
      ipAddress: '192.168.1.100'
    },
    'AuthService'
  );

  await delay(500);

  // User places an order
  await eventEmitter.emit<OrderPlacedPayload>(
    EventTypes.ORDER_PLACED,
    {
      orderId: 'ORD-12345',
      userId: 101,
      amount: 149.99,
      items: ['TypeScript Book', 'Mechanical Keyboard']
    },
    'OrderService'
  );

  await delay(500);

  // Update user (should trigger once handler)
  await eventEmitter.emit<UserUpdatedPayload>(
    EventTypes.USER_UPDATED,
    {
      userId: 101,
      changes: { email: 'newemail@example.com' }
    },
    'UserService'
  );

  await delay(500);

  // Update user again (once handler should not trigger)
  await eventEmitter.emit<UserUpdatedPayload>(
    EventTypes.USER_UPDATED,
    {
      userId: 101,
      changes: { username: 'john_doe' }
    },
    'UserService'
  );

  console.log("\n" + "=".repeat(70));
  console.log("\n System Statistics:\n");
  console.log(`Total event types registered: ${eventEmitter.getEventTypes().length}`);
  console.log(`Event types: ${eventEmitter.getEventTypes().join(', ')}`);
  console.log(`Total events in history: ${eventEmitter.getHistory().length}`);
  console.log(`User 101 login count: ${analyticsService.getLoginCount(101)}`);

  console.log("\n Event History:");
  eventEmitter.getHistory().forEach((event, index) => {
    console.log(`  ${index + 1}. [${event.type}] from ${event.source} at ${event.timestamp.toLocaleTimeString()}`);
  });

  console.log("\n" + "=".repeat(70));
  console.log(" Demo complete!");
}

function delay(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Run the demo
runDemo().catch(error => {
  console.error(" Error running demo:", error);
});

// To run this file:
// 1. Install TypeScript: npm install -g typescript
// 2. Compile: tsc event-system.ts
// 3. Run: node event-system.js
// OR use ts-node: npx ts-node event-system.ts