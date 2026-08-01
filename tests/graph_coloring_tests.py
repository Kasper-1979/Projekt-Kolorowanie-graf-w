import time
import itertools
import networkx as nx
import pandas as pd
from collections import defaultdict
import os

# Ustawienia pramentrów grafów do przeprowadzanych testów :
liczba_wierzcholkow = 12  # liczba wierzchołków w grafie
prawdopodobienstwo_krawedzi = 0.3  # prawdopodobieństwo istnienia krawędzi
sciezka_excel = r"C:\Users\hp\Desktop\OD Projekt Kolorowanie grafów\Kolorowanie_grafów_wyniki_testów1.xlsx"  # pełna ścieżka do pliku Excel

# Implementacja Aalgorytmów kolorowania grafów :
def zachlanny_najwiekszy_pierwszy(graf):
    uporzadkowane = sorted(graf.nodes(), key=lambda v: graf.degree[v], reverse=True)
    return koloruj_zachlannie(graf, uporzadkowane)

def zachlanny_najmniejszy_ostatni(graf):
    tymczasowy = graf.copy()
    kolejnosc = []
    while tymczasowy.nodes:
        wierzcholek = min(tymczasowy.nodes, key=lambda v: tymczasowy.degree[v])
        kolejnosc.append(wierzcholek)
        tymczasowy.remove_node(wierzcholek)
    return koloruj_zachlannie(graf, list(reversed(kolejnosc)))

def zachlanny_saturacja(graf):
    kolorowanie = {}
    nasycenie = defaultdict(int)
    stopnie = dict(graf.degree())
    while len(kolorowanie) < len(graf.nodes()):
        niepokolorowane = [v for v in graf.nodes if v not in kolorowanie]
        wybor = max(niepokolorowane, key=lambda v: (nasycenie[v], stopnie[v]))
        zajete = {kolorowanie[sasiad] for sasiad in graf.neighbors(wybor) if sasiad in kolorowanie}
        kolor = 0
        while kolor in zajete:
            kolor += 1
        kolorowanie[wybor] = kolor
        for sasiad in graf.neighbors(wybor):
            if sasiad not in kolorowanie:
                nasycenie[sasiad] = len({kolorowanie[n] for n in graf.neighbors(sasiad) if n in kolorowanie})
    return kolorowanie

def koloruj_zachlannie(graf, kolejnosc):
    kolorowanie = {}
    for wierzcholek in kolejnosc:
        zajete = {kolorowanie[sasiad] for sasiad in graf.neighbors(wierzcholek) if sasiad in kolorowanie}
        kolor = 0
        while kolor in zajete:
            kolor += 1
        kolorowanie[wierzcholek] = kolor
    return kolorowanie

def brutalne_kolorowanie(graf):
    wierzcholki = list(graf.nodes())
    for liczba_kolorow in range(1, len(wierzcholki) + 1):
        for kombinacja in itertools.product(range(liczba_kolorow), repeat=len(wierzcholki)):
            przypisanie = dict(zip(wierzcholki, kombinacja))
            if all(przypisanie[u] != przypisanie[v] for u, v in graf.edges()):
                return przypisanie
    return {}

def kolorowanie_rekurencyjne(graf):
    wierzcholki = list(graf.nodes())
    kolorowanie = {}
    def bezpieczne(w, kolor):
        return all(kolorowanie.get(sasiad) != kolor for sasiad in graf.neighbors(w))
    def rekurencja(index, maks_kolor):
        if index == len(wierzcholki):
            return True
        for kolor in range(maks_kolor):
            if bezpieczne(wierzcholki[index], kolor):
                kolorowanie[wierzcholki[index]] = kolor
                if rekurencja(index + 1, maks_kolor):
                    return True
                del kolorowanie[wierzcholki[index]]
        return False
    for liczba_kolorow in range(1, len(wierzcholki) + 1):
        kolorowanie.clear()
        if rekurencja(0, liczba_kolorow):
            return kolorowanie
    return {}

# implementacja generatora grafów :
def generuj_graf_losowy(n, p):
    return nx.erdos_renyi_graph(n, p)

# Uruchamianie algorytmów :
def wykonaj_algorytmy(graf):
    wyniki = []
    def zmierz_i_zapisz(nazwa, funkcja):
        try:
            start = time.perf_counter()
            kolory = funkcja(graf)
            czas = time.perf_counter() - start
            wyniki.append({
                "Algorytm": nazwa,
                "Liczba kolorów": len(set(kolory.values())),
                "Czas [s]": czas
            })
        except:
            wyniki.append({
                "Algorytm": nazwa,
                "Liczba kolorów": "BŁĄD",
                "Czas [s]": "BŁĄD"
            })

    zmierz_i_zapisz("Zachłanny Największy Pierwszy (LF)           ", zachlanny_najwiekszy_pierwszy)
    zmierz_i_zapisz("Zachłanny Najmniejszy Ostatni (SL)           ", zachlanny_najmniejszy_ostatni)
    zmierz_i_zapisz("Zachłanny Nasycenie Największe Pierwsze (SLF)", zachlanny_saturacja)

    if len(graf.nodes()) <= 15:
        zmierz_i_zapisz("Brute Force                                  ", brutalne_kolorowanie)
    else:
        wyniki.append({"Algorytm": "Brute Force                                  ", "Liczba kolorów": "N/D", "Czas [s]": "N/D"})

    if len(graf.nodes()) <= 30:
        zmierz_i_zapisz("Backtracking                                 ", kolorowanie_rekurencyjne)
    else:
        wyniki.append({"Algorytm": "Backtracking                                 ", "Liczba kolorów": "N/D", "Czas [s]": "N/D"})

    return wyniki

# Implementacja zapisu wyników testów do Excela :
def dopisz_do_pliku_excel(wyniki, sciezka):
    df = pd.DataFrame(wyniki)
    df["Liczba wierzchołków"] = liczba_wierzcholkow
    df["Prawdopodobieństwo"] = prawdopodobienstwo_krawedzi

    if os.path.exists(sciezka):
        df_stary = pd.read_excel(sciezka)
        df = pd.concat([df_stary, df], ignore_index=True)

    df.to_excel(sciezka, index=False)
    print(f"[INFO] Wyniki zapisano do: {sciezka}")
 
# Program główny :
if __name__ == "__main__":
    graf = generuj_graf_losowy(liczba_wierzcholkow, prawdopodobienstwo_krawedzi)
    print(f"[INFO] Wygenerowano graf z {liczba_wierzcholkow} wierzchołkami, prawdopodobieństwo krawędzi wynosi {prawdopodobienstwo_krawedzi}")

    wyniki = wykonaj_algorytmy(graf)
    for wiersz in wyniki:
        print(f"{wiersz['Algorytm']:20} | Kolory: {wiersz['Liczba kolorów']:>5} | Czas: {wiersz['Czas [s]']}")

    dopisz_do_pliku_excel(wyniki, sciezka_excel)
