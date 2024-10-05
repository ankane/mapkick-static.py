from mapkick.static import StaticMap, StaticAreaMap, StaticBaseMap
import os
import pytest
from random import random
import subprocess

if 'MAPBOX_ACCESS_TOKEN' not in os.environ:
    os.environ['MAPBOX_ACCESS_TOKEN'] = 'pk.token'


class TestMap:
    def test_static_map(self):
        self.assert_map(StaticMap(self.data()))

    def test_static_area_map(self):
        self.assert_map(StaticAreaMap([]))

    def test_invalid_style(self):
        with pytest.raises(ValueError) as excinfo:
            StaticMap([], style='custom')
        assert 'Invalid style' in str(excinfo.value)

    def test_secret_token(self):
        with pytest.raises(ValueError) as excinfo:
            StaticMap([], access_token='sk.token')
        assert 'Expected public access token' in str(excinfo.value)

    def test_invalid_token(self):
        with pytest.raises(ValueError) as excinfo:
            StaticMap([], access_token='token')
        assert 'Invalid access token' in str(excinfo.value)

    def test_request_too_large(self):
        data = [{'latitude': random(), 'longitude': random()} for _ in range(265)]
        with pytest.warns(UserWarning, match='URL exceeds 8192 byte limit'):
            StaticMap(data)

    def data(self):
        return [{'latitude': 1.23, 'longitude': 4.56}]

    def assert_map(self, map):
        assert isinstance(map, StaticBaseMap)
        assert 'https://api.mapbox.com/' in map.url
        assert str(map).startswith('<img ')
        if 'OPEN' in os.environ:
            subprocess.run(['open', map.url])
