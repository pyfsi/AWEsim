#include "udf.h"
#include "mem.h"

#define y0 0.0002		/*  roughness height of the ground */
#define u_star 0.3828883453000257	/* friction velocity of the ABL */
#define Cmu 0.09		/* constant of the k-epsilon model */
#define C1 -0.04
#define C2 0.53

DEFINE_PROFILE(inlet_x_velocity,thread,position)
{
real x[ND_ND];
real y;
face_t f;

begin_f_loop(f,thread)
{
F_CENTROID(x,f,thread);
y = x[2];
F_PROFILE(f,thread,position)=  (u_star/KAPPA)*log((y+y0)/y0);
}
end_f_loop(f,thread)
}


DEFINE_PROFILE(omega,thread,position)
{
real x[ND_ND];
real y;
face_t f;

begin_f_loop(f,thread)
{
F_CENTROID(x,f,thread);
y = x[2];
F_PROFILE(f,thread,position)=(u_star/(KAPPA*sqrt(Cmu)))*(1/(y+y0));
}
end_f_loop(f,thread)
}


DEFINE_PROFILE(k,thread,position)
{
real x[ND_ND];
real y;
face_t f;

begin_f_loop(f,thread)
{
F_CENTROID(x,f,thread);
y = x[2];
F_PROFILE(f,thread,position)=(pow(u_star,2)/sqrt(Cmu))*sqrt(C1*log((y+y0)/y0)+C2);
}
end_f_loop(f,thread)
}


DEFINE_WALL_FUNCTIONS(Parente_Benocci, f, t, c0, t0, wf_ret, yPlus, Emod)
{
real wf_value;
real x[ND_ND];
real D;
float Emodx;
float yPlusx;

C_CENTROID(x,c0,t0);
D=x[2];		/* store in D the y coordinate of the cell centroid; the y coordinate is the wall distance! */


if (THREAD_ID(t)==8) {
	Emodx=C_MU_L(c0,t0)/(C_R(c0,t0)*y0*pow(Cmu,0.25)*pow(C_K(c0,t0),0.5));
	yPlusx=(D+y0)*C_R(c0,t0)*pow(Cmu, 0.25)*pow(C_K(c0,t0),0.5)/C_MU_L(c0,t0);
}
else {
	Emodx=Emod;
	yPlusx=yPlus;
}


  switch (wf_ret)
    {
    case UPLUS_LAM:
      wf_value = yPlusx;
      break;
    case UPLUS_TRB:
      wf_value = log(Emodx*yPlusx)/KAPPA;
      break;
    case DUPLUS_LAM:
      wf_value = 1.0;
      break;
    case DUPLUS_TRB:
      wf_value = 1./(KAPPA*yPlusx);
      break;
    case D2UPLUS_TRB:
      wf_value = -1./(KAPPA*yPlusx*yPlusx);
      break;
    default:
	printf("Wall function return value unavailable\n");
    }  
  return wf_value;
}
