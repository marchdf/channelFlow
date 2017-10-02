// ----------- BEGIN INPUT ------------

N = 1; // INPUT N=p+1

nl = Round(64./N); // Coarse
//nl = Round(96./N); // Baseline
//nl = Round(128./N); // Fine

// ----------- END INPUT --------------

lc = Pi/nl;
Printf("dx+ = %g",lc*550);

lx=2*Pi;
lz=Pi;
Point(1) = {0, 0, 0, lc};
line[] = Extrude {2*Pi, 0, 0.} {
  Point{1}; Layers{Round(2*nl)};
};

Physical Line(1) = {line[1]};
surface[] = Extrude {0, 0, Pi} {
  Line{line[1]}; Layers{nl}; Recombine;
};

ny = 2*Round(48/N);
Printf("ny = %g",ny);

r = 1.2^(N/2);
h0 = 0.5*(1-r)/(1-r^(ny/2));
h=0.;
For i In {0:(ny-2)/2}
  h += h0*r^i;
  y[i] = h;
  y[ny-i-2] = 1-h;
EndFor
y[ny/2-1] = 0.5;
y[ny-1] = 1.;

For i In {0:ny/2-1}
  Printf("y+[%g] = %g", i, 2*550*y[i]);
  layer[i] = 1;
EndFor
For i In {0:ny-1}
  layer[i] = 1;
EndFor

volume[] = Extrude {0.0,2.0,0.0} {
  Surface{surface[1]}; Layers{ layer[], y[] }; Recombine;
};

