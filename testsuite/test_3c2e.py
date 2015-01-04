#!/usr/bin/env python
# $Id$
# -*- coding: utf-8

'''
test libcint
'''

__author__ = "Qiming Sun <osirpt.sun@gmail.com>"

import sys
import os
import ctypes
import numpy

_cint = numpy.ctypeslib.load_library('libcint', '.')


PTR_LIGHT_SPEED    = 0
PTR_COMMON_ORIG    = 1
PTR_SHIELDING_ORIG = 4
PTR_RINV_ORIG      = 4

CHARGE_OF  = 0
PTR_COORD  = 1
NUC_MOD_OF = 2
PTR_MASS   = 3
RAD_GRIDS  = 4
ANG_GRIDS  = 5
ATM_SLOTS  = 6

ATOM_OF   = 0
ANG_OF    = 1
NPRIM_OF  = 2
NCTR_OF   = 3
KAPPA_OF  = 4
PTR_EXP   = 5
PTR_COEFF = 6
BAS_SLOTS = 8

natm = 4
nbas = 0
atm = numpy.zeros((natm+1,ATM_SLOTS), dtype=numpy.int32)
bas = numpy.zeros((1000,BAS_SLOTS), dtype=numpy.int32)
env = numpy.zeros(10000)
off = 10
for i in range(natm):
    atm[i, CHARGE_OF] = (i+1)*2
    atm[i, PTR_COORD] = off
    env[off+0] = .2 * (i+1)
    env[off+1] = .3 + (i+1) * .5
    env[off+2] = .1 - (i+1) * .5
    off += 3
off0 = off

# basis with kappa > 0
nh = 0

bas[nh,ATOM_OF ]  = 0
bas[nh,ANG_OF  ]  = 1
bas[nh,KAPPA_OF]  = 1
bas[nh,NPRIM_OF]  = 1
bas[nh,NCTR_OF ]  = 1
bas[nh,PTR_EXP]   = off
env[off+0] = 1
bas[nh,PTR_COEFF] = off + 1
env[off+1] = 1
off += 2
nh += 1

bas[nh,ATOM_OF ]  = 1
bas[nh,ANG_OF  ]  = 2
bas[nh,KAPPA_OF]  = 2
bas[nh,NPRIM_OF]  = 2
bas[nh,NCTR_OF ]  = 2
bas[nh,PTR_EXP]   = off
env[off+0] = 5
env[off+1] = 3
bas[nh,PTR_COEFF] = off + 2
env[off+2] = 1
env[off+3] = 2
env[off+4] = 4
env[off+5] = 1
off += 6
nh += 1

bas[nh,ATOM_OF ]  = 2
bas[nh,ANG_OF  ]  = 3
bas[nh,KAPPA_OF]  = 3
bas[nh,NPRIM_OF]  = 1
bas[nh,NCTR_OF ]  = 1
bas[nh,PTR_EXP ]  = off
env[off+0] = 1
bas[nh,PTR_COEFF] = off + 1
env[off+1] = 1
off += 2
nh += 1

bas[nh,ATOM_OF ]  = 3
bas[nh,ANG_OF  ]  = 4
bas[nh,KAPPA_OF]  = 4
bas[nh,NPRIM_OF]  = 1
bas[nh,NCTR_OF ]  = 1
bas[nh,PTR_EXP ]  = off
env[off+0] = .5
bas[nh,PTR_COEFF] = off + 1
env[off+1] = 1.
off = off + 2
nh += 1

nbas = nh

# basis with kappa < 0
n = off - off0
for i in range(n):
    env[off+i] = env[off0+i]

for i in range(nh):
        bas[i+nh,ATOM_OF ] = bas[i,ATOM_OF ]
        bas[i+nh,ANG_OF  ] = bas[i,ANG_OF  ] - 1
        bas[i+nh,KAPPA_OF] =-bas[i,KAPPA_OF]
        bas[i+nh,NPRIM_OF] = bas[i,NPRIM_OF]
        bas[i+nh,NCTR_OF ] = bas[i,NCTR_OF ]
        bas[i+nh,PTR_EXP ] = bas[i,PTR_EXP ]  + n
        bas[i+nh,PTR_COEFF]= bas[i,PTR_COEFF] + n
        env[bas[i+nh,PTR_COEFF]] /= 2 * env[bas[i,PTR_EXP]]

