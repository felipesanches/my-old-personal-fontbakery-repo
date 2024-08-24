PROFILE = {
    "configuration_defaults": {
        "file_size": {
            "WARN_SIZE": 1 * 1024 * 1024,
            "FAIL_SIZE": 16 * 1024 * 1024,
        },
    },
    "include_profiles": ["googlefonts"],
    "sections": {
        "Noto Fonts": [
            "notofonts:cmap/unexpected_subtables",
            "notofonts:unicode_range_bits",
            "notofonts:name/manufacturer",
            "notofonts:name/designer",
            "notofonts:name/trademark",
            "notofonts:os2/vendor",
            "notofonts:hmtx/encoded_latin_digits",
            "notofonts:hmtx/comma_period",
            "notofonts:hmtx/whitespace_advances",
            "notofonts:cmap/alien_codepoints",
            #
            "cmap/format_12",
        ]
    },
    # For builds which target Google Fonts, we do want these checks, but as part of
    # onboarding we will be running check-googlefonts on such builds.
    # On other builds (e.g. targetting Android), we still want most of the Google
    # strictures but size is a premium and we will be expecting to deliver a
    # "minimal" font, so we accept the fact that there will be no Latin set and no
    # hinting information at all.
    "exclude_checks": [
        "googlefonts:glyph_coverage",
        "googlefonts:gasp",
        #
        "render_own_name",
        "smart_dropout",
    ],
}
