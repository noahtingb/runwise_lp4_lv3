import numpy as np
import biglimpcopy1.Solweig1D_2020a_calc as so
import biglimpcopy1.clearnessindex_2013b as ci
import biglimpcopy1.PET_calculations as p
import biglimpcopy1.sun_position as sp
import datetime

def indexflask(form):
        month = int(form["month"])
        day = int(form["day"])
        hour = int(form["hour"])
        year = int(form["year"])
        minu = 30
        Ta = float(form["Ta"])        
        RH = float(form["RH"])
        Ws = float(form["Ws"])
        location = form["loc"]

        if month > 12 or month < 0:
            print("petresult.html","Incorrect month filled in")
        if day > 31 or day < 0:
            print("petresult.html","Incorrect day filled in")
        if hour > 23 or hour < 0:
            print("petresult.html","Incorrect hour filled in")
        if Ta > 60 or Ta < -75:
            print("petresult.html", "Unreasonable air temperature filled in",Ta)
        if RH > 100 or RH < 0:
            print("petresult.html", "Unreasonable relative humidity filled in")
        if Ws > 100 or Ws < 0:
            print("petresult.html", "Unreasonable Wind speed filled in")
 
        # Main calculation
        if Ta is not None and RH is not None and Ws is not None:
            Tmrt, resultPET, _ = petcalc(Ta, RH, Ws, 0, year, month, day, hour, minu,location)
        return resultPET,Tmrt

def petcalc(Ta, RH, Ws, radG, year, month, day, hour, minu,location):
#    sh = 1.  # 0 if shadowed by building
#    vegsh = 1.  # 0 if shadowed by tree

    # Location and time settings. Should be moved out later on

    # Human parameter data. Should maybe be move out later on
    
    pos = 0
    if pos == 0:
        Fside = 0.22
        Fup = 0.06
        Fcyl = 0.28
    else:
        Fside = 0.166666
        Fup = 0.166666
        Fcyl = 0.2

    # main loop
    # Nocturnal cloudfraction from Offerle et al. 2003
    #cant have this funktion with this data
    #absK = 0.70
    #absL = 0.95
    Tmrt = so.Solweig1D_2020a_calc(Fside, Fup, Fcyl,location,Ta, RH, year, month, day, hour, minu)

    # Recalculating wind speed based on pwerlaw
    WsPET = (1.1 / 10) ** 0.2 * Ws
    mbody = 75.
    ht = 180 / 100.
    clo = 0.9
    age = 35
    activity = 80.
    sex = 1
    resultPET = p._PET(Ta, RH, Tmrt, WsPET, mbody, age, ht, activity, clo, sex)

    return Tmrt, resultPET, None

def day_of_year(yyyy, month, day):
    if (yyyy % 4) == 0 and ( ((yyyy % 100)==0 and (yyyy % 400) == 0) or ((yyyy % 100)!=0)):
        dayspermonth = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    else:
        dayspermonth = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(dayspermonth[0:month - 1]) + day
