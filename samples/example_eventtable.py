'''
Sample code to open Event Table xml file.
'''

import matplotlib
matplotlib.use('Agg')  # this line is required for the batch job before importing other matplotlib modules.

import numpy as np
from gwpy.table import EventTable

import argparse

parser = argparse.ArgumentParser(description='Open event table xml file.')
parser.add_argument('-i','--inputfile',help='input trigger filename.',default='/home/controls/triggers/K1/LSC_CARM_SERVO_MIXER_DAQ_OUT_DQ_OMICRON/12440/K1-LSC_CARM_SERVO_MIXER_DAQ_OUT_DQ_OMICRON-1244013258-60.xml.gz')

args = parser.parse_args()

inputfile = args.inputfile


events = EventTable.read(inputfile,tablename='sngl_burst')
# Tablename option
#'process', 'process_params', 'sngl_burst', 'segment_definer', 'segment_summary', 'segment'
# Column option
#ifo peak_time peak_time_ns start_time start_time_ns duration search process_id event_id peak_frequency central_freq bandwidth channel amplitude snr confidence chisq chisq_dof param_one_name param_one_value
#events = EventTable.read('K1-IMC_CAV_ERR_OUT_DQ_OMICRON-1241900058-60.xml.gz', tablename='sngl_burst', columns=['peak_time', 'peak_time_ns', 'start_time', 'start_time_ns', 'duration', 'peak_frequency', 'central_freq', 'bandwidth', 'channel', 'amplitude', 'snr', 'confidence', 'chisq', 'chisq_dof', 'param_one_name', 'param_one_value'])

#np.get_printoptions()
#np.set_printoptions(threshold=1000)

#print(events)

events.pprint(max_lines=100,max_width=1000)
