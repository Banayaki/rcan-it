from .utility import Singleton

import torch
from torch.utils.tensorboard import SummaryWriter
from torchmetrics import PeakSignalNoiseRatio


class TensorboardLogger(metaclass=Singleton):
    writer = SummaryWriter(log_dir="outputs/tb_logs")
    metrics = {
        'PSNR': PeakSignalNoiseRatio()
    }

    def __init__(self, device):
        self.device = device
        [m.to(self.device) for m in self.metrics.values()]

    def log_value(self, name: str, value: float, epoch: int):
        self.writer.add_scalar(name, value, epoch)

    def calc_and_log_metrics(self, x: torch.tensor, y: torch.tensor, epoch: int):
        for key, f in self.metrics.items():
            value = f(x, y)
            self.writer.add_scalar(f"Metric/{key}", value, epoch)
