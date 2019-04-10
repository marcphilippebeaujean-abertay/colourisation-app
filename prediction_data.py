import numpy as np
from img_processing import process_net_output, generate_chrominance, cv2_to_tk_img


class PredictionData:
    def __init__(self, input_img, ab_channels, ground_truth=None):
        self.ab_channels = ab_channels
        self.input_img = input_img
        self.channel_dist = None
        self.mse = None
        self.multi_factor = 1.05
        if ground_truth is not None:
            self.mse = np.square(np.subtract(self.ab_channels, ground_truth)).mean()
        self.stats = self.generate_stats()

    def update_brightness(self, decrement):
        multifactor_mod = -0.05 if decrement else 0.05
        self.multi_factor += multifactor_mod
        self.ab_channels *= self.multi_factor
        self.chrominance *= self.multi_factor
        self.stats = self.generate_stats()

    def generate_stats(self):
        dict = {
            'mean': (np.mean(self.ab_channels[..., :1]),
                     np.mean(self.ab_channels[..., 1:])),
            'max': (np.amax(self.ab_channels[..., :1]),
                    np.amax(self.ab_channels[..., 1:])),
            'min': (np.amax(self.ab_channels[..., :1]),
                    np.amin(self.ab_channels[..., 1:])),
            'stdev': (np.std(self.ab_channels[..., :1]),
                      np.std(self.ab_channels[..., 1:]))
            }
        return dict

    def generate_output(self):
        # colour brightness enhancement
        mod_pred = self.ab_channels * self.multi_factor
        # generate chrominance
        output = process_net_output(mod_pred, self.input_img)
        chrom = generate_chrominance(mod_pred, self.input_img)
        return output, chrom
