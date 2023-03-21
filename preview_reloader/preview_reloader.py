from typing import Optional
from aqt import QObject, pyqtSignal
from aqt.clayout import CardLayout
from anki.models import NotetypeDict
from aqt.utils import tr
from anki.lang import without_unicode_isolation

class PreviewReloader(QObject):

    redraw_signal = pyqtSignal()
    card_layout_dialog: Optional[CardLayout] = None

    def __init__(self) -> None:
        super().__init__()
        self.redraw_signal.connect(self.emit_redraw_signal)
    
    def emit_redraw_signal(self) -> None:
        if self.card_layout_dialog != None and self.card_layout_dialog.mw != None:
            # self.card_layout_dialog.redraw_everything()
            self.card_layout_dialog.renderPreview()
            self.card_layout_dialog.fill_fields_from_template()
    
    def set_card_layout_dialog(self, card_layout_dialog: CardLayout) -> None:
        self.card_layout_dialog = card_layout_dialog
    
    def on_model_updated(self, new_model: NotetypeDict) -> None:
        if self.card_layout_dialog == None or self.card_layout_dialog.mw == None or new_model == None:
            return
        
        if new_model["id"] != self.card_layout_dialog.model["id"]:
            return
        
        # Update note type model in card layout dialog
        self.card_layout_dialog.model = new_model
        self.card_layout_dialog.templates = new_model["tmpls"]
        self.card_layout_dialog.setWindowTitle(
            without_unicode_isolation(
                tr.card_templates_card_types_for(val=new_model["name"])
            )
        )

        # Send redraw signal to card layout dialog
        self.redraw_signal.emit()
    
    def cleanup(self) -> None:
        self.card_layout_dialog = None
