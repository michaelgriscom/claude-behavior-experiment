export interface Employee {
  id: string;
  name: string;
  department: string;
  /** Most recent performance rating, 1 (lowest) to 5. */
  rating: number;
  tenureYears: number;
  status: "active" | "terminated";
  protectedLeave: boolean;
}
