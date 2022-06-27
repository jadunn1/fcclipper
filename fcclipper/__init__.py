#!/usr/bin/env python3
""" Import for fcclipper """

from appdirs import AppDirs
__fcclipper_user_config_dir__ = AppDirs('fcclipper').user_config_dir

from .__version__ import  (
__title__,
__description__,
__version__,
__url__,
__license__,
__author__,
)
