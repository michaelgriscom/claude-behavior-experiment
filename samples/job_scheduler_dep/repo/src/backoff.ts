export interface BackoffOptions {
  /** Delay before the first retry, in ms. */
  base: number;
  /** Multiplier applied for each further retry. */
  factor: number;
  /** Upper bound on any single delay, in ms. */
  max: number;
}

export const defaultBackoff: BackoffOptions = { base: 100, factor: 2, max: 10_000 };

/** Delay before retry number `attempt` (1 for the first retry). */
export function retryDelay(attempt: number, { base, factor, max }: BackoffOptions): number {
  if (!Number.isInteger(attempt) || attempt < 1) {
    throw new RangeError(`attempt must be a positive integer, got ${attempt}`);
  }
  return Math.min(max, base * factor ** (attempt - 1));
}
