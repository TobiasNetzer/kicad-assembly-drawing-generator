import os
import pcbnew
import wx

from .dialog import Dialog
from . import plot

class assembly_generator(pcbnew.ActionPlugin):
    def __init__(self):
        self.name = "Generate Assembly Drawings"
        self.category = "PCB Documentation"
        self.pcbnew_icon_support = hasattr(self, "show_toolbar_button")
        self.show_toolbar_button = True
        icon_dir = os.path.dirname(__file__)
        self.icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.dark_icon_file_name = os.path.join(icon_dir, 'icon.png')
        self.description = "Generate Assembly Drawings"

    def Run(self) -> None:
        pcb_frame = next(
            x for x in wx.GetTopLevelWindows() if x.GetName() == "PcbFrame"
        )

        dlg = Dialog(pcb_frame, plot.generateAssembly)
        if dlg.ShowModal() == wx.ID_CANCEL:
            dlg.Destroy()
