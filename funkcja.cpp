#include "Interval.h"

//funkcja x^2 - 4
extern "C" {
    __declspec(dllexport) const char* get_info() {
        return "f(x) = x^2 - 4";
    }
    
    __declspec(dllexport) double f_real(double x) { //funkcja
        return x*x - 4.0;
    }

    __declspec(dllexport) double df_real(double x) { //pochodna
        return 2.0*x;
    }

    __declspec(dllexport) interval_arithmetic::Interval<double> f_int(interval_arithmetic::Interval<double> x) {
        interval_arithmetic::Interval<double> four(4.0, 4.0);
        return x*x - four; 
    }

    __declspec(dllexport) interval_arithmetic::Interval<double> df_int(interval_arithmetic::Interval<double> x) {
        interval_arithmetic::Interval<double> two(2.0, 2.0);
        return two*x;
    }
}