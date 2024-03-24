# Import folium MarkerCluster plugin
from folium.plugins import MarkerCluster
# Import folium MousePosition plugin
from folium.plugins import MousePosition
# Import folium DivIcon plugin
from folium.features import DivIcon
import folium
from folium.plugins import Realtime
import asyncio
import winsdk.windows.devices.geolocation as wdg


class ViewMap:

    def __init__(self):
        self.map = None
        asyncio.run(self.init())

    async def getCoords(self):
        locator = wdg.Geolocator()
        pos = await locator.get_geoposition_async()
        return [pos.coordinate.latitude, pos.coordinate.longitude]

    async def init(self):
        self.Coords = await self.getCoords()
        self.map = self.create_map()

    def create_map(self):
        coords = self.Coords
        world_map = folium.Map(
            location=coords,
            zoom_start=30
        )
        return world_map

    def map_creator(self):
        if self.map is None:
            print("ERROR: Map not created yet")
            return
        # self.map.save("map.html")
        self.map.show_in_browser()








if __name__ == '__main__':
    view_map = ViewMap()
    view_map.map_creator()


