from typing import Callable
from aqt import gui_hooks
from aqt.clayout import CardLayout
from aqt.models import NotetypeDict
from aqt import mw
from anki.hooks import wrap
from anki.collection import OpChanges
from aqt.browser.previewer import BrowserPreviewer, Previewer
from preview_reloader.previewer_reloader import PreviewerReloader

from .card_layout_reloader import CardLayoutReloader

def on_main_window_init():

    card_layout_reloader = CardLayoutReloader()
    previewer_reloader = PreviewerReloader()

    # Model updates monkey patching
    def on_model_updated(notetype: NotetypeDict, _old: Callable[[NotetypeDict], OpChanges]) -> OpChanges:
        result = _old(notetype)
        card_layout_reloader.on_model_updated(notetype)
        previewer_reloader.on_model_updated()
        return result

    mw.col.models.update_dict = wrap(mw.col.models.update_dict, on_model_updated, "around")

    # Card layout dialog gui hooks and monkey patching    
    def on_card_layout_will_show(card_layout_dialog: CardLayout) -> None:
        card_layout_reloader.set_card_layout(card_layout_dialog)
    
    gui_hooks.card_layout_will_show.append(on_card_layout_will_show)
    
    # Card previewer hooks
    def on_previewer_did_init(previewer: Previewer):
        if not isinstance(previewer, BrowserPreviewer):
            return
        previewer_reloader.set_previewer(previewer)
    
    gui_hooks.previewer_did_init.append(on_previewer_did_init)

if __name__ != "__main__":
    # Initialize addon when main window loads
    gui_hooks.main_window_did_init.append(on_main_window_init)
