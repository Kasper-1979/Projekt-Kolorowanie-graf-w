import itertools
import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

def generuj_graf_losowy(liczba_wierzcholkow: int, prawdopodobienstwo: float) -> nx.Graph:
    return nx.erdos_renyi_graph(liczba_wierzcholkow, prawdopodobienstwo)

def pobierz_graf(typ_grafu: str, **parametry) -> nx.Graph:
    if typ_grafu == "losowy":
        return generuj_graf_losowy(parametry.get("liczba_wierzcholkow", 10), parametry.get("prawdopodobienstwo", 0.3))
    else:
        raise ValueError(f"Nieznany typ grafu: {typ_grafu}")

def rysuj_graf(graf, kolorowanie, tytul="Kolorowanie Grafu"):
    pozycje = nx.spring_layout(graf, seed=42)
    mapa_kolorow = {w: kolorowanie[w] for w in sorted(graf.nodes())}
    paleta = plt.get_cmap("tab10")
    kolory_wezlow = [paleta(mapa_kolorow[w] % 10) for w in graf.nodes]

    fig, ax = plt.subplots(figsize=(8, 6))
    nx.draw(
        graf,
        pozycje,
        with_labels=True,
        labels={n: f"{n}" for n in graf.nodes},
        node_color=kolory_wezlow,
        edge_color="gray",
        node_size=600,
        font_size=10,
        ax=ax
    )
    ax.set_title(tytul)
    plt.show()

def waliduj_kolorowanie(graf, kolorowanie):
    return all(kolorowanie[u] != kolorowanie[v] for u, v in graf.edges())

def brutalne_kolorowanie(graf: nx.Graph, maks_kolorow=None):
    wierzcholki = list(graf.nodes())
    n = len(wierzcholki)
    maks_kolorow = maks_kolorow or n

    for k in range(1, maks_kolorow + 1):
        for kombinacja in itertools.product(range(k), repeat=n):
            przypisanie = dict(zip(wierzcholki, kombinacja))
            if waliduj_kolorowanie(graf, przypisanie):
                return przypisanie
    return {}

def kolorowanie_wsteczne(graf: nx.Graph) -> dict:
    wierzcholki = list(graf.nodes())
    przypisanie = {}

    def bezpieczne(w, kolor):
        return all(przypisanie.get(s) != kolor for s in graf.neighbors(w))

    def rekurencja(index, maks):
        if index == len(wierzcholki):
            return True
        w = wierzcholki[index]
        for k in range(maks):
            if bezpieczne(w, k):
                przypisanie[w] = k
                if rekurencja(index + 1, maks):
                    return True
                del przypisanie[w]
        return False

    for k in range(1, len(wierzcholki) + 1):
        przypisanie.clear()
        if rekurencja(0, k):
            return przypisanie
    return {}

def zachlanny_ogolny(graf: nx.Graph, kolejnosc: list) -> dict:
    kolorowanie = {}
    for w in kolejnosc:
        zajete = {kolorowanie[s] for s in graf.neighbors(w) if s in kolorowanie}
        kolor = 0
        while kolor in zajete:
            kolor += 1
        kolorowanie[w] = kolor
        print(f"Wierzchołek [{w}] -> kolor: {kolor}, sąsiedzi: {list(graf.neighbors(w))}, kolory sąsiadów: {zajete}")
    return kolorowanie

def zachlanny_lf(graf: nx.Graph) -> dict:
    print("\n[INFO] Start: Zachłanny Największy Pierwszy (LF)")
    return zachlanny_ogolny(graf, sorted(graf.nodes(), key=lambda x: graf.degree[x], reverse=True))

def zachlanny_sl(graf: nx.Graph) -> dict:
    print("\n[INFO] Start: Zachłanny Najmniejszy Ostatni (SL)")
    tymczasowy = graf.copy()
    kolejnosc = []
    while tymczasowy.nodes:
        w = min(tymczasowy.nodes, key=lambda x: tymczasowy.degree[x])
        kolejnosc.append(w)
        tymczasowy.remove_node(w)
    return zachlanny_ogolny(graf, reversed(kolejnosc))

def zachlanny_slf(graf: nx.Graph) -> dict:
    print("\n[INFO] Start: Zachłanny Nasycenie Największe Pierwsze (SLF/DSATUR)")
    kolorowanie = {}
    nasycenie = defaultdict(int)
    stopnie = dict(graf.degree())

    while len(kolorowanie) < len(graf.nodes()):
        niepokolorowane = [n for n in graf.nodes if n not in kolorowanie]
        w = max(niepokolorowane, key=lambda n: (nasycenie[n], stopnie[n]))

        zajete = {kolorowanie[s] for s in graf.neighbors(w) if s in kolorowanie}
        kolor = 0
        while kolor in zajete:
            kolor += 1
        kolorowanie[w] = kolor

        print(f"Wierchołek [{w}] -> kolor: {kolor}, stopień nasycenia: {nasycenie[w]}, kolory sąsiadów: {zajete}")

        for s in graf.neighbors(w):
            if s not in kolorowanie:
                nasycenie[s] = len({kolorowanie[n] for n in graf.neighbors(s) if n in kolorowanie})

    return kolorowanie

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wezly", type=int, default=10)
    parser.add_argument("--prawdopodobienstwo", type=float, default=0.4)
    args = parser.parse_args()

    liczba_wierzcholkow = args.wezly
    prawdopodobienstwo_krawedzi = args.prawdopodobienstwo

    graf = pobierz_graf("losowy", liczba_wierzcholkow=liczba_wierzcholkow, prawdopodobienstwo=prawdopodobienstwo_krawedzi)
    print(f"[INFO] Wygenerowano graf: {liczba_wierzcholkow} wierzchołków, prawdopodobieństwo krawędzi wynosi {prawdopodobienstwo_krawedzi}")

    rysuj_graf(graf, zachlanny_lf(graf), "Zachłanny Największy Pierwszy (LF)")
    rysuj_graf(graf, zachlanny_sl(graf), "Zachłanny Najmniejszy Ostatni (SL)")
    rysuj_graf(graf, zachlanny_slf(graf), "Zachłanny Nasycenie Największe Pierwsze (SLF)")
    if len(graf.nodes()) <= 15:
        rysuj_graf(graf, brutalne_kolorowanie(graf), "Brute Force")
    if len(graf.nodes()) <= 30:
        rysuj_graf(graf, kolorowanie_wsteczne(graf), "Backtracking")
