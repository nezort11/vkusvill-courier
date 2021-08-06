from datetime import datetime, timedelta
from requests import get
from util import id_courier, vkusvill_token


def print_parcels(parcels, name):
    n = len(parcels)
    if n > 0:
        print(f"Parcels {name} ({n}): ")
        for i, p in enumerate(parcels):
            # Formatted data
            weight = round(float(p['ves']))
            distance = round(float(p['distance']))
            address = p['corr_addr'].replace(
                "Санкт-Петербург", '').strip(' ,-')

            # Format parcel
            print(f"{i+1}) {weight}kg, {distance}m - {address} []")
    else:
        print(f"Parcels {name}: \n- No")


def main():
    api_url = "https://mobile.vkusvill.ru/api/sql/exec/"

    now = datetime.now()
    date_from = (now - timedelta(days=3)).strftime('%Y%m%d')
    date_to = (now + timedelta(days=3)).strftime('%Y%m%d')

    headers = {
        "x-vkusvill-device": "android",
        "x-vkusvill-token": vkusvill_token
    }

    prepare_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsPrepare',
        'id_courier': id_courier
    }

    ready_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsShop_new',
        'id_courier': id_courier,
        'date_from': date_from,
        'date_to': date_to
    }

    taken_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsShop',
        'id_courier': id_courier,
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


if __name__ == "__main__":
    main()
