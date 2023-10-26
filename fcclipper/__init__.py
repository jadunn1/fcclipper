#!/usr/bin/env python3
""" Import for fcclipper """

from appdirs import AppDirs
__fcclipper_user_config_dir__ = AppDirs('fcclipper').user_config_dir
__fcclipper_user_data_dir__ = AppDirs('fcclipper').user_data_dir
__fcclipper_user_log_dir__ = AppDirs('fcclipper').user_log_dir

from .__version__ import  (
__title__,
__description__,
__version__,
__url__,
__license__,
__author__,
)
__version_msg__ = f"Copyright (c) 2022 jadunn1 Open Source Initiative\nLicense: {__license__} - \
<{__url__}/blob/main/LICENSE>\nWritten by: {__author__}"
