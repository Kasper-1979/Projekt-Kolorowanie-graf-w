import itertools
import networkx as nx
import random
import matplotlib.pyplot as plt
from collections import defaultdict
import argparse

# implementacja generatora grafów :
def generuj_graf_losowy(liczba_wierzcholkow: int, prawdopodobienstwo: float) -> nx.Graph:
    return nx.erdos_renyi_graph(liczba_wierzcholkow, prawdopodobienstwo)

def pobierz_graf(typ_grafu: str, **parametry) -> nx.Graph:
    if typ_grafu == "losowy":
        return generuj_graf_losowy(parametry.get("liczba_wierzcholkow", 10), parametry.get("prawdopodobienstwo", 0.3))
    else:
        raise ValueError(f"Nieznany typ grafu: {typ_grafu}")

# Implementacja wizualizacji grafów :
def rysuj_graf(graf, kolorowanie, tytul="Kolorowanie Grafu"):
    pozycje = nx.spring_layout(graf, seed=42)
    mapa_kolorow = {w: kolorowanie[w] for w in sorted(graf.nodes())}
    unikalne_kolory = sorted(set(mapa_kolorow.values()))
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

# Implementacja Algorytmu Brute Force :
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

# Implementacja Algorytmu Backtracking :
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

# Implementacja Algorytmów Zachłannych :
def zachlanny_ogolny(graf: nx.Graph, kolejnosc: list) -> dict:
    kolorowanie = {}
    for w in kolejnosc:
        zajete = {kolorowanie[s] for s in graf.neighbors(w) if s in kolorowanie}
        kolor = 0
        while kolor in zajete:
            kolor += 1
        kolorowanie[w] = kolor
    return kolorowanie

def zachlanny_lf(graf: nx.Graph) -> dict:
    return zachlanny_ogolny(graf, sorted(graf.nodes(), key=lambda x: graf.degree[x], reverse=True))

def zachlanny_sl(graf: nx.Graph) -> dict:
    tymczasowy = graf.copy()
    kolejnosc = []
    while tymczasowy.nodes:
        w = min(tymczasowy.nodes, key=lambda x: tymczasowy.degree[x])
        kolejnosc.append(w)
        tymczasowy.remove_node(w)
    return zachlanny_ogolny(graf, reversed(kolejnosc))

def zachlanny_slf(graf: nx.Graph) -> dict:
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

        for s in graf.neighbors(w):
            if s not in kolorowanie:
                nasycenie[s] = len({kolorowanie[n] for n in graf.neighbors(s) if n in kolorowanie})

    return kolorowanie

# Uruchamianie algorytmów :
def uruchom_algorytmy(graf):
    import time
    wyniki = {}

    def wykonaj(nazwa, funkcja):
        try:
            start = time.perf_counter()
            mapa = funkcja(graf)
            czas = time.perf_counter() - start
            wyniki[nazwa] = {"kolory": len(set(mapa.values())), "czas": czas}
        except Exception:
            wyniki[nazwa] = {"kolory": "BŁĄD", "czas": "BŁĄD"}

    wykonaj("Zachłanny Największy Pierwszy (LF)           ", zachlanny_lf)
    wykonaj("Zachłanny Najmniejszy Ostatni (SL)           ", zachlanny_sl)
    wykonaj("Zachłanny Nasycenie Największe Pierwsze (SLF)", zachlanny_slf)

    if len(graf.nodes()) <= 16:
        wykonaj("Brute Force                                  ", brutalne_kolorowanie)
    else:
        wyniki["Brute Force                                  "] = {"kolory": "N/D", "czas": "N/D"}

    if len(graf.nodes()) <= 30:
        wykonaj("Backtracking                                 ", kolorowanie_wsteczne)
    else:
        wyniki["Backtracking                                 "] = {"kolory": "N/D", "czas": "N/D"}

    return wyniki

# Implementacja wykresu czasu wykonania każdego algorytmu :
def wykres_czasu(wyniki):
    algorytmy = [n for n in wyniki if isinstance(wyniki[n]['czas'], float)]
    czasy = [wyniki[n]['czas'] for n in algorytmy]

    plt.figure(figsize=(10, 6))
    plt.bar(algorytmy, czasy, color='skyblue')
    plt.title("Czas wykonania algorytmów kolorowania grafu")
    plt.xlabel("Algorytm")
    plt.ylabel("Czas (sekundy)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Wykres liczby kolorów użytych przez każdy algorytm
def wykres_kolorow(wyniki):
    algorytmy = [n for n in wyniki if isinstance(wyniki[n]['kolory'], int)]
    kolory = [wyniki[n]['kolory'] for n in algorytmy]

    plt.figure(figsize=(10, 6))
    plt.bar(algorytmy, kolory, color='lightcoral')
    plt.title("Liczba kolorów użyta przez algorytmy")
    plt.xlabel("Algorytm")
    plt.ylabel("Liczba kolorów")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Program główny :
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--wezly", type=int, default=random.randint(8, 30))
    parser.add_argument("--prawdopodobienstwo", type=float, default=round(random.uniform(0.1, 0.6), 2))
    args = parser.parse_args()

    liczba_wierzcholkow = args.wezly
    prawdopodobienstwo_krawedzi = args.prawdopodobienstwo

    graf = pobierz_graf("losowy", liczba_wierzcholkow=liczba_wierzcholkow, prawdopodobienstwo=prawdopodobienstwo_krawedzi)
    print(f"[INFO] Wygenerowano graf: {liczba_wierzcholkow} wierzchołków, prawdopodobieństwo krawędzi wynosi {prawdopodobienstwo_krawedzi}")

    wyniki = uruchom_algorytmy(graf)
    for nazwa, metryki in wyniki.items():
        if metryki["czas"] == "N/D":
            print(f"{nazwa:25} | POMINIĘTO")
        else:
            print(f"{nazwa:25} | Kolory: {metryki['kolory']} | Czas: {metryki['czas']:.6f} sek")

    rysuj_graf(graf, zachlanny_lf(graf), "Zachłanny Największy Pierwszy (LF)")
    rysuj_graf(graf, zachlanny_sl(graf), "Zachłanny Najmniejszy Ostatni (SL)")
    rysuj_graf(graf, zachlanny_slf(graf), "Zachłanny Nasycenie Największe Pierwsze (SLF)")
    if len(graf.nodes()) <= 15:
        rysuj_graf(graf, brutalne_kolorowanie(graf), "Brute Force")
    if len(graf.nodes()) <= 30:
        rysuj_graf(graf, kolorowanie_wsteczne(graf), "Backtracking")

    wykres_czasu(wyniki)
    wykres_kolorow(wyniki)