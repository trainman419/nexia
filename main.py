#!/usr/bin/python3

"""Nexia Climate Device Access"""

import argparse
import code
import readline
import rlcompleter

import aiohttp

from nexia.const import BRAND_NEXIA
from nexia.home import NexiaHome



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", type=str, help="Your Nexia username/email address.")
    parser.add_argument("--password", type=str, help="Your Nexia password.")
    parser.add_argument("--brand", type=str, help="Brand (nexia or asair or trane).")

    args = parser.parse_args()
    brand = args.brand or BRAND_NEXIA

    if not args.username or not args.password:
        parser.print_help()
        exit()

    session = aiohttp.ClientSession()
    nexia_home = NexiaHome(session, username=args.username, password=args.password, brand=brand)

    print("NexiaThermostat instance can be referenced using nt.<command>.")
    print("List of available thermostats and zones:")
    for _thermostat_id in nexia_home.get_thermostat_ids():
        thermostat = nexia_home.get_thermostat_by_id(_thermostat_id)
        _thermostat_name = thermostat.get_name()
        _thermostat_model = thermostat.get_model()
        _thermostat_compressor_speed = thermostat.get_current_compressor_speed()

        print(
            f'{_thermostat_id} - "{_thermostat_name}" ({_thermostat_model}) [{_thermostat_compressor_speed}]'
        )
        print("  Zones:")

        for _zone_id in thermostat.get_zone_ids():
            zone = thermostat.get_zone_by_id(_zone_id)
            _zone_name = zone.get_name()
            _zone_status = zone.get_status()

            print(f'    {_zone_id} - "{_zone_name}" ({_zone_status})')
    del (
        _thermostat_id,
        _thermostat_model,
        _thermostat_name,
        _zone_name,
        _zone_id,
        args,
        parser,
    )

    nexia_home.update()


    variables = globals()
    variables.update(locals())

    readline.set_completer(rlcompleter.Completer(variables).complete)
    readline.parse_and_bind("tab: complete")
    code.InteractiveConsole(variables).interact()

if __name__ == '__main__':
    main()
