#include <iostream>
#include <iomanip>
#include <mpreal.h>
#include <boost/version.hpp>
#include <boost/core/demangle.hpp>

using namespace mpfr;
using namespace std;

int main() {
    // 1. Test MPFR++ / GMP / MPFR
    mpreal::set_default_prec(256); // Precyzja ~77 cyfr po przecinku
    mpreal a = 2;
    mpreal result = sqrt(a);

    cout << "--- TEST GMP / MPFR / MPFR++ ---" << endl;
    cout << "Pierwiastek z 2 (256 bitow):" << endl;
    cout << setprecision(70) << result << endl << endl;

    // 2. Test BOOST
    cout << "--- TEST BOOST ---" << endl;
    cout << "Wersja biblioteki Boost: " 
         << BOOST_VERSION / 100000 << "."  // wersja glowna
         << BOOST_VERSION / 100 % 1000 << "." // wersja drugorzedna
         << BOOST_VERSION % 100 << endl;      // poprawka

    cout << "\nStatus: Wszystko wydaje sie dzialac poprawnie!" << endl;

    return 0;
}