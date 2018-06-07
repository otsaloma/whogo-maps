# -*- coding: utf-8 -*-

# Copyright (C) 2014 Osmo Salomaa
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

"""Managing a history of search queries."""

import os
import poor

from poor.i18n import _

__all__ = ("HistoryManager",)


class HistoryManager:

    """Managing a history of search queries."""

    _places_blacklist = ["Current position", _("Current position")]

    def __init__(self):
        """Initialize a :class:`HistoryManager` instance."""
        self._path = os.path.join(poor.CONFIG_HOME_DIR, "search-history.json")
        self._place_names = []
        self._place_types = []
        self._places = []
        self._read()

    def add_place(self, place):
        """Add `place` to the list of places."""
        place = place.strip()
        if not place: return
        if place in self._places_blacklist: return
        self.remove_place(place)
        self._places.insert(0, place)

    def add_place_name(self, place_name):
        """Add `place_name` to the list of place names."""
        place_name = place_name.strip()
        if not place_name: return
        self.remove_place_name(place_name)
        self._place_names.insert(0, place_name)

    def add_place_type(self, place_type):
        """Add `place_type` to the list of place types."""
        place_type = place_type.strip()
        if not place_type: return
        self.remove_place_type(place_type)
        self._place_types.insert(0, place_type)

    @property
    def place_names(self):
        """Return a list of place names."""
        return self._place_names[:]

    @property
    def place_types(self):
        """Return a list of place types."""
        return self._place_types[:]

    @property
    def places(self):
        """Return a list of places."""
        return self._places[:]

    def _read(self):
        """Read list of queries from file."""
        with poor.util.silent(Exception, tb=True):
            if os.path.isfile(self._path):
                history = poor.util.read_json(self._path)
                self._places = history.get("places", [])
                self._place_names = history.get("place_names", [])
                self._place_types = history.get("place_types", [])
        for place in self._places_blacklist:
            self.remove_place(place)
        if not self._place_types:
            # Provide some examples of place types.
            self._place_types = ["ATM",
                                 "Café",
                                 "Gas station",
                                 "Grocery store",
                                 "Hotel",
                                 "Pub",
                                 "Restaurant"]

    def remove_place(self, place):
        """Remove `place` from the list of places."""
        place = place.strip().lower()
        for i in reversed(range(len(self._places))):
            if self._places[i].lower() == place:
                del self._places[i]

    def remove_place_name(self, place_name):
        """Remove `place_name` from the list of place names."""
        place_name = place_name.strip().lower()
        for i in reversed(range(len(self._place_names))):
            if self._place_names[i].lower() == place_name:
                del self._place_names[i]

    def remove_place_type(self, place_type):
        """Remove `place_type` from the list of place types."""
        place_type = place_type.strip().lower()
        for i in reversed(range(len(self._place_types))):
            if self._place_types[i].lower() == place_type:
                del self._place_types[i]

    def write(self):
        """Write list of queries to file."""
        with poor.util.silent(Exception, tb=True):
            poor.util.write_json({
                "places": self._places[:1000],
                "place_names": self._place_names[:1000],
                "place_types": self._place_types[:1000],
            }, self._path)
