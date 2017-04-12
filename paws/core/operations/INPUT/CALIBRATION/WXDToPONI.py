import os

import numpy as np
import pyFAI

from ...Operation import Operation
from ... import optools

class WXDToPONI(Operation):
    """
    Convert WXDIFF .calib output 
    to a dict of PyFAI PONI parameters,
    by first converting from WXDIFF to Fit2D,
    then using a pyFAI.AzimuthalIntegrator 
    to convert from Fit2D to PONI format.
    
    The conversion from WXDiff parameters to Fit2D parameters 
    was originally contributed to paws by Fang Ren.

    Input .calib file from WXDIFF automated calibration,
    input pixel size and polarization factor,
    output dict of pyFAI PONI calibration parameters.
    """
    
    def __init__(self):
        input_names = ['wxd_file','pixel_size_um','fpolz']
        output_names = ['poni_dict']
        super(WXDToPONI,self).__init__(input_names,output_names)
        self.input_doc['wxd_file'] = '.calib file produced by WXDIFF calibration'
        self.input_doc['pixel_size_um'] = 'pixel size in microns'
        self.input_doc['fpolz'] = 'polarization factor'
        self.input_src['wxd_file'] = optools.fs_input
        self.input_src['pixel_size_um'] = optools.text_input 
        self.input_src['fpolz'] = optools.text_input
        self.input_type['wxd_file'] = optools.path_type
        self.input_type['pixel_size_um'] = optools.float_type
        self.input_type['fpolz'] = optools.float_type
        self.inputs['pixel_size_um'] = 79 
        self.inputs['fpolz'] = 0.95 
        self.output_doc['poni_dict'] = 'Dict of pyFAI calibration parameters, as found in a .poni file'

    def run(self):
        fpath = self.inputs['wxd_file']
        pxsz_um = self.inputs['pixel_size_um']
        pxsz_m = pxsz_um*1E-6
        fpolz = self.inputs['fpolz']
        for line in open(fpath,'r'):
            kv = line.strip().split('=')
            if kv[0] == 'detect_dist':
                d_px = float(kv[1])         # WXDIFF direct detector distance, 
                                            # from sample to where beam axis intersects detector plane, in pixels.
                                            # Fit2D uses this input in mm to set its spatial scale,
                                            # so it has to be converted to distance units (mm for Fit2D). 
                                            # Because this scales the spatial representation for Fit2D,
                                            # the other inputs can still be given in pixel units,
                                            # without converting between pixel sizes.
                d_m = d_px*pxsz_m 
                d_mm = d_m*1E3 
            if kv[0] == 'bcenter_x':
                bcx_px = float(kv[1])       # WXDIFF x coord relative to 'bottom left' corner of detector
                                            # where beam axis intersects detector plane, in pixels 
                                            # Fit2D centerX is also in pixels 
            if kv[0] == 'bcenter_y':
                bcy_px = float(kv[1])       # WXDIFF y coord relative to 'bottom left' corner of detector
                                            # where beam axis intersects detector plane, in pixels 
                                            # Fit2D centerY is also in pixels
            if kv[0] == 'detect_tilt_alpha':    
                rot_rad = float(kv[1])      # WXDIFF alpha is tilt plane rotation in rad 
                                            # Fit2D tiltPlanRotation  = 360-rot_rad*180/pi 
                rot_deg = rot_rad*float(180)/np.pi
                rot_fit2d = float(360)-rot_deg
            if kv[0] == 'detect_tilt_delta':
                tilt_rad = float(kv[1])     # WXDIFF delta is the tilt in rad
                tilt_deg = tilt_rad*float(180)/np.pi
            if kv[0] == 'wavelenght':
                wl_A = float(kv[1])         # WXDIFF 'wavelenght' is in Angstroms
        # get wavelength in m 
        wl_m = wl_A*1E-10
        # use a pyFAI.AzimuthalIntegrator() to do the conversion
        p = pyFAI.AzimuthalIntegrator(wavelength = wl_m) 
        p.setFit2D(d_mm,bcx_px,bcy_px,tilt_deg,rot_fit2d,pxsz_um,pxsz_um)
        poni_dict = p.getPyFAI()
        poni_dict['fpolz'] = fpolz
        self.outputs['poni_dict'] = poni_dict 

