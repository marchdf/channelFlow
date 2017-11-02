#!/usr/bin/env python3

# ========================================================================
#
# Imports
#
# ========================================================================
import argparse
import sys
import os
import glob
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import yaml
from netCDF4 import Dataset, chartostring


# ========================================================================
#
# Some defaults variables
#
# ========================================================================
plt.rc('text', usetex=True)
plt.rc('font', family='serif', serif='Times')
cmap_med = ['#F15A60', '#7AC36A', '#5A9BD4', '#FAA75B',
            '#9E67AB', '#CE7058', '#D77FB4', '#737373']
cmap = ['#EE2E2F', '#008C48', '#185AA9', '#F47D23',
        '#662C91', '#A21D21', '#B43894', '#010202']
dashseq = [(None, None), [10, 5], [10, 4, 3, 4], [
    3, 3], [10, 4, 3, 4, 3, 4], [3, 3], [3, 3]]
markertype = ['s', 'd', 'o', 'p', 'h']


# ========================================================================
#
# Function definitions
#
# ========================================================================
def parse_ic(fname):
    """Parse the Nalu yaml input file for the initial conditions"""
    with open(fname, 'r') as stream:
        try:
            dat = yaml.load(stream)
            rho0 = float(dat['realms'][0]['material_properties']
                         ['specifications'][0]['value'])
            mu = float(dat['realms'][0]['material_properties']
                       ['specifications'][1]['value'])

            return rho0, mu

        except yaml.YAMLError as exc:
            print(exc)


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == '__main__':

    # ========================================================================
    # Parse arguments
    parser = argparse.ArgumentParser(
        description='A simple plot tool')
    parser.add_argument(
        '-s', '--show', help='Show the plots', action='store_true')
    args = parser.parse_args()

    fdir = os.path.abspath('./coarse_smag')
    rdir = os.path.abspath(os.path.join(fdir, 'results'))
    yname = os.path.join(fdir, 'channelFlow.i')
    bname = os.path.join(fdir, 'bottomwall.dat')
    tname = os.path.join(fdir, 'topwall.dat')
    mname = os.path.join(fdir, 'mdot.dat')
    delta = 1
    height = 2 * delta
    rho0, mu = parse_ic(yname)
    Re_tau = 550
    utau = (mu * Re_tau) / (rho0 * delta)
    tau_wall = rho0 * utau**2
    kappa = 0.40

    # ========================================================================
    # inlet flux
    mdf = pd.read_csv(mname)
    mdf['mdot'] = rho0 * mdf['uavg']

    plt.figure(0)
    p = plt.plot(mdf['time'],
                 mdf['mdot'],
                 ls='-',
                 lw=2,
                 color=cmap[0],
                 label='Nalu')
    p[0].set_dashes(dashseq[0])

    plt.figure(1)
    p = plt.plot(mdf['time'],
                 mdf['vavg'],
                 ls='-',
                 lw=2,
                 color=cmap[0],
                 label='v')
    p[0].set_dashes(dashseq[0])
    p = plt.plot(mdf['time'],
                 mdf['wavg'],
                 ls='-',
                 lw=2,
                 color=cmap[1],
                 label='w')
    p[0].set_dashes(dashseq[1])

    # ========================================================================
    # tau wall
    area = 2 * np.pi * np.pi
    bdf = pd.read_csv(bname, delim_whitespace=True)
    tdf = pd.read_csv(tname, delim_whitespace=True)

    bdf['tau_wall'] = np.sqrt(bdf['Fvx']**2
                              + bdf['Fvy']**2
                              + bdf['Fvz']**2) / area
    tdf['tau_wall'] = np.sqrt(tdf['Fvx']**2
                              + tdf['Fvy']**2
                              + tdf['Fvz']**2) / area

    plt.figure(2)
    p = plt.plot(bdf['Time'],
                 bdf['tau_wall'],
                 ls='-',
                 lw=2,
                 color=cmap[0],
                 label='Bottom')
    p[0].set_dashes(dashseq[0])
    p = plt.plot(tdf['Time'],
                 tdf['tau_wall'],
                 ls='-',
                 lw=2,
                 color=cmap[1],
                 label='Top')
    p[0].set_dashes(dashseq[1])

    # ========================================================================
    # Reference data

    # Integrate velocity profile
    yph = (2.0 * delta) * utau * rho0 / mu
    C = (1.0 / kappa * np.log(1.0 + kappa * yph)) / (1 - np.exp(- yph / 11.0) -
                                                     yph / 11.0 * np.exp(- yph / 3.0)) + np.log(kappa) / kappa
    y = np.linspace(0, height, 500)
    yp = np.minimum(y, height - y) * utau * rho0 / mu
    reichardt = (1.0 / kappa * np.log(1.0 + kappa * yp)) + (C - np.log(kappa) /
                                                            kappa) * (1 - np.exp(- yp / 11.0) - yp / 11.0 * np.exp(- yp / 3.0))
    mdot_ref = rho0 * utau * np.trapz(reichardt, x=y) / height

    plt.figure(0)
    p = plt.plot([0, mdf['time'].iloc[-1]],
                 [mdot_ref, mdot_ref],
                 ls='-',
                 lw=2,
                 color=cmap[-1],
                 label='Reichardt')

    # Moser DNS data
    fname = 'refdata/chan590.means'
    df = pd.read_csv(fname,
                     delim_whitespace=True,
                     comment='#',
                     header=None,
                     names=['y', 'yplus', 'Umean', 'dUmeandy', 'Wmean',  'dWmeandy', 'Pmean'])

    mdot_dns = rho0 * utau * np.trapz(df['Umean'], x=df['y'])

    plt.figure(0)
    p = plt.plot([0, mdf['time'].iloc[-1]],
                 [mdot_dns, mdot_dns],
                 ls='-',
                 lw=2,
                 color=cmap[-2],
                 label='DNS 590')

    plt.figure(2)
    p = plt.plot([0, tdf['Time'].iloc[-1]],
                 [tau_wall, tau_wall],
                 ls='-',
                 lw=2,
                 color=cmap[-1],
                 label='Ref.')

    # ======================================================================
    # Format the plots
    plt.figure(0)
    ax = plt.gca()
    plt.xlabel(r"$t~[s]$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$\dot{m}$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    # ax.set_xlim([0, 1.2])
    # ax.set_ylim([1, 5])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    # plt.savefig('mdot.pdf', format='pdf')
    plt.savefig('mdot.png', format='png')

    plt.figure(1)
    ax = plt.gca()
    plt.xlabel(r"$t~[s]$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$\overline{u}$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    # ax.set_xlim([0, 1.2])
    # ax.set_ylim([1, 5])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    # plt.savefig('uavg.pdf', format='pdf')
    plt.savefig('uavg.png', format='png')

    plt.figure(2)
    ax = plt.gca()
    plt.xlabel(r"$t~[s]$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$\tau_w$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    # ax.set_xlim([0, 1.2])
    # ax.set_ylim([1, 5])
    legend = ax.legend(loc='best')
    plt.tight_layout()
    # plt.savefig('tau_wall.pdf', format='pdf')
    plt.savefig('tau_wall.png', format='png')
