# Sweep Line Algorithm for Segment Intersections

This project implements a **sweep-line algorithm** as part of a Computational Geometry homework assignment.

Given a set of \(n\) line segments in the plane, the goal is to **count the number of intersection points** between them.

---

## Problem Overview

A naïve solution checks all pairs of segments and tests whether they intersect.  
This approach has time complexity \(O(n^2)\), which becomes inefficient as the number of segments grows.

To improve performance, this project implements a **sweep-line algorithm**, which runs in  
\[
O\big((n + k)\log n\big),
\]
where \(k\) is the number of intersection points.

---

## High-Level Idea

The sweep-line algorithm uses a **vertical line** that moves from left to right across the plane.  
Events are processed in increasing order of their \(x\)-coordinates. Whenever the sweep line encounters an event, the algorithm updates its internal data structures and detects new intersections.

---

## Data Structures

The algorithm maintains two main data structures:

1. **Event Queue**  
   A priority queue (provided by the course staff) that stores:
   - segment start points,
   - segment end points,
   - intersection points.

   Events are ordered lexicographically by their \(x\)- and \(y\)-coordinates, with additional tie-breaking by event type.

2. **Sweep-Line Status**  
   An **AVL tree** that stores all segments currently intersecting the sweep line.  
   The segments are ordered by their vertical position (their \(y\)-coordinate) at the current sweep-line \(x\)-position.

---

## Algorithm Description

- When the sweep line encounters a **segment start point**, the segment is inserted into the sweep-line status.  
  The algorithm checks for intersections with its immediate neighbors in the status.

- When the sweep line encounters an **intersection point**, the intersection is counted.  
  Near the intersection point (at an infinitesimal distance), only the two intersecting segments change their relative order.  
  To handle this correctly, the algorithm removes the two segments from the sweep-line status at \(x - \varepsilon\) and reinserts them at \(x + \varepsilon\), ensuring the correct ordering after the intersection.

- When the sweep line encounters a **segment end point**, the segment is removed from the sweep-line status, and a possible new intersection between its former neighbors is checked.

---

## Key Insight

Near an intersection point, only the two intersecting segments affect the ordering of the sweep-line status.  
All other segments remain in the same relative order. This observation allows the algorithm to efficiently detect intersections without checking all pairs of segments.

---

## Complexity

- **Time Complexity:** \(O((n + k)\log n)\), where \(k\) is the number of intersections.
- **Space Complexity:** \(O(n + k)\), for storing events, active segments, and detected intersections. (Note this can be reduced to n if we only add intersection points of consecutative segments in the sweep status)

---

This implementation follows the classical Bentley–Ottmann sweep-line framework and is designed to be efficient and robust for the problem constraints.

