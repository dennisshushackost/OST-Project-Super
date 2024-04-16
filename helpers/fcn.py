import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'

import tensorflow as tf
from tensorflow.keras.layers import Conv2D, BatchNormalization, Activation, Conv2DTranspose, Input
from tensorflow.keras.models import Model

class FCNSegmenter:
    """
    This class defines a Fully Convolutional Network for binary semantic segmentation.
    This can be optimized for any input shape.
    """

    def __init__(self, input_shape=(488, 488, 4)):
        if not isinstance(input_shape, tuple) or len(input_shape) != 3:
            raise ValueError("Input shape must be a tuple of length 3 (H, W, C)")
        self.input_shape = input_shape

    def create_fcn(self):
        """
        Builds the FCN model.
        """
        inputs = Input(shape=self.input_shape)
        
        # Encoder
        x = self.conv_block(inputs, 64, stride=1)
        x = self.conv_block(x, 128, stride=2)
        x = self.conv_block(x, 256, stride=2)
        
        # Decoder
        x = self.deconv_block(x, 128)
        x = self.deconv_block(x, 64)

        # Output layer
        outputs = Conv2D(1, (1, 1), activation='sigmoid', padding='same')(x)
        model = Model(inputs, outputs)
        return model

    def conv_block(self, inputs, num_filters, stride):
        x = Conv2D(num_filters, (3, 3), strides=(stride, stride), padding='same')(inputs)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

    def deconv_block(self, inputs, num_filters):
        x = Conv2DTranspose(num_filters, (3, 3), strides=(2, 2), padding='same')(inputs)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        return x

if __name__ == "__main__":
    fcn = FCNSegmenter()
    model = fcn.create_fcn()
    model.summary()
 