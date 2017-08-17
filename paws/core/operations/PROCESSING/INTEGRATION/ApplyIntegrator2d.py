"""
Integrate an image to 2d,
using an existing PyFAI.AzimuthalIntegrator,
with a bunch of input parameters
for calling AzimuthalIntegrator.integrate1d().
"""

import numpy as np
import pyFAI

from ... import Operation as opmod 
from ...Operation import Operation

class ApplyIntegrator2d(Operation):
    """
    Input image data (ndarray), PyFAI.AzimuthalIntegrator, 
    mask, ROI mask, dark field image, flat field image,
    q-range, chi-range, number of points for integration bin centers,
    polz factor, choice of units (string), 
    and choice of integration method (string).
 
    Output arrays containing q and I(q) 
    """
    def __init__(self):
        input_names = list(['image_data','integrator','mask','ROI_mask','dark_image','flat_image',
        'q_range','chi_range','npts_rad','npts_azim','polarization_factor','normalization_factor','units','method','integration_mode'])
        output_names = ['q','I','q_I']
        super(ApplyIntegrator2d,self).__init__(input_names,output_names)
        self.input_doc['image_data'] = '2d array representing intensity for each pixel'
        self.input_doc['integrator'] = 'A PyFAI.AzimuthalIntegrator object'
        self.input_doc['mask'] = '2d array for image mask, same shape as image_data'
        self.input_doc['ROI_mask'] = '2d array for ROI mask, same shape as image_data'
        self.input_doc['dark_image'] = '2d array for dark field, same shape as image_data'
        self.input_doc['flat_image'] = '2d array for flat field, same shape as image_data'
        self.input_doc['q_range'] = 'list with two values, lower and upper limits of q (scattering vector)'
        self.input_doc['chi_range'] = 'list with two values, lower and upper limits of chi (azimuthal angle)'
        self.input_doc['npts_rad'] = 'number of q-points to integrate, as evenly spaced bins between q_range[0] and q_range[1]'
        self.input_doc['npts_azim'] = 'number of q-points to integrate, as evenly spaced bins between q_range[0] and q_range[1]'
        self.input_doc['polarization_factor'] = 'polarization factor, if polarization correction is needed'
        self.input_doc['units'] = 'choice of units. See PyFAI documentation for options.' 
        self.input_doc['method'] = 'choice of integration method. See PyFAI documentation for options.' 
        self.input_doc['normalization_factor'] = 'normalization monitor value'

        self.input_type['image_data'] = opmod.workflow_item
        self.input_type['integrator'] = opmod.workflow_item
        self.input_type['mask'] = opmod.workflow_item
        self.input_type['ROI_mask'] = opmod.workflow_item
        self.input_type['dark_image'] = opmod.workflow_item
        self.input_type['flat_image'] = opmod.workflow_item
        self.input_type['q_range'] = opmod.float_type
        self.input_type['chi_range'] = opmod.float_type
        self.input_type['npts_rad'] = opmod.integer_type
        self.input_type['npts_azim'] = opmod.integer_type
        self.input_type['polarization_factor'] = opmod.float_type
        self.input_type['units'] = opmod.string_type
        self.input_type['method'] = opmod.string_type
        self.input_type['normalization_factor'] = opmod.workflow_item

        self.inputs['mask'] = None 
        self.inputs['ROI_mask'] = None 
        self.inputs['dark_image'] = None 
        self.inputs['flat_image'] = None 
        self.inputs['q_range'] = None 
        self.inputs['chi_range'] = None  
        self.inputs['npts_rad'] = 1000
        self.inputs['polarization_factor'] = 1.
        self.inputs['units'] = 'q_A^-1' 
        self.inputs['method'] = None

        self.output_doc['q'] = 'Scattering vector magnitude q array in 1/Angstrom.'
        self.output_doc['I'] = 'Integrated intensity at q.'
        self.output_doc['chi'] = 'Azimuthal angle array.'

    def run(self):
        if self.inputs['ROI_mask']: self.inputs['mask'] = self.inputs['mask'] | self.inputs['ROI_mask']
        # use a mask to screen negative pixels
        # mask should be 1 for masked pixels, 0 for unmasked pixels
        kwargexcludemask = ['ROI_mask', 'integrator']
        kwargs = {key:val for key,val in self.inputs.items() if key not in kwargexcludemask}

        integ_result = self.inputs['integrator'].integrate1d(**kwargs)
        # save results to self.outputs
        q = integ_result.radial
        I = integ_result.intensity
        chi = integ_result.chi
        self.outputs['q'] = q
        self.outputs['I'] = I
        self.outputs['chi'] = chi

