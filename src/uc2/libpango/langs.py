# -*- coding: utf-8 -*-
#
#  Copyright (C) 2016 by Ihor E. Novikov
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License
#  as published by the Free Software Foundation, either version 3
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


MYANMAR = ('\u1000', '\u109f')
MYANMAR_EXT = ('\uaa60', '\uaa7f')
ARABIC = ('\u0600', '\u06ff')
ARABIC_SUPPLEMENT = ('\u0750', '\u077f')
ARABIC_FORMS_A = ('\ufb50', '\ufdff')
ARABIC_FORMS_B = ('\ufe70', '\ufeff')


def check_unicode_range(rng, symbol):
    return rng[0] <= symbol <= rng[1]


def check_lang(text, ranges):
    test = text
    if len(test) > 20:
        test = test[:20]
    ret = False
    for item in test:
        for reg in ranges:
            if check_unicode_range(reg, item):
                ret = True
        if ret:
            break
    return ret


def check_maynmar(text):
    return check_lang(text, (MYANMAR, MYANMAR_EXT))


def check_arabic(text):
    return check_lang(text, (ARABIC, ARABIC_SUPPLEMENT,
                             ARABIC_FORMS_A, ARABIC_FORMS_B))
