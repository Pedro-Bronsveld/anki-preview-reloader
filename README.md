# Anki Preview Reloader

An add-on for [Anki](https://apps.ankiweb.net/) to reload the card preview in the [templates screen](https://docs.ankiweb.net/templates/intro.html#the-templates-screen) and the card preview window.

By default these previews are only updated when making changes to card templates from within the Anki window.
However, when a model template is updated externally, for example through [Anki-Connect](https://ankiweb.net/shared/info/2055492159), these previews are not affected if they're open.

This add-on detects when a card template is updated externally, and when either the templates screen or card preview window is open, will reload the previews in these windows.

This add-on was developed alongside the [Anki Editor](https://github.com/Pedro-Bronsveld/anki-editor) extension for VSCode, but should work with any other program that updates model templates through Anki-Connect.

## Demo

Templates screen preview reloading when a card template is updated through Anki-Connect.

![Anki Editor extension and Anki Preview Reloader add-on demo](media/anki-editor-example.gif)

Card preview reloading when a card template is updated through Anki-Connect.
Allows for testing a card template with a specific note.

![Card Previewer Reloading](media/card-preview-example.gif)