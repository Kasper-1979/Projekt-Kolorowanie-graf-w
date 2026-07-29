# 🎨 Optymalizacja i Analiza Algorytmów Kolorowania Grafów

![optymalizacja-kolorowania-grafow](https://socialify.git.ci/Kasper-1979/optymalizacja-kolorowania-grafow/image?description=1&font=Jost&language=1&name=1&owner=1&pattern=Circuit+Board&theme=Dark)

## 📖 O projekcie
Projekt to inżynierska analiza efektywności różnych podejść do klasycznego problemu unikalnego kolorowania wierzchołków grafu (Graph Coloring Problem). 

Głównym celem analitycznym projektu było przypisanie każdemu wierzchołkowi grafu koloru w taki sposób, aby żadne dwa sąsiadujące ze sobą wierzchołki nie miały tej samej barwy, przy jednoczesnej minimalizacji liczby chromatycznej (całkowitej liczby użytych barw). Kod nie tylko implementuje rozwiązania, ale stanowi środowisko testowe do benchmarkingu – analizuje złożoność obliczeniową, czas wykonania oraz jakość wyników zwracanych przez algorytmy dokładne i heurystyczne.

## ⚙️ Zastosowane Algorytmy
W ramach weryfikacji wydajności zaimplementowano następujące podejścia:

**Algorytmy dokładne (dla grafów o mniejszej złożoności):**
*   **Brute Force** - wyczerpujące sprawdzanie wszystkich możliwych kombinacji (gwarancja optymalności kosztem czasu).
*   **Backtracking (Kolorowanie wsteczne)** - rekurencyjne przeszukiwanie drzewa decyzyjnego z nawrotami, odrzucające błędne gałęzie na wczesnym etapie.

**Algorytmy heurystyczne (Zachłanne):**
*   **LF (Largest First)** - kolorowanie wierzchołków w kolejności malejących stopni.
*   **SL (Smallest Last)** - optymalizacja kolejności na podstawie minimalnego stopnia w podgrafach.
*   **SLF/DSATUR (Degree of Saturation)** - dynamiczny dobór wierzchołków na podstawie najwyższego stopnia nasycenia kolorami sąsiadów.

## 📂 Struktura Repozytorium
Architektura projektu została podzielona zgodnie z dobrymi praktykami:

*   `/skrypty` - główny kod źródłowy (silnik generujący grafy i moduły z algorytmami).
*   `/wyniki` - dane wyjściowe i arkusze kalkulacyjne z wynikami przeprowadzonych testów wydajnościowych.
*   `/testy` - weryfikacja poprawności logiki przypisywania kolorów.
*   `/dokumentacja` - dokumentacja oraz wnioski z przeprowadzonych analiz.

## 🚀 Wymagania i Uruchomienie

Projekt wykorzystuje standardowe pakiety do modelowania danych i analizy sieci:
*   `networkx` - obsługa, strukturyzacja i generowanie grafów.
*   `matplotlib` - wizualizacja rozkładów oraz wyników wydajnościowych.

**Przykładowe wywołanie z poziomu terminala (CLI):**
Środowisko pozwala na dynamiczne generowanie grafów losowych (Erdősa-Rényiego) o zadanych parametrach. 

```bash
python skrypty/przyklad/kolorowanie_grafow_zadanie.py --wezly 15 --prawdopodobienstwo 0.4
