LAS_IMC = ['K1:LAS-POW_IMC_DC_INMON']

IMC = ['K1:IMC-CAV_REFL_OUT_DQ',
       'K1:IMC-CAV_TRANS_OUT_DQ',
       'K1:IMC-SERVO_SLOW_MON_OUT_DQ',
       'K1:IMC-SERVO_FAST_MON_OUT_DQ',
       'K1:IMC-SERVO_SUM_MON_OUT_DQ',
       'K1:IMC-MCL_SERVO_OUT_DQ']

PEM_IMC = ['K1:PEM-SEIS_MCE_GND_EW_IN1_DQ',
           'K1:PEM-SEIS_MCE_GND_NS_IN1_DQ',
           'K1:PEM-SEIS_MCE_GND_UD_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_EW_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_NS_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_UD_IN1_DQ',
           'K1:PEM-ACC_MCF_TABLE_IMCREFL_Z_OUT_DQ',
           'K1:PEM-MIC_MCF_TABLE_IMCREFL_Z_OUT_DQ',
           'K1:PEM-MIC_MCE_TABLE_IMCTRANS_Z_OUT_DQ']

PSL_PMC = ['K1:PSL-PMC_CAV_REFL_DC_OUT_DQ',
           'K1:PSL-PMC_CAV_TRANS_DV_OUT_DQ',
           'K1:PSL-PMC_MIXER_MON_OUT_DQ',
           'K1:PSL-PMC_PZT_HV_MON_OUT_DQ',
           'K1:PSL-PMC_SLOW_MON_OUT_DQ',
           'K1:PSL-PMC_PZT_SLOW_MON_OUT_DQ',
           'K1:PSL-PMC_FAST_MON_OUT_DQ',
           'K1:PSL-PMC_PZT_FAST_MON_OUT_DQ',
           'K1:PSL-PMC_TEMP_OUT_DQ']

PEM_PSL = ['K1:PEM-ACC_PSL_TABLE_PSL1_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_TABLE_PSL2_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_TABLE_PSL3_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_PERI_PSL1_Y_OUT_DQ',
           'K1:PEM-ACC_PSL_PERI_PSL2_X_OUT_DQ',
           'K1:PEM-MIC_PSL_TABLE_PSL4_Z_OUT_DQ']

PEM_PSL_old = ['K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ',
               'K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ',
               'K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ',
               'K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ',
               'K1:PEM-PSL_MIC_CENTER_OUT_DQ']

PEM_PSL_slow_old = ['K1:PEM-HUMIDITY_BOOTH_PSL',
                    'K1:PEM-TEMPERATURE_BOOTH_PSL',
                    'K1:PEM-HUMIDITY_FIELD_PSL2',
                    'K1:PEM-TEMPERATURE_FIELD_PSL2',
                    'K1:PEM-HUMIDITY_FIELD_PSL',
                    'K1:PEM-TEMPERATURE_FIELD_PSL']

if __name__ == '__main__':

    file = open('Kchannels.sh','w')

    file.write("#!/bin/bash\n")
    file.write("\n")
    file.write("# PLEASE NEVER CHANGE THIS FILE BY HAND. \n")
    file.write("# This file is generated from Kchannels.py. \n")
    file.write("# If you need a new list, please write it in Kchannels.py. \n")
    file.write("# Please also copy and paste the last 2 lines and replace the channel name.\n")
    file.write("# $ python Kchannels.py \n")
    file.write("# will update this file including your new list. \n")
    file.write("\n")

    str = "export LAS_IMC=(\"" + "\" \"".join(LAS_IMC) + "\")\n"
    file.write(str)

    str = "export IMC=(\"" + "\" \"".join(IMC) + "\")\n"
    file.write(str)

    str = "export PEM_IMC=(\"" + "\" \"".join(PEM_IMC) + "\")\n"
    file.write(str)

    str = "export PSL_PMC=(\"" + "\" \"".join(PSL_PMC) + "\")\n"
    file.write(str)

    str = "export PEM_PSL_old=(\"" + "\" \"".join(PEM_PSL_old) + "\")\n"
    file.write(str)

    str = "export PEM_PSL_slow_old=(\"" + "\" \"".join(PEM_PSL_slow_old) + "\")\n"
    file.write(str)