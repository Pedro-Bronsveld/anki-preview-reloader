from typing import Optional
from aqt.browser.previewer import Previewer
from aqt import gui_hooks
from anki.collection import OpChanges
from anki.hooks import wrap

class PreviewerReloader:

    previewer: Optional[Previewer] = None

    def set_previewer(self, previewer: Previewer) -> None:
        self.previewer = previewer
        previewer._close_callback = wrap(previewer._close_callback, self.cleanup, "before")

    def on_model_updated(self) -> None:
        if self.previewer == None:
            return
        
        # Set `_last_state` of previewer to None to force the previewer to reload
        # when firing the `operation_did_execute` hook.
        self.previewer._last_state = None
        gui_hooks.operation_did_execute(OpChanges(card=True), None)
    
    def cleanup(self) -> None:
        self.previewer = None
