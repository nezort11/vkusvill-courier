#!/usr/local/bin/python3
#
# Console app for checking new prepare/ready/taken parcels using VkusVill courier API.
#
from threading import Timer
from os import system

from api import VkusVillCourierAPI
from util import COURIER_ID, VKUSVILL_TOKEN
from notify import notify

prepare_shown = set()
ready_shown = set()


def print_parcels(parcels, name):
    n = len(parcels)
    if n > 0:
        print(f"Parcels {name} ({n}): ")
        for i, p in enumerate(parcels):
            print(f"{i+1}. {p}")
    else:
        print(f"Parcels {name}: \n- No")


def main():
    api = VkusVillCourierAPI(COURIER_ID, VKUSVILL_TOKEN)

    try:
        # Possible HTTPError, ValueError
        prepare = api.get_parcels_prepare()
        ready = api.get_parcels_ready()
        taken = api.get_parcels_taken()
    except Exception as e:
        print(f"HTTP respose error: {e}")
    else:
        print_parcels(prepare, 'prepare')
        print_parcels(ready, 'ready')
        print_parcels(taken, 'taken')

        # Notify about new preparing parcels
        for p in prepare:
            if p.id not in prepare_shown:
                notify("New parcel!", f"{p.weight}kg, {p.distance}m")
                prepare_shown.add(p.id)

        # Notify about new ready parcels
        for p in ready:
            if p.id not in ready_shown:
                notify("Parcel is ready!",
                       f"{p.weight}kg, {p.distance}m")
                ready_shown.add(p.id)


def check(period):
    """Run main function every :period: seconds recursively."""
    system('clear')
    main()
    Timer(period, lambda: check(period)).start()


if __name__ == "__main__":
    # Poll up API periodicly
    check(3)