env[bas[5,PTR_COEFF]+0] = env[bas[1,PTR_COEFF]+0] / (2 * env[bas[1,PTR_EXP]+0])
env[bas[5,PTR_COEFF]+1] = env[bas[1,PTR_COEFF]+1] / (2 * env[bas[1,PTR_EXP]+1])
env[bas[5,PTR_COEFF]+2] = env[bas[1,PTR_COEFF]+2] / (2 * env[bas[1,PTR_EXP]+0])
env[bas[5,PTR_COEFF]+3] = env[bas[1,PTR_COEFF]+3] / (2 * env[bas[1,PTR_EXP]+1])

nfitid = nbas*2
off += n
bas[nfitid,ATOM_OF ]  = 0
bas[nfitid,ANG_OF  ]  = 0
bas[nfitid,KAPPA_OF]  = 0
bas[nfitid,NPRIM_OF]  = 1
bas[nfitid,NCTR_OF ]  = 1
bas[nfitid,PTR_EXP ]  = off
env[off+0] = 0
off += 1
bas[nfitid,PTR_COEFF] = off
env[off+0] = 2 * numpy.sqrt(numpy.pi)

nfitid1 = nbas*2 + 1
off += n
bas[nfitid1,ATOM_OF ]  = 0
bas[nfitid1,ANG_OF  ]  = 0
bas[nfitid1,KAPPA_OF]  = 0
bas[nfitid1,NPRIM_OF]  = 1
bas[nfitid1,NCTR_OF ]  = 1
bas[nfitid1,PTR_EXP ]  = off
env[off+0] = 0
off += 1
bas[nfitid1,PTR_COEFF] = off
env[off+0] = 2 * numpy.sqrt(numpy.pi)

natm = ctypes.c_int(natm)
nbas = ctypes.c_int(nbas)
c_atm = atm.ctypes.data_as(ctypes.c_void_p)
c_bas = bas.ctypes.data_as(ctypes.c_void_p)
c_env = env.ctypes.data_as(ctypes.c_void_p)

opt = ctypes.POINTER(ctypes.c_void_p)()
_cint.CINTlen_spinor.restype = ctypes.c_int



def test_int3c2e_sph(name, fnref, vref, dim, place):
    intor = getattr(_cint, name)
    intoref = getattr(_cint, fnref)
    intor.restype = ctypes.c_void_p
    op = numpy.empty(1000000*dim)
    pop = op.ctypes.data_as(ctypes.c_void_p)
    opref = numpy.empty(1000000*dim)
    pref = opref.ctypes.data_as(ctypes.c_void_p)
    v1 = 0
    for k in range(nbas.value):
        l = nfitid
        bas[l,ATOM_OF] = bas[k,ATOM_OF]
        for j in range(nbas.value):
            for i in range(nbas.value):
                di = (bas[i,ANG_OF] * 2 + 1) * bas[i,NCTR_OF]
                dj = (bas[j,ANG_OF] * 2 + 1) * bas[j,NCTR_OF]
                dk = (bas[k,ANG_OF] * 2 + 1) * bas[k,NCTR_OF]
                nd = di*dj*dk*dim
                shls = (ctypes.c_int * 4)(i, j, k, l)
                intoref(pref, shls, c_atm, natm, c_bas, nbas, c_env, opt)
                intor(pop, shls, c_atm, natm, c_bas, nbas, c_env, opt)
                if not numpy.allclose(opref[:nd], op[:nd]):
                    print 'Fail:', name, i,j,k
                v1 += abs(numpy.array(op[:nd])).sum()
    if round(abs(v1-vref), place):
        print "* FAIL: ", name, ". err:", '%.16g' % abs(v1-vref), "/", vref
    else:
        print "pass: ", name


def sf2spinor(mat, i, j, bas):
    import pyscf.symm.cg
    import scipy.linalg
    assert(mat.ndim == 3)
    l1 = bas[i,ANG_OF]
    l2 = bas[j,ANG_OF]
    d1 = bas[i,NCTR_OF]
    d2 = bas[j,NCTR_OF]
    u1a, u1b = pyscf.symm.cg.real2spinor(l1)
    u2a, u2b = pyscf.symm.cg.real2spinor(l2)
    u1a = scipy.linalg.block_diag(*((u1a,)*d1))
    u1b = scipy.linalg.block_diag(*((u1b,)*d1))
    u2a = scipy.linalg.block_diag(*((u2a,)*d2))
    u2b = scipy.linalg.block_diag(*((u2b,)*d2))
    u1 = numpy.vstack((u1a,u1b))
    u2 = numpy.vstack((u2a,u2b))
    m, n, k = mat.shape
    matab = numpy.zeros((m*2,n*2,k))
    matab[:m,:n,:] = matab[m:,n:,:] = mat
    zmat = numpy.einsum('pjk,pi->ijk', matab, u1.conj())
    zmat = numpy.einsum('ipk,pj->ijk', zmat, u2)
    return zmat

