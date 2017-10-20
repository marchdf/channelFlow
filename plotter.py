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

    fdir = os.path.abspath('./coarse')
    rdir = os.path.abspath(os.path.join(fdir, 'results'))
    yname = os.path.join(fdir, 'channelFlow.i')
    bname = os.path.join(fdir, 'bottomwall.dat')
    tname = os.path.join(fdir, 'topwall.dat')
    mname = os.path.join(fdir, 'mdot.dat')
    rho0, mu = parse_ic(yname)

    # ========================================================================
    # inlet flux
    mdf = pd.read_csv(mname)
    mdf['mdot'] = rho0 * mdf['uavg']

    plt.figure(0)
    p = plt.plot(mdf['time'],
                 mdf['mdot'],
                 ls='-',
                 lw=2,
                 color=cmap[0])
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
    plt.tight_layout()
    #plt.savefig('mdot.pdf', format='pdf')
    plt.savefig('mdot.png', format='png')

    plt.figure(1)
    ax = plt.gca()
    plt.xlabel(r"$t~[s]$", fontsize=22, fontweight='bold')
    plt.ylabel(r"$\overline{u}$", fontsize=22, fontweight='bold')
    plt.setp(ax.get_xmajorticklabels(), fontsize=18, fontweight='bold')
    plt.setp(ax.get_ymajorticklabels(), fontsize=18, fontweight='bold')
    # ax.set_xlim([0, 1.2])
    # ax.set_ylim([1, 5])
    plt.tight_layout()
    #plt.savefig('uavg.pdf', format='pdf')
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
    #plt.savefig('tau_wall.pdf', format='pdf')
    plt.savefig('tau_wall.png', format='png')
