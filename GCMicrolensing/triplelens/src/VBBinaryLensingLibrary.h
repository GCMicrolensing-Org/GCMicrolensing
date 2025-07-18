// VBBinaryLensing v2.0.3 (2018)
//
// This code has been developed by Valerio Bozza, University of Salerno.
// Any use of this code for scientific publications should be acknowledged by a citation to
// V. Bozza, E. Bachelet, F. Bartolic, T.M. Heintz, A.R. Hoag, M. Hundertmark, MNRAS 479 (2018) 5157
// The original methods present in v1.0 are described in
// V. Bozza, MNRAS 408 (2010) 2188
// Check the repository at http://www.fisica.unisa.it/GravitationAstrophysics/VBBinaryLensing.htm
// for the newest version.
//
// The code relies on the root solving algorithm by Jan Skworon and Andy Gould
// described in Skowron & Gould arXiv:1203.1034.
// Please also cite this paper if specifically relevant in your scientific publication.
// The original Fortran code available on http://www.astrouw.edu.pl/~jskowron/cmplx_roots_sg/
// has been translated to C++ by Tyler M. Heintz and Ava R. Hoag (2017)
//
// GNU Lesser General Public License applies to all parts of this code.
// Please read the separate LICENSE.txt file for more details.

#ifndef __binlens
#define __binlens
#define __unmanaged

#define FRAC_ERR 2.0e-17 //Fractional Error for double precision, 2.0e-15

// #define _PRINT_ERRORS2

#define _L1 x1-((x1+a/2.0)/((x1+a/2.0)*(x1+a/2.0)+x2*x2)+q*(x1-a/2.0)/((x1-a/2.0)*(x1-a/2.0)+x2*x2))/(1.0+q) // Used in PlotCrits
#define _L2 x2-(x2/((x1+a/2.0)*(x1+a/2.0)+x2*x2)+q*x2/((x1-a/2.0)*(x1-a/2.0)+x2*x2))/(1.0+q)
#define _LL (y-z)+coefs[21]/(zc-coefs[20])+coefs[22]/zc //Lens equation test
#define _J1c coefs[21]/((zc-coefs[20])*(zc-coefs[20]))+coefs[22]/(zc*zc) //#define _J1 m1/((zc-0.5*a)*(zc-0.5*a))+m2/((zc+0.5*a)*(zc+0.5*a))
#define _J2 -2.0*(coefs[21]/((z-coefs[20])*(z-coefs[20])*(z-coefs[20]))+coefs[22]/(z*z*z))
#define _J3 6.0*(coefs[21]/((z-coefs[20])*(z-coefs[20])*(z-coefs[20])*(z-coefs[20]))+coefs[22]/(z*z*z*z))
#define _skew(p1,p2,q1,q2) p1*q2-p2*q1
#define _NP 200.0

#define _sign(x) ((x>0)? +1 : -1)

#include<math.h>
#include<stdio.h>

// #define M_PI = 3.1415926;

class _curve;
class _sols;
class _theta;
class complex;
struct annulus;

