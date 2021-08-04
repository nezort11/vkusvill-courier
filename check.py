from requests import get
from util import id_courier, vkusvill_token


def main():
    api_url = "https://mobile.vkusvill.ru/api/sql/exec/"

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
        'date_from': '20210801',
        'date_to': '20210807'
    }

    taken_payload = {
        'func': 'loyalty.dbo.Parcels_GetParcelsShop',
        'id_courier': id_courier,
        'date_from': '20210801',
        'date_to': '20210807'
    }

    r1 = get(api_url, prepare_payload, headers=headers)
    r2 = get(api_url, ready_payload, headers=headers)
    r3 = get(api_url, taken_payload, headers=headers)

    prepare = r1.json()[0]
    ready = r2.json()[0]
    taken = r3.json()[0]

    def print_parcel(p):
        distance = int(float(p['distance']))
        weight = round(float(p['ves']))
        address = p['corr_addr']
        print(f"- {weight}kg, {distance}m - {address}")

    print("Parcels prepare: ")
    if len(prepare) > 0:
        for p in prepare:
            print_parcel(p)
    else:
        print("- No")

    print("Parcels ready: ")
    if len(ready) > 0:
        for p in ready:
            print_parcel(p)
    else:
        print("- No")

    print("Parcels taken: ")
    if len(ready) > 0:
        for p in taken:
            print_parcel(p)
    else:
        print("- No")


if __name__ == "__main__":
    main()
