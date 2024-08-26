# pylint: disable=line-too-long  # This is data, not code
PROFILE = {
    "include_profiles": ["opentype"],
    "sections": {
        "Superfamily Checks": [
            "superfamily/list",
            "superfamily/vertical_metrics",
        ],
        "UFO Sources": [
            "designspace_has_consistent_codepoints",
            "designspace_has_consistent_glyphset",
            "designspace_has_consistent_groups",
            "designspace_has_default_master",
            "designspace_has_sources",
            "ufolint",
            # "ufo_consistent_curve_type",  # FIXME (orphan check) https://github.com/fonttools/fontbakery/pull/4809
            "ufo_features_default_languagesystem",
            # "ufo_no_open_corners",  # FIXME (orphan check) https://github.com/fonttools/fontbakery/pull/4809
            "ufo_recommended_fields",
            "ufo_required_fields",
            "ufo_unnecessary_fields",
        ],
        "Universal Profile Checks": [
            "alt_caron",
            "arabic_high_hamza",
            "arabic_spacing_symbols",
            # "caps_vertically_centered",  # Disabled: issue #4274
            "case_mapping",
            "cjk_chws_feature",
            "contour_count",
            "family/single_directory",
            "family/vertical_metrics",
            "family/win_ascent_and_descent",
            "fvar_name_entries",
            "fontbakery_version",
            "freetype_rasterizer",
            "gpos7",
            "gsub/smallcaps_before_ligatures",
            "inconsistencies_between_fvar_stat",
            "interpolation_issues",
            "legacy_accents",
            "linegaps",
            "mandatory_glyphs",
            "math_signs_width",
            "name/trailing_spaces",
            "no_debugging_tables",
            "os2_metrics_match_hhea",
            "ots",
            "required_tables",
            "rupee",
            "sfnt_version",
            "soft_hyphen",
            "STAT_in_statics",
            "STAT_strings",
            "tabular_kerning",
            "transformed_components",
            "ttx_roundtrip",
            "typoascender_exceeds_Agrave",
            "unique_glyphnames",
            "unreachable_glyphs",
            "unwanted_aat_tables",
            "unwanted_tables",
            "valid_glyphnames",
            "whitespace_glyphnames",
            "whitespace_glyphs",
            "whitespace_ink",
            "whitespace_widths",
        ],
    },
}
