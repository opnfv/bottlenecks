##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

from vstf.common.utils import check_call
import os
import logging

LOG = logging.getLogger(__name__)


class _ImageManager(object):
    """
    A qemu-img wrapper to create qcow2 child image from a parent image.

    """

    def __init__(self, parent_image_path, child_image_dir):
        """
        :param parent_image_path    str: the parent image path.
        :param child_image_dir      str: the destination path to put child images.
        """
        self._create_child_str = 'qemu-img create -f %(image_type)s %(child_path)s -o backing_file=%(parent_path)s'
        self._convert_str = "qemu-img convert -O %(image_type)s %(parent_path)s %(child_path)s"
        self.child_image_dir = child_image_dir
        self.parent_image_path = parent_image_path
        assert os.path.isfile(self.parent_image_path)
        assert os.path.isdir(self.child_image_dir)

    def create_child_image(
            self,
            child_name,
            full_clone=False,
            image_type='qcow2'):
        """
        create a child image and put it in self.child_image_dir.

        :param child_name:  the image name to be created..
        :return: return the path of child image.
        """

        image_path = os.path.join(
            self.child_image_dir,
            child_name) + '.' + image_type
        if full_clone:
            cmd = self._convert_str % {
                'image_type': image_type,
                'child_path': image_path,
                'parent_path': self.parent_image_path}
        else:
            cmd = self._create_child_str % {
                'child_path': image_path,
                'parent_path': self.parent_image_path,
                'image_type': image_type}
        check_call(cmd.split())
        return image_path


class ImageManager(object):

    def __init__(self, cfg):
        """
        ImageManager creates images from configuration context.

        :param cfg: dict, example:
        {
            'parent_image': "/mnt/sdb/ubuntu_salt_master.img",
            'dst_location': "/mnt/sdb",
            'full_clone':False,
            'type': "qcow2",
            'names': ['vm1','vm2','vm3','vm4']
        }
        :return:
        """
        super(ImageManager, self).__init__()
        cfg = self._check_cfg(cfg)
        self.parent_image = cfg['parent_image']
        self.image_dir = cfg['dst_location']
        self.full_clone = cfg['full_clone']
        self.image_type = cfg['type']
        self.names = cfg['names']
        self.mgr = _ImageManager(self.parent_image, self.image_dir)

    @staticmethod
    def _check_cfg(cfg):
        for key in (
            'parent_image',
            'dst_location',
            'full_clone',
            'type',
                'names'):
            if key not in cfg:
                raise Exception("does't find %s config" % key)
        if cfg['type'] not in ('raw', 'qcow2'):
            raise Exception(
                "type:%s not supported, only support 'raw' and 'qcow2'" %
                cfg['type'])
        if not cfg['full_clone'] and cfg['type'] == 'raw':
            raise Exception(
                "only support 'qcow2' for not full_clone image creation" %
                cfg['type'])
        return cfg

    def create_all(self):
        """
        create images by configuration context.

        :return: True for success, False for failure.
        """
        for name in self.names:
            image = self.mgr.create_child_image(
                name, self.full_clone, self.image_type)
            LOG.info("image: %s created", image)
        return True

    def clean_all(self):
        """
        remove all the images created in one go.

        :return: True for success. Raise exception otherwise.
        """
        for name in self.names:
            image_path = os.path.join(
                self.image_dir, name + '.' + self.image_type)
            try:
                os.unlink(image_path)
                LOG.info("remove:%s successfully", image_path)
            except Exception:
                LOG.info("cann't find path:%s", image_path)
        return True


if __name__ == '__main__':
    import argparse
    import json
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'action',
        choices=(
            'create',
            'clean'),
        help='action:create|clean')
    parser.add_argument('--config', help='config file to parse')
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)
    image_cfg = json.load(open(args.config))
    mgr = ImageManager(image_cfg)
    if args.action == 'create':
        mgr.create_all()
    if args.action == 'clean':
        mgr.clean_all()
