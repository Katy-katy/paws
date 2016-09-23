import numpy as np

from core.operations.slacxop import Operation

class Rotation(Operation):
    """The Rotation(Operation) class: rotates an image by 90, 180, or 270 degrees"""

    def __init__(self):
        input_names = ['image_data','rotation_deg']
        output_names = ['image_data']
        super(Rotation,self).__init__(input_names,output_names)        
        self.input_doc['image_data'] = '2d array representing intensity for each pixel'
        self.input_doc['rotation_deg'] = str('rotation in degrees counter-clockwise, '
                                    + 'must be either 90, 180, or 270')
        self.output_doc['image_data'] = '2d array representing rotated image'

    def run(self):
        """
        Rotate self.inputs['image_data'] and save as self.outputs['image_data']"""
        img = self.inputs['image_data']
        rot_deg = self.inputs['rotation_deg']
        if rot_deg==90:
            img_rot = np.rot90(img)
        elif rot_deg==180:
            img_rot = np.rot90(np.rot90(img))
        elif rot_deg==270:
            img_rot = np.rot90(np.rot90(np.rot90(img)))
        else:
            msg = '[{}] expected rot_deg = 90, 180, or 270, got {}'.format(__name__,rot_deg)
            raise ValueError(msg)
        # save results to self.outputs
        self.outputs['image_data'] = img_rot

#    @classmethod
#    def description(cls):
#        return str(
#        "A Rotation operation takes two input arguments: "
#        + "inputs['image_data'] (2d pixel array), "
#        + "and inputs['rotation_deg'] (angle in degrees). "
#        + "Calling run() populates the outputs['image_data'] "
#        + "with a pixel array that is rotated CCW from the input. "
#        + "Rotation angle must be 90, 180, or 270 degrees."
#        )

#    def tag(self):
#        return "Image-Rotation"



