# Tutor Branding Plugin

This plugin customizes Open edX branding for Tutor, with a focus on Ulmo-era MFE theming.

## Installation

```bash
pip install tutor-contrib-branding
```

This release targets Open edX Ulmo with Tutor 21.x.

## Quick Start

- Register for free at [branding.aulasneo.com](https://branding.aulasneo.com). 
Follow the instructions to create and publish your theme. Copy the provided tutor command.
- Enable the `tutor-contrib-branding` plugin.
- Paste the tutor command
- Restart services

Now you can tweak the theme parameters in <https://branding.aulasneo.com> and see the results 
in real time in your Open edX site (you might need to hard refresh or clear cache in your browser
to see the changes).

Refer to the [Branding documentation](https://docs.aulasneo.com/branding/index.html) for more information.

## Current approach

Branding is now centered on externally published Paragon theme assets.
The [Branding](https://branding.aulasneo.com) applications is an online editor that manages your
Paragon assets and publishes it to be used in your Open edX site with no effort. It provides the 
tutor commands you need to link your site with the theme.

The supported path is:

- publish Paragon `core.css` and variant CSS files from your design-token theme
- point MFEs at those assets with `BRANDING_PARAGON_THEME_URLS`
- configure logos and favicon explicitly with `BRANDING_MFE_LOGO_URL`, `BRANDING_MFE_LOGO_WHITE_URL`, `BRANDING_MFE_LOGO_TRADEMARK_URL`, and `BRANDING_MFE_FAVICON_URL`
- use `BRANDING_THEME_REPOS` only for comprehensive theme content that still belongs to legacy pages, mainly certificates and static pages

Official references:

- Open edX design tokens: <https://docs.openedx.org/en/latest/community/release_notes/ulmo/design_tokens.html>
- `frontend-platform` theming and `PARAGON_THEME_URLS`: <https://github.com/openedx/frontend-platform/blob/master/docs/how_tos/theming.md>

## Configuring `BRANDING_PARAGON_THEME_URLS`

Set `BRANDING_PARAGON_THEME_URLS` to the `PARAGON_THEME_URLS` object expected by `frontend-platform`.

Example:

```yaml
BRANDING_PARAGON_THEME_URLS:
  core:
    url: "https://cdn.example.com/theme/core.css"
  defaults:
    light: light
    dark: dark
  variants:
    light:
      url: "https://cdn.example.com/theme/light.css"
    dark:
      url: "https://cdn.example.com/theme/dark.css"
    high-contrast-dark:
      url: "https://cdn.example.com/theme/high-contrast-dark.css"
```

When multiple variants are declared, this plugin adds a footer theme selector to MFEs. It supports:

- `Auto`
- the configured default light variant
- the configured default dark variant, if present
- any additional variants declared under `BRANDING_PARAGON_THEME_URLS.variants`

## MFE logos and favicon

MFEs still expect explicit asset URLs for brand images.

Available settings:

- `BRANDING_MFE_LOGO_URL`
- `BRANDING_MFE_LOGO_WHITE_URL`
- `BRANDING_MFE_LOGO_TRADEMARK_URL`
- `BRANDING_MFE_FAVICON_URL`

These values must be public URLs.

## Catalog home page overlay

`BRANDING_OVERLAY_HTML` replaces the catalog home page overlay HTML when it is defined.

This value is passed through the `org.openedx.frontend.catalog.home_page.overlay_html` plugin slot and is only applied when the setting is set.

## Theme repositories and comprehensive theming

`BRANDING_THEME_REPOS` is still supported, but only for the remaining legacy/comprehensive theme surface.

That means:

- certificates
- legacy static pages
- other legacy Django-rendered theming needs that are still served from the comprehensive theme

Example:

```yaml
BRANDING_THEME_REPOS:
  - name: my-theme
    url: https://github.com/myorg/my-theme.git
    version: main
```

After updating the configuration:

```bash
tutor config save
tutor images build openedx
tutor local do init --limit branding
```

Notes:

- only one theme can be active at a time
- do not use `theme` as a custom theme name; that name is reserved for the base theme directory
- assign the theme in Django admin if you need to switch the active comprehensive theme for a site

## Deprecated and removed settings

The following legacy build-time branding settings are no longer supported and have been removed in favor of externally published Paragon theme assets and runtime MFE configuration:

- `BRANDING_WELCOME_MESSAGE`
- `BRANDING_FOOTER_NAV_LINKS`
- `BRANDING_FOOTER_LEGAL_LINKS`
- `BRANDING_BACKGROUND`
- `BRANDING_BG_PRIMARY`
- `BRANDING_BODY`
- `BRANDING_PRIMARY`
- `BRANDING_SECONDARY`
- `BRANDING_FONT_FAMILY`
- `BRANDING_BRAND`
- `BRANDING_SUCCESS`
- `BRANDING_INFO`
- `BRANDING_DANGER`
- `BRANDING_WARNING`
- `BRANDING_LIGHT`
- `BRANDING_DARK`
- `BRANDING_ACCENT_A`
- `BRANDING_ACCENT_B`
- `BRANDING_HOMEPAGE_BG_IMAGE`
- `BRANDING_EXTRAS`
- `BRANDING_OVERRIDES`
- `BRANDING_FONTS`
- `BRANDING_FONTS_URLS`
- `BRANDING_LMS_IMAGES`
- `BRANDING_CMS_IMAGES`
- `BRANDING_HIDE_DASHBOARD_SIDEBAR`
- `BRANDING_HIDE_LOOKING_FOR_CHALLENGE_WIDGET`
- `BRANDING_FIT_COURSE_IMAGE`
- `BRANDING_INDEX_ADDITIONAL_HTML`
- `BRANDING_FRONTEND_COMPONENT_HEADER_REPO`
- `BRANDING_FRONTEND_COMPONENT_FOOTER_REPO`
- `BRANDING_MFE_PLATFORM_REPO`
- `BRANDING_CERTIFICATE_HTML`
- `BRANDING_STATIC_TEMPLATE_404`
- `BRANDING_STATIC_TEMPLATE_429`
- `BRANDING_STATIC_TEMPLATE_ABOUT`
- `BRANDING_STATIC_TEMPLATE_BLOG`
- `BRANDING_STATIC_TEMPLATE_CONTACT`
- `BRANDING_STATIC_TEMPLATE_DONATE`
- `BRANDING_STATIC_TEMPLATE_EMBARGO`
- `BRANDING_STATIC_TEMPLATE_FAQ`
- `BRANDING_STATIC_TEMPLATE_HELP`
- `BRANDING_STATIC_TEMPLATE_HONOR`
- `BRANDING_STATIC_TEMPLATE_JOBS`
- `BRANDING_STATIC_TEMPLATE_MEDIA_KIT`
- `BRANDING_STATIC_TEMPLATE_NEWS`
- `BRANDING_STATIC_TEMPLATE_PRESS`
- `BRANDING_STATIC_TEMPLATE_PRIVACY`
- `BRANDING_STATIC_TEMPLATE_SERVER_DOWN`
- `BRANDING_STATIC_TEMPLATE_SERVER_ERROR`
- `BRANDING_STATIC_TEMPLATE_SERVER_OVERLOADED`
- `BRANDING_STATIC_TEMPLATE_SITEMAP`
- `BRANDING_STATIC_TEMPLATE_TOS`

## Custom MFEs

You can still override or add MFEs with `BRANDING_MFE`.

Example:

```yaml
BRANDING_MFE:
  authn:
    port: 2001
    repository: https://github.com/myorg/myfork.git
    version: mybranch
```

Repositories must end in `.git`, and custom MFEs must remain compatible with Tutor MFE build expectations.

## Usage

```bash
tutor plugins enable branding
tutor images build openedx
tutor images build mfe
tutor local do init --limit branding
```

Notes: 
- `tutor local do init --limit branding` is needed only if you are using `BRANDING_THEME_REPOS`.
This command associates the comprehensive theme directory to the site for legacy HTML pages.
- `tutor images build openedx` is needed only if you are using `BRANDING_THEME_REPOS`.
- `tutor images build mfe` is needed only if you want the theme variant (light/dark/auto/...) switch.

For Kubernetes deployments, also push rebuilt images and restart the affected services.

## License

This software is licensed under the terms of the AGPLv3.
