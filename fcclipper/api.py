""" This module contains API calls to FoodCity """
import asyncio
import logging
import time
import re
from pyppeteer.errors import ElementHandleError
from pyppeteer import launch

from fcclipper import __fcclipper_user_data_dir__
from .libs.memoize import Memoized


LOG = logging.getLogger('FoodCityLogger')

class FoodCityAPI:
    """ FoodCityAPI class with methods for getting Fuel Buck points and clipping coupons """
    dry_run = False
    browser_options = {
        'headless': True,
        'userDataDir': __fcclipper_user_data_dir__,
        'args': ['--blink-settings=imagesEnabled=false',  # Disable images for faster load-time
                 '--no-sandbox']
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }


    def __init__(self, cli):
        self.cli: cli.FoodCityCLI = cli
        self.browser = None
        self.page = None
        LOG.debug('In API __init__')


    async def init(self):
        """ Function init for inititalizing browser, page and headers """
        self.browser = await launch(self.browser_options)
        self.page = await self.browser.newPage()
        await self.page.setExtraHTTPHeaders(self.headers)
        await self.page.setViewport({'width': 700, 'height': 0})


    async def destroy(self):
        """ Close page and browser for cleanup """
        await self.page.close()
        await self.browser.close()


    def clip_coupons(self):
        """ Clip coupons asyncio loop """
        LOG.debug("In clip_coupons")
        return asyncio.get_event_loop().run_until_complete(self._clip_coupons())


    async def _clip_coupons(self):
        """ _clip_coupons loops to load more coupon pages and clip coupons """
        LOG.debug('In _clip_coupons')
        signed_in = await self.sign_in_routine(contains=['My Account'])
        if not signed_in:
            await self.destroy()
            return None

        self.cli.console.print('[italic]Retrieving coupons...[/italic]')
        with self.cli.console.status("[italic](please wait)...[/italic]", spinner='moon'):
            await self.page.goto('https://www.' + self.cli.domain + '/coupons/mycoupons', \
                {"waitUntil": "networkidle0"})

            # Display Available Coupon Count
            available_coupon_count = await self.get_first_xpath_property \
                    ("//button[contains(., 'Available Coupons')]", 'textContent') or "0"
            self.cli.console.print(' '.join((available_coupon_count.strip()).split()))

            # Display Loaded Coupon Count
            loaded_coupon_count = await self.get_first_xpath_property \
                    ("//button[contains(., 'Loaded Coupons')]", 'textContent') or "0"
            self.cli.console.print(' '.join((loaded_coupon_count.strip()).split()))

        # Clip Coupons
        if self.dry_run:
            self.cli.console.print('[bold]Dry run NOT[/bold]', end=' ')

        self.cli.console.print('[italic]Clipping coupons...[/italic]')

        with self.cli.console.status("[italic](please wait)...[/italic]", spinner='moon'):
            pagecount =  await self.get_first_xpath_property \
                    ("//input[@id=\'hdnPageCount\']",'value') or "0"

            if int(pagecount) > 1:
                while True:
                    # Click Show More to display all available Coupons
                    try:
                        await self.page.waitForSelector('#showMore')
                        await self.page.click('#showMore')
                        await self.page.waitForFunction('document.getElementById \
                              ("hdnLoadingNextPage").value == "0"')
                    except (ElementHandleError, asyncio.TimeoutError) as error:
                        LOG.debug('Breaking loop: caught Exception: %s', error)
                        break

            # Clip coupons
            btn = await self.page.Jx("//button[contains(., 'Load to Card') \
                      and not (contains(@id, 'Modal'))]")

            index = 0
            for index, elem in enumerate(btn, start=1):
                # pylint: disable=protected-access
                LOG.debug("Index elem is: %s %s", index, elem._remoteObject['description'])
                index_span_cliptxt = "{0}".format(re.findall(r"[\w']+", \
                              elem._remoteObject['description'])[1].replace('Coupon','ClipTxt'))
                index_button = "#{0}".format(re.findall(r"[\w']+", \
                                   elem._remoteObject['description'])[1])
                self.cli.console.print("Coupon Button: ", index_button)

                if not self.dry_run:
                    try:
                        await asyncio.gather(
                            self.page.hover(index_button),
                            self.page.click(index_button),
                            self.page.waitForXPath(f"//span[@id=\'{index_span_cliptxt}\' \
                                and contains(@style, \'display: none\')]"),
                        )
                    except asyncio.TimeoutError as error:
                        self.cli.console.print('(',index-1,') [bold]Coupons successfully ' \
                                       'clipped to your account[/bold]')
                        LOG.error('\nCaught TimeoutError Exception: %s Processing %s',\
                             error, index_span_cliptxt)
                        await self.destroy()
                        return False

            if self.dry_run:
                self.cli.console.print('(',index,') [bold]Coupons found! :thumbs_up:[/bold]')
            else:
                self.cli.console.print('(',index,') [bold]Coupons successfully clipped to ' \
                                   'your account! :thumbs_up:[/bold]')

            if not self.browser_options['headless']:
                time.sleep(2)

            await self.destroy()
            return True


    @Memoized
    def get_fuel_bucks(self):
        """ get_fuel_bucks asyncio loop """
        LOG.debug("In get_fuel_bucks")
        return asyncio.get_event_loop().run_until_complete(self._get_fuel_bucks())


    async def _get_fuel_bucks(self):
        """ Get fuel bucks balance """
        LOG.debug("In _get_fuel_bucks")
        signed_in = await self.sign_in_routine(contains=['My Account'])
        if not signed_in:
            await self.destroy()
            return None

        self.cli.console.print('[italic]Getting Balance...[/italic]')
        with self.cli.console.status("[italic](please wait)...[/italic]", spinner='moon'):
            await self.page.goto('https://www.' + self.cli.domain + \
                             '/account/dashboard#l-dashboard', {'waitUntil' : 'networkidle0'})

        await self.page.waitForSelector(".card-dash__brief")
        await self.page.waitForSelector(".dfac")
        elements_cd = await self.page.Jx("//div[@class='card-dash__brief'] \
                          [contains(., 'Fuel Bucks')]")
        elements_dfac = await self.page.Jx('//div[@class="dfac"]')

        points_balance = []
        for element_cd in elements_cd:
            edata_cd = await self.page.evaluate('(elements_cd) => \
                           elements_cd.textContent', element_cd)
            points_balance.append(edata_cd)

        for element_dfac in elements_dfac:
            edata_dfac = await self.page.evaluate('(elements_dfac) => \
                             elements_dfac.textContent', element_dfac)
            points_balance.append(edata_dfac)

        await self.destroy()
        if not points_balance:
            return None

        return points_balance


    async def sign_in_routine(self, contains=None):
        """ Routine to initialize and call sign_in """
        if contains is None:
            contains = ['My Account']

        LOG.debug('In sign_in_routine')
        LOG.debug('Domain is: %s', self.cli.config['main']['domain'])

        await self.init()
        self.cli.console.print('[italic]Signing in...[/italic]')
        with self.cli.console.status("[italic](please wait)...[/italic]", spinner='moon'):
            signed_in = await self.sign_in(contains)

        if not signed_in:
            self.cli.console.print('Sign in failed.')

        return signed_in


    async def sign_in(self, contains):
        """ Fill out login form, attempt login and check result """
        timeout = 20000
        LOG.debug('In sign_in')
        LOG.debug('Username is: %s', self.cli.username)
        LOG.debug('Domain is: %s', self.cli.domain)
        LOG.debug("contains is %s", contains)
        await self.page.goto('https://www.' + self.cli.domain + '/home/login')

        await self.page.click('#login_email', {'clickCount': 3})
        await self.page.type('#login_email', self.cli.username)
        await self.page.type('#login_password', self.cli.password)

        try:
            await asyncio.gather(
                self.page.waitForNavigation(timeout=timeout),
                self.page.click('#btnLogin'),
            )
        except asyncio.TimeoutError as error:
            LOG.warning('Caught TimeoutError Exception: %s', error)
            return False

        if contains is not None:
            html = await self.page.content()
            for item in contains:
                if item not in html:
                    return False

        return True


    async def get_first_xpath_property(self,xpath,xproperty):
        """ get first occurence of xpath property or return None """
        LOG.debug('xpath is: %s xproperty is: %s', xpath, xproperty)
        try:
            xpath_values = await self.page.Jx(xpath)
            first_xpath_val = await (await xpath_values[0].getProperty(xproperty)).jsonValue()
        except (IndexError) as error:
            LOG.debug('Index exception %s', error)
            first_xpath_val = None

        return first_xpath_val