def test_int3c2e_spinor(name, fnref, vref, dim, place):
    abas = bas.copy()
    abas[:,KAPPA_OF] = 0
    c_bas = abas.ctypes.data_as(ctypes.c_void_p)
    intor = getattr(_cint, name)
    intoref = getattr(_cint, fnref)
    intor.restype = ctypes.c_void_p
    v1 = 0
    for k in range(nbas.value):
        l = nfitid
        for j in range(nbas.value):
            for i in range(nbas.value):
                di = (bas[i,ANG_OF] * 2 + 1) * bas[i,NCTR_OF]
                dj = (bas[j,ANG_OF] * 2 + 1) * bas[j,NCTR_OF]
                dk = (bas[k,ANG_OF] * 2 + 1) * bas[k,NCTR_OF]
                shls = (ctypes.c_int * 4)(i, j, k, l)
                opref = numpy.empty((di,dj,dk,dim), order='F')
                intoref(opref.ctypes.data_as(ctypes.c_void_p), shls,
                        c_atm, natm, c_bas, nbas, c_env, opt)
                zmat = sf2spinor(opref[:,:,:,0], i, j, bas)

                di = (bas[i,ANG_OF] * 4 + 2) * bas[i,NCTR_OF]
                dj = (bas[j,ANG_OF] * 4 + 2) * bas[j,NCTR_OF]
                dk = (bas[k,ANG_OF] * 2 + 1) * bas[k,NCTR_OF]
                op = numpy.empty((di,dj,dk,dim), order='F', dtype=numpy.complex)
                intor(op.ctypes.data_as(ctypes.c_void_p), shls,
                      c_atm, natm, c_bas, nbas, c_env, opt)
                if not numpy.allclose(zmat, op[:,:,:,0]):
                    print 'Fail:', name, i,j,k
                v1 += abs(numpy.array(op)).sum()
    if round(abs(v1-vref), place):
        print "* FAIL: ", name, ". err:", '%.16g' % abs(v1-vref), "/", vref
    else:
        print "pass: ", name


def test_int2c2e_sph(name, fnref, vref, dim, place):
    intor = getattr(_cint, name)
    intoref = getattr(_cint, fnref)
    intor.restype = ctypes.c_void_p
    op = numpy.empty(1000000*dim)
    pop = op.ctypes.data_as(ctypes.c_void_p)
    opref = numpy.empty(1000000*dim)
    pref = opref.ctypes.data_as(ctypes.c_void_p)
    v1 = 0
    for k in range(nbas.value):
        l = nfitid
        bas[l,ATOM_OF] = bas[k,ATOM_OF]
        for i in range(nbas.value):
            j = nfitid1
            bas[j,ATOM_OF] = bas[i,ATOM_OF]
            di = (bas[i,ANG_OF] * 2 + 1) * bas[i,NCTR_OF]
            dk = (bas[k,ANG_OF] * 2 + 1) * bas[k,NCTR_OF]
            nd = di*dk*dim
            shls = (ctypes.c_int * 4)(i, j, k, l)
            intoref(pref, shls, c_atm, natm, c_bas, nbas, c_env, opt)
            shls = (ctypes.c_int * 4)(i, k, 0, 0)
            intor(pop, shls, c_atm, natm, c_bas, nbas, c_env, opt)
            if not numpy.allclose(opref[:nd], op[:nd]):
                print 'Fail:', name, i,k
            v1 += abs(numpy.array(op[:nd])).sum()
    if round(abs(v1-vref), place):
        print "* FAIL: ", name, ". err:", '%.16g' % abs(v1-vref), "/", vref
    else:
        print "pass: ", name



if __name__ == "__main__":
    for f in (('cint3c2e_sph', 'cint2e_sph', 1586.350797432699, 1, 10),
              ('cint3c2e_ip1_sph', 'cint2e_ip1_sph', 2242.052249267909, 3, 10),
              ('cint3c2e_ip2_sph', 'cint2e_ip2_sph', 1970.982483860059, 3, 10),
             ):
        test_int3c2e_sph(*f)

    for f in (('cint3c2e_spinor', 'cint3c2e_sph', 4412.363002831547, 1, 10),
             ):
        test_int3c2e_spinor(*f)

    for f in (('cint2c2e_sph', 'cint2e_sph', 782.3104849606677, 1, 10),
              ('cint2c2e_ip1_sph', 'cint2e_ip1_sph', 394.6515972715189, 3, 10),
              ('cint2c2e_ip2_sph', 'cint2e_ip2_sph', 394.6515972715189, 3, 10),
             ):
        test_int2c2e_sph(*f)
