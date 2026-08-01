# ⚙️ Core Logic & Algorithms

This directory serves as the computational engine of the project. It contains the primary implementations of the graph coloring algorithms, strictly isolated from execution scripts and testing environments to adhere to the principles of modularity and Clean Architecture.

### 📄 Contents:

* **`graph_coloring.py`** - The main module containing the implementation of all evaluated approaches:
  * **Exact Algorithms:** Brute Force, Backtracking.
  * **Heuristic Algorithms:** LF (Largest First), SL (Smallest Last), SLF / DSATUR (Degree of Saturation).
  * **Utility Functions:** Methods for graph generation, degree calculation, and performance metric collection.

> **Architecture Note:** This module is designed to be imported and utilized by external scripts (like those in `src/example` or `tests`), rather than being executed directly.
