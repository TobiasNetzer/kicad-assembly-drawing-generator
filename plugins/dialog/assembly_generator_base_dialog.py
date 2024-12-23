# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainDialog
###########################################################################

class MainDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Assembly drawing generator"), pos = wx.DefaultPosition, size = wx.Size( 550,750 ), style = wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER|wx.SYSTEM_MENU )

        self.SetSizeHints( self.FromDIP(wx.Size( 550,750 )), wx.DefaultSize )

        bSizer1 = wx.BoxSizer( wx.VERTICAL )

        bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

        LayersTOP = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Layers top view") ), wx.VERTICAL )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer2 = wx.BoxSizer( wx.VERTICAL )

        checkListTopChoices = []
        self.checkListTop = wx.CheckListBox( LayersTOP.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, checkListTopChoices, wx.LB_NEEDED_SB )
        self.checkListTop.SetMinSize( wx.Size( 150,200 ) )

        bSizer2.Add( self.checkListTop, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer6.Add( bSizer2, 1, wx.EXPAND, 5 )

        bSizer4 = wx.BoxSizer( wx.VERTICAL )

        self.upTopViewBtn = wx.Button( LayersTOP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.upTopViewBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_BUTTON ) )
        bSizer4.Add( self.upTopViewBtn, 0, wx.ALL, 5 )

        self.downTopViewBtn = wx.Button( LayersTOP.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.downTopViewBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_BUTTON ) )
        bSizer4.Add( self.downTopViewBtn, 0, wx.ALL, 5 )


        bSizer6.Add( bSizer4, 0, wx.ALIGN_RIGHT, 5 )


        LayersTOP.Add( bSizer6, 1, wx.EXPAND, 5 )


        bSizer10.Add( LayersTOP, 1, wx.ALL|wx.EXPAND, 5 )

        LayersBOT = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Layers bottom view") ), wx.VERTICAL )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        checkListBottomChoices = []
        self.checkListBottom = wx.CheckListBox( LayersBOT.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, checkListBottomChoices, wx.LB_NEEDED_SB )
        self.checkListBottom.SetMinSize( wx.Size( 150,200 ) )

        bSizer8.Add( self.checkListBottom, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer7.Add( bSizer8, 1, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.VERTICAL )

        self.upBottomViewBtn = wx.Button( LayersBOT.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.upBottomViewBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_BUTTON ) )
        bSizer9.Add( self.upBottomViewBtn, 0, wx.ALL, 5 )

        self.downBottomViewBtn = wx.Button( LayersBOT.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.BU_EXACTFIT )

        self.downBottomViewBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_DOWN, wx.ART_BUTTON ) )
        bSizer9.Add( self.downBottomViewBtn, 0, wx.ALL, 5 )


        bSizer7.Add( bSizer9, 0, wx.EXPAND, 5 )


        LayersBOT.Add( bSizer7, 1, wx.EXPAND, 5 )


        bSizer10.Add( LayersBOT, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer1.Add( bSizer10, 1, wx.EXPAND, 5 )

        LayerSettings = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Layer properties") ), wx.VERTICAL )

        bSizer17 = wx.BoxSizer( wx.HORIZONTAL )

        bSizer18 = wx.BoxSizer( wx.VERTICAL )

        bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText4 = wx.StaticText( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Drill marks:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )

        bSizer21.Add( self.m_staticText4, 0, wx.ALIGN_CENTER, 5 )

        drillMarksChoiceChoices = [ _(u"None"), _(u"Small"), _(u"Actual size") ]
        self.drillMarksChoice = wx.Choice( LayerSettings.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, drillMarksChoiceChoices, 0 )
        self.drillMarksChoice.SetSelection( 2 )
        bSizer21.Add( self.drillMarksChoice, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Color:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )

        bSizer21.Add( self.m_staticText6, 0, wx.ALIGN_CENTER, 5 )

        self.colourPicker = wx.ColourPickerCtrl( LayerSettings.GetStaticBox(), wx.ID_ANY, wx.Colour( 0, 0, 0 ), wx.DefaultPosition, wx.DefaultSize, wx.CLRP_DEFAULT_STYLE )
        bSizer21.Add( self.colourPicker, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

        self.layerOpacityText = wx.StaticText( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Opacity:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.layerOpacityText.Wrap( -1 )

        bSizer19.Add( self.layerOpacityText, 1, wx.ALIGN_CENTER_VERTICAL, 5 )

        self.LayerOpacitySlider = wx.Slider( LayerSettings.GetStaticBox(), wx.ID_ANY, 50, 0, 100, wx.DefaultPosition, wx.DefaultSize, wx.SL_HORIZONTAL|wx.SL_VALUE_LABEL )
        bSizer19.Add( self.LayerOpacitySlider, 0, 0, 5 )


        bSizer21.Add( bSizer19, 0, 0, 5 )


        bSizer18.Add( bSizer21, 0, 0, 5 )

        bSizer22 = wx.BoxSizer( wx.HORIZONTAL )

        self.mirrorLayerCheckBox = wx.CheckBox( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Mirror layer"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.mirrorLayerCheckBox, 1, wx.ALL, 5 )

        self.negativeLayerCheckBox = wx.CheckBox( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Negative layer"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.negativeLayerCheckBox, 0, wx.ALL, 5 )

        self.plotRefDesignatorsCheckBox = wx.CheckBox( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Plot reference designators"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.plotRefDesignatorsCheckBox, 0, wx.ALL, 5 )

        self.plotFootprintValuesCheckBox = wx.CheckBox( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Plot footprint values"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer22.Add( self.plotFootprintValuesCheckBox, 0, wx.ALL, 5 )


        bSizer18.Add( bSizer22, 0, 0, 5 )

        self.m_staticline2 = wx.StaticLine( LayerSettings.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer18.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer221 = wx.BoxSizer( wx.HORIZONTAL )

        self.indicateDNP = wx.CheckBox( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Indicate DNP on Fab layer:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer221.Add( self.indicateDNP, 0, wx.ALL, 5 )

        self.DNPHide = wx.RadioButton( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Hide"), wx.DefaultPosition, wx.DefaultSize, wx.RB_GROUP )
        bSizer221.Add( self.DNPHide, 0, wx.ALL, 5 )

        self.DNPCrossOut = wx.RadioButton( LayerSettings.GetStaticBox(), wx.ID_ANY, _(u"Cross-out"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.DNPCrossOut.SetValue( True )
        bSizer221.Add( self.DNPCrossOut, 0, wx.ALL, 5 )


        bSizer18.Add( bSizer221, 1, wx.EXPAND, 5 )


        bSizer17.Add( bSizer18, 0, wx.ALL, 5 )

        bSizer11 = wx.BoxSizer( wx.VERTICAL )


        bSizer17.Add( bSizer11, 0, wx.LEFT, 30 )


        LayerSettings.Add( bSizer17, 0, 0, 5 )


        bSizer1.Add( LayerSettings, 0, wx.ALL|wx.EXPAND, 5 )

        Output = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, _(u"Output") ), wx.VERTICAL )

        bSizer111 = wx.BoxSizer( wx.VERTICAL )

        fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
        fgSizer2.AddGrowableCol( 1 )
        fgSizer2.AddGrowableRow( 0 )
        fgSizer2.SetFlexibleDirection( wx.BOTH )
        fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.outputText = wx.StaticText( Output.GetStaticBox(), wx.ID_ANY, _(u"Output directory:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.outputText.Wrap( -1 )

        fgSizer2.Add( self.outputText, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.dirPicker = wx.DirPickerCtrl( Output.GetStaticBox(), wx.ID_ANY, wx.EmptyString, _(u"Select output directory"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE )
        fgSizer2.Add( self.dirPicker, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer111.Add( fgSizer2, 0, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

        self.scaleFactorText = wx.StaticText( Output.GetStaticBox(), wx.ID_ANY, _(u"Scale factor:"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.scaleFactorText.Wrap( -1 )

        bSizer13.Add( self.scaleFactorText, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.layerScaleTextBox = wx.TextCtrl( Output.GetStaticBox(), wx.ID_ANY, _(u"1"), wx.DefaultPosition, self.FromDIP(wx.Size( 50,-1 )), 0 )
        self.layerScaleTextBox.SetMaxLength( 3 )
        self.layerScaleTextBox.Enable( False )

        bSizer13.Add( self.layerScaleTextBox, 0, wx.ALL, 5 )

        self.autoScaleCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Auto scale"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.autoScaleCheckBox.SetValue(True)
        bSizer13.Add( self.autoScaleCheckBox, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        bSizer111.Add( bSizer13, 0, 0, 5 )

        self.boundingBoxCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Only use board edges for determining board size"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer111.Add( self.boundingBoxCheckBox, 0, wx.ALL, 5 )

        self.m_staticline1 = wx.StaticLine( Output.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer111.Add( self.m_staticline1, 0, wx.ALL|wx.EXPAND, 5 )

        self.generateTopCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Generate top view"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer111.Add( self.generateTopCheckBox, 0, wx.ALL, 5 )

        self.generateBotCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Generate bottom view"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer111.Add( self.generateBotCheckBox, 0, wx.ALL, 5 )

        self.generateCombinedCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Generate combined view"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer111.Add( self.generateCombinedCheckBox, 0, wx.ALL, 5 )

        self.mergeFilesCheckBox = wx.CheckBox( Output.GetStaticBox(), wx.ID_ANY, _(u"Merge files into one document"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer111.Add( self.mergeFilesCheckBox, 0, wx.ALL, 5 )

        bSizer121 = wx.BoxSizer( wx.HORIZONTAL )

        self.saveConfigBtn = wx.Button( Output.GetStaticBox(), wx.ID_ANY, _(u"Save config"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.saveConfigBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HARDDISK, wx.ART_BUTTON ) )
        bSizer121.Add( self.saveConfigBtn, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )


        bSizer111.Add( bSizer121, 1, wx.ALIGN_RIGHT, 5 )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.exitBtn = wx.Button( Output.GetStaticBox(), wx.ID_ANY, _(u"Exit"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.exitBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_QUIT, wx.ART_MESSAGE_BOX ) )
        bSizer12.Add( self.exitBtn, 1, wx.ALL, 5 )

        self.generateBtn = wx.Button( Output.GetStaticBox(), wx.ID_ANY, _(u"Generate"), wx.DefaultPosition, wx.DefaultSize, 0 )

        self.generateBtn.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_SAVE, wx.ART_MESSAGE_BOX ) )
        bSizer12.Add( self.generateBtn, 1, wx.ALL, 5 )


        bSizer111.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer191 = wx.BoxSizer( wx.HORIZONTAL )

        self.statusText = wx.StaticText( Output.GetStaticBox(), wx.ID_ANY, _(u"Ready"), wx.DefaultPosition, wx.DefaultSize, wx.ST_NO_AUTORESIZE )
        self.statusText.Wrap( -1 )

        bSizer191.Add( self.statusText, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer111.Add( bSizer191, 0, wx.EXPAND, 5 )


        Output.Add( bSizer111, 0, wx.EXPAND, 5 )


        bSizer1.Add( Output, 0, wx.ALL|wx.EXPAND, 5 )


        self.SetSizer( bSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.checkListTop.Bind( wx.EVT_LISTBOX, self.onSelectTop )
        self.checkListTop.Bind( wx.EVT_CHECKLISTBOX, self.onSelectionChangedTop )
        self.upTopViewBtn.Bind( wx.EVT_BUTTON, self.onClickUpTopViewBtn )
        self.downTopViewBtn.Bind( wx.EVT_BUTTON, self.onClickDownTopViewBtn )
        self.checkListBottom.Bind( wx.EVT_LISTBOX, self.onSelectBottom )
        self.checkListBottom.Bind( wx.EVT_CHECKLISTBOX, self.onSelectionChangedBottom )
        self.upBottomViewBtn.Bind( wx.EVT_BUTTON, self.onClickUpBottomViewBtn )
        self.downBottomViewBtn.Bind( wx.EVT_BUTTON, self.onClickDownBottomViewBtn )
        self.drillMarksChoice.Bind( wx.EVT_CHOICE, self.onDrillMarkChanged )
        self.colourPicker.Bind( wx.EVT_COLOURPICKER_CHANGED, self.onColourPickerColourChanged )
        self.LayerOpacitySlider.Bind( wx.EVT_SLIDER, self.onOpacitySliderChange )
        self.mirrorLayerCheckBox.Bind( wx.EVT_CHECKBOX, self.onMirrorLayerCheckBox )
        self.negativeLayerCheckBox.Bind( wx.EVT_CHECKBOX, self.onNegativeLayerCheckBox )
        self.plotRefDesignatorsCheckBox.Bind( wx.EVT_CHECKBOX, self.onPlotRefDesignatorsCheckBox )
        self.plotFootprintValuesCheckBox.Bind( wx.EVT_CHECKBOX, self.onPlotFootprintValuesCheckBox )
        self.indicateDNP.Bind( wx.EVT_CHECKBOX, self.onIndicateDNPCheckBox )
        self.autoScaleCheckBox.Bind( wx.EVT_CHECKBOX, self.onAutoScale )
        self.boundingBoxCheckBox.Bind( wx.EVT_CHECKBOX, self.onBoundingBoxCheckBox )
        self.saveConfigBtn.Bind( wx.EVT_BUTTON, self.onClickSaveConfig )
        self.exitBtn.Bind( wx.EVT_BUTTON, self.onClickExit )
        self.generateBtn.Bind( wx.EVT_BUTTON, self.onClickGenerate )

    def __del__( self ):
        pass


    # Virtual event handlers, override them in your derived class
    def onSelectTop( self, event ):
        event.Skip()

    def onSelectionChangedTop( self, event ):
        event.Skip()

    def onClickUpTopViewBtn( self, event ):
        event.Skip()

    def onClickDownTopViewBtn( self, event ):
        event.Skip()

    def onSelectBottom( self, event ):
        event.Skip()

    def onSelectionChangedBottom( self, event ):
        event.Skip()

    def onClickUpBottomViewBtn( self, event ):
        event.Skip()

    def onClickDownBottomViewBtn( self, event ):
        event.Skip()

    def onDrillMarkChanged( self, event ):
        event.Skip()

    def onColourPickerColourChanged( self, event ):
        event.Skip()

    def onOpacitySliderChange( self, event ):
        event.Skip()

    def onMirrorLayerCheckBox( self, event ):
        event.Skip()

    def onNegativeLayerCheckBox( self, event ):
        event.Skip()

    def onPlotRefDesignatorsCheckBox( self, event ):
        event.Skip()

    def onPlotFootprintValuesCheckBox( self, event ):
        event.Skip()

    def onIndicateDNPCheckBox( self, event ):
        event.Skip()

    def onAutoScale( self, event ):
        event.Skip()

    def onBoundingBoxCheckBox( self, event ):
        event.Skip()

    def onClickSaveConfig( self, event ):
        event.Skip()

    def onClickExit( self, event ):
        event.Skip()

    def onClickGenerate( self, event ):
        event.Skip()


