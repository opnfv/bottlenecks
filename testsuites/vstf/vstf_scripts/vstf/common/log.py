##############################################################################
# Copyright (c) 2015 Huawei Technologies Co.,Ltd and others.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Apache License, Version 2.0
# which accompanies this distribution, and is available at
# http://www.apache.org/licenses/LICENSE-2.0
##############################################################################

import logging


def _init_log_to_file(log_file, level, _format):
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(level)
    file_handler.setFormatter(logging.Formatter(_format))
    return file_handler


def _init_log_to_console(level, _format):
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(logging.Formatter(_format))
    return console


def _init_log(log_file, level=logging.INFO, clevel=logging.INFO):
    _format = '%(asctime)s <%(levelname)s> [%(funcName)s.%(lineno)d]: %(message)s'
    # _format = '%(asctime)s [%(levelname)s] %(message)s'
    _verbose = '%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(funcName)s ### %(message)s'
    _simple = '<%(levelname)s> [%(filename)s:%(lineno)d] ### %(message)s'
    file_handler = _init_log_to_file(log_file, level, _verbose)
    console = _init_log_to_console(clevel, _simple)
    return file_handler, console


def setup_logging(
        level=logging.INFO,
        log_file="/var/log/esp_test.log",
        clevel=logging.WARNING):
    log = logging.getLogger()
    log.setLevel(level)
    file_handler, console = _init_log(log_file, level, clevel)
    log.addHandler(file_handler)
    log.addHandler(console)


if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger("common")
    logger.info('this is a test.')
    logger.warning('this is a test.')
    logger.error('this is a test.')
