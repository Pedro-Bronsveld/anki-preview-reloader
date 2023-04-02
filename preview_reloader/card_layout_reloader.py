from typing import Optional
from aqt import QObject, pyqtSignal
from aqt.clayout import CardLayout
from anki.models import NotetypeDict
from aqt.utils import tr
from anki.lang import without_unicode_isolation
from anki.hooks import wrap
class CardLayoutReloader(QObject):

    refresh_signal = pyqtSignal()
    card_layout: Optional[CardLayout] = None

    def __init__(self) -> None:
        super().__init__()
        self.refresh_signal.connect(self.emit_refresh_signal)
    
    def emit_refresh_signal(self) -> None:
        if self.card_layout != None and self.card_layout.mw != None:
            self.card_layout.fill_fields_from_template()
            self.card_layout.renderPreview()
    
    def set_card_layout(self, card_layout: CardLayout) -> None:
        self.card_layout = card_layout
        card_layout.cleanup = wrap(card_layout.cleanup, self.cleanup, "after")
    
    def on_model_updated(self, new_model: NotetypeDict) -> None:
        if self.card_layout == None or self.card_layout.mw == None or new_model == None:
            return
        
        if new_model["id"] != self.card_layout.model["id"]:
            return
        
        # Update note type model in card layout dialog
        self.card_layout.model = new_model
        self.card_layout.templates = new_model["tmpls"]
        self.card_layout.setWindowTitle(
            without_unicode_isolation(
                tr.card_templates_card_types_for(val=new_model["name"])
            )
        )

        # Send refresh signal to card layout dialog
        self.refresh_signal.emit()
    
    def cleanup(self) -> None:
        self.card_layout = None