#ifndef __unmanaged
namespace VBBinaryLensingLibrary {
public ref class VBBinaryLensing
#else
class VBBinaryLensing
#endif
	{
	int *ndatasat;
	double **tsat, ***possat;
	// double Mag0, corrquad, corrquad2, safedist;
	int nim0;
	// double e, phi, phip, phi0, Om, inc, t0, d3, v3, GM, flagits;
	double t0;
	double Obj[3], rad[3], tang[3], t0old;
	double Eq2000[3], Quad2000[3], North2000[3];
	double ESPLout[101][101], ESPLin[101][101];
	bool ESPLoff, multidark;
	annulus *annlist;

	void ComputeParallax(double, double, double *);
	_curve *NewImages(complex, complex  *, _theta *);
	void OrderImages(_sols *, _curve *);
	void cmplx_laguerre(complex *, int, complex *, int &, bool &);
	void cmplx_newton_spec(complex *, int, complex *, int &, bool &);

	void solve_quadratic_eq(complex &, complex &, complex *);
	void solve_cubic_eq(complex &, complex &, complex &, complex *);

public:
	double Mag0, corrquad, corrquad2, safedist;
	double Tol, RelTol, a1, t0_par;
	int satellite, parallaxsystem, t0_par_fixed, nsat, finalNPS;
	int minannuli, nannuli, NPS, ifFinite;
	double y_1, y_2, av, therr;

	// void solv_lens_equation(double *zrxy, double *mlens, double *zlens, double xs, double ys, int NLENS);
	void outputCriticalTriple_list(double resxy[], double mlens[], double Zlens[], int nlens, int NPS);
	void outputCriticalBinary_list(double allxys[], double a, double q, int NPS);
	// Critical curves and caustic calculation
	_sols *PlotCrit(double a, double q, int NPS);
	_sols *PlotCritTriple(double m[], complex z[], int NPS, int nlens);
	_sols *outCritTriple(double m[], complex z[], int NPS, int nlens);
	void PrintCau(double a, double q);

	// Initialization for calculations including parallax
	void SetObjectCoordinates(char *Coordinates_file, char *Directory_for_satellite_tables);

	// Magnification calculation outputCriticalTriple_listfunctions.

	double BinaryMag0(double s, double q, double y1, double y2, _sols **Images);
	double BinaryMag0(double s, double q, double y1, double y2);
	double BinaryMag(double s, double q, double y1, double y2, double rho, double accuracy, _sols **Images);
	double BinaryMag(double s, double q , double y1, double y2, double rho, double accuracy);
	double BinaryMag2(double s, double q, double y1, double y2, double rho);
	double BinaryMagDark(double s, double q, double y1, double y2, double rho, double a1, double accuracy);
	double BinaryMagDark_2paras(double a, double q, double y1, double y2, double RSv, double a1, double b , double Tol);
	void BinaryMagMultiDark(double s, double q, double y1, double y2, double rho, double *a1_list, int n_filters, double *mag_list, double accuracy);

	void LoadESPLTable(char *tablefilename);
	double ESPLMag(double u, double rho);
	double ESPLMag2(double u, double rho);
	double ESPLMagDark(double u, double rho, double a1);


	// New (v2) light curve functions, operating on arrays

	void PSPLLightCurve(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void PSPLLightCurveParallax(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void ESPLLightCurve(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void ESPLLightCurveParallax(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);

	void BinaryLightCurve(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void BinaryLightCurveW(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void BinaryLightCurveParallax(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void BinaryLightCurveOrbital(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, double *sep_array, int np);

	void BinSourceLightCurve(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void BinSourceLightCurveParallax(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, int np);
	void BinSourceLightCurveXallarap(double *parameters, double *t_array, double *mag_array, double *y1_array, double *y2_array, double *sep_array, int np);

	// Old (v1) light curve functions, for a single calculation
	double PSPLLightCurve(double *parameters, double t);
	double PSPLLightCurveParallax(double *parameters, double t);
	double ESPLLightCurve(double *parameters, double t);
	double ESPLLightCurveParallax(double *parameters, double t);

	double BinaryLightCurve(double *parameters, double t);
	double BinaryLightCurveW(double *parameters, double t);
	double BinaryLightCurveParallax(double *parameters, double t);
	double BinaryLightCurveOrbital(double *parameters, double t);


	double BinSourceLightCurve(double *parameters, double t);
	double BinSourceLightCurveParallax(double *parameters, double t);
	double BinSourceLightCurveXallarap(double *parameters, double t);

	// Skowron & Gould root calculator
	void cmplx_roots_gen(complex *, complex *, int, bool, bool);
	void cmplx_laguerre2newton(complex *, int, complex *, int &, bool &, int);

	// Constructor and destructor
	VBBinaryLensing();
	~VBBinaryLensing();
	void saveTracks(_sols ** track);

};

struct annulus {
	double bin;
	double cum;
	double Mag;
	double err;
	double f;
	int nim;
	annulus *prev, *next;
};


#ifndef __unmanaged
}
#endif





void findCloseImages(double mlens[], complex zlens[], double xs, double ys, int NLENS, complex close_zr[], int iter[]);
void newtonSolver(double mlens[], complex zlens[], double xs, double ys, int NLENS, complex *z, int *iter);

class _theta {
public:
	double th, maxerr, Mag, errworst;
	_theta *prev, *next;

	_theta(double);

};

class _thetas {
public:
	_theta *first, *last;
	int length;

	_thetas(void);
	~_thetas(void);
	_theta *insert(double);


};

class complex {
public:
	double re;
	double im;
	complex(double, double);
	complex(double);
	complex(void);
};

class Node {
public:
	double value;
	int nimages;
	Node *next;
	Node *prev;
	Node(double);
	double operator-(Node);
};

class _point {
public:
	double phi;		//angle phi on the source circle
	// Node *nodephi;
	double mu;	//signed magnification
	short int flag;		// is this a true solution
	complex zs;		// corresponding source position
	double thetaJ;	// angle of the eigen matrix

	double area;
	double error;

	double x1;
	double x2;
	double parab, absdzs, ds, dJ;
	complex d, J2, dz;
	_theta *theta;
	int closepairparity;//add on 20200414, used to mark the critical points at creation and destroy of images.
	_point(double , double, _theta *);
	~_point(void);
	_point *next, *prev;
	double operator-(_point);
};

class _curve {
public:
	int length, parity;
	_point *first, *last;//, *maxerr_pnt, *second_maxerr_pnt, *third_maxerr_pnt;
	unsigned short int jumped_flag;
	_curve *next, *prev;
	_curve *partneratstart, *partneratend;
	double parabstart, maxerr, second_maxerr, third_maxerr;
	int posflagnum;

	_curve(_point *);
	_curve(void);
	~_curve(void);

	_curve *divide(_point *);
	void drop(_point *, int del = 0);
	void append(double, double);
	void append(_point *);
	void insert(_point *, _point*);
	void prepend(double, double);
//	void prepend(_point *);
	_curve *join(_curve *);
	_curve *joinbefore(_curve *);
	_curve *reverse(void);
	double closest(_point *, _point **);
	double closest2(_point *, _point **);
	double closest3(_point *, _point **);
	void complement(_point **, int, _point **, int);
};

class _sols {
public:
	int length;
	_curve *first, *last;

	_sols(void);
	~_sols(void);
	void drop(_curve *, int del = 0);
	void append(_curve *);
	void prepend(_curve *);
	void join(_sols *);
	void sort(void);
	void removelen1track();
};


#define MR 8
#define MT 10
#define MAXIT (MT*MR)
#define MAXM 30

#endif

double abs(complex);
double absint(int);
double absf(double);
complex conj(complex);
complex sqrt(complex);
double real(complex);
double imag(complex);
complex expcmplx(complex);
complex cbrt(complex);
complex operator+(complex, complex);
complex operator-(complex, complex);
complex operator*(complex, complex);
complex operator/(complex, complex);
complex operator+(complex, double);
complex operator-(complex, double);
complex operator*(complex, double);
complex operator/(complex, double);
complex operator+(double, complex);
complex operator-(double, complex);
complex operator*(double, complex);
complex operator/(double, complex);
complex operator+(int, complex);
complex operator-(int, complex);
complex operator*(int, complex);
complex operator/(int, complex);
complex operator+(complex, int);
complex operator-(complex, int);
complex operator*(complex, int);
complex operator/(complex, int);
complex operator-(complex);
bool operator==(complex, complex);
bool operator!=(complex, complex);
