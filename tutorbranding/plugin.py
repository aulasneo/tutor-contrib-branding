"""
Tutor plugin to brand your Open edX instance.
"""
import sys
from glob import glob
import os
import zipfile
from pathlib import Path
from urllib.error import HTTPError

import importlib_resources
import click
import requests
from tutormfe.hooks import MFE_APPS


from tutor import config as tutor_config
from tutor import hooks, fmt

from .__about__ import __version__

# Configuration
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
        "HOMEPAGE_BG_IMAGE": "",
        # EXTRAS: additional CSS for html theme
        "EXTRAS": "",
        # OVERRIDES: additional CSS for mfe branding
        "OVERRIDES": "",
        "FONTS": "",
        "MFE": {},
        "MFE_LOGO_URL": '',
        "MFE_LOGO_WHITE_URL": '',
        "MFE_LOGO_TRADEMARK_URL": '',

        # Customizations of the learner dashboard in Quince. May not apply if the MFE is redesigned.
        "HIDE_UPGRADE_BUTTON": True,
        "HIDE_DASHBOARD_SIDEBAR": False,
        "HIDE_PROGRAMS": False,
        "FIT_COURSE_IMAGE": True,

        # static page templates
        "STATIC_TEMPLATE_404": None,
        "STATIC_TEMPLATE_429": None,
        "STATIC_TEMPLATE_ABOUT": None,
        "STATIC_TEMPLATE_BLOG": None,
        "STATIC_TEMPLATE_CONTACT": None,
        "STATIC_TEMPLATE_DONATE": None,
        "STATIC_TEMPLATE_EMBARGO": None,
        "STATIC_TEMPLATE_FAQ": None,
        "STATIC_TEMPLATE_HELP": None,
        "STATIC_TEMPLATE_HONOR": None,
        "STATIC_TEMPLATE_JOBS": None,
        "STATIC_TEMPLATE_MEDIA_KIT": None,
        "STATIC_TEMPLATE_NEWS": None,
        "STATIC_TEMPLATE_PRESS": None,
        "STATIC_TEMPLATE_PRIVACY": None,
        "STATIC_TEMPLATE_SERVER_DOWN": None,
        "STATIC_TEMPLATE_SERVER_ERROR": None,
        "STATIC_TEMPLATE_SERVER_OVERLOADED": None,
        "STATIC_TEMPLATE_SITEMAP": None,
        "STATIC_TEMPLATE_TOS": None,
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

# Initialization tasks
# To run the script from templates/panorama/tasks/myservice/init, add:
with open(
        str(importlib_resources.files("tutorbranding") / "templates" / "tasks" / "lms" / "init"),
        encoding="utf-8",
) as task_file:
    hooks.Filters.CLI_DO_INIT_TASKS.add_item(("lms", task_file.read()))

# Add the "templates" folder as a template root
hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    str(importlib_resources.files("tutorbranding") / "templates")
)

hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("theme", "build/openedx/themes"),
        ("brand-openedx", "plugins/mfe/build/mfe"),
        ("brand-openedx-learner-dashboard", "plugins/mfe/build/mfe"),
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(r"theme/lms/static/sass/partials/lms/theme/")


# MFEs
@MFE_APPS.add()
def _add_my_mfe(mfes):
    configuration = tutor_config.load('')

    for mfe_name, mfe_info in configuration['BRANDING_MFE'].items():
        mfes[mfe_name] = mfe_info

    return mfes


# Commands
@click.group(help="Branding tools", name='branding')
@click.pass_obj
def branding_command(context):  # pylint: disable=unused-argument
    """
    Dummy function to group the branding commands
    :return:
    """


def _download_file(url: str, dest_dir: str, filename: str = None) -> str:
    """
    Download a file from internet and store it in the destination directory.
    :param url: where to get the file from
    :param dest_dir: where to put the file
    :return: file name.
    """
    fmt.echo_info(f"Downloading {url} to {dest_dir}")

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not filename:
            filename = os.path.basename(url)

        with open(os.path.join(dest_dir, filename), "wb") as f:
            f.write(response.content)

    except HTTPError as http_err:
        fmt.echo_error(f'HTTP error occurred downloading {url}: {http_err}')

    return filename

@click.command(help="Download image from url")
@click.pass_obj
def download_images(context):
    """
    Command to download images from a URL.
    :param context: Click context
    :return:
    """
    fmt.echo_info("*** Downloading images ***")
    full_config = tutor_config.load(context.root)

    # Download LMS images
    dest_dir = os.path.join(context.root, 'env', 'build', 'openedx', 'themes',
                            'theme', 'lms', 'static', 'images')

    if "BRANDING_LMS_IMAGES" in full_config:
        for image in full_config['BRANDING_LMS_IMAGES']:
            Path(dest_dir).mkdir(parents=True, exist_ok=True)
            _download_file(url=image.get('url'), filename=image.get('filename'), dest_dir=dest_dir)
    else:
        fmt.echo_alert("No BRANDING_LMS_IMAGES configured")

    # Download CMS images
    dest_dir = os.path.join(context.root, 'env', 'build', 'openedx', 'themes',
                            'theme', 'cms', 'static', 'images')

    if "BRANDING_CMS_IMAGES" in full_config:
        Path(dest_dir).mkdir(parents=True, exist_ok=True)
        for image in full_config['BRANDING_CMS_IMAGES']:
            _download_file(url=image.get('url'), filename=image.get('filename'), dest_dir=dest_dir)
    else:
        fmt.echo_alert("No BRANDING_CMS_IMAGES configured")


@click.command(help="Download and unzip font from url")
@click.pass_obj
def download_fonts(context):
    """
    Command to download fonts from a URL.
    :param context: Click context
    :return:
    """
    full_config = tutor_config.load(context.root)

    # Download fonts
    dest_dirs = [
        os.path.join(context.root, 'env', 'build', 'openedx', 'themes',
                     'theme', 'lms', 'static', 'fonts'),
        os.path.join(context.root, 'env', 'plugins', 'mfe', 'build', 'mfe',
                     'brand-openedx', 'fonts'),
        os.path.join(context.root, 'env', 'plugins', 'mfe', 'build', 'mfe',
                     'brand-openedx-learner-dashboard', 'fonts'),
    ]

    if "BRANDING_FONTS_URLS" in full_config:
        for font_url in full_config['BRANDING_FONTS_URLS']:
            for dest_dir in dest_dirs:
                Path(dest_dir).mkdir(parents=True, exist_ok=True)
                fmt.echo_info(f"Downloading fonts from {font_url}")
                filename = _download_file(url=font_url, dest_dir=dest_dir)

                if filename.endswith('.zip'):
                    # Unzip the file
                    fmt.echo_info(f"Unzipping font file {filename}")
                    zipped_filename = os.path.join(dest_dir, filename)
                    try:
                        with zipfile.ZipFile(zipped_filename, 'r') as zipped_file:
                            zipped_file.extractall(dest_dir)
                            zipped_file.printdir()

                            os.remove(os.path.join(dest_dir, filename))
                    except zipfile.BadZipFile:
                        fmt.echo_error(f"File {zipped_filename} is not a zip file.")
                        sys.exit(1)

    else:
        fmt.echo_alert("No BRANDING_FONTS_URLS configured")


branding_command.add_command(download_images)
branding_command.add_command(download_fonts)

hooks.Filters.CLI_COMMANDS.add_item(branding_command)

# Load patches from files
for path in glob(str(importlib_resources.files("tutorbranding") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
