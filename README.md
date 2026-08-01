# 🎨 Graph Coloring Algorithms:

![Project Banner](https://socialify.git.ci/Kasper-1979/optymalizacja-kolorowania-grafow/image?description=1&font=Jost&language=1&name=1&owner=1&pattern=Circuit%20Board&theme=Dark)Optimization and Analysis

## 📖 About the Project
This project provides an engineering analysis of the efficiency of various approaches to the classic Graph Coloring Problem. 

The primary analytical goal was to assign a color to each vertex of a graph such that no two adjacent vertices share the same color, while simultaneously minimizing the chromatic number (the total number of colors used). The code serves not only as an implementation but also as a testing environment for benchmarking—analyzing computational complexity, execution time, and the quality of outputs returned by both exact and heuristic algorithms.

## ⚙️ Implemented Algorithms
The following approaches were implemented for performance verification:

**Exact Algorithms (for graphs with lower complexity):**
*   **Brute Force** - Exhaustive search of all possible combinations (guarantees optimality at the cost of execution time).
*   **Backtracking** - Recursive searching of the decision tree, eliminating invalid branches at an early stage.

**Heuristic Algorithms (Greedy approach):**
*   **LF (Largest First)** - Coloring vertices in descending order of their degrees.
*   **SL (Smallest Last)** - Optimizing the order based on the minimum degree within subgraphs.
*   **SLF / DSATUR (Degree of Saturation)** - Dynamic vertex selection based on the highest saturation degree (number of uniquely colored neighbors).

## 📂 Repository Structure
The project architecture is organized according to best practices:

*   `/src` - Main source code (graph generation engine and algorithm modules).
*   `/results` - Output data and spreadsheets containing performance test results.
*   `/tests` - Verification of the color assignment logic.
*   `/docs` - Project documentation and analytical conclusions.

## 🚀 Requirements & Execution

The project utilizes standard packages for data modeling and network analysis:
*   `networkx` - Graph manipulation, structuring, and generation.
*   `matplotlib` - Visualization of distributions and performance results.

**Example CLI Execution:**
The environment allows for the dynamic generation of random graphs (Erdős–Rényi model) with specified parameters.

```bash
python src/example/graph_coloring_task.py --nodes 15 --probability 0.4
```

**Execution Output:**
The program will generate a node layout, process it using all available methods, return performance metrics in the console, and generate bar charts comparing execution time and color selection optimality.

## 📊 Conclusions & Results
The performance tests and computational complexity analysis yielded the following conclusions:

1. Exact Algorithms (Brute Force, Backtracking): They guarantee finding the absolute minimum chromatic number, but their exponential time complexity makes them impractical for graphs with a larger number of vertices. Backtracking significantly optimizes the process compared to Brute Force by pruning invalid branches early, but it still lacks scalability for commercial-sized data.

2. Heuristic Algorithms (Greedy): These offer a drastic reduction in execution time down to fractions of a second, even for highly complex networks.

3. Heuristic Optimality: The DSATUR (SLF) algorithm demonstrated the highest efficacy among the approximation methods, consistently getting closest to the optimal chromatic number. The LF and SL algorithms, although marginally faster, are more prone to overestimating the required number of colors in graphs with high edge density.
