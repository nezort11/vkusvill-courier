"""VkusVill courier API (courier.fullstack.vkusvill.ru) for Python."""

from datetime import datetime, timedelta

import requests

__all__ = ['VkusVillCourierAPI', 'Parcel']

API_URL = "https://mobile.vkusvill.ru/api/sql/exec/"

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0",
}


class Parcel:
    """Class representing parcel."""

    def __init__(self, parcel: dict):
        """Make parcel object form parcel dict."""
        self.id = parcel['id_order']
        self.code = parcel['id_order'][-4:]
        self.weight = round(float(parcel['ves']), 1)
        self.distance = round(float(parcel['distance']))
        self.address = parcel['corr_addr'].replace("Россия", '').replace(
            "Санкт-Петербург", '').strip(' ,-.')

    def __str__(self):
        """Format parcel information."""
        return f"{self.distance}m {self.weight}kg - {self.address} [{self.code}]"

    def __repr__(self):
        """Represent parcel."""
        return f"<Parcel id={self.id}, distance={self.distance}, weight={self.weight}>"


class VkusVillCourierAPI:
    """Class for VkusVill courier API."""

    def __init__(self, courier_id, api_token):
        """Create API instance."""

        now = datetime.now()
        self.date_from = (now - timedelta(days=3)).strftime('%Y%m%d')
        self.date_to = (now + timedelta(days=3)).strftime('%Y%m%d')

        self.base_payload = {
            'id_courier': courier_id,
            'date_from': self.date_from,
            'date_to': self.date_to
        }

        self.headers = BASE_HEADERS | {
            "x-vkusvill-device": "android",
            'x-vkusvill-token': api_token
        }

    def _get_parcels(self, func):
        """Return specific parcel using func."""
        payload = self.base_payload | {
            'func': func
        }
        response = requests.get(API_URL, payload, headers=self.headers)
        response.raise_for_status()
        parcels = response.json()[0]
        return [Parcel(p) for p in parcels]

    def get_parcels_prepare(self):
        """Return prepare parcels objects."""
        func = 'loyalty.dbo.Parcels_GetParcelsPrepare'
        return self._get_parcels(func)

    def get_parcels_ready(self):
        """Return ready parcels objects."""
        func = 'loyalty.dbo.Parcels_GetParcelsShop_new'
        return self._get_parcels(func)

    def get_parcels_taken(self):
        """Return taken parcels objects."""
        func = 'loyalty.dbo.Parcels_GetParcelsShop'
        return self._get_parcels(func)
