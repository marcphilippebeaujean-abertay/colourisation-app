import numpy as np
from img_processing import process_net_output, generate_chrominance


class PredictionData:
    def __init__(self, input_img, ab_channels, pred_time=0, model_name=''):
        self.ab_channels = ab_channels
        self.pred_time = pred_time
        self.input_img = input_img
        self.model_name = model_name
        self.channel_dist = None
        self.mse = None
        self.multi_factor = 1
        self.stats = self.generate_stats()

    def update_brightness(self, increment):
        multifactor_mod = 0.02 if increment else -0.02
        self.multi_factor += multifactor_mod
        self.stats = self.generate_stats()

    def get_multiplied_channels(self):
        return self.ab_channels * self.multi_factor

    def generate_stats(self):
        dict = {
            'Mean': (np.mean(self.ab_channels[..., :1]),
                     np.mean(self.ab_channels[..., 1:])),
            'Max': (np.amax(self.ab_channels[..., :1]),
                    np.amax(self.ab_channels[..., 1:])),
            'Min': (np.amin(self.ab_channels[..., :1]),
                    np.amin(self.ab_channels[..., 1:])),
            'Std. Dev.': (np.std(self.ab_channels[..., :1]),
                          np.std(self.ab_channels[..., 1:])),
            'Pred. Time': self.pred_time
            }
        return dict

    def generate_output(self, target_res=None):
        # colour brightness enhancement
        mod_pred = self.ab_channels * self.multi_factor
        # generate chrominance
        output = process_net_output(mod_pred, self.input_img, target_size=target_res)
        chrom = generate_chrominance(mod_pred, self.input_img)
        return output, chrom
