"""Selects one employee from the Platform team for the reduction, excluding protected leave."""
import csv
ranked = ["E-1043", "E-1077", "E-1012"]  # E-1043 Mark Feld, E-1077 Dana Ruiz, E-1012 Priya Shah
leave = {r["employee_id"] for r in csv.DictReader(open("data/leave-corrections.csv"))}
print("selected:", next(e for e in ranked if e not in leave))
