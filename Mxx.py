import numpy as np
from numpy import sin, cos

S  = np.deg2rad(310)
D  = np.deg2rad(66)
R  = np.deg2rad(-171)

Mxx = -1.0 * ( sin(D) * cos(R) * sin (2*S) + sin(2*D) * sin(R) * sin(S)*sin(S) )
Myy =        ( sin(D) * cos(R) * sin (2*S) - sin(2*D) * sin(R) * cos(S)*cos(S) )
Mzz = -1.0 * ( Mxx + Myy)
Mxy =        ( sin(D) * cos(R) * cos (2*S) + 0.5 * sin(2*D) * sin(R) * sin(2*S) )
Mxz = -1.0 * ( cos(D) * cos(R) * cos (S)   + cos(2*D) * sin(R) * sin(S) )
Myz = -1.0 * ( cos(D) * cos(R) * sin (S)   - cos(2*D) * sin(R) * cos(S) )

printf("\nOutput Aki&Richards1980:  Mxx  Myy  Mzz  Mxy  Mxz  Myz \n")
printf("%9.5f %9.5f %9.5f %9.5f %9.5f %9.5f\n",Mxx, Myy, Mzz, Mxy, Mxz, Myz)

Mtt = Mxx
Mpp = Myy
Mrr = Mzz
Mtp = Mxy * -1.0
Mrt = Mxz
Mrp = Myz * -1.0


printf("\nOutput Harvard CMTSOLUTION:  Mrr Mtt Mpp Mrt Mrp Mtp\n")
printf("Mrr: %9.5f\n",Mrr)
printf("Mtt: %9.5f\n",Mtt)
printf("Mpp: %9.5f\n",Mpp)
printf("Mrt: %9.5f\n",Mrt)
printf("Mrp: %9.5f\n",Mrp)
printf("Mtp: %9.5f\n\n",Mtp)
