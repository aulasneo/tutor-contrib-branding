# Change log

## Version 18.8.1 (2025-03-26)
fix: restored mfe-dockerfile-pre-npm-install-learner-dashboard for specific learner-dashboard customizations

## Version 18.8.0 (2025-03-13)
- fix: Refactored patch for custom frontend-platform for Redwood
- fix: Removed footer from account, which now uses slots.

## Version 18.7.0 (2025-01-26)
- feat: Add BRANDING_MFE_PLATFORM_REPO to set a custom frontend-platform
- doc: Update README

## Version 18.6.2 (2024-10-25)
- fix: Fix MFE overrides, empty root issue

## Version 18.6.1 (2024-10-23)
- fix: Fixed a bug that happened when the plugin was ran from a different directory than the config.yml.

## Version 18.6.0 (2024-09-07)
- ref: Refactor download images
- feat: Add BRANDING_HIDE_LOOKING_FOR_CHALLENGE_WIDGET setting

## Version 18.5.0 (2024-08-26)
- feat: Allow hiding the Programs tab and the sideber in the learner dashboard
- feat: Make the course image fit in the course card at the learner dashboard.

## Version 18.4.0 (2024-08-22)
- feat: refactor BRANDING_THEME_REPOS to allow repo versioning

## Version 18.3.0 (2024-08-21)
- feat: Hide the upgrade button by default

## Version 18.2.0 (2024-08-21)
- fix: Use pre-npm install for custom branding, header and footers
- fix: use gettext instead of ugettext in static html templates
- feat: Add BRANDING_THEME_REPOS setting to allow downloading themes from git.
- feat: Allow overriding MFE logos

## Version 18.1.0 (2024-07-29)
- Fix Refactor MFE overriding of branding, header and footer

## Version 18.0.0 (2024-07-26)
- Upgrade to Redwood

## Version 17.0.0 (2024-07-25)
- Upgrade to Quince

## Version 16.1.2 (2024-07-22)
- fix: Make BRANDING_CERTIFICATE_HTML override all _accomplishment-rendering.html

## Version 16.1.1 (2024-06-27)

- fix: Fix bug

## Version 16.1.0 (2024-06-27)
- feat: add BRANDING_MFE setting to customize mfe repo, port and version

## Version 16.0.1 (2024-02-19)
- fix: Use urllib3==1.26.6 to avoid issues with Open SSL version

## Version 16.0.0 (2023-11-17)
- Upgrade to Palm

## Version 15.1.1 (2023-10-17)
- Fix bug in dockerfile to import footer

## Version 15.1.0 (2023-10-04)
- Support Olive release

## Version 14.1.0 (2023-08-29)
- Add support for custom frontend component header and footer

## Version 14.0.0 (2023-08-29)
- Align versioning convention with Tutor. Upload to PyPI 

## Version 0.5.3 (2023-06-23)
- Fix: create fonts directory if not exists

## Version 0.5.2 (2023-05-22)
- Fix "Register" button text

## Version 0.5.1 (2023-04-24)
- Fix error downloading images

## Version 0.5.0 (2023-02-24)
- Add customizable static pages (about, contact us, 404, etc.)

## Version 0.4.0 (2022-12-30)
- Add BRANDING_CERTIFICATE_HTML setting to customize certificates
- Add BRANDING_INDEX_ADDITIONAL_HTML setting to add a custom HTML code to the home page

## Version 0.3.0 (2022-12-28)
- Allow non-authenticated header to hide links by setting '#' to the urls.
## Version 0.2.0
- Download fonts and images from URL
## Version 0.1.0
- First release