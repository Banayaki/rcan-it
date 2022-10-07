import os
from ptsr.data import srdata
from glob import glob

class CustomData(srdata.SRData):
    def __init__(self, cfg, name='MyData', train=True, benchmark=False):
        data_range = cfg.DATASET.DATA_RANGE
        if train:
            data_range = data_range[0]
        else:
            if cfg.SOLVER.TEST_ONLY and len(data_range) == 1:
                data_range = data_range[0]
            else:
                data_range = data_range[1]

        self.begin, self.end = data_range
        super().__init__(
            cfg, name=name, train=train, benchmark=benchmark
        )

    def _scan(self):
        list_hr = []
        list_lr = [[] for _ in self.scale]

        filelist = glob(os.path.join(self.dir_hr, f'*{self.ext}'))
        
        for ith_file in filelist[slice(self.begin, self.end)]:
            filename = os.path.basename(ith_file)
            list_hr.append(os.path.join(self.dir_hr, filename))
            for si, s in enumerate(self.scale):
                list_lr[si].append(os.path.join(
                    self.dir_lr, filename
                ))

        return list_hr, list_lr

    def _set_filesystem(self, dir_data):
        self.apath = dir_data
        self.dir_hr = os.path.join(self.apath, 'train', 'gt')
        self.dir_lr = os.path.join(self.apath, 'train', 'doe')
        self.ext = '.png'

    def _name_hrbin(self):
        return os.path.join(
            self.apath,
            'bin',
            '{}_bin_HR.npy'.format(self.split)
        )

    def _name_lrbin(self, scale):
        return os.path.join(
            self.apath,
            'bin',
            '{}_bin_LR_X{}.npy'.format(self.split, scale)
        )

    def __len__(self):
        if self.train:
            return len(self.images_hr) * self.repeat
        else:
            return len(self.images_hr)

    def _get_index(self, idx):
        if self.train:
            return idx % len(self.images_hr)
        else:
            return idx
