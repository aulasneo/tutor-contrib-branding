import os
from glob import glob
from typing import Any, cast

import click
import importlib_resources
from tutor import config as tutor_config
from tutor import fmt, hooks
from tutormfe.hooks import MFE_APPS

from .__about__ import __version__

# Configuration
config: dict[str, dict[str, Any]] = {
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
        "LMS_IMAGES": [],
        "CMS_IMAGES": [],
        "FONTS_URLS": [],
        "MFE": {},
        "FRONTEND_COMPONENT_HEADER_REPO": None,
        "FRONTEND_COMPONENT_FOOTER_REPO": None,
        "MFE_LOGO_URL": "",
        "MFE_LOGO_WHITE_URL": "",
        "MFE_LOGO_TRADEMARK_URL": "",
        # Repos
        "MFE_PLATFORM_REPO": None,
        "THEME_REPOS": None,
        # Customizations of the learner dashboard in Quince. May not apply if the MFE is redesigned.
        "HIDE_DASHBOARD_SIDEBAR": False,
        "HIDE_LOOKING_FOR_CHALLENGE_WIDGET": False,
        "FIT_COURSE_IMAGE": True,
        "INDEX_ADDITIONAL_HTML": None,
        "CERTIFICATE_HTML": None,
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

hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))

# Initialization tasks
# To run the script from templates/panorama/tasks/myservice/init, add:
with open(
    str(
        importlib_resources.files("tutorbranding")
        / "templates"
        / "tasks"
        / "lms"
        / "init"
    ),
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
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(
    r"theme/lms/static/sass/partials/lms/theme/"
)


@MFE_APPS.add()  # type: ignore[untyped-decorator]
def _add_my_mfe(mfes: dict[str, Any]) -> dict[str, Any]:
    current_context = click.get_current_context()
    root = current_context.params.get("root")
    if root:
        configuration = tutor_config.load(root)
        branding_mfe = cast(dict[str, dict[str, Any]], configuration["BRANDING_MFE"])
        for mfe_name, mfe_config in branding_mfe.items():
            # Check for custom MFE port
            if mfe_name not in mfes:
                if "repository" not in mfe_config:
                    raise click.ClickException(
                        f"Custom MFE {mfe_name} must have a repository"
                    )
                if "port" not in mfe_config:
                    raise click.ClickException(
                        f"Custom MFE {mfe_name} must have a port"
                    )
                if not mfe_config["repository"].endswith(".git"):
                    raise click.ClickException(
                        f"Custom MFE {mfe_name} repository must end with .git"
                    )
                for base_mfe_name, base_mfe_config in mfes.items():
                    if base_mfe_config["port"] == mfe_config["port"]:
                        raise click.ClickException(
                            f"Custom MFE {mfe_name} port {mfe_config['port']} "
                            f"already taken by {base_mfe_name}"
                        )
                fmt.echo_alert(
                    "Adding custom MFE "
                    f"{mfe_name} with repository {mfe_config['repository']} "
                    f"and port {mfe_config['port']}"
                )
                mfes[mfe_name] = mfe_config
            else:
                mfes[mfe_name].update(mfe_config)
    return mfes


# Load patches from files
for path in glob(str(importlib_resources.files("tutorbranding") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
