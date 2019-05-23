'''
Channel lists are given. 
If you want to add new list, first write it in it.  
Then copy and paste the last 2 lines replacing channel name to your new channnel list. 
Please run
$ python Kchannels.py 
and you will get Kchannel.sh with new list. 
It can be used by exporting in a shell script.
'''

#LAS_IMC = ['K1:LAS-POW_IMC_DC_INMON']
LAS_IMC = ['K1:LAS-POW_IMC_INMON']

IMC = ['K1:IMC-CAV_REFL_OUT_DQ',
       'K1:IMC-CAV_REFL_NORM_OUTPUT',
       'K1:IMC-CAV_TRANS_OUT_DQ',
       'K1:IMC-CAV_TRANS_NORM_OUTPUT',
       'K1:IMC-CAV_ERR_OUT_DQ',
       'K1:IMC-SERVO_SLOW_MON_OUT_DQ',
       'K1:IMC-SERVO_FAST_MON_OUT_DQ',
       'K1:IMC-SERVO_SUM_MON_OUT_DQ',
       'K1:IMC-SERVO_MIXER_DAQ_OUT_DQ',
       'K1:IMC-SERVO_SLOW_DAQ_OUT_DQ',
       'K1:IMC-MCL_SERVO_OUT_DQ']

PEM_IMC =  ['K1:PEM-ACC_MCF_TABLE_IMCREFL_Z_OUT_DQ',
           'K1:PEM-MIC_MCF_TABLE_IMCREFL_Z_OUT_DQ',
           'K1:PEM-MIC_MCE_TABLE_IMCTRANS_Z_OUT_DQ']

SEIS_IMC = ['K1:PEM-SEIS_MCE_GND_EW_IN1_DQ',
           'K1:PEM-SEIS_MCE_GND_NS_IN1_DQ',
           'K1:PEM-SEIS_MCE_GND_UD_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_EW_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_NS_IN1_DQ',
           'K1:PEM-SEIS_MCF_GND_UD_IN1_DQ']
           
SEIS_IXV = ['K1:PEM-SEIS_IXV_GND_EW_IN1_DQ',
           'K1:PEM-SEIS_IXV_GND_NS_IN1_DQ',
           'K1:PEM-SEIS_IXV_GND_UD_IN1_DQ']

VIS_IMC = ['K1:VIS-MCE_TM_OPLEV_YAW_OUT_DQ',
           'K1:VIS-MCE_TM_OPLEV_PIT_OUT_DQ',
           'K1:VIS-MCI_TM_OPLEV_YAW_OUT_DQ',
           'K1:VIS-MCI_TM_OPLEV_PIT_OUT_DQ',
           'K1:VIS-MCO_TM_OPLEV_YAW_OUT_DQ',
           'K1:VIS-MCO_TM_OPLEV_PIT_OUT_DQ']

PSL_PMC = ['K1:PSL-PMC_REFL_DC_OUT_DQ',
           'K1:PSL-PMC_TRANS_DC_OUT_DQ',
           'K1:PSL-PMC_MIXER_MON_OUT_DQ',
           'K1:PSL-PMC_PZT_HV_MON_OUT_DQ',
           'K1:PSL-PMC_SLOW_MON_OUT_DQ',
           'K1:PSL-PMC_PZT_SLOW_OUT_DQ',
           'K1:PSL-PMC_FAST_MON_OUT_DQ',
           'K1:PSL-PMC_TEMP_OUT_DQ',
           'K1:PSL-PMC_TEMP_CTRL_OUTPUT']

PSL_FSS = ['K1:PSL-TTFSS_MIXER_MON_OUT_DQ',
           'K1:PSL-TTFSS_TEMP_FILTER_OUT_DQ',
           'K1:PSL-TTFSS_PZT_MON_OUT_DQ',
           'K1:PSL-TTFSS_EOM_MON_OUT_DQ',
           'K1:PSL-REFCAV_TRANS_NORM_OUTPUT',
           'K1:PSL-REFCAV_REFL_NORM_OUTPUT',
       ]

PEM_PSL = ['K1:PEM-ACC_PSL_TABLE_PSL1_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_TABLE_PSL2_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_TABLE_PSL3_Z_OUT_DQ',
           'K1:PEM-ACC_PSL_PERI_PSL1_Y_OUT_DQ',
           'K1:PEM-ACC_PSL_PERI_PSL2_X_OUT_DQ',
           'K1:PEM-ACC_PSL_PORTABLE_1_OUT_DQ',
           'K1:PEM-ACC_PSL_PORTABLE_2_OUT_DQ',
           'K1:PEM-MIC_PSL_TABLE_PSL4_Z_OUT_DQ']

PEM_PSL_old = ['K1:PEM-PSL_ACC_PERI_REFCAV_OUT_DQ',
               'K1:PEM-PSL_ACC_PERI_EXIT_OUT_DQ',
               'K1:PEM-PSL_ACC_SIGNAL1_OUT_DQ',
               'K1:PEM-PSL_ACC_SIGNAL2_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE1_Z_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE2_Z_OUT_DQ',
               'K1:PEM-PSL_ACC_TABLE3_Z_OUT_DQ',
               'K1:PEM-PSL_MIC_CENTER_OUT_DQ']

PEM_PSL_slow = ['K1:PEM-HUMIDITY_BOOTH_PSL',
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

    str = "export LAS_IMC=(\"" + "\" \"".join(LAS_IMC) + "\" )\n"
    file.write(str)

    str = "export IMC=(\"" + "\" \"".join(IMC) + "\" )\n"
    file.write(str)

    str = "export PEM_IMC=(\"" + "\" \"".join(PEM_IMC) + "\" )\n"
    file.write(str)

    str = "export SEIS_IXV=(\"" + "\" \"".join(SEIS_IXV) + "\" )\n"
    file.write(str)

    str = "export VIS_IMC=(\"" + "\" \"".join(VIS_IMC) + "\" )\n"
    file.write(str)

    str = "export PSL_PMC=(\"" + "\" \"".join(PSL_PMC) + "\" )\n"
    file.write(str)

    str = "export PSL_FSS=(\"" + "\" \"".join(PSL_FSS) + "\" )\n"
    file.write(str)

    str = "export PEM_PSL=(\"" + "\" \"".join(PEM_PSL) + "\" )\n"
    file.write(str)

    str = "export PEM_PSL_old=(\"" + "\" \"".join(PEM_PSL_old) + "\" )\n"
    file.write(str)

    str = "export PEM_PSL_slow=(\"" + "\" \"".join(PEM_PSL_slow) + "\" )\n"
    file.write(str)

    print("Kchannels.sh is generated.")
