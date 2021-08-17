# VkusVill Courier Automation Project

This program helps me manage (automates) parcels tracking and tacking. It calles vkusvill API directly and works faster than webapp.

Example:

```sh
$ python3 check.py
Parcels prepare: 
- 9kg, 344m - Санкт-Петербург, Туристская улица, 28к3
Parcels ready: 
- No
```
## Project

**What?**: I want a program that helps me manage parcels as a courier.

1. Get parcels conveniently
2. Notify about new parcels
3. Automate taking parcels

## Program design

Program design (v1):

- design convinient CLI for retriving parcels


2021-08-7:

- Periodic execution
- Python console library (printing, colors, clearing, etc.)
- Runtime/persistant storage + notification


2021-08-14:

- Code API module
- Implement Telegram Bot using API

## Vkussvill courier API

Base API URL: `https://mobile.vkusvill.ru/api/sql/exec/`

GET HTTP request:

    Scheme: https
    Host: mobile.vkusvill.ru
    Filename: /api/sql/exec/
    func: loyalty.dbo.***
    id_courier: ***
    IP Address: 94.79.19.45:443

Information `func`s:

- `loyalty.dbo.delivery_v02_GetCourierInfo` (courier information)
- `loyalty.dbo.delivery_v02_GetCourierContractsList` (courier job)
- `loyalty.dbo.delivery_v02_GetShopInfo` (shop information)
- `loyalty.dbo.delivery_v02_GetCourierMP_build`

Parcels `func`s:

- `loyalty.dbo.Parcels_GetParcelsShop` (parcels taken)
- `loyalty.dbo.Parcels_GetParcelsShop_new` (parcels ready)
- `loyalty.dbo.Parcels_GetParcelsPrepare` (parcels prepare)
- `loyalty.dbo.Parcels_GetParcelsCourier` (parcels done)

## Parcel JSON object structure

```json
{
	"0": {
		"id_order": "32980113",
		"date_order": "2021-08-06 14:43:09.223",
		"date_supply": "2021-08-07 10:00:00.000",
		"status_name": "Оформлен",
		"login": "",
		"FullName": "АННА",
		"phone": "921331****",
		"number": "7810666",
		"shopno": "2056",
		"comment": "Домофон на воротах ***, домофон на парадной ***",
		"count_pos": "12",
		"ves": "8.969000",
		"collected_pkgs": "0",
		"corr_addr": "Санкт-Петербург, Мебельная улица, ****",
		"user_address": "Квартира: *** Домофон: *** Подъезд: * Этаж: *",
		"distance": "1195.166",
		"latitude": "59.9962010000000000",
		"longitude": "30.2173000000000000",
		"gettype": "44",
		"pay_way": "0",
		"id_services_chosen": "1",
		"name_services_chosen": "Доставка сейчас                                   ",
		"freeze": "0",
		"hot": "0",
		"eco": "0",
		"thermolability": "0",
		"id_general": "32980113-1"
	}
}
```

## macOS notifications

macOS notification center API levels:

1. macOS (operating system)
2. Objective-C (system programming language)
3. AppleScript (system scripting language)
4. Bash (system interface)
5. Python (general programming language)
