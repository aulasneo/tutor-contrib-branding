from glob import glob
import os
import pkg_resources

from tutor import hooks

from .__about__ import __version__


########################################
# CONFIGURATION
########################################

config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "WELCOME_MESSAGE": "Welcome to Open edX®",
        # Footer links are dictionaries with a "title" and "url"
        # To remove all links, run:
        # tutor config save --set BRANDING_FOOTER_NAV_LINKS=[] --set BRANDING_FOOTER_LEGAL_LINKS=[]
        "FOOTER_NAV_LINKS": [
            {"title": "About", "url": "/about"},
            {"title": "Contact", "url": "/contact"},
        ],
        "FOOTER_LEGAL_LINKS": [
            {"title": "Terms of service", "url": "/tos"},
        ],
        "BACKGROUND": "#ffffff",
        "BG_PRIMARY": "#ffffff",
        "BODY": "#FFFFFF",
        "PRIMARY": "#0000FF",
        "SECONDARY": "#454545",
        "FONT_FAMILY": "",
        "BRAND": "#9D0054",
        "SUCCESS": "#178253",
        "INFO": "#006DAA",
        "DANGER": "#C32D3A",
        "WARNING": "#FFD900",
        "LIGHT": "#E1DDDB",
        "DARK": "#273F2F",
        "ACCENT_A": "#00BBF9",
        "ACCENT_B": "#FFEE88",
        # EXTRAS: additional CSS for html theme
        "EXTRAS": "",
        # OVERRIDES: additional CSS for mfe branding
        "OVERRIDES": "",
        "FONTS": "",
    },
    "unique": {},
    "overrides": {},
}


hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"BRANDING_{key}", value) for key, value in config["defaults"].items()]
)

hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"BRANDING_{key}", value) for key, value in config["unique"].items()]
)

hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config["overrides"].items())
)

########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorbranding", "templates"),
    ]
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("theme", "build/openedx/themes"),
        ("brand-openedx", "plugins/mfe/build/mfe"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"theme/lms/static/sass/partials/lms/theme/")


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorbranding/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorbranding", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
