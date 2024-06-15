# Enum for plane types
from enum import Enum
import random


class PlaneType(Enum):
    Airbus_A319 = 0
    Airbus_A320 = 1
    Airbus_A321 = 2
    Airbus_A320neo = 3
    Airbus_A321neo = 4
    Airbus_A380 = 5
    Boeing_737 = 6
    Boeing_747 = 7
    Boeing_757 = 8
    Boeing_767 = 9
    Boeing_777 = 10
    Boeing_787 = 11
    Embraer_190 = 12
    Embraer_195 = 13
    Bombardier_CRJ700 = 14
    Bombardier_CRJ900 = 15
    Bombardier_CRJ1000 = 16
    Bombardier_CS100 = 17
    Bombardier_CS300 = 18
    Bombardier_Q400 = 19
    ATR_42 = 20
    ATR_72 = 21
    Cessna_208 = 22
    Cessna_Citation = 23


def get_random_plane_type():
    return random.choice(list(PlaneType))


def get_plane_size_for_plane_type(plane_type):
    if plane_type in [PlaneType.Airbus_A319, PlaneType.Airbus_A320, PlaneType.Airbus_A321, PlaneType.Airbus_A320neo,
                      PlaneType.Airbus_A321neo, PlaneType.Embraer_190, PlaneType.Embraer_195,
                      PlaneType.Bombardier_CRJ700, PlaneType.Bombardier_CRJ900, PlaneType.Bombardier_CRJ1000,
                      PlaneType.Bombardier_CS100, PlaneType.Bombardier_CS300, PlaneType.Bombardier_Q400,
                      PlaneType.ATR_42, PlaneType.ATR_72]:
        return 1
    elif plane_type in [PlaneType.Airbus_A380, PlaneType.Boeing_747, PlaneType.Boeing_777, PlaneType.Boeing_787]:
        return 2
    else:
        return 1


def get_number_of_seats_for_plane_type(plane_type):
    dict_with_seats = {
        PlaneType.Airbus_A319: 124,
        PlaneType.Airbus_A320: 150,
        PlaneType.Airbus_A321: 185,
        PlaneType.Airbus_A320neo: 165,
        PlaneType.Airbus_A321neo: 206,
        PlaneType.Airbus_A380: 555,
        PlaneType.Boeing_737: 149,
        PlaneType.Boeing_747: 467,
        PlaneType.Boeing_757: 200,
        PlaneType.Boeing_767: 290,
        PlaneType.Boeing_777: 396,
        PlaneType.Boeing_787: 330,
        PlaneType.Embraer_190: 114,
        PlaneType.Embraer_195: 124,
        PlaneType.Bombardier_CRJ700: 78,
        PlaneType.Bombardier_CRJ900: 90,
        PlaneType.Bombardier_CRJ1000: 104,
        PlaneType.Bombardier_CS100: 108,
        PlaneType.Bombardier_CS300: 130,
        PlaneType.Bombardier_Q400: 78,
        PlaneType.ATR_42: 48,
        PlaneType.ATR_72: 70,
        PlaneType.Cessna_208: 9,
        PlaneType.Cessna_Citation: 10
    }
    return dict_with_seats[plane_type]


def get_mayday_fuel_for_plane_type(plane_type):
    # kg of fuel needed before mayday fuel (30 mins of flight)
    dict_fuel_remaining = {
        PlaneType.Airbus_A319: 1600,
        PlaneType.Airbus_A320: 1700,
        PlaneType.Airbus_A321: 1800,
        PlaneType.Airbus_A320neo: 1800,
        PlaneType.Airbus_A321neo: 1900,
        PlaneType.Airbus_A380: 2500,
        PlaneType.Boeing_737: 1600,
        PlaneType.Boeing_747: 2500,
        PlaneType.Boeing_757: 1800,
        PlaneType.Boeing_767: 2000,
        PlaneType.Boeing_777: 2200,
        PlaneType.Boeing_787: 2000,
        PlaneType.Embraer_190: 1500,
        PlaneType.Embraer_195: 1600,
        PlaneType.Bombardier_CRJ700: 1200,
        PlaneType.Bombardier_CRJ900: 1300,
        PlaneType.Bombardier_CRJ1000: 1400,
        PlaneType.Bombardier_CS100: 1400,
        PlaneType.Bombardier_CS300: 1500,
        PlaneType.Bombardier_Q400: 1200,
        PlaneType.ATR_42: 900,
        PlaneType.ATR_72: 1000,
        PlaneType.Cessna_208: 250,
        PlaneType.Cessna_Citation: 250
    }
    return dict_fuel_remaining[plane_type]


def get_max_fuel_for_plane_type(plane_type):
    # max kg of fuel for each type of plane
    dict_max_fuel = {
        PlaneType.Airbus_A319: 21000,
        PlaneType.Airbus_A320: 24000,
        PlaneType.Airbus_A321: 26000,
        PlaneType.Airbus_A320neo: 26000,
        PlaneType.Airbus_A321neo: 29000,
        PlaneType.Airbus_A380: 320000,
        PlaneType.Boeing_737: 20000,
        PlaneType.Boeing_747: 240000,
        PlaneType.Boeing_757: 43000,
        PlaneType.Boeing_767: 91000,
        PlaneType.Boeing_777: 200000,
        PlaneType.Boeing_787: 140000,
        PlaneType.Embraer_190: 21000,
        PlaneType.Embraer_195: 24000,
        PlaneType.Bombardier_CRJ700: 11000,
        PlaneType.Bombardier_CRJ900: 12000,
        PlaneType.Bombardier_CRJ1000: 13000,
        PlaneType.Bombardier_CS100: 14000,
        PlaneType.Bombardier_CS300: 15000,
        PlaneType.Bombardier_Q400: 11000,
        PlaneType.ATR_42: 5000,
        PlaneType.ATR_72: 7000,
        PlaneType.Cessna_208: 1500,
        PlaneType.Cessna_Citation: 2000
    }
    return dict_max_fuel[plane_type]

