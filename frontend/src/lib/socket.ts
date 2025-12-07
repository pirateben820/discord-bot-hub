/**
 * Socket.IO client for real-time updates
 */
import { io, Socket } from 'socket.io-client';
import { config } from '../config';

class SocketService {
  private socket: Socket | null = null;
  private listeners: Map<string, Set<Function>> = new Map();

  connect() {
    if (this.socket?.connected) return;

    this.socket = io(config.socketUrl, {
      transports: ['websocket', 'polling'],
      autoConnect: true,
    });

    this.socket.on('connect', () => {
      console.log('Socket connected:', this.socket?.id);
    });

    this.socket.on('disconnect', () => {
      console.log('Socket disconnected');
    });

    this.socket.on('connection_established', (data) => {
      console.log('Connection established:', data);
    });

    // Set up event forwarding
    this.socket.onAny((event, ...args) => {
      const handlers = this.listeners.get(event);
      if (handlers) {
        handlers.forEach((handler) => handler(...args));
      }
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  on(event: string, callback: Function) {
    if (!this.listeners.has(event)) {
      this.listeners.set(event, new Set());
    }
    this.listeners.get(event)!.add(callback);
  }

  off(event: string, callback: Function) {
    const handlers = this.listeners.get(event);
    if (handlers) {
      handlers.delete(callback);
    }
  }

  emit(event: string, data?: any) {
    if (this.socket?.connected) {
      this.socket.emit(event, data);
    }
  }

  ping() {
    this.emit('ping', { timestamp: Date.now() });
  }
}

export const socketService = new SocketService();

