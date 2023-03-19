from typing import Callable
from aqt import gui_hooks
from aqt.clayout import CardLayout
from aqt.models import NotetypeDict
from aqt import mw
from anki.hooks import wrap
from anki.collection import OpChanges

from .preview_reloader import PreviewReloader

def on_main_window_init():

    preview_reloader = PreviewReloader()

    # Model updates monkey patching
    def on_model_updated(notetype: NotetypeDict, _old: Callable[[NotetypeDict], OpChanges]) -> OpChanges:
        result = _old(notetype)
        preview_reloader.on_model_updated(notetype)
        return result

    mw.col.models.update_dict = wrap(mw.col.models.update_dict, on_model_updated, "around")

    # Card layout dialog gui hooks and monkey patching
    def on_card_layout_cleanup() -> None:
        preview_reloader.cleanup()
    
    def on_card_layout_will_show(card_layout_dialog: CardLayout) -> None:
        preview_reloader.set_card_layout_dialog(card_layout_dialog)
        card_layout_dialog.cleanup = wrap(card_layout_dialog.cleanup, on_card_layout_cleanup, "after")
    
    gui_hooks.card_layout_will_show.append(on_card_layout_will_show)


if __name__ != "__main__":
    # Initialize addon when main window loads
    gui_hooks.main_window_did_init.append(on_main_window_init)
