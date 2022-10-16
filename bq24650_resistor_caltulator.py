#######################################################
#     Spiros Daskalakis                               #
#     last Revision: 15/1-/2022                       #
#     Python Version:  3.7                            #
#     Email: daskalakispiros@gmail.com                #
#######################################################

# LIPO BATTERIES LIMITS
# Source: https://blog.ampow.com/lipo-voltage-chart/
# 2 cell
lipo_bat_2s_100pc_charged = 8.4
lipo_bat_2s_50pc_charged = 7.67
lipo_bat_2s_thres = 7.41
# 3 cell
lipo_bat_3s_100pc_charged = 12.6
lipo_bat_3s_50pc_charged = 11.51
lipo_bat_3s_thres = 11.1

# For maximum cycle life, the end-of-charge voltage threshold could be lowered 100mV
Vbat = lipo_bat_2s_100pc_charged - 0.1

# BQ24650
# Maximum Power Point Tracking (MPPT) capability
# by input Voltage regulation
# • Programmable MPPT setting
# • 5-V to 28-V Input solar panel
# • 600-kHz NMOS-NMOS Synchronous buck controller
# Supports a battery from 2.1 V to 26 V with VFB set to a 2.1V feedback reference

Vin_min = 5
Vin_max = 28
Vin_nom = 6

# Battery Voltage Regulation
R2_top = 499e3
R1_bot = 100e3
VFB = 2.1
Vbat = VFB * (1 + R2_top / R1_bot)
print('calculated Vbat (V):', Vbat)

# Input Voltage Regulation
R3_top = 499e3
R4_bot = 36e3
V_MPPSET = 1.2 * (1 + R3_top / R4_bot)
print('calculated V_MPPSET (V):', V_MPPSET)

# Battery Current Regulation
R_SR = 0.02
I_CHARGE = 40e-3 / R_SR
print('calculated I_CHARGE (A):', I_CHARGE)
# Battery Precharge
I_PRECHARGE = 4e-3 / R_SR
print('calculated I_PRECHARGE (A):', I_PRECHARGE)

# Input Overvoltage Protection (ACOV)
# Once the adapter voltage reaches the ACOV threshold, charge is disabled.
V_ACOV = 32
print('Input Overvalue Protection (V):', V_ACOV)

# Input Undervoltage Lockout (UVLO)
# When VCC is below the UVLO threshold, all circuits on the IC, including VREF LDO, are disabled.
V_UVLO = 3.85
print('Input Undervalue Lockout (V):', V_UVLO)

# Battery Overvoltage Protection
# The converter does not allow the high-side FET to turn on until the BAT voltage goes below 102% of the regulation voltage.
# A current sink from SRP to GND is on to discharge the stored energy on the output capacitors.
V_OV_FALL = Vbat * 102 / 100
print('Battery Overvoltage Protection (V):', V_OV_FALL)

# Temperature Qualification
# To initiate a charge cycle, the battery temperature must be within the VLTF to VHTF thresholds. If battery
# temperature is outside of this range, the controller suspends charge and waits until the battery temperature is
# within the VLTF to VHTF range.

# 103AT NTC thermistor
# THERMISTOR COMPARATOR LIMITS
VREF = 3.3
VLTF = VREF * 73.5 / 100
VLTF_HYS = VREF * 0.4 / 100
VHTF = VREF * 47.5 / 100
VTCO = VREF * 45 / 100

RTHrm_cold = 40e3
RTHrm_hot = 100e3
RT2_bot = (VREF * RTHrm_cold * RTHrm_hot * ((1 / VLTF) - (1 / VTCO))) / (
        RTHrm_hot * ((VREF / VTCO) - 1) - RTHrm_cold * ((VREF / VLTF) - 1))
RT1_top = ((VREF / VLTF) - 1) / ((1 / RT2_bot) + (1 / RTHrm_cold))
print('RT2_bot: ', RT2_bot)
print('RT1_top: ', RT1_top)

# Total output capacitance Caltulation
print('Output capacitance Calculation')
I_DISCH = 6e-3  # mA
t_DISCH = 1  # (sec)
Cmax = (I_DISCH * t_DISCH) / (0.5 * (1 + (R2_top / R1_bot)))
print('Cmax:  (uF)', Cmax / 1e-6)

# Inductor Selection
print('Inductor Selection')
# I I +(1/2)I SAT CHG RIPPLE
L1 = 22e-6  # 0.5 A
L2 = 15e-6  # 1 A
L3 = 10e-6  # 2 A
L3_isat = 2
L4 = 6.8e-6  # 4 A
L5 = 3.3e-6  # 8 A

# 17 kHz to 25 kHz
Fs = 15e3
Vout = Vbat
D = Vout / Vin_nom
L = L3
I_RIPPLE = (Vin_nom * D * (1 - D)) / (Fs * L)
if L3_isat > (I_CHARGE + (1 / 2) * I_RIPPLE):
    print('Inductor value is OK')
else:
    print('Inductor value is NOT OK')

# MPPT Temperature Compensation
print('MPPT Temperature Compensation')
VOC_solar = 10.03  # Open-circuit voltage (VOC)
V_MP_solar = 9  # Maximum power voltage (VMP)
Voc_coeff = -38e-3  # (mV / C) Open-circuit voltage temperature coefficient (VOC)
RSET = 1e3
Iset = 0.0677 / RSET
V_MPPSET=1.2
print('calculated Iset: ', Iset)
cells = 18  # number of solar cells in series
R3_top = RSET * ((2e-3*cells) / 227e-6)
R4_bot = (V_MPPSET*R3_top)/((V_MP_solar+R3_top*(0.0677/RSET))-V_MPPSET)
print('calculated R3_top: (kOhm) ', R3_top/1e3)
print('calculated R4_bot: (kOhm)', R4_bot/1e3)