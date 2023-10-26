""" FoodCity CLI module """
import configparser
from datetime import datetime, timedelta
import os
import time
import gc
import logging
from pathlib import Path
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from fcclipper import (
        __fcclipper_user_config_dir__, __fcclipper_user_data_dir__,
        __fcclipper_user_log_dir__
        )

from .libs.memoize import Memoized
from .api import FoodCityAPI


LOG = logging.getLogger('FoodCityLogger')

class FoodCityCLI:
    """ class FoodCityCLI and methods """
    def __init__(self, config_file='config.ini'):
        if not Path(__fcclipper_user_data_dir__).exists():
            Path(__fcclipper_user_data_dir__).mkdir(parents=True)
        if not Path(__fcclipper_user_config_dir__).exists():
            Path(__fcclipper_user_config_dir__).mkdir(parents=True)
        self.config_file = os.path.join(Path(__fcclipper_user_config_dir__), config_file)
        if not Path(__fcclipper_user_log_dir__).exists():
            Path(__fcclipper_user_log_dir__).mkdir(parents=True)
        self.config = configparser.ConfigParser()
        self.username = None
        self.password = None
        self.domain = None
        self.console = Console()
        self.api = FoodCityAPI(self)
        if not os.path.exists(self.config_file):
            self._init_config_file()
        self.config.read(self.config_file)
        self.init()


    def init(self):
        """ init function for credentials """
        LOG.debug('In CLI init')
        if self.username is None and self.config['main']['username'] != '':
            self.username = self.config['main']['username']
            self.password = self.config['main']['password']
            self.domain = self.config['main']['domain']
        else:
            self.prompt_credentials()


    def _init_config_file(self):
        """ initizlize configuration variables and call to write """
        self.config.add_section('main')
        self.config['main']['username'] = ''
        self.config['main']['password'] = ''
        self.config['main']['domain'] = 'foodcity.com'
        self.config.add_section('profile')
        self.config['profile']['first_name'] = ''
        self._write_config_file()


    def _write_config_file(self):
        """ write configuration file """
        with open(self.config_file, encoding="utf-8", mode="w") as filename:
            self.config.write(filename)


    def prompt_credentials(self):
        """ prompt user for credentials """
        self.console.print('In order to continue, please enter your username ' \
                           '(email) and password for foodcity.com ')
        username = click.prompt('Username (email)')
        password = click.prompt('Password')
        self._set_credentials(username, password)


    def _set_credentials(self, username, password):
        """ set credential variables and call to write configuration file """
        self.username = username
        self.password = password
        self.config['main']['username'] = self.username
        self.config['main']['password'] = self.password
        self._write_config_file()


    def prompt_options(self):
        """ prompt user for cli options """
        self.console.print(Panel('[bold]Welcome to [dark_orange]Food CIty[/dark_orange] CLI[/bold] '
                              '(unofficial) command line interface :smiley:'))
        while True:
            self.console.print('[bold]1[/bold] - Clip all digital coupons')
            self.console.print('[bold]2[/bold] - Get Fuel Buck Points Balance')
            self.console.print('[bold]3[/bold] - Re-Enter username/password')
            self.console.print('[bold]4[/bold] - Clear cache')
            self.console.print('[bold]5[/bold] - Exit')
            option = click.prompt('Please select from one of the options', type=int)
            self.console.rule()
            if option == 1:
                self.option_clip_coupons()
            elif option == 2:
                self.option_get_fuel_bucks()
            elif option == 3:
                self.prompt_credentials()
            elif option == 4:
                self.clear_cache()
            elif option == 5:
                return

            self.console.rule()
            time.sleep(2)


    def option_clip_coupons(self):
        """ call clip_coupons api """
        LOG.debug("In option_clip_coupons")
        self.api.clip_coupons()


    def option_get_fuel_bucks(self):
        """ call get_fuel_bucks api """
        LOG.debug("In option_get_fuel_bucks")
        info = self.api.get_fuel_bucks()
        fb_table = Table(show_lines=True)
        fb_table.add_column("[bold italic]Food City Fuel Bucks Info", \
               justify="center", style="dark_orange", no_wrap="True")
        if info:
            for i in range(0, len(info)):
                info_string = '\n'.join([line.strip() for line in info[i].splitlines() \
                              if line.strip()])
                fb_table.add_row(info_string)
            self.console.print(fb_table)
        else:
            self.console.print("[bold]:X:  Balance is not available[/bold]")


    def clear_cache(self):
        """ clear_cache  """
        LOG.debug("In clear_cache")
        if os.path.exists(Memoized.cache_file):
            os.remove(Memoized.cache_file)

        for obj in gc.get_objects():
            if isinstance(obj, Memoized):
                obj.cache = {
                    'expire': datetime.now() + timedelta(hours=Memoized.cache_expiration_hours),
                    'data': {}
                }

        self.console.print("Cache had been cleared")
