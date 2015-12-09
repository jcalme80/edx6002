# 6.00.2x Problem Set 4

import numpy
import random
import pylab
from ps3b import *

#
# PROBLEM 1
#        
def simulationDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 1.

    Runs numTrials simulations to show the relationship between delayed
    treatment and patient outcome using a histogram.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    timeBeforeTreatment=0
    numViruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    resistances={'guttagonol': False}
    clearProb = 0.05
    mutProb=0.005
    numTrials = numTrials
    totalPopResults = []



    for trial in range(0,numTrials):
        viruses = []
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb,clearProb, resistances, mutProb))
        patient = TreatedPatient(viruses, maxPop)

        for step in range(0, timeBeforeTreatment):
            patient.update()


        patient.addPrescription("guttagonol")

        for step in range(timeBeforeTreatment, timeBeforeTreatment + 150):
            patient.update()

        totalPopResults.append(patient.getTotalPop())



    pylab.hist(totalPopResults, bins=20)
    pylab.xlabel("Virus Population")
    pylab.ylabel("# Trials w/ Result")
    pylab.title("Delayed Treatment Simulation")
    pylab.legend()

    pylab.show()





#
# PROBLEM 2
#
def simulationTwoDrugsDelayedTreatment(numTrials):
    """
    Runs simulations and make histograms for problem 2.

    Runs numTrials simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    300, 150, 75, 0 timesteps between adding drugs (followed by an additional
    150 timesteps of simulation).

    numTrials: number of simulation runs to execute (an integer)
    """

    timeBeforeTreatment=150
    timeBetweenTreatments=75
    numViruses = 100
    maxPop = 1000
    maxBirthProb = 0.1
    resistances={'guttagonol': False, 'grimpex': False}
    clearProb = 0.05
    mutProb=0.005
    numTrials = numTrials
    totalPopResults = []



    for trial in range(0,numTrials):
        viruses = []
        for i in range(numViruses):
            viruses.append(ResistantVirus(maxBirthProb,clearProb, resistances, mutProb))
        patient = TreatedPatient(viruses, maxPop)

        for step in range(0, timeBeforeTreatment):
            patient.update()


        patient.addPrescription("guttagonol")

        for step in range(timeBeforeTreatment, timeBeforeTreatment + timeBetweenTreatments):
            patient.update()

        patient.addPrescription('grimpex')

        for step in range(timeBeforeTreatment + timeBetweenTreatments, timeBeforeTreatment + timeBetweenTreatments + 150):
            patient.update()

        totalPopResults.append(patient.getTotalPop())



    pylab.hist(totalPopResults, bins=20)
    pylab.xlabel("Virus Population")
    pylab.ylabel("# Trials w/ Result")
    pylab.title("Two Drugs Delayed Treatment Simulation")
    pylab.legend()

    pylab.show()


simulationTwoDrugsDelayedTreatment(100)
