import numpy as np
from img_processing import process_net_output, generate_chrominance


class PredictionData:
    def __init__(self, input_img, ab_channels, model_name=''):
        self.ab_channels = ab_channels
        self.input_img = input_img
        self.model_name = model_name
        self.channel_dist = None
        self.mse = None
        self.multi_factor = 1.05
        self.stats = self.generate_stats()

    def update_brightness(self, decrement):
        multifactor_mod = -0.05 if decrement else 0.05
        self.multi_factor += multifactor_mod
        self.ab_channels *= self.multi_factor
        self.chrominance *= self.multi_factor
        self.stats = self.generate_stats()

    def generate_stats(self):
        dict = {
            'Mean': (np.mean(self.ab_channels[..., :1]),
                     np.mean(self.ab_channels[..., 1:])),
            'Max': (np.amax(self.ab_channels[..., :1]),
                    np.amax(self.ab_channels[..., 1:])),
            'Min': (np.amax(self.ab_channels[..., :1]),
                    np.amin(self.ab_channels[..., 1:])),
            'Std. Dev.': (np.std(self.ab_channels[..., :1]),
                      np.std(self.ab_channels[..., 1:]))
            }
        return dict

    def generate_output(self, target_res=None):
        # colour brightness enhancement
        mod_pred = self.ab_channels * self.multi_factor
        # generate chrominance
        output = process_net_output(mod_pred, self.input_img, target_size=target_res)
        chrom = generate_chrominance(mod_pred, self.input_img)
        return output, chrom
