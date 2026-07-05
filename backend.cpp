#include <iostream>
#include <iomanip>
#include <string>
#include <algorithm>
#include <windows.h>
#include "mpreal.h"
#include "Interval.h"

using namespace mpfr;
using namespace std;
using namespace interval_arithmetic;

typedef double (*F_REAL)(double);
typedef double (*DF_REAL)(double);
typedef Interval<double> (*F_INT)(Interval<double>);
typedef Interval<double> (*DF_INT)(Interval<double>);
typedef const char* (*F_INFO)();

void NewtonZwykly(F_REAL f, DF_REAL df, string wejscie, int max_iter, double epsilon) {
    mpreal::set_default_prec(256);
    mpreal x = wejscie;

    for (int i = 0; i < max_iter; i++) {
        double current_x = x.toDouble();
        double fx = f(current_x);
        double dfx = df(current_x);

        if (abs(dfx) < 1e-20) {
            cout << "Blad: Pochodna bliska zeru." << endl;
            break;
        }

        mpreal x_nowy = x - fx / dfx;
        cout << "Iteracja " << i + 1 << " -> x = " << scientific << setprecision(17) << x_nowy << endl;

        if (abs(x_nowy - x) < epsilon) {
            cout << "SUKCES: Osiagnieto zadana dokladnosc (epsilon = " << epsilon << ")." << endl;
            break;
        }

        x = x_nowy;

        if (i == max_iter - 1) cout << "Osiagnieto limit iteracji." << endl;
    }
}

void NewtonPrzedzialowy(F_INT f_int, DF_INT df_int, string wejscie, int max_iter, int tryb, double epsilon) {
    Interval<double>::Initialize();
    Interval<double> X;

    if (tryb == 2) { 
        X.a = LeftRead<double>(wejscie);
        X.b = RightRead<double>(wejscie);
    } else { 
        size_t sep = wejscie.find(';');
        if (sep != string::npos) {
            string L_str = wejscie.substr(0, sep);
            string R_str = wejscie.substr(sep + 1);
            X.a = LeftRead<double>(L_str);
            X.b = RightRead<double>(R_str);
        } else {
            X.a = LeftRead<double>(wejscie);
            X.b = RightRead<double>(wejscie);
        }
    }

    for (int i = 0; i < max_iter; i++) {
        double m = X.Mid();
        
        Interval<double> m_interval;
        m_interval.a = m;
        m_interval.b = m;
        Interval<double> fm = f_int(m_interval);
        
        Interval<double> dfX = df_int(X);

        if (dfX.a <= 0.0 && dfX.b >= 0.0) {
            cout << "Blad: Zero znajduje sie w przedziale pochodnej (dzielenie przez zero)." << endl;
            break;
        }

        Interval<double> N = m_interval - (fm / dfX);

        Interval<double> X_nowy;
        
        if (tryb == 3) {
            X_nowy.a = max(X.a, N.a);
            X_nowy.b = min(X.b, N.b);

            if (X_nowy.a > X_nowy.b) {
                cout << "Blad: Przeciecie przedzialow jest puste. Brak pierwiastka w podanym obszarze." << endl;
                break;
            }
        } else {
            X_nowy = N;
        }

        X = X_nowy;
        string lewy_koniec, prawy_koniec;
        X.IEndsToStrings(lewy_koniec, prawy_koniec);
        double szerokosc = X.b - X.a;

        cout << "Iteracja " << i + 1 << " -> przedzial: [" 
             << lewy_koniec << " ; " << prawy_koniec 
             << "] (szerokosc: " << scientific << setprecision(17) << szerokosc << ")" << endl;

        if (tryb == 3) {
            if (szerokosc < epsilon) {
                cout << "SUKCES: Osiagnieto zadana dokladnosc (szerokosc przedzialu < epsilon)." << endl;
                break;
            }
        } else {
            if (abs(X.Mid() - m) < epsilon) {
                cout << "SUKCES: Osiagnieto zadana dokladnosc (roznica przyblizen < epsilon)." << endl;
                break;
            }
        }

        if (i == max_iter - 1) cout << "Osiagnieto limit iteracji." << endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 6) {
        cout << "Blad: Brak argumentow." << endl;
        return 1;
    }

    string sciezka_dll = argv[1];
    int tryb = stoi(argv[2]);
    string wejscie = argv[3];
    int max_iter = stoi(argv[4]);
    double epsilon = stod(argv[5]);

    cout << "Wczytywanie biblioteki: " << sciezka_dll << endl;
    cout << "Tryb: " << tryb << endl;

    HINSTANCE hDLL = LoadLibraryA(sciezka_dll.c_str());
    if (hDLL == NULL) {
        cout << "Blad: Nie mozna zaladowac pliku .dll!" << endl;
        return 1;
    }

    F_INFO get_info = (F_INFO)GetProcAddress(hDLL, "get_info");
    if (get_info) {
        cout << "Wzor funkcji: " << get_info() << endl;
    }

    if (tryb == 1) {
        F_REAL f_real = (F_REAL)GetProcAddress(hDLL, "f_real");
        DF_REAL df_real = (DF_REAL)GetProcAddress(hDLL, "df_real");
        if (!f_real || !df_real) {
            cout << "Blad: Brak funkcji w .dll!" << endl;
            return 1;
        }
        NewtonZwykly(f_real, df_real, wejscie, max_iter, epsilon);
    } else {
        F_INT f_int = (F_INT)GetProcAddress(hDLL, "f_int");
        DF_INT df_int = (DF_INT)GetProcAddress(hDLL, "df_int");
        if (!f_int || !df_int) {
            cout << "Blad: Brak przedzialowych funkcji w .dll!" << endl;
            return 1;
        }
        NewtonPrzedzialowy(f_int, df_int, wejscie, max_iter, tryb, epsilon);
    }

    FreeLibrary(hDLL);
    return 0;
}