export type TimerId = number;

export interface FakeClock {
  now(): number;
  setTimeout<A extends unknown[]>(callback: (...args: A) => void, ms?: number, ...args: A): TimerId;
  clearTimeout(id: TimerId | undefined): void;
  setInterval<A extends unknown[]>(callback: (...args: A) => void, ms?: number, ...args: A): TimerId;
  clearInterval(id: TimerId | undefined): void;
  tick(ms: number): number;
  next(): number;
  runAll(): number;
  countTimers(): number;
  reset(): void;
}

export interface ClockOptions {
  now?: number;
}

export function createClock(options?: ClockOptions): FakeClock;
