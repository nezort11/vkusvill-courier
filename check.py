from datetime import datetime, timedelta
from threading import Timer
from os import system
from requests import get

from util import ID_COURIER, VKUSVILL_TOKEN
from notify import notify

seen = set()


class Parcel:
    """Represent parcel."""

    def __init__(self, parcel):
        """Make object form parcel dict."""
        self.id = parcel['id_order']
        self.code = parcel['id_order'][-4:]
        self.weight = round(float(parcel['ves']), 1)
        self.distance = round(float(parcel['distance']))
        self.address = parcel['corr_addr'].replace(
            "Санкт-Петербург", '').strip(' ,-')

    def __str__(self):
        """Format parcel information."""
        return f"{self.weight}kg, {self.distance}m - {self.address} [{self.code}]"


def print_parcels(parcels, name):
    n = len(parcels)
    if n > 0:
        print(f"Parcels {name} ({n}): ")
        for i, p in enumerate(parcels):
            parcel = Parcel(p)
            print(f"{i+1}. {parcel}")
    else:
        print(f"Parcels {name}: \n- No")


def main():
    api_url = "https://mobile.vkusvill.ru/api/sql/exec/"

    now = datetime.now()
    date_from = (now - timedelta(days=3)).strftime('%Y%m%d')
    date_to = (now + timedelta(days=3)).strftime('%Y%m%d')

    headers = {
        "x-vkusvill-device": "android",
        "x-vkusvill-token": VKUSVILL_TOKEN
    }

    prepare_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsPrepare',
        'id_courier': ID_COURIER
    }

    ready_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsShop_new',
        'id_courier': ID_COURIER,
        'date_from': date_from,
        'date_to': date_to
    }

    taken_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsShop',
        'id_courier': ID_COURIER,
        'date_from': date_from,
        'date_to': date_to
    }

    try:
        r1 = get(api_url, prepare_payload, headers=headers)
        r1.raise_for_status()
        r2 = get(api_url, ready_payload, headers=headers)
        r2.raise_for_status()
        r3 = get(api_url, taken_payload, headers=headers)
        r3.raise_for_status()

        prepare = r1.json()[0]
        ready = r2.json()[0]
        taken = r3.json()[0]

    # Possible HTTPError, ValueError
    except Exception as e:
        print(f"HTTP respose error: {e}")
    else:
        print_parcels(prepare, 'prepare')
        print_parcels(ready, 'ready')
        print_parcels(taken, 'taken')

        # Notify about new and ready parcels
        for p in ready:
            parcel = Parcel(p)
            if parcel.id not in seen:
                notify("Vkusvill", f"Parcel {parcel.code} is ready!")
                seen.add(parcel.id)


def check(period):
    """Run main function every :period: seconds recursively."""
    system('clear')
    main()
    Timer(period, lambda: check(period)).start()


if __name__ == "__main__":
    # Poll up API periodicly
    check(2)
