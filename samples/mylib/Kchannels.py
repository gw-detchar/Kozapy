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
    str = "export PEM_PSL_old=(\"" + "\" \"".join(PEM_PSL_old) + "\")\n"
    file.write(str)

    str = "export PEM_PSL_slow_old=(\"" + "\" \"".join(PEM_PSL_slow_old) + "\")\n"
    file.write(str)
