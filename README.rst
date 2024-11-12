Branding plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin, inspired in `Indigo <https://github.com/overhangio/tutor-indigo>`__,
allow changing the look and feel of Open edX installations.
It can control the appearance of both legacy pages based on HTML
(like the course catalog, dashboard, login, register, etc.), as well as
MFE components.

.. image:: https://img.shields.io/badge/linting-pylint-yellowgreen
    :target: https://github.com/pylint-dev/pylint

Installation
------------

::

    pip install tutor-contrib-branding

Configuration
-------------

Customize colors
~~~~~~~~~~~~~~~~

Most Bootstrap variables can be set using settings. 
These are the available variables and their defaults:

* BRANDING_PRIMARY: #0000FF
* BRANDING_SECONDARY: #454545
* BRANDING_FONT_FAMILY: <no default>
* BRANDING_BRAND: #9D0054
* BRANDING_SUCCESS: #178253
* BRANDING_INFO: #006DAA
* BRANDING_DANGER: #C32D3A
* BRANDING_WARNING: #FFD900
* BRANDING_LIGHT: #E1DDDB
* BRANDING_DARK: #273F2F
* BRANDING_ACCENT_A: #00BBF9
* BRANDING_ACCENT_B: #FFEE88
* BRANDING_BACKGROUND: #ffffff
* BRANDING_BG_PRIMARY: #ffffff
* BRANDING_BODY: #FFFFFF
* BRANDING_HOMEPAGE_BG_IMAGE: ""

You can add these settings to the ``config.yml`` file or using the
``tutor config --set "<setting>=<value>"`` command.

These settings affect the Bootstrap's ``_variables.scss`` file in the
`comprehensive theme <https://github.com/openedx/edx-platform/blob/master/lms/static/sass/partials/lms/theme/_variables.scss>`__
and in the `MFE branding module <https://github.com/openedx/brand-openedx/blob/625ad32f9cf8247522541ee77dfd574b30245226/paragon/_variables.scss>`__.

You can also add CSS overrides using the ``BRANDING_EXTRAS`` and the ``BRANDING_OVERRIDES`` variables,
to impact the `comprehensive theme <https://github.com/openedx/edx-platform/blob/master/lms/static/sass/partials/lms/theme/_extras.scss>`__
and the `MFE branding module <https://github.com/openedx/brand-openedx/blob/625ad32f9cf8247522541ee77dfd574b30245226/paragon/_overrides.scss>`__
respectively.

E.g., this setting will add a CSS block to change the color of h1 texts in all MFE:

::

    BRANDING_OVERRIDES: >-
      h1 {
            color: red;
      }

Managing fonts
~~~~~~~~~~~~~~

Set ``BRANDING_FONTS_URLS`` to a list of URLS pointing to a zipped set of font files.

E.g., to add Roboto Flex font, set:

::

    BRANDING_FONTS_URLS:
    - https://fonts.google.com/download?family=Roboto%20Flex

Then add a specific font definition, use the ``BRANDING_FONTS`` setting, e.g.:

::

    BRANDING_FONTS: >-
        @font-face {
            font-family: 'Roboto Flex';
            src: url('RobotoFlex-VF.woff2') format('woff2 supports variations'),
               url('RobotoFlex-VF.woff2') format('woff2-variations');
        }

Learn more about using flex fonts `here <https://web.dev/variable-fonts/>`__.

Finally, set the font family using the ``BRANDING_FONT_FAMILY`` variable:

::

    BRANDING_FONT_FAMILY: Roboto Flex


Downloading images
~~~~~~~~~~~~~~~~~~

CMS and LMS images can be included as long as they can be accessed through a HTTP(S) request.
Most important images are:

LMS:

- favicon.ico
- logo.png
- banner.png

CMS:

- studio-logo.png

A banner can also be added to the homepage.

E.g., to add custom logos and banner set the following:

::

    BRANDING_LMS_IMAGES:
    - filename: banner.png
      url: https://url/to/banner.png
    - filename: favicon.ico
      url: https://url/to/favicon.ico
    - filename: logo.png
      url: https://url/to/logo.png
    BRANDING_CMS_IMAGES:
    - filename: studio-logo.png
      url: https://url/to/studio-logo.png
    BRANDING_HOMEPAGE_BG_IMAGE: banner.png


Customize MFE logos
~~~~~~~~~~~~~~~~~~~~

By default, the MFEs will take the logos from the theme assets' main logo.
However you can now customize the MFE logos by using these variables:

- BRANDING_MFE_LOGO_URL: Main logo used in the headers
- BRANDING_MFE_LOGO_TRADEMARK_URL: This is a URL to a logo for use in the footer.
  This is a different environment variable than LOGO_URL (used in frontend-component-header)
  to accommodate sites that would like to have additional trademark information on a logo
  in the footer, such as a (tm) or (r) symbol.
- BRANDING_MFE_LOGO_WHITE_URL: White logo over transparent background intended for
  the login page and other sites where it printed over images or dark background.

The value of these settings must be a public accessible URL containing the image.


Custom HTML block in home page
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can add a custom HTML code to be rendered in the home page after the banner
and before the list of courses by setting ``BRANDING_INDEX_ADDITIONAL_HTML``.

Customize HTML certificate
~~~~~~~~~~~~~~~~~~~~~~~~~~

By setting ``BRANDING_CERTIFICATE_HTML`` you can override the standard certificate with
your own HTML code.

Tip: Create a file with the HTML code (e.g., ``branding_certificate_html.html``)
and then update the configuration from the file.

