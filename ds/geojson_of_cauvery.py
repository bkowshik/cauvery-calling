import json

import geojson
import osmium


class CauveryHandler(osmium.SimpleHandler):

    def __init__(self):
        osmium.SimpleHandler.__init__(self)

        # To store ways and relations related to Cauvery.
        self.ways = []

    def way(self, w):

        if 'waterway' not in w.tags:
            return

        if 'name' not in w.tags:
            return

        if 'Kaveri' not in w.tags['name']:
            return

        # Tags must be copied when they need to be stored.
        properties = dict(w.tags)
        properties['id'] = w.id
        properties['updated_at'] = w.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        properties['version'] = w.version

        # Turn nodes of the way into a geometry feature.
        geometry = geojson.LineString([(n.lon, n.lat) for n in w.nodes])

        # Turn geometry into a geojson feature.
        feature = geojson.Feature(geometry=geometry, properties=properties)
        print(feature)

        # Append the feature.
        self.ways.append(feature)


def main():

    h = CauveryHandler()

    filename = '../data/india-latest.osm.pbf'
    h.apply_file(filename, locations=True)
    print('Total ways: {}'.format(len(h.ways)))

    # Create a feature collection with all the features.
    fc = geojson.FeatureCollection([])
    fc.features = h.ways

    with open('../data/kaveri.geojson', 'w') as f:
        json.dump(fc, f, indent=4)


if __name__ == '__main__':
    main()
