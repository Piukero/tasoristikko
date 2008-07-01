# -*- coding: utf-8 -*-
# Tasoristikko: Tasristikkoja ratkaiseva ohjelma
# Copyright (C) 2008 Ville Leskinen
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

"""Tässä modulissa on ohjelman omat poikkeukset."""

class RistikkoIOVirhe(Exception):
    """Luokka, joka kuvaa ristikon IO-operaatioissa tapahtunutta virhettä."""
    def __init__(self, virhe):
        """@param virhe: tapahtunut virhe
        @type virhe: C{string}"""
        self.virhe = virhe

    def __str__(self):
        return 'Virhe ristikon IO-operaatiossa: %s' % self.virhe