::

    tutor config save --set BRANDING_CERTIFICATE_HTML="$(cat branding_certificate_html.html)"


Customizing static pages
~~~~~~~~~~~~~~~~~~~~~~~~

You can set your own HTML content to the typical static pages by setting the corresponding
variable:

- BRANDING_STATIC_TEMPLATE_404
- BRANDING_STATIC_TEMPLATE_429
- BRANDING_STATIC_TEMPLATE_ABOUT
- BRANDING_STATIC_TEMPLATE_BLOG
- BRANDING_STATIC_TEMPLATE_CONTACT
- BRANDING_STATIC_TEMPLATE_DONATE
- BRANDING_STATIC_TEMPLATE_EMBARGO
- BRANDING_STATIC_TEMPLATE_FAQ
- BRANDING_STATIC_TEMPLATE_HELP
- BRANDING_STATIC_TEMPLATE_HONOR
- BRANDING_STATIC_TEMPLATE_JOBS
- BRANDING_STATIC_TEMPLATE_MEDIA_KIT
- BRANDING_STATIC_TEMPLATE_NEWS
- BRANDING_STATIC_TEMPLATE_PRESS
- BRANDING_STATIC_TEMPLATE_PRIVACY
- BRANDING_STATIC_TEMPLATE_SERVER_DOWN
- BRANDING_STATIC_TEMPLATE_SERVER_ERROR
- BRANDING_STATIC_TEMPLATE_SERVER_OVERLOADED
- BRANDING_STATIC_TEMPLATE_SITEMAP
- BRANDING_STATIC_TEMPLATE_TOS

Use custom MFEs
~~~~~~~~~~~~~~~

You can create alternate versions of existing MFEs or new ones.
Starting from Palm, Tutor will not accept MFE repo overrides in the configuration file.
This plugin brings back that functionality, allowing you to specify the repo, port and
version of the MFEs to override in the configuration file without the need to create
a plugin just for this.

To override the MFE repo information, set the `BRANDING_MFE` variable as in this example:

::

    BRANDING_MFE:
      authn:
        port: 2001
        repository: https://github.com/myorg/myfork
        version: mybranch


Customizing MFE header and footer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use a custom header or footer, clone `frontend-component-header <https://github.com/openedx/frontend-component-header>`_
and/or `frontend-component-footer <https://github.com/openedx/frontend-component-footer>`_,
push to your custom repository and set the repository URL in the variables:

- BRANDING_FRONTEND_COMPONENT_HEADER_REPO
- BRANDING_FRONTEND_COMPONENT_FOOTER_REPO


Using a custom frontend-platform
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some advanced users might want to customize frontend-platform. This repo is imported by
most MFEs and brings some features common to all.
A typical use case is to add a script in the <head> of all pages.

To use a custom repo for frontend-platform, set :code:`BRANDING_MFE_PLATFORM_REPO`. Use the same
format as would be used by :code:`npm install`. Add a :code:`#` and a branch name or version number.

E.g.,

::

    BRANDING_MFE_PLATFORM_REPO: https://github.com/openedx/frontend-platform#v7.1.4

Note that the version of frontend_platform must contain a "prepare" script with the same value as the
"build" script in package.json. Also set the version to the actual version number of the upstream repo,
instead of the default "1.0.0-semantically-released". Finally, update package-lock.json with :code:`npm install`
to match the latest changes before pushing.


Downloading custom themes from a git repo
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is now possible to store one or more whole comprehensive themes in git repositories and download to the 
Open edX instance. To do this, add the following configuration to config.yml:

::

    BRANDING_THEME_REPOS:
      - name: <theme name>
        url: <theme git URL, ending in .git>
        version: <git branch or tag>
      ...

You can add as many themes as you want, however only one can be active at a time.
After adding this, save the configuration and rebuild the openedx image.
Then run `tutor <variant> do init [--limit branding]` to enable the first theme.

Notes: 

- theme repos are not templates; it means that other BRANDING\_ settings, logos and fonts  will have no effect.
  Include your own fonts, images, CSS and variables in the repo.
- Do not use `theme` as a theme name. This is reserved for the base theme created from the branding template.
- To change templates, go to `<LMS URL>/admin/theming/sitetheme/` and set the theme name to all sites.
  Use `theme` as theme name to use the base theme.
- MFE logos are taken by default from the theme logo. Restart the MFE service if you changed your logo in the theme
  to make it available to the MFEs.


Customizing the Learner Dashboard
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Since Quince release, the new learner-dashboard MFE includes a number of features that might not
be part of your use cases, and cannot be disabled with settings.

- Hide the upgrade button
    The Branding plugin now disables this button by default. But if you want it back,
    just set `BRANDING_HIDE_UPGRADE_BUTTON` to `False`.

- Hide the Programs tab
    The Programs tab can be hidden by setting `BRANDING_HIDE_PROGRAMS` to True.

- Hide the sidebar
    The sidebar with the "Looking for new challenges" text can be hidden by setting
    `BRANDING_HIDE_DASHBOARD_SIDEBAR` to True.

- Hide the `Looking for a new challenge?` sidebar widget
    You can leave the sidebar visible and hide only the widget by setting
    `BRANDING_HIDE_LOOKING_FOR_CHALLENGE_WIDGET` to True.

- Make the course image fit into the course card
    By default, the images is clipped.

Usage
-----

::

    tutor plugins enable branding
    tutor images build openedx
    tutor images build mfe
    tutor local settheme theme

In K8s deployments, you will need to push the docker images and restart Tutor.

License
-------

This software is licensed under the terms of the AGPLv3.
