from os import stat_result
from typing import TYPE_CHECKING, List, Optional

from math import nan
from sqlmodel import Session, select

from .database import create_db_and_tables, engine
from .models import MPart, Magnet, MSite, MRecord, MSimulation
from .models import MaterialBase, Material, MaterialCreate, MaterialRead
from .models import MPartMagnetLink, MagnetMSiteLink
from .status import MStatus, MType

from .crud import *
from .operations import *
from .checks import *

import json

def main():
    create_db_and_tables()

# TODO: how to create objects
# create materials
# create site
# create magnet with a link to site
# create parts for a magnet

# WORKFLOWS
# add a new site:
# if magnet exist, update magnet (aka add miste to msites)
# else
#   add new magnet:
#   if part exist, update part (aka add magnet to magnets)
#   else
#       create part
#       if material exist
#       otherwise create material

# change site status:

IACS = 58.e+6

# TODO: create a clip.py

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--createdb", help="createdb", action='store_true')
    parser.add_argument("--createsite", help="createsite", action='store_true')
    parser.add_argument("--displaymagnet", help="display magnet", type=str, default=None)
    parser.add_argument("--displaymsite", help="display msite", type=str, default=None)
    parser.add_argument("--checkmaterial", help="check material data", action='store_true')
    args = parser.parse_args()

    if args.createdb:
        main()

    if args.createsite:
        with Session(engine) as session:

            '''
            m1 = create_msite(session=session, name="M19061901", conffile="MAGFILE2019.06.20.35T.conf", status="Off")
        
            Helices = create_magnet(session=session, name="HL-34", be="HL-34-001-A", geom="HL-31.yaml", status="On", msites=[m1])
            Bitters = create_magnet(session=session, name="M9Bitters", be="B_XYZ", geom="Bitters.yaml", status="On", msites=[m1])
        
            H1 = create_material(session=session, name="MA15101601", nuance="Cu5Ag5,08", Rpe=481e+6, ElectricalConductivity=52.4e+6)
            H2 = create_material(session=session, name="MA15061703", nuance="Cu5Ag5,65", Rpe=482e+6, ElectricalConductivity=53.3e+6)
            H3 = create_material(session=session, name="MA15061801", nuance="Cu5Ag5,65", Rpe=496e+6, ElectricalConductivity=52.6e+6)
            H4 = create_material(session=session, name="MA15100501", nuance="Cu5Ag5,08", Rpe=508e+6, ElectricalConductivity=52.8e+6)
            H5 = create_material(session=session, name="MA15101501", nuance="Cu5Ag5,08", Rpe=506e+6, ElectricalConductivity=53.1e+6)
            H6 = create_material(session=session, name="MA18060101", nuance="Cu5Ag5,35", Rpe=0, ElectricalConductivity=53.2e+6)
            H7 = create_material(session=session, name="MA18012501", nuance="Cu5Ag5,09", Rpe=0, ElectricalConductivity=53.1e+6)
            H8 = create_material(session=session, name="MA18051801", nuance="Cu5Ag5,22", Rpe=0, ElectricalConductivity=51.9e+6)
            H9 = create_material(session=session, name="MA18101201", nuance="Cu5Ag5,08", Rpe=0, ElectricalConductivity=53.7e+6)
            H10 = create_material(session=session, name="MA18110501", nuance="Cu5Ag5,08", Rpe=0, ElectricalConductivity=53.3e+6)
            H11 = create_material(session=session, name="MA19012101", nuance="Cu5Ag5,5", Rpe=0, ElectricalConductivity=53.8e+6)
            H12 = create_material(session=session, name="MA19011601", nuance="Cu5Ag5,5", Rpe=0, ElectricalConductivity=53.2e+6)
            H13 = create_material(session=session, name="MA10061702", nuance="CuCrZr", Rpe=366e+6, ElectricalConductivity=46.5e+6)
            H14 = create_material(session=session, name="MA10061703", nuance="CuCrZr", Rpe=373e+6, ElectricalConductivity=50.25e+6)
        
            create_mpart(session=session, name='H15101601', mtype=MType.Helix, be='HL-34-001-A', geom='HL-31_H1.yaml', status=MStatus.operation, magnets=[Helices], material=H1)
            create_mpart(session=session, name='H15061703', mtype=MType.Helix, be='HL-34-003-A', geom='HL-31_H2.yaml', status=MStatus.operation, magnets=[Helices], material=H2)
            create_mpart(session=session, name='H15061801', mtype=MType.Helix, be='HL-34-005-A', geom='HL-31_H3.yaml', status=MStatus.operation, magnets=[Helices], material=H3)
            create_mpart(session=session, name='H15100501', mtype=MType.Helix, be='HL-34-007-A', geom='HL-31_H4.yaml', status=MStatus.operation, magnets=[Helices], material=H4)
            create_mpart(session=session, name="H15101501", mtype=MType.Helix, be='HL-34-009-A', geom='HL-31_H5.yaml', status=MStatus.operation, magnets=[Helices], material=H5)
            create_mpart(session=session, name="H18060101", mtype=MType.Helix, be='HL-34-011-A', geom='HL-31_H6.yaml', status=MStatus.operation, magnets=[Helices], material=H6)
            create_mpart(session=session, name="H18012501", mtype=MType.Helix, be='HL-34-013-A', geom='HL-31_H7.yaml', status=MStatus.operation, magnets=[Helices], material=H7)
            create_mpart(session=session, name="H18051801", mtype=MType.Helix, be='HL-34-015-A', geom='HL-31_H8.yaml', status=MStatus.operation, magnets=[Helices], material=H8)
            create_mpart(session=session, name="H18101201", mtype=MType.Helix, be='HL-34-017', geom='HL-31_H9.yaml', status=MStatus.operation, magnets=[Helices], material=H9)
            create_mpart(session=session, name="H18110501", mtype=MType.Helix, be='HL-34-019', geom='HL-31_H10.yaml', status=MStatus.operation, magnets=[Helices], material=H10)
            create_mpart(session=session, name="H19012101", mtype=MType.Helix, be='HL-34-021', geom='HL-31_H11.yaml', status=MStatus.operation, magnets=[Helices], material=H11)
            create_mpart(session=session, name="H19011601", mtype=MType.Helix, be='HL-34-023', geom='HL-31_H12.yaml', status=MStatus.operation, magnets=[Helices], material=H12)
            create_mpart(session=session, name="H10061702", mtype=MType.Helix, be='HR-21-125-A', geom='HL-31_H13.yaml', status=MStatus.operation, magnets=[Helices], material=H13)
            create_mpart(session=session, name="H10061703", mtype=MType.Helix, be='HR-21-127-A', geom='HL-31_H14.yaml', status=MStatus.operation, magnets=[Helices], material=H14)

            # Rings
            R1 = create_material(session=session, name="MA20072301", nuance="CuNiBe", Rpe=568e+6, ElectricalConductivity=0)
            R2 = create_material(session=session, name="MA20072304", nuance="CuCrZr", Rpe=324e+6, ElectricalConductivity=0)
            R3 = create_material(session=session, name="MA20072302", nuance="CuCrZr", Rpe=343e+6, ElectricalConductivity=80*IACS/100.) # !! % IACS
            R4 = create_material(session=session, name="MA20072303", nuance="CuCrZr", Rpe=357e+6, ElectricalConductivity=81.7*IACS/100.) # !! % IACS
            R5 = create_material(session=session, name="MA21040901", nuance="CuCrZr", Rpe=0, ElectricalConductivity=0)
            R6 = create_material(session=session, name="MARING", nuance="CuCrZr", Rpe=0, ElectricalConductivity=0)

            create_mpart(session=session, name="B20061903", mtype=MType.Ring, be='HL-27-029-G', geom='Ring-H1H2.yaml', status=MStatus.operation, magnets=[Helices], material=R1)
            create_mpart(session=session, name="B20061904", mtype=MType.Ring, be='HL-27-030-D', geom='Ring-H2H3.yaml', status=MStatus.operation, magnets=[Helices], material=R2)
            create_mpart(session=session, name="B20061901", mtype=MType.Ring, be='HL-27-031-C', geom='Ring-H3H4.yaml', status=MStatus.operation, magnets=[Helices], material=R3)
            create_mpart(session=session, name="B20061902", mtype=MType.Ring, be='HL-27-032-C', geom='Ring-H4H5.yaml', status=MStatus.operation, magnets=[Helices], material=R4)
            create_mpart(session=session, name="B20061902", mtype=MType.Ring, be='HL-27-033-C', geom='Ring-H5H6.yaml', status=MStatus.operation, magnets=[Helices], material=R5)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-034-C', geom='Ring-H6H7.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-035-C', geom='Ring-H7H8.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-036-C', geom='Ring-H8H9.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-037-C', geom='Ring-H9H10.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-038-C', geom='Ring-H10H11.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-039-C', geom='Ring-H11H12.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-040-C', geom='Ring-H12H13.yaml', status=MStatus.operation, magnets=[Helices], material=R6)
            create_mpart(session=session, name="B21040901", mtype=MType.Ring, be='HL-27-041-C', geom='Ring-H13H14.yaml', status=MStatus.operation, magnets=[Helices], material=R6)

            # Rings: HL-27-xx
            # 029 030 031  032 033 034 035 036 037 038 039 040 041
            # BP  HP  HP   BP  HP  BP  HP  BP  HP  BP  HP  BP  HP
        
            # CurrentLeads
            L1 = create_material(session=session, name="MALINNER", nuance="Cu", Rpe=0, ElectricalConductivity=58.0e+6)
            L2 = create_material(session=session, name="MALOUTER", nuance="Cu", Rpe=0, ElectricalConductivity=58.0e+6)
            
            #m2 = create_msite(session=session, name="HM20022001", conffile="MAGFILEM20022001b.conf", status="On")
            #Helices = duplicate_magnet(session=session, iname="HL-34", oname="HM20022001")
            # meme chose que Helices de m1 sauf pour la derniere

            # create new mpart
            H14 = create_material(session=session, name="MA19022701", nuance="CuAg5.5", Rpe=500e+6, ElectricalConductivity=52.e+6)
            create_mpart(session=session, name="H20020501", mtype=MType.Helix, be='HR-21-127-A', geom='HL-31_H14.yaml', status=MStatus.operation, magnets=[], material=H4)
            magnet_replace_mpart(session=session, name="HM20022001", impart="H10061703", ompart='H20020501')
            magnet_add_msite(session=session, magnet=Helices, msite=m2)
            # add Bitters to m2

            #m1 = create_msite(session=session, name="TestSite", conffile="MAGFILE2021.07.19.conf", status="On")
            # add Bitters to m2
            '''

            ####################
            # Test
            # Insert Two Helices
            m1 = create_msite(session=session, name="MTest", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.defunct)
        
            Helices = create_magnet(session=session, name="HL-test", be="HL-34-001-A", geom="test.yaml", status=MStatus.operation, msites=[m1])

            MAT_TEST1 = create_material(session=session, name="MAT_TEST1", nuance="Cu5Ag5,08",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)

            create_mpart(session=session, name='HL-34_H1', mtype=MType.Helix, be='HL-34-001-A', geom='HL-31_H1.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST1)
            create_mpart(session=session, name='HL-34_H2', mtype=MType.Helix, be='HL-34-001-A', geom='HL-31_H2.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST1)
            
            MAT_TEST2 = create_material(session=session, name="MAT_TEST2", nuance="Cu5Ag5,08",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)
            create_mpart(session=session, name="Ring-H1H2", mtype=MType.Ring, be="HL-34-001-A", geom='Ring-H1H2.yaml', status=MStatus.operation, magnets=[Helices], material=MAT_TEST2)
            ####################

            ####################
            # M19061901
            ####################

            # Definition of Site
            m2 = create_msite(session=session, name="M10", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.operation)

            # Definition of M19061901 magnet
            M19061901 = create_magnet(session=session, name="M19061901", be="unknow", geom="HL-31.yaml", status=MStatus.operation, msites=[m2])
            Bitters = create_magnet(session=session, name="M9Bitters", be="B_XYZ", geom="M9Bitters.yaml", status=MStatus.operation, msites=[m2])
            CuAg01 = create_material(session=session, name="B_CuAg01", nuance="CuAg01",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=380, alpha=3.6e-3, ElectricalConductivity=50.1e+6,
                                    ThermalConductivity=360, MagnetPermeability=1, Young=127e+9, Poisson=0.335,  CoefDilatation=18e-6,
                                    Rpe=481000000.0)
            create_mpart(session=session, name='M9Bi', mtype=MType.Bitter, be='BI-03-002-A', geom='M9Bitters_Bi.yaml', status=MStatus.operation, magnets=[Bitters], material=CuAg01)
            create_mpart(session=session, name='M9Be', mtype=MType.Bitter, be='BE-03-002-A', geom='M9Bitters_Be.yaml', status=MStatus.operation, magnets=[Bitters], material=CuAg01)

            m1 = create_msite(session=session, name="MTest2", conffile="MAGFILE2019.06.20.35T.conf", status=MStatus.defunct)
            msite_add_magnet(session=session, msite=m1, magnet=Helices)
            msite_add_magnet(session=session, msite=m1, magnet=Bitters)
            
            # TODO : SpecificHeat, Rpe, nan for sigma_isolant

            # Definition of Materials
            MA15101601 = create_material(session=session, name="MA15101601", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=52.4e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=481)  # H1
            MA15061703 = create_material(session=session, name="MA15061703", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.3e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=482)  # H2
            MA15061801 = create_material(session=session, name="MA15061801", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=52.6e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=496)  # H3
            MA15100501 = create_material(session=session, name="MA15100501", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=52.8e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=508)  # H4
            MA15101501 = create_material(session=session, name="MA15101501", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.1e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=506)  # H5
            MA18060101 = create_material(session=session, name="MA18060101", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.2e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=512)  # H6
            MA18012501 = create_material(session=session, name="MA18012501", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.1e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=500)  # H7
            MA18051801 = create_material(session=session, name="MA18051801", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=51.9e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=512)  # H8
            MA18101201 = create_material(session=session, name="MA18101201", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.7e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=500)  # H9
            MA18110501 = create_material(session=session, name="MA18110501", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.3e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=500)  # H10
            MA19012101 = create_material(session=session, name="MA19012101", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.8e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=500)  # H11
            MA19011601 = create_material(session=session, name="MA19011601", nuance="CuAg5.5",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.6e-3, ElectricalConductivity=53.2e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=500)  # H12
            MA10061702 = create_material(session=session, name="MA10061702", nuance="CuCrZr",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.4e-3, ElectricalConductivity=46.5e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=366)  # H13
            MA10061703 = create_material(session=session, name="MA10061703", nuance="CuCrZr",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.4e-3, ElectricalConductivity=50.25e+6,
                                    ThermalConductivity=380, MagnetPermeability=1, Young=117e+9, Poisson=0.33, CoefDilatation=18e-6,
                                    Rpe=373)  # H14

            MAT1_RING = create_material(session=session, name="MAT1_RING", nuance="unknow",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.4e-3, ElectricalConductivity=41e+6,
                                    ThermalConductivity=320, MagnetPermeability=1, Young=131e+9, Poisson=0.3, CoefDilatation=17e-6,
                                    Rpe=0)  # R1, R2
            MAT2_RING = create_material(session=session, name="MAT2_RING", nuance="unknow",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.4e-3, ElectricalConductivity=50e+6,
                                    ThermalConductivity=320, MagnetPermeability=1, Young=131e+9, Poisson=0.3, CoefDilatation=17e-6,
                                    Rpe=0)  # R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, R13
            MAT_LEAD = create_material(session=session, name="MAT_LEAD", nuance="unknow",
                                    Tref=293, VolumicMass=9e+3, SpecificHeat=0, alpha=3.4e-3, ElectricalConductivity=58.0e+6,
                                    ThermalConductivity=390, MagnetPermeability=1, Young=131e+9, Poisson=0.3, CoefDilatation=17e-6,
                                    Rpe=0)  # il1 ol2
            MAT_ISOLANT = create_material(session=session, name="MAT_ISOLANT", nuance="unknow",
                                    Tref=nan, VolumicMass=2e+3, SpecificHeat=0, alpha=nan, ElectricalConductivity=0,
                                    ThermalConductivity=1.2, MagnetPermeability=1, Young=2.1e9, Poisson=0.21, CoefDilatation=9e-6,
                                    Rpe=0)

            # Definition of mparts

            # Helices
            create_mpart(session=session, name='H15101601', mtype=MType.Helix, be='HL-34-002-A',  geom='HL-31_H1.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA15101601)
            create_mpart(session=session, name='H15061703', mtype=MType.Helix, be='HL-34-004-A',  geom='HL-31_H2.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA15061703)
            create_mpart(session=session, name='H15061801', mtype=MType.Helix, be='HL-34-006-A',  geom='HL-31_H3.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA15061801)
            create_mpart(session=session, name='H15100501', mtype=MType.Helix, be='HL-34-008-A',  geom='HL-31_H4.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA15100501)
            create_mpart(session=session, name='H15101501', mtype=MType.Helix, be='HL-34-0010-A', geom='HL-31_H5.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA15101501)
            create_mpart(session=session, name='H18060101', mtype=MType.Helix, be='HL-34-0012-A', geom='HL-31_H6.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA18060101)
            create_mpart(session=session, name='H18012501', mtype=MType.Helix, be='HL-34-0014-A', geom='HL-31_H7.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA18012501)
            create_mpart(session=session, name='H18051801', mtype=MType.Helix, be='HL-34-0016-A', geom='HL-31_H8.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA18051801)
            create_mpart(session=session, name='H19060601', mtype=MType.Helix, be='HL-34-0018',   geom='HL-31_H9.yaml',  status=MStatus.operation, magnets=[M19061901], material=MA18101201)
            create_mpart(session=session, name='H19060602', mtype=MType.Helix, be='HL-34-0020',   geom='HL-31_H10.yaml', status=MStatus.operation, magnets=[M19061901], material=MA18110501)
            create_mpart(session=session, name='H19061201', mtype=MType.Helix, be='HL-34-0022',   geom='HL-31_H11.yaml', status=MStatus.operation, magnets=[M19061901], material=MA19012101)
            create_mpart(session=session, name='H19060603', mtype=MType.Helix, be='HL-34-0024',   geom='HL-31_H12.yaml', status=MStatus.operation, magnets=[M19061901], material=MA19011601)
            create_mpart(session=session, name='H10061702', mtype=MType.Helix, be='HR-21-126-A',  geom='HL-31_H13.yaml', status=MStatus.operation, magnets=[M19061901], material=MA10061702)
            create_mpart(session=session, name='H10061703', mtype=MType.Helix, be='HR-21-128-A',  geom='HL-31_H14.yaml', status=MStatus.operation, magnets=[M19061901], material=MA10061703)

            # Rings
            create_mpart(session=session, name='M19061901_R1',  mtype=MType.Ring, be='unknow', geom='Ring-H1H2.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT1_RING)
            create_mpart(session=session, name='M19061901_R2',  mtype=MType.Ring, be='unknow', geom='Ring-H2H3.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT1_RING)
            create_mpart(session=session, name='M19061901_R3',  mtype=MType.Ring, be='unknow', geom='Ring-H3H4.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R4',  mtype=MType.Ring, be='unknow', geom='Ring-H4H5.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R5',  mtype=MType.Ring, be='unknow', geom='Ring-H5H6.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R6',  mtype=MType.Ring, be='unknow', geom='Ring-H6H7.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R7',  mtype=MType.Ring, be='unknow', geom='Ring-H7H8.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R8',  mtype=MType.Ring, be='unknow', geom='Ring-H8H9.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R9',  mtype=MType.Ring, be='unknow', geom='Ring-H9H10.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R10', mtype=MType.Ring, be='unknow', geom='Ring-H10H11.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R11', mtype=MType.Ring, be='unknow', geom='Ring-H11H12.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R12', mtype=MType.Ring, be='unknow', geom='Ring-H12H13.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)
            create_mpart(session=session, name='M19061901_R13', mtype=MType.Ring, be='unknow', geom='Ring-H13H14.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT2_RING)

            # Leads
            create_mpart(session=session, name='M19061901_iL1', mtype=MType.Lead, be='unknow', geom='inner.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT_LEAD)
            create_mpart(session=session, name='M19061901_oL2', mtype=MType.Lead, be='unknow', geom='outer-H14.yaml', status=MStatus.operation, magnets=[M19061901], material=MAT_LEAD)

            
            # load appenv
            from python_magnetsetup.config import appenv
            MyEnv = appenv()
            if args.debug: print(MyEnv.template_path())

            # MRecords
            # list files from /data/mrecords attached them to msite=M19061901
            from .crud import create_mrecord
            from pathlib import Path
            p = Path(MyEnv.mrecord_repo)
            filelist = [x for x in p.iterdir() if x.is_file()]
            print("mrecords list:", filelist)
            for item in filelist:
                data = item.split('_')
                tformat="%Y.%m.%d---%H:%M:%S"
                rtimestamp = datetime.datetime.strptime(data[1].replace('.txt',''), tformat)
                msite_name = M19061901.name
                msite_id = M19061901.id
                print("housing:", data[0], "timestamp:", rtimestamp, "msite:", msite_name, msite_id) 
                # create_mrecord(session=session, msite_id=msite_id, rtimestamp=rtimestamp)
            
    if args.displaymagnet:
        with Session(engine) as session:
            mdata = get_magnet_data(session, args.displaymagnet)
            with open(args.displaymagnet + "-data.json", "x") as out:
                out.write(json.dumps(mdata, indent = 4))
            
    if args.displaymsite:
        import yaml
        with Session(engine) as session:
            mdata = get_msite_data(session, args.displaymsite)
            with open(args.displaymsite + "-data.yaml", "x") as out:
                out.write("!<MSite>\n")
                yaml.dump(mdata, out)
            
            

    if args.checkmaterial:
        with Session(engine) as session:
            statement = select(Material)
            materials = session.exec(statement).all()
            print("\n=== Checking material data consistency ===")
            for material in materials:
                undef_set = check_material(session, material.id)
                if undef_set:
                    print(material.name, ":", check_material(session, material.id))

