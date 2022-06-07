""" This module is to clip Food City digital coupons and retrieve Fuel Bucks points balance"""
import logging
import click

from .libs.log import setup_richlogging
from .cli import FoodCityCLI


# Logging
LOG = logging.getLogger('FoodCityLogger')
setup_richlogging(logging.WARN)

food_city_cli = FoodCityCLI()


@click.group(invoke_without_command=True)
@click.pass_context
@click.option('--disable-headless', is_flag=True, help='Display browser.')
@click.option('--debug', '-d', is_flag=True, help='Debug output displayed.')
def cli(ctx, disable_headless, debug):
    """
       This program is the unoficial CLI for FoodCity
       - check Fuel Buck Balance and clip digital coupons
    """

    if debug:
        # set debug level for logging
        LOG.setLevel(logging.DEBUG)
        LOG.debug("Debug is %s", debug)

    if disable_headless:
        food_city_cli.api.browser_options['headless'] = False
        LOG.debug("Disable Headless is %s", disable_headless)

    if ctx.invoked_subcommand is None:
        food_city_cli.prompt_options()


@click.command('clip-coupons', help='Clip all digital coupons.')
@click.option('--dry-run',  is_flag=True, help='No Coupons are clipped.')
def clip_coupons(dry_run):
    """ Function for option to clip coupons """
    if dry_run:
        food_city_cli.api.dry_run = True
        LOG.debug("Dry Run is set: %s", dry_run)

    food_city_cli.option_clip_coupons()


@click.command('get-fuel-bucks', help='Get Fuel Buck Points Balance.')
def get_fuel_bucks():
    """ Function for option to retrieve fuel bucks point balance """
    food_city_cli.option_get_fuel_bucks()

@click.command('clear-cache', help='Clear cached items.')
def clear_cache():
    """ Function for option to clear cached items """
    food_city_cli.clear_cache()

if __name__ == '__main__':
    cli.add_command(clip_coupons)
    cli.add_command(get_fuel_bucks)
    cli.add_command(clear_cache)
    cli()
