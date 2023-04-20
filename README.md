# Anki Preview Reloader

An add-on for [Anki](https://apps.ankiweb.net/) to automatically reload the preview in the [templates screen](https://docs.ankiweb.net/templates/intro.html#the-templates-screen) or the card preview window when model data is modified externally.

By default these previews are only updated when making changes to card templates from within the Anki window.
However, when a model template is updated externally, for example through [Anki-Connect](https://ankiweb.net/shared/info/2055492159), these previews are not affected if they're open.

This add-on detects when a card template is updated, and when either the templates screen or card preview window is open, will reload the preview in these windows.

- [Download](https://ankiweb.net/shared/info/0000000000) add-on from Anki Web
- [Source Code](https://github.com/Pedro-Bronsveld/anki-preview-reloader) on GitHub

This add-on was developed alongside the [Anki Editor](https://marketplace.visualstudio.com/items?itemName=pedro-bronsveld.anki-editor) extension for [Visual Studio Code](https://code.visualstudio.com/), 
but should work with any other application that updates model templates through Anki-Connect.

## Demo

Templates screen preview reloading when a card template is updated through Anki-Connect.

![Anki Editor extension and Anki Preview Reloader add-on demo](media/anki-editor-example.gif)

Card preview reloading when a card template is updated through Anki-Connect.
Allows for testing a card template with a specific note.

![Card Previewer Reloading](media/card-preview-example.gif)
