Branding plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This plugin, inspired in `Indigo <https://github.com/overhangio/tutor-indigo>`__,
allow changing the look and feel of Open edX installations.
It can control the appearance of both legacy pages based on HTML
(like the course catalog, dashboard, login, register, etc.), as well as
MFE components.

Installation
------------

::

    pip install git+https://github.com/aulasneo/tutor-contrib-branding

Configuration
-------------

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

To add a specific font definition, use the ``BRANDING_FONTS`` setting, e.g.:

::

    BRANDING_FONTS: >-
        @font-face {
            font-family: 'font name';
            src: url('#{$static-path}/fonts/font_name-Regular.woff2') format('woff2'),
                url('#{$static-path}/fonts/font_name-Regular.woff') format('woff');
            font-weight: normal;
            font-style: normal;
            font-display: swap;
        }

Then put your font files in the ``env/build/openedx/themes/theme/lms/static/fonts`` directory.

*Note*: Currently this plugin does not support uploading logos, images, fonts or static pages.
To do so, you will have to add them manually to the corresponding location under the ``env`` directory.

To set a home page banner image, upload it to ``env/build/openedx/themes/theme/lms/static/images``
directory and set BRANDING_HOMEPAGE_BG_IMAGE to its file name.

Usage
-----

::

    tutor plugins enable branding
    tutor images build openedx
    tutor images build mfe
    tutor local settheme theme

In K8s deployments, you will need to push the images and restart Tutor.

License
-------

This software is licensed under the terms of the AGPLv3.
