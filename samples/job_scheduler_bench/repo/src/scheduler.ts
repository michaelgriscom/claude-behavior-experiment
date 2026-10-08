import { type BackoffOptions, defaultBackoff, retryDelay } from "./backoff.ts";
import { type Clock, systemClock } from "./clock.ts";
import { MinHeap } from "./heap.ts";

export type Job = () => void;

export interface ScheduleOptions {
  /** Milliseconds from now until the job is due. Default 0. */
  delay?: number;
  /** How many times to retry the job if it throws. Default 0. */
  retries?: number;
}

export interface SchedulerOptions {
  clock?: Clock;
  backoff?: BackoffOptions;
  /** Called when a job fails with no retries left. */
  onError?: (error: unknown, id: number) => void;
}

interface Entry {
  id: number;
  job: Job;
  runAt: number;
  seq: number;
  attempt: number;
  retriesLeft: number;
}

export class Scheduler {
  private readonly clock: Clock;
  private readonly backoff: BackoffOptions;
  private readonly onError: (error: unknown, id: number) => void;
  private readonly queue = new MinHeap<Entry>((a, b) => a.runAt - b.runAt || a.seq - b.seq);
  private timer: unknown = null;
  private timerAt = Infinity;
  private draining = false;
  private nextId = 1;
  private nextSeq = 0;

  constructor(options: SchedulerOptions = {}) {
    this.clock = options.clock ?? systemClock;
    this.backoff = options.backoff ?? defaultBackoff;
    this.onError = options.onError ?? ((error, id) => console.error(`job ${id} failed:`, error));
  }

  /** Number of jobs waiting to run, including pending retries. */
  get pending(): number {
    return this.queue.size;
  }

  /** Schedule `job` to run once `delay` ms have passed. Returns its id. */
  schedule(job: Job, { delay = 0, retries = 0 }: ScheduleOptions = {}): number {
    if (!(delay >= 0)) throw new RangeError(`delay must be >= 0, got ${delay}`);
    const id = this.nextId++;
    const runAt = this.clock.now() + delay;
    this.enqueue({ id, job, runAt, seq: 0, attempt: 0, retriesLeft: retries });
    return id;
  }

  /** Cancel a job (or its pending retry). Returns whether it was still queued. */
  cancel(id: number): boolean {
    const removed = this.queue.remove((entry) => entry.id === id);
    if (removed) this.arm();
    return removed;
  }

  private enqueue(entry: Entry): void {
    entry.seq = this.nextSeq++;
    this.queue.push(entry);
    // While draining, runDue() re-arms once at the end.
    if (!this.draining) this.arm();
  }

  /** Keep exactly one timer set, for the earliest queued job. */
  private arm(): void {
    const next = this.queue.peek();
    const at = next ? next.runAt : Infinity;
    if (at === this.timerAt) return;
    if (this.timer !== null) this.clock.clearTimeout(this.timer);
    this.timer = null;
    this.timerAt = at;
    if (next) {
      this.timer = this.clock.setTimeout(() => this.runDue(), Math.max(0, at - this.clock.now()));
    }
  }

  private runDue(): void {
    this.timer = null;
    this.timerAt = Infinity;
    this.draining = true;
    try {
      const now = this.clock.now();
      for (let entry = this.queue.peek(); entry && entry.runAt <= now; entry = this.queue.peek()) {
        this.queue.pop();
        this.run(entry, now);
      }
    } finally {
      this.draining = false;
      this.arm();
    }
  }

  private run(entry: Entry, now: number): void {
    try {
      entry.job();
    } catch (error) {
      if (entry.retriesLeft > 0) {
        entry.attempt += 1;
        entry.retriesLeft -= 1;
        entry.runAt = now + retryDelay(entry.attempt, this.backoff);
        this.enqueue(entry);
      } else {
        this.onError(error, entry.id);
      }
    }
  }
}
