
import os
from collections import OrderedDict

#//// variables ////#
myl = OrderedDict()
myl['utils']   = False
myl['linalg']  = False
myl['anaflat'] = False
myl['anafull'] = False
myl['nldd']    = False
myl['prj']     = ''
myl['cfitsio'] = False
myl['healpix'] = False
myl['lenspix'] = False
#myl['mylib']   = '\${HOME}/Work/Lib/cosmodat/f90/'
myl['mylib']   = '\${HOME}/Work/Lib/myf90lib/'

#//// text adds to a file ////#
def add(text,f,ini=False,opt=''):
  if ini:     os.system('echo '+opt+' "'+text+'" > '+f)
  if not ini: os.system('echo '+opt+' "'+text+'" >> '+f)


def makefile(f='Makefile',flag='-O3 -ip -fpp --no-wrap-margin',debug=False,myl='',obj='main.o'):
  #//// create Makefile ////#

  ## executable file
  exe = 'exe'

  ## Complier and options
  add('FC = ifort',f,ini=True)
  if myl['healpix'] or myl['anafull'] or myl['lenspix']: flag = '-qopenmp -ip -fpp' # should use qopenmp for healpix
  add('FLAG = '+flag,f)
  if debug: add('DBAG = -check all -std -gen_interfaces -fpe0 -ftrapuv -traceback',f)
  add('FLAGS = \$(FLAG) \$(DBAG)',f)

  ## Directories and Link options
  dir, mod, lib, link, prj, pub = myl['mylib'], '', '', '', myl['prj'], myl['mylib']+'pub/'

  # local project lib
  if prj!='':
    mod, lib = mod+' -I'+prj+'/mod',  lib+' -L'+prj+'/lib'
    link = '-lprj '+link

  # my lib
  mod, lib = mod+' -I'+dir+'mod', lib+' -L'+dir+'lib'
  if myl['nldd']    : link = link + ' -lnldd'
  if myl['anafull'] : link = link + ' -lanafull'
  if myl['anaflat'] : link = link + ' -lanaflat'
  if myl['linalg']  : link = link + ' -llinalg'
  if myl['utils']   : link = link + ' -lutils'

  # FFTW
  if myl['anaflat']:
    mod, lib = mod+' -I'+pub+'FFTW/api',  lib+' -L'+pub+'FFTW/'
    link = link+' -lfftw3'

  # LAPACK
  if myl['linalg']:
    mod, lib = mod+' -I'+pub+'LAPACK95/mod',  lib+' -L'+pub+'LAPACK95/lib'
    link = link+' -llapack95 -llapack -lrefblas'

  # Lenspix
  if myl['lenspix']:
    mod, lib = mod+' -I'+pub+'lenspix/mod',  lib+' -L'+pub+'lenspix/lib'
    link = link+' -llenspix'

  # Healpix
  if myl['healpix'] or myl['anafull'] or myl['lenspix']:
    mod, lib = mod+' -I'+pub+'Healpix/include',  lib+' -L'+pub+'Healpix/lib'
    link = link+' -lhealpix'

  # cfitsio
  if myl['cfitsio'] or myl['healpix'] or myl['anafull'] or myl['lenspix']:
    lib = lib+' -L'+pub+'cfitsio'
    link = link+' -lcfitsio'

  # summary
  add('OPT = '+mod+' '+lib+' '+link,f)

  ## files to be compiled 
  add('OBJ = '+obj,f)

  ## rules
  add('all: '+exe,f)
  add('%.o: %.f90',f)
  add('\t \$(FC) \$(FLAGS) \$(OPT) -c \$*.f90',f,opt='-e')
  add(exe+': \$(OBJ)',f)
  add('\t \$(FC) \$(FLAGS) \$(OBJ) \$(OPT) -o \$@',f,opt='-e')
  add('clean:',f)
  add('\t rm -f *.o* *.e* *.mod *.d *.pc *.obj core* *.il',f,opt='-e')


def compile(clean=True,remove=True):
  #//// compile ////#
  os.system('make')
  if clean:  os.system('make clean')
  if remove: os.system('rm -f Makefile')


