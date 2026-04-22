import os
from glob import glob
from textwrap import dedent
from typing import Any, cast

import click
import importlib_resources
from tutor import config as tutor_config
from tutor import fmt, hooks
from tutormfe.hooks import MFE_APPS, PLUGIN_SLOTS

from .__about__ import __version__

# Configuration
config: dict[str, dict[str, Any]] = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "PARAGON_THEME_URLS": {},
        "DISABLE_THEME_SWITCH": False,
        "MFE": {},
        "MFE_LOGO_URL": "",
        "MFE_LOGO_WHITE_URL": "",
        "MFE_LOGO_TRADEMARK_URL": "",
        "MFE_FAVICON_URL": "",
        "OVERLAY_HTML": None,
        # Repos
        "THEME_REPOS": None,
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
    ],
)

# Force the rendering of scss files, even though they are included in a "partials" directory
hooks.Filters.ENV_PATTERNS_INCLUDE.add_item(
    r"theme/lms/static/sass/partials/lms/theme/"
)

# Enable the catalog microfrontend and set its URL in settings
# Remove after Ulmo release, when the catalog MFE will be enabled by default
hooks.Filters.ENV_PATCHES.add_items(
    [
        (
            "openedx-common-settings",
            'CATALOG_MICROFRONTEND_URL = "http://{{ MFE_HOST }}/catalog"',
        ),
        (
            "openedx-development-settings",
            "CATALOG_MICROFRONTEND_URL = \"http://{{ MFE_HOST }}:{{ get_mfe('catalog').port }}/catalog\"",
        ),
        (
            "openedx-lms-common-settings",
            "ENABLE_CATALOG_MICROFRONTEND = True",
        ),
    ]
)


def _theme_switch_disabled() -> bool:
    current_context = click.get_current_context(silent=True)
    if current_context is None:
        return False

    root = current_context.params.get("root")
    if not root:
        return False

    configuration = tutor_config.load(root)
    return bool(configuration.get("BRANDING_DISABLE_THEME_SWITCH", False))


def _overlay_html_defined() -> bool:
    current_context = click.get_current_context(silent=True)
    if current_context is None:
        return False

    root = current_context.params.get("root")
    if not root:
        return False

    configuration = tutor_config.load(root)
    return bool(configuration.get("BRANDING_OVERLAY_HTML"))


if not _theme_switch_disabled():
    PLUGIN_SLOTS.add_item(
        (
            "all",
            "footer_slot",
            dedent("""
                {
                  op: PLUGIN_OPERATIONS.Insert,
                  widget: {
                    id: 'branding_theme_selector',
                    type: DIRECT_PLUGIN,
                    priority: 80,
                    RenderWidget: ThemeSelectorFooterWidget,
                  },
                }
                """).strip(),
        )
    )

if _overlay_html_defined():
    PLUGIN_SLOTS.add_item(
        (
            "catalog",
            "org.openedx.frontend.catalog.home_page.overlay_html",
            dedent("""
                {
                  op: PLUGIN_OPERATIONS.Hide,
                  widgetId: 'default_contents',
                }
                """).strip(),
        )
    )
    PLUGIN_SLOTS.add_item(
        (
            "catalog",
            "org.openedx.frontend.catalog.home_page.overlay_html",
            dedent("""
                {
                  op: PLUGIN_OPERATIONS.Insert,
                  widget: {
                    id: 'branding_overlay_html',
                    type: DIRECT_PLUGIN,
                    RenderWidget: BrandingOverlayHtmlWidget,
                  },
                }
                """).strip(),
        )
    )


@MFE_APPS.add()  # type: ignore[untyped-decorator]
def _add_my_mfe(mfes: dict[str, Any]) -> dict[str, Any]:
    # Enable the catalog microfrontend and set its URL in settings
    # Remove after Ulmo release, when the catalog MFE will be enabled by default
    mfes.setdefault(
        "catalog",
        {
            "repository": "https://github.com/openedx/frontend-app-catalog.git",
            "port": 1998,
            "version": "master",
        },
    )
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
