/* This file generated automatically. */
/*          Do not modify.            */
#include "udf.h"
#include "prop.h"
#include "dpm.h"
extern DEFINE_PROFILE(inlet_x_velocity,thread,position);
extern DEFINE_PROFILE(omega,thread,position);
extern DEFINE_PROFILE(k,thread,position);
extern DEFINE_WALL_FUNCTIONS(Parente_Benocci, f, t, c0, t0, wf_ret, yPlus, Emod);
UDF_Data udf_data[] = {
{"inlet_x_velocity", (void (*)(void))inlet_x_velocity, UDF_TYPE_PROFILE},
{"omega", (void (*)(void))omega, UDF_TYPE_PROFILE},
{"k", (void (*)(void))k, UDF_TYPE_PROFILE},
{"Parente_Benocci", (void (*)(void))Parente_Benocci, UDF_TYPE_WALL_FUNCTIONS},
};
int n_udf_data = sizeof(udf_data)/sizeof(UDF_Data);
#include "version.h"
void UDF_Inquire_Release(int *major, int *minor, int *revision)
{
  *major = RampantReleaseMajor;
  *minor = RampantReleaseMinor;
  *revision = RampantReleaseRevision;
}
