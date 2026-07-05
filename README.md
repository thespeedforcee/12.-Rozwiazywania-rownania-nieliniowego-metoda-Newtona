# Rozwiązywanie równania nieliniowego metodą Newtona

Projekt zaliczeniowy z przedmiotu **Elementy Analizy Numerycznej (EAN)** realizowany na **Politechnice Poznańskiej** (Rok I, Semestr II).

Aplikacja służy do numerycznego wyznaczania pierwiastków równań nieliniowych przy użyciu **metody Newtona**. 

## 🛠️ Architektura i Technologie

Projekt charakteryzuje się hybrydową architekturą, łączącą prostotę tworzenia interfejsów w Pythonie z wydajnością obliczeniową języka C++:

* **Frontend (GUI):** Napisany w języku **Python** (odpowiada za okno aplikacji, wprowadzanie danych przez użytkownika oraz wyświetlanie wyników).
* **Backend (Rdzeń obliczeniowy):** Napisany w **C++**. (odpowiada za obliczenia i wyznaczanie pierwiastków, 3 tryby: zwykle (mpreal), przedzialowe (dane rzeczywiste) oraz przedzialowe (dane przedzialowe))
* **funkcja.cpp:** funkcja, ktora trzeba skompilowac jako plik .dll, poniewaz program wczytuje funkcje jako biblioteke .dll
