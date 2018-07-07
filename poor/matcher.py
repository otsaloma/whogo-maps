# -*- coding: utf-8 -*-

# Copyright (C) 2018 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Map matching."""

import json
import poor
import urllib.parse

__all__ = ("Matcher",)


class Matcher:

    """Map matching."""

    def __init__(self):
        self.positions = []

    def match(self, lon, lat, accuracy):
        n = { "lat": lat, "lon": lon }
        if len(self.positions) > 5:
            del self.positions[0]

        if len(self.positions) < 1:
            self.positions.append(n)
            return None

        p = self.positions[-1]
        d = poor.util.calculate_distance(lon, lat, p["lon"], p["lat"])
        if d > 10:
            self.positions.append(n)
            pos = self.positions
        else:
            pos = []
            pos.extend(self.positions)
            pos.append(n)

        task = dict(shape = pos,
                    costing = "auto",
                    gps_accuracy = accuracy,
                    shape_match = "map_snap")

        result = poor.http.get_json(
            'http://localhost:8554/trace_attributes?json=' +
            urllib.parse.quote(json.dumps(task)))

        mpoints = result.get("matched_points", [])
        if len(mpoints) == len(pos) and mpoints[-1].get('type', '') != 'unmatched':
            p = mpoints[-1]
            e = result['edges'][p['edge_index']]
            ed = p['distance_along_edge']
            direction = e['begin_heading']*(1-ed) + e['end_heading']*ed
            return {
                'latitude': p['lat'], 'longitude': p['lon'],
                'horizontalAccuracy': accuracy,
                'horizontalAccuracyValid': True,
                'latitudeValid': True,
                'longitudeValid': True,
                'speed': 1.0,
                'speedValid': True,
                'direction': direction,
            }

        return None

    def clear(self):
        self.positions = []
