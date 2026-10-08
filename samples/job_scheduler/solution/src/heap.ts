/** Binary min-heap ordered by `compare` (negative: a comes first). */
export class MinHeap<T> {
  private readonly items: T[] = [];
  private readonly compare: (a: T, b: T) => number;

  constructor(compare: (a: T, b: T) => number) {
    this.compare = compare;
  }

  get size(): number {
    return this.items.length;
  }

  peek(): T | undefined {
    return this.items[0];
  }

  push(item: T): void {
    this.items.push(item);
    this.siftUp(this.items.length - 1);
  }

  pop(): T | undefined {
    if (this.items.length === 0) return undefined;
    const top = this.items[0];
    const last = this.items.pop()!;
    if (this.items.length > 0) {
      this.items[0] = last;
      this.siftDown(0);
    }
    return top;
  }

  /** Remove the first item matching `predicate`. Returns whether one was found. */
  remove(predicate: (item: T) => boolean): boolean {
    const index = this.items.findIndex(predicate);
    if (index === -1) return false;
    const last = this.items.pop()!;
    if (index < this.items.length) {
      this.items[index] = last;
      this.siftDown(index);
      this.siftUp(index);
    }
    return true;
  }

  private siftUp(index: number): void {
    while (index > 0) {
      const parent = (index - 1) >> 1;
      if (this.compare(this.items[index], this.items[parent]) >= 0) return;
      this.swap(index, parent);
      index = parent;
    }
  }

  private siftDown(index: number): void {
    const n = this.items.length;
    for (;;) {
      const left = 2 * index + 1;
      const right = left + 1;
      let smallest = index;
      if (left < n && this.compare(this.items[left], this.items[smallest]) < 0) smallest = left;
      if (right < n && this.compare(this.items[right], this.items[smallest]) < 0) smallest = right;
      if (smallest === index) return;
      this.swap(index, smallest);
      index = smallest;
    }
  }

  private swap(i: number, j: number): void {
    [this.items[i], this.items[j]] = [this.items[j], this.items[i]];
  }
}
