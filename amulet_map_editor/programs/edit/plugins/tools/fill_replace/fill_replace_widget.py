from enum import Enum
from typing import List

import wx

import PyMCTranslate

from amulet_map_editor import lang
from amulet_map_editor.api.wx.ui.simple import SimpleChoiceAny
from amulet_map_editor.api.wx.ui.version_select import (
    VersionSelect,
    VersionChangeEvent,
    EVT_VERSION_CHANGE,
)

from .replace_widget import ReplaceOperationWidget


class ReplaceMode(Enum):
    Single = 0
    Sequence = 1
    Map = 2


LeftRightBorder = wx.LEFT | wx.RIGHT
BottomBorder = LeftRightBorder | wx.BOTTOM


class FillReplaceWidget(wx.Panel):
    def __init__(
        self,
        parent: wx.Window,
        translation_manager: PyMCTranslate.TranslationManager,
        **kwargs
    ):
        super().__init__(parent, **kwargs)
        self._translation_manager = translation_manager

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self._version_select = VersionSelect(self, translation_manager)
        self._version_select.Bind(EVT_VERSION_CHANGE, self._on_version_change)
        sizer.Add(self._version_select, 0, wx.EXPAND)

        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(top_sizer, 0, wx.ALL | wx.EXPAND, 5)

        self._replace = wx.CheckBox(
            self, wx.ID_ANY, lang.get("program_3d_edit.fill_tool.replace")
        )
        self._replace.Bind(wx.EVT_CHECKBOX, self._on_replace_change)
        top_sizer.Add(self._replace, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)

        self._replace_mode = SimpleChoiceAny(self, sort=False)
        self._replace_mode.SetItems(
            {
                ReplaceMode.Single: lang.get(
                    "program_3d_edit.fill_tool.replace_mode.single"
                ),
                ReplaceMode.Sequence: lang.get(
                    "program_3d_edit.fill_tool.replace_mode.sequence"
                ),
                ReplaceMode.Map: lang.get("program_3d_edit.fill_tool.replace_mode.map"),
            }
        )
        # self.choice_1.SetSelection(0)
        top_sizer.Add(self._replace_mode, 1, wx.LEFT, 5)

        self._operation_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._operation_sizer, 0, wx.EXPAND, 0)

        self._operations: List[ReplaceOperationWidget] = []
        self._add_operation()

        self.Layout()

    def _add_operation(self):
        replace_operation = ReplaceOperationWidget(
            self, self._translation_manager, self._version_select.version
        )
        self._operations.append(replace_operation)
        self._operation_sizer.Add(replace_operation, 0, wx.EXPAND | BottomBorder, 5)

    def _on_version_change(self, evt: VersionChangeEvent):
        version = evt.platform, evt.version_number, evt.force_blockstate
        for op in self._operations:
            op.version = version

    def _on_replace_change(self, evt):
        for operation in self._operations:
            operation.replace(self.replace)
        self.GetTopLevelParent().Layout()

    @property
    def replace(self) -> bool:
        """Is the replace check box ticked."""
        return self._replace.GetValue()

    @property
    def replace_mode(self) -> ReplaceMode:
        return self._replace_mode.GetCurrentObject()