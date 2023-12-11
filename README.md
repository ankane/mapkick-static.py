# Mapkick Static

Create beautiful static maps with one line of Python. No more fighting with mapping libraries!

[See it in action](#maps)

:fire: For JavaScript maps, check out [Mapkick.py](https://chartkick.com/mapkick-py)

[![Build Status](https://github.com/ankane/mapkick-static.py/actions/workflows/build.yml/badge.svg)](https://github.com/ankane/mapkick-static.py/actions)

## Installation

Run:

```sh
pip install mapkick-static
```

Then follow the instructions for your web framework:

- [Django](#django)
- [Flask](#flask)

Mapkick Static uses the [Mapbox Static Images API](https://docs.mapbox.com/api/maps/static-images/). [Create a Mapbox account](https://account.mapbox.com/auth/signup/) to get an access token and set `os.environ['MAPBOX_ACCESS_TOKEN']` in your environment.

### Django

Create a map in a view

```python
from mapkick.static import StaticMap

def index(request):
    map = StaticMap([{'latitude': 37.7829, 'longitude': -122.4190}])
    return render(request, 'home/index.html', {'map': map})
```

And add it to the template

```django
{{ map }}
```

### Flask

Create a map in a route

```python
from mapkick.static import StaticMap

def index():
    map = StaticMap([{'latitude': 37.7829, 'longitude': -122.4190}])
    return render_template('home/index.html', map=map)
```

And add it to the template

```jinja
{{ map }}
```

## Maps

Point map

<img src="https://chartkick.com/mapkick-static/map-2x?v3" alt="Point map" width="100%" height="100%">

```python
StaticMap([{'latitude': 37.7829, 'longitude': -122.4190}])
```

Area map

<img src="https://chartkick.com/mapkick-static/area-map-2x?v1" alt="Area map" width="100%" height="100%">

```python
StaticAreaMap([{'geometry': {'type': 'Polygon', 'coordinates': ...}}])
```

## Data

Data can be an array

```python
StaticMap([{'latitude': 37.7829, 'longitude': -122.4190}])
```

### Point Map

Use `latitude` or `lat` for latitude and `longitude`, `lon`, or `lng` for longitude

You can specify a color for each data point

```python
{
    'latitude': ...,
    'longitude': ...,
    'color': '#f84d4d'
}
```

### Area Map

Use `geometry` with a GeoJSON `Polygon` or `MultiPolygon`

You can specify a color for each data point

```python
{
    'geometry': {'type': 'Polygon', 'coordinates': ...},
    'color': '#0090ff'
}
```

## Options

Width and height

```python
StaticMap(data, width=800, height=500)
```

Alt text

```python
StaticMap(data, alt='Map of ...')
```

Marker color

```python
StaticMap(data, markers={'color': '#f84d4d'})
```

Map style

```python
StaticMap(data, style='mapbox/outdoors-v12')
```

## History

View the [changelog](https://github.com/ankane/mapkick-static.py/blob/master/CHANGELOG.md)

## Contributing

Everyone is encouraged to help improve this project. Here are a few ways you can help:

- [Report bugs](https://github.com/ankane/mapkick-static.py/issues)
- Fix bugs and [submit pull requests](https://github.com/ankane/mapkick-static.py/pulls)
- Write, clarify, or fix documentation
- Suggest or add new features

To get started with development:

```sh
git clone https://github.com/ankane/mapkick-static.py.git
cd mapkick-static.py
pip install -r requirements.txt
pytest
```
