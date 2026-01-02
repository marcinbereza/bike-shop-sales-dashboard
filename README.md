# Analiza sprzeday sklepu rowerowego

## Proces biznesowy – cel projektu
Celem projektu było dostarczenie potencjalnemu właścicielowi sieci sklepów rowerowych interaktywnego narzędzia 
**analitycznego (kokpitu BI)**, który umożliwia kompleksową **ocenę efektywności** sprzedaży detalicznej oraz internetowej na 
**przestrzeni ostatnich lat**.

Kluczowe aspekty analityczne:
- **Wykrywanie trendów i sezonowości**: identyfikacja okresów o podwyższonej sprzedaży w 
celu optymalizacji stanów magazynowych.
- **Analiza geograficzna**: wskazanie województw, powiatów o najlepszych wskaźnikach sprzedaży.
- **Optymalizacja asortymentu**: pozyskanie wiedzy o najchętniej kupowanych markach i produktach w 
danych regionach w celu lepszego dostosowania lokalnych ofert.
- **Charakterystyka koszyka**: analiza rozkładu produktów w zależności od kanału 
sprzedaży (online/stacjonarnie) oraz faktu zakupu roweru.

Główny nacisk położono na aspekt czasowy, umożliwiając analizę w ujęciu miesięcznym, kwartalnym i rocznym oraz 
swobodne przesuwanie analizowanego okna czasowego.

Kluczowe dla sukcesu było pozyskanie danych o:
- Rzeczywistym asortymencie sklepu rowerowego ([sprint-rower.pl](sprint-rower.pl)).
- Podziale administracyjnym województw i powiatów ([polskawliczbach.pl](polskawliczbach.pl)).
- Najpopularniejszych imionach i nazwiskach w Polsce ([dane.gov.pl/pl/dataset](dane.gov.pl/pl/dataset))

## Przygotowanie danych
Proces ten wymagał kilku etapów, aby od podstaw zbudować wiarygodne i spójne środowisko danych, które 
nie było dostępne w gotowych zbiorach:
- **Pozyskanie asortymentu:** wykorzystanie bibliotek Selenium i BeautifulSoup4 do ekstrakcji danych. Etap ten objął przejście 
przez 201 podstron z rowerami, oświetleniem, zapięciami, narzędziami, sakwami, kaskami i rękawiczkami. Pozwoliło to na 
uzyskanie rzeczywistej bazy produktów zawierających: kategorie, podkategorie, producenta, model, ceny oraz zdjęcia.
- **Uzyskanie danych geograficznych**: scraping danych o województwach, powiatach, w tym informacji o liczbie mieszkańców.
- **Budowa baza klientów**: wykorzystanie listy tysiąca najpopularniejszych imion i trzystu nazwisk (dla obu płci) oraz danych 
geograficznych do stworzenia unikalnej bazy 10 tys. odbiorców wraz z ich adresami dostawy.
- **Symulacja transakcji**: konstrukcja tabeli faktów na podstawie prawdopodobieństwa zakupowego (zależności pomiędzy 
płcią, kanałem sprzedaży a kategorią produktów; wpływ wielkości miasta na liczbę zamówień) oraz logiki sezonowej 
(szczyty sprzedaży w okresach letnich)