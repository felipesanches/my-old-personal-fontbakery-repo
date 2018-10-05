#!/usr/bin/env python3
# Copyright 2016 The Fontbakery Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import enum

# =====================================
# GLOBAL CONSTANTS DEFINITIONS
STYLE_NAMES = ["Thin",
               "ExtraLight",
               "Light",
               "Regular",
               "Medium",
               "SemiBold",
               "Bold",
               "ExtraBold",
               "Black",
               "Thin Italic",
               "ExtraLight Italic",
               "Light Italic",
               "Italic",
               "Medium Italic",
               "SemiBold Italic",
               "Bold Italic",
               "ExtraBold Italic",
               "Black Italic"]

RIBBI_STYLE_NAMES = ["Regular",
                     "Italic",
                     "Bold",
                     "BoldItalic",
                     "Bold Italic"]  # <-- Do we really need this one?

# nameID definitions for the name table:
class NameID(enum.IntEnum):
  COPYRIGHT_NOTICE = 0
  FONT_FAMILY_NAME = 1
  FONT_SUBFAMILY_NAME = 2
  UNIQUE_FONT_IDENTIFIER = 3
  FULL_FONT_NAME = 4
  VERSION_STRING = 5
  POSTSCRIPT_NAME = 6
  TRADEMARK = 7
  MANUFACTURER_NAME = 8
  DESIGNER = 9
  DESCRIPTION = 10
  VENDOR_URL = 11
  DESIGNER_URL = 12
  LICENSE_DESCRIPTION = 13
  LICENSE_INFO_URL = 14
  # Name ID 15 is RESERVED
  TYPOGRAPHIC_FAMILY_NAME = 16
  TYPOGRAPHIC_SUBFAMILY_NAME = 17
  COMPATIBLE_FULL_MACONLY = 18
  SAMPLE_TEXT = 19
  POSTSCRIPT_CID_NAME = 20
  WWS_FAMILY_NAME = 21
  WWS_SUBFAMILY_NAME = 22
  LIGHT_BACKGROUND_PALETTE = 23
  DARK_BACKGROUD_PALETTE = 24

NAMEID_STR = {
  NameID.COPYRIGHT_NOTICE: "COPYRIGHT_NOTICE",
  NameID.FONT_FAMILY_NAME: "FONT_FAMILY_NAME",
  NameID.FONT_SUBFAMILY_NAME: "FONT_SUBFAMILY_NAME",
  NameID.UNIQUE_FONT_IDENTIFIER: "UNIQUE_FONT_IDENTIFIER",
  NameID.FULL_FONT_NAME: "FULL_FONT_NAME",
  NameID.VERSION_STRING: "VERSION_STRING",
  NameID.POSTSCRIPT_NAME: "POSTSCRIPT_NAME",
  NameID.TRADEMARK: "TRADEMARK",
  NameID.MANUFACTURER_NAME: "MANUFACTURER_NAME",
  NameID.DESIGNER: "DESIGNER",
  NameID.DESCRIPTION: "DESCRIPTION",
  NameID.VENDOR_URL: "VENDOR_URL",
  NameID.DESIGNER_URL: "DESIGNER_URL",
  NameID.LICENSE_DESCRIPTION: "LICENSE_DESCRIPTION",
  NameID.LICENSE_INFO_URL: "LICENSE_INFO_URL",
  NameID.TYPOGRAPHIC_FAMILY_NAME: "TYPOGRAPHIC_FAMILY_NAME",
  NameID.TYPOGRAPHIC_SUBFAMILY_NAME: "TYPOGRAPHIC_SUBFAMILY_NAME",
  NameID.COMPATIBLE_FULL_MACONLY: "COMPATIBLE_FULL_MACONLY",
  NameID.SAMPLE_TEXT: "SAMPLE_TEXT",
  NameID.POSTSCRIPT_CID_NAME: "POSTSCRIPT_CID_NAME",
  NameID.WWS_FAMILY_NAME: "WWS_FAMILY_NAME",
  NameID.WWS_SUBFAMILY_NAME: "WWS_SUBFAMILY_NAME",
  NameID.LIGHT_BACKGROUND_PALETTE: "LIGHT_BACKGROUND_PALETTE",
  NameID.DARK_BACKGROUD_PALETTE: "DARK_BACKGROUD_PALETTE"
}

# fsSelection bit definitions:
FSSEL_ITALIC         = (1 << 0)
FSSEL_UNDERSCORE     = (1 << 1)
FSSEL_NEGATIVE       = (1 << 2)
FSSEL_OUTLINED       = (1 << 3)
FSSEL_STRIKEOUT      = (1 << 4)
FSSEL_BOLD           = (1 << 5)
FSSEL_REGULAR        = (1 << 6)
FSSEL_USETYPOMETRICS = (1 << 7)
FSSEL_WWS            = (1 << 8)
FSSEL_OBLIQUE        = (1 << 9)

# macStyle bit definitions:
MACSTYLE_BOLD   = (1 << 0)
MACSTYLE_ITALIC = (1 << 1)

# Panose definitions:
PANOSE_PROPORTION__ANY = 0
PANOSE_PROPORTION__NO_FIT = 1
PANOSE_PROPORTION__OLD_STYLE = 2
PANOSE_PROPORTION__MODERN = 3
PANOSE_PROPORTION__EVEN_WIDTH = 4
PANOSE_PROPORTION__EXTENDED = 5
PANOSE_PROPORTION__CONDENSED = 6
PANOSE_PROPORTION__VERY_EXTENDED = 7
PANOSE_PROPORTION__VERY_CONDENSED = 8
PANOSE_PROPORTION__MONOSPACED = 9

# 'post' table / isFixedWidth definitions:
IS_FIXED_WIDTH__NOT_MONOSPACED = 0
IS_FIXED_WIDTH__MONOSPACED = 1  # any non-zero value means monospaced

class PlatformID(enum.IntEnum):
  UNICODE = 0
  MACINTOSH = 1
  ISO = 2
  WINDOWS = 3
  CUSTOM = 4

PLATID_STR = {
  PlatformID.UNICODE: "UNICODE",
  PlatformID.MACINTOSH: "MACINTOSH",
  PlatformID.ISO: "ISO",
  PlatformID.WINDOWS: "WINDOWS",
  PlatformID.CUSTOM: "CUSTOM"
}

# Unicode platform-specific encoding IDs (when platID == 0):
class UnicodeEncodingID(enum.IntEnum):
  UNICODE_1_0 = 0
  UNICODE_1_1 = 1
  ISO_IEC_10646 = 2
  UNICODE_2_0_BMP_ONLY = 3
  UNICODE_2_0_FULL = 4
  UNICODE_VARIATION_SEQUENCES = 5
  UNICODE_FULL = 6

# Windows platform-specific encoding IDs (when platID == 3):
class WindowsEncodingID(enum.IntEnum):
  SYMBOL = 0
  UNICODE_BMP = 1
  SHIFTJIS = 2
  PRC = 3
  BIG5 = 4
  WANSUNG = 5
  JOHAB = 6
  # IDs 7, 8 and 9 are reserved.
  UNICODE_FULL_REPERTOIRE = 10


PLACEHOLDER_LICENSING_TEXT = {
    'UFL.txt': 'Licensed under the Ubuntu Font Licence 1.0.',
    'OFL.txt': 'This Font Software is licensed under the SIL Open Font '
               'License, Version 1.1. This license is available with a FAQ '
               'at: http://scripts.sil.org/OFL',
    'LICENSE.txt': 'Licensed under the Apache License, Version 2.0'
}

# =====================================
# Helper logging class
RED_STR = '\033[1;31;40m{}\033[0m'
GREEN_STR = '\033[1;32;40m{}\033[0m'
YELLOW_STR = '\033[1;33;40m{}\033[0m'
BLUE_STR = '\033[1;34;40m{}\033[0m'
CYAN_STR = '\033[1;36;40m{}\033[0m'
WHITE_STR = '\033[1;37;40m{}\033[0m'

# =====================================
# Check priority levels:
TRIVIAL = 4
LOW = 3
NORMAL = 2
IMPORTANT = 1
CRITICAL = 0  # ON FIRE! Must immediately fix!
