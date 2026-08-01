# 🧪 Testing & Verification

This directory contains the testing suite designed to verify the correctness, reliability, and edge-case handling of the implemented graph coloring algorithms. 

Ensuring that the fundamental rule of graph coloring is strictly met—meaning no two adjacent vertices ever share the same color—is critical for the validity of the performance benchmarks and analytical conclusions.

### 📄 Contents:
* **`graph_coloring_tests.py`** - The primary testing script containing validation logic. It checks algorithm stability, validates coloring constraints on various graph topologies, and ensures the integrity of the core computational engine (`src/main/graph_coloring.py`).

### 🚀 How to Run
To execute the test suite and verify the logic, run the following command from the root directory of the repository:

```bash
python tests/graph_coloring_tests.py
```
