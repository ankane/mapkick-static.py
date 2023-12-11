from html import escape
import json
import os
from urllib.parse import quote_plus, urlencode
import warnings


class StaticBaseMap:
    def __init__(self, data, width=800, height=500, markers={}, style='mapbox/streets-v12', alt='Map', access_token=None, view_context=None):
        self.width = int(width)
        self.height = int(height)
        self.alt = alt
        self.view_context = view_context

        prefix = 'https://api.mapbox.com/styles/v1'
        style = self.__set_style(style)
        geojson = self.__create_geojson(data, markers)
        geojson2 = json.dumps(geojson, separators=(',', ':'))
        overlay = f'geojson({quote_plus(geojson2)})'
        viewport = self.__set_viewport(geojson)
        size = '%dx%d' % (int(self.width), int(self.height))
        query = self.__set_query(access_token, viewport)

        url = f'{prefix}/{style}/static/{overlay}/{viewport}/{size}'
        self.url = f'{url}?{query}'
        self.url_2x = f'{url}@2x?{query}'

        self.__check_request_size()

    def __html__(self):
        srcset = f'{self.url} 1x, {self.url_2x} 2x'
        return f'<img src="{escape(self.url)}" alt="{escape(self.alt)}" style="{escape(self.__image_style())}" srcset="{escape(srcset)}" />'

    def __str__(self):
        html = self.__html__()
        try:
            from django.utils.safestring import mark_safe
            return mark_safe(html)
        except ImportError:
            return html

    def __set_style(self, style):
        if style.startswith('mapbox://styles/'):
            style = style[16:]
        if style.count('/') != 1:
            raise ValueError('Invalid style')
        return '/'.join([quote_plus(v) for v in style.split('/', 2)])

    def __create_geojson(self, data, markers):
        default_color = markers.get('color')
        return {
            'type': 'FeatureCollection',
            'features': self._generate_features(data, default_color)
        }

    def __set_viewport(self, geojson):
        if not geojson['features']:
            return '0,0,0'

        if len(geojson['features']) == 1:
            geometry = geojson['features'][0]['geometry']
            if geometry['type'] == 'MultiPoint' and len(geometry['coordinates']) == 1:
                coordinates = geometry['coordinates'][0]
                zoom = 15
                return '%f,%f,%d' % (self._round_coordinate(float(coordinates[0])), self._round_coordinate(float(coordinates[1])), int(zoom))

        return 'auto'

    def __set_query(self, access_token, viewport):
        params = {}
        params['access_token'] = self.__check_access_token(access_token or os.environ.get('MAPBOX_ACCESS_TOKEN'))
        if viewport == 'auto':
            params['padding'] = 40
        return urlencode(params)

    def __check_access_token(self, access_token):
        if access_token is None:
            raise ValueError('No access token')
        elif access_token.startswith('sk.'):
            # can bypass with string keys
            # but should help prevent common errors
            raise ValueError('Expected public access token')
        elif not access_token.startswith('pk.'):
            raise ValueError('Invalid access token')
        return access_token

    # round to reduce URL size
    def _round_coordinate(self, point):
        return round(point, 7)

    # https://docs.mapbox.com/api/overview/#url-length-limits
    def __check_request_size(self):
        if len(self.url_2x) > 8192:
            warnings.warn(f'[mapkick-static] URL exceeds 8192 byte limit of API ({len(self.url_2x)} bytes)')

    def __image_style(self):
        return 'width: %dpx; height: %dpx;' % (int(self.width), int(self.height))


class StaticMap(StaticBaseMap):
    def _generate_features(self, data, default_color):
        if not default_color:
            default_color = '#f84d4d'
        default_icon = None

        groups = {}
        for v in data:
            color = v.get('color', default_color)
            icon = v.get('x_icon', default_icon)
            if color not in groups:
                groups[color] = {}
            if icon not in groups[color]:
                groups[color][icon] = []
            groups[color][icon].append(v)

        features = []
        for color, vc in groups.items():
            for icon, vs in vc.items():
                geometry = {
                    'type': 'MultiPoint',
                    'coordinates': [[self._round_coordinate(vi) for vi in self.__row_coordinates(v)] for v in vs]
                }

                properties = {
                    'marker-color': color
                }
                if icon:
                    properties['marker-symbol'] = icon

                features.append({
                    'type': 'Feature',
                    'geometry': geometry,
                    'properties': properties
                })
        return features

    def __row_coordinates(self, row):
        return [row.get('longitude') or row.get('lng') or row.get('lon'), row.get('latitude') or row.get('lat')]


class StaticAreaMap(StaticBaseMap):
    def _generate_features(self, data, default_color):
        if not default_color:
            default_color = '#0090ff'

        features = []
        for v in data:
            color = v.get('color', default_color)
            features.append({
                'type': 'Feature',
                # TODO round coordinates
                'geometry': v['geometry'],
                'properties': {
                    'fill': color,
                    'fill-opacity': 0.3,
                    'stroke': color,
                    'stroke-width': 1,
                    'stroke-opacity': 0.7
                }
            })
        return features
