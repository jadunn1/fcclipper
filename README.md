##fcclipper 
**fcclipper** is an automatic digital coupon clipper for grocery store chain "Food City" and can report current balance.

It has a command line (CLI) interface via:
```console
$ fcclipper
```

![fcclipper main prompt](ext/fcclipper_main.png  "fcclipper main prompt")

Commands can be run directly through command options.
For example:

The help section is available with ```--help``` with all commands:

```console
$ fcclipper --help
Usage: fcclipper [OPTIONS] COMMAND [ARGS]...

  This program is the unoficial CLI for FoodCity - check Fuel Buck Balance
  and clip digital coupons

Options:
  --disable-headless  Display browser.
  -d, --debug         Debug output is logged.
  --version           Show the version and exit.
  --help              Show this message and exit.

Commands:
  clear-cache     Clear cached items.
  clip-coupons    Clip all digital coupons.
  get-fuel-bucks  Get Fuel Buck Points Balance.
  
```
```console
$ fcclipper clip-coupons --help
Usage: fcclipper clip-coupons [OPTIONS]

  Clip all digital coupons.

Options:
  --dry-run  No Coupons are clipped.
  --help     Show this message and exit.
```

Python 3.7+ is required to run. If windows OS is being use the [Official Python Download](https://www.python.org/downloads/) site to install.

The code can be downloaded via command:
```shell
git clone https://github.com/jadunn1/fcclipper.git
```

A virtual environment can be set up if you would like following the  [python venv site](https://docs.python.org/3/library/venv.html)  documentation.

Install the fcclipper code via command:

```console
pip install .
```

 
