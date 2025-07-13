import wx
import configparser
import pcbnew
import os
import ast

from . import assembly_generator_base_dialog

class Dialog(assembly_generator_base_dialog.MainDialog):
    def __init__(self, parent, generateFunc):
        assembly_generator_base_dialog.MainDialog.__init__(self, parent)
        self.generateFunc = generateFunc
        self.sortOrderLayersTop = []
        self.sortOrderLayersBot = []
        self.checkedLayersTop = []
        self.checkedLayersBot = []
        self.settingsLayersTop = {}
        self.settingsLayersBot = {}

        config = configparser.ConfigParser()
        pluginDir = os.path.dirname(os.path.dirname(__file__))
        configPath = os.path.join(pluginDir, "config.ini")


        board = pcbnew.GetBoard()
        projectDir = os.path.dirname(board.GetFileName())
        self.dirPicker.SetPath(projectDir)
        
        try:
            config.read(configPath)
            self.sortOrderLayersTop = ast.literal_eval(config.get("LayersTop", "sortorder"))
            self.checkedLayersTop = ast.literal_eval(config.get("LayersTop", "checked"))
            self.settingsLayersTop = ast.literal_eval(config.get("LayersTop", "settings"))
            self.sortOrderLayersBot = ast.literal_eval(config.get("LayersBot", "sortorder"))
            self.checkedLayersBot = ast.literal_eval(config.get("LayersBot", "checked"))
            self.settingsLayersBot = ast.literal_eval(config.get("LayersBot", "settings"))

            self.generateTopCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "Generatetopview")))
            self.generateBotCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "Generatebotview")))
            self.generateCombinedCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "Generatecombinedview")))
            self.mergeFilesCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "mergefiles")))
            self.autoScaleCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "autoscaling")))
            self.layerScaleTextBox.SetValue(config.get("OutputSettings", "layerscale"))
            self.boundingBoxCheckBox.SetValue(ast.literal_eval(config.get("OutputSettings", "onlyboardedges")))
            self.indicateDNP.SetValue(ast.literal_eval(config.get("OutputSettings", "indicatednp")))
            self.DNPHide.SetValue(ast.literal_eval(config.get("OutputSettings", "dnphide")))
            self.DNPCrossOut.SetValue(ast.literal_eval(config.get("OutputSettings", "dnpcross")))

            #Check if config file is still up to date. Needed for the changes made in KiCad V9.
            i = pcbnew.PCBNEW_LAYER_ID_START
            while i < pcbnew.PCBNEW_LAYER_ID_START + pcbnew.PCB_LAYER_ID_COUNT:
                layerStdName = pcbnew.BOARD.GetStandardLayerName(i)

                try:
                    if self.settingsLayersTop[layerStdName]["ID"] != i:
                        self.settingsLayersTop[layerStdName]["ID"] = i
                except KeyError:
                    self.settingsLayersTop.update({
                        layerStdName: {
                        "ID": i,
                        "Opacity": 100,
                        "Mirrored": False,
                        "Negative": False,
                        "DrillMarks": 0,
                        "PlotReferenceDesignators": True,
                        "PlotFootprintValues": True,
                        "Color": 0
                        }
                    })
                    self.sortOrderLayersTop.append(layerStdName)

                try:
                    if self.settingsLayersBot[layerStdName]["ID"] != i:
                        self.settingsLayersBot[layerStdName]["ID"] = i
                except KeyError:
                    self.settingsLayersBot.update({
                        layerStdName: {
                        "ID": i,
                        "Opacity": 100,
                        "Mirrored": True,
                        "Negative": False,
                        "DrillMarks": 0,
                        "PlotReferenceDesignators": True,
                        "PlotFootprintValues": True,
                        "Color": 0
                        }
                    })
                    self.sortOrderLayersBot.append(layerStdName)
                i += 1

        except:
            dlg=wx.MessageDialog(None, "Error while reading config.ini file!", "Error", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()

            self.sortOrderLayersTop.clear()
            self.sortOrderLayersBot.clear()
            self.checkedLayersTop.clear()
            self.checkedLayersBot.clear()
            self.settingsLayersTop.clear()
            self.settingsLayersBot.clear()

            i = pcbnew.PCBNEW_LAYER_ID_START
        
            while i < pcbnew.PCBNEW_LAYER_ID_START + pcbnew.PCB_LAYER_ID_COUNT:
                layerStdName = pcbnew.BOARD.GetStandardLayerName(i)
                #layer_name = pcbnew.BOARD.GetLayerName(pcbnew.GetBoard(), i)
                self.settingsLayersTop.update({
                    layerStdName: {
                    "ID": i,
                    "Opacity": 100,
                    "Mirrored": False,
                    "Negative": False,
                    "DrillMarks": 0,
                    "PlotReferenceDesignators": True,
                    "PlotFootprintValues": True,
                    "Color": 0
                    }
                })
                self.settingsLayersBot.update({
                    layerStdName: {
                    "ID": i,
                    "Opacity": 100,
                    "Mirrored": True,
                    "Negative": False,
                    "DrillMarks": 0,
                    "PlotReferenceDesignators": True,
                    "PlotFootprintValues": True,
                    "Color": 0
                    }
                })

                self.sortOrderLayersTop.append(layerStdName)
                self.sortOrderLayersBot.append(layerStdName)
                i += 1
        
            self.sortOrderLayersTop.sort()
            self.sortOrderLayersBot.sort()

        self.checkListTop.SetItems(self.sortOrderLayersTop)
        self.checkListTop.SetCheckedStrings(tuple(self.checkedLayersTop))
        self.checkListBottom.SetItems(self.sortOrderLayersBot)
        self.checkListBottom.SetCheckedStrings(tuple(self.checkedLayersBot))
        
        if self.autoScaleCheckBox.IsChecked():
            self.layerScaleTextBox.Disable()
        else:
            self.layerScaleTextBox.Enable()

        if self.indicateDNP.IsChecked():
            self.DNPHide.Enable()
            self.DNPCrossOut.Enable()
        else:
            self.DNPHide.Disable()
            self.DNPCrossOut.Disable()

    def onSelectTop(self, event):
        self.checkListBottom.Deselect(self.checkListBottom.GetSelection())
        self.mirrorLayerCheckBox.SetValue(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Mirrored"])
        self.negativeLayerCheckBox.SetValue(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Negative"])
        self.LayerOpacitySlider.SetValue(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Opacity"])
        self.drillMarksChoice.SetSelection(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["DrillMarks"])
        self.plotRefDesignatorsCheckBox.SetValue(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["PlotReferenceDesignators"])
        self.plotFootprintValuesCheckBox.SetValue(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["PlotFootprintValues"])
        color = wx.Colour()
        color.SetRGB(self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Color"])
        self.colourPicker.SetColour(color)
        
    
    def onSelectBottom(self, event):
        self.checkListTop.Deselect(self.checkListTop.GetSelection())
        self.mirrorLayerCheckBox.SetValue(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Mirrored"])
        self.negativeLayerCheckBox.SetValue(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Negative"])
        self.LayerOpacitySlider.SetValue(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Opacity"])
        self.drillMarksChoice.SetSelection(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["DrillMarks"])
        self.plotRefDesignatorsCheckBox.SetValue(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["PlotReferenceDesignators"])
        self.plotFootprintValuesCheckBox.SetValue(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["PlotFootprintValues"])
        color = wx.Colour()
        color.SetRGB(self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Color"])
        self.colourPicker.SetColour(color)


    def onSelectionChangedTop(self, event):
        self.checkedLayersTop = list(self.checkListTop.GetCheckedStrings())

    def onSelectionChangedBottom(self, event):
        self.checkedLayersBot = list(self.checkListBottom.GetCheckedStrings())

    def onClickUpTopViewBtn(self, event):
        if self.checkListTop.GetSelection() > 0:
            self.checkListBottom.Deselect(self.checkListBottom.GetSelection())
            currentSelection = self.checkListTop.GetSelection()
            temp = self.sortOrderLayersTop[currentSelection - 1]
            self.sortOrderLayersTop[currentSelection - 1] = self.sortOrderLayersTop[currentSelection]
            self.sortOrderLayersTop[currentSelection] = temp
        
            self.checkListTop.SetItems(self.sortOrderLayersTop)
            self.checkListTop.SetCheckedStrings(tuple(self.checkedLayersTop))
            self.checkListTop.Select(currentSelection - 1)
            
            self.checkedLayersTop = list(self.checkListTop.GetCheckedStrings())
    
    def onClickDownTopViewBtn(self, event):
        if self.checkListTop.GetSelection() < pcbnew.PCB_LAYER_ID_COUNT:
            self.checkListBottom.Deselect(self.checkListBottom.GetSelection())
            currentSelection = self.checkListTop.GetSelection()
            temp = self.sortOrderLayersTop[currentSelection + 1]
            self.sortOrderLayersTop[currentSelection + 1] = self.sortOrderLayersTop[currentSelection]
            self.sortOrderLayersTop[currentSelection] = temp
        
            self.checkListTop.SetItems(self.sortOrderLayersTop)
            self.checkListTop.SetCheckedStrings(tuple(self.checkedLayersTop))
            self.checkListTop.Select(currentSelection + 1)
            
            self.checkedLayersTop = list(self.checkListTop.GetCheckedStrings())

    def onClickUpBottomViewBtn(self, event):
        if self.checkListBottom.GetSelection() > 0:
            self.checkListTop.Deselect(self.checkListTop.GetSelection())
            currentSelection = self.checkListBottom.GetSelection()
            temp = self.sortOrderLayersBot[currentSelection - 1]
            self.sortOrderLayersBot[currentSelection - 1] = self.sortOrderLayersBot[currentSelection]
            self.sortOrderLayersBot[currentSelection] = temp
        
            self.checkListBottom.SetItems(self.sortOrderLayersBot)
            self.checkListBottom.SetCheckedStrings(self.checkedLayersBot)
            self.checkListBottom.Select(currentSelection - 1)

            self.checkedLayersBot = self.checkListBottom.GetCheckedStrings()
    
    def onClickDownBottomViewBtn(self, event):
        if self.checkListBottom.GetSelection() < pcbnew.PCB_LAYER_ID_COUNT:
            self.checkListTop.Deselect(self.checkListTop.GetSelection())
            currentSelection = self.checkListBottom.GetSelection()
            temp = self.sortOrderLayersBot[currentSelection + 1]
            self.sortOrderLayersBot[currentSelection + 1] = self.sortOrderLayersBot[currentSelection]
            self.sortOrderLayersBot[currentSelection] = temp
        
            self.checkListBottom.SetItems(self.sortOrderLayersBot)
            self.checkListBottom.SetCheckedStrings(self.checkedLayersBot)
            self.checkListBottom.Select(currentSelection + 1)

            self.checkedLayersBot = self.checkListBottom.GetCheckedStrings()

    def onMirrorLayerCheckBox(self, event):
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Mirrored"] = self.mirrorLayerCheckBox.IsChecked()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Mirrored"] = self.mirrorLayerCheckBox.IsChecked()

    def onNegativeLayerCheckBox(self, event):
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Negative"] = self.negativeLayerCheckBox.IsChecked()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Negative"] = self.negativeLayerCheckBox.IsChecked()

    def onPlotRefDesignatorsCheckBox(self, event):
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["PlotReferenceDesignators"] = self.plotRefDesignatorsCheckBox.IsChecked()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["PlotReferenceDesignators"] = self.plotRefDesignatorsCheckBox.IsChecked()
    
    def onPlotFootprintValuesCheckBox(self, event):
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["PlotFootprintValues"] = self.plotFootprintValuesCheckBox.IsChecked()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["PlotFootprintValues"] = self.plotFootprintValuesCheckBox.IsChecked()

    def onColourPickerColourChanged(self, event):
        color = self.colourPicker.GetColour()
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Color"] = color.GetRGB()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Color"] = color.GetRGB()

    def onOpacitySliderChange(self, event):
        if self.checkListTop.GetSelection() != -1:
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["Opacity"] = self.LayerOpacitySlider.GetValue()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["Opacity"] = self.LayerOpacitySlider.GetValue()

    def onAutoScale(self, event):
        if self.autoScaleCheckBox.IsChecked():
            self.layerScaleTextBox.Disable()
        else:
            self.layerScaleTextBox.Enable()
    
    def onDrillMarkChanged(self, event):
        if self.checkListTop.GetSelection() != -1: 
            self.settingsLayersTop[self.checkListTop.GetString(self.checkListTop.GetSelection())]["DrillMarks"] = self.drillMarksChoice.GetSelection()
        elif self.checkListBottom.GetSelection() != -1:
            self.settingsLayersBot[self.checkListBottom.GetString(self.checkListBottom.GetSelection())]["DrillMarks"] = self.drillMarksChoice.GetSelection()

    def onIndicateDNPCheckBox(self, event):
        if self.indicateDNP.IsChecked():
            self.DNPHide.Enable()
            self.DNPCrossOut.Enable()
        else:
            self.DNPHide.Disable()
            self.DNPCrossOut.Disable()

    def onClickSaveConfig(self, event):

        self.checkedLayersTop = list(self.checkListTop.GetCheckedStrings())
        self.checkedLayersBot = list(self.checkListBottom.GetCheckedStrings())

        config = configparser.ConfigParser()
        config["LayersTop"] = {}
        config["LayersBot"] = {}
        config["OutputSettings"] = {}
        config["LayersTop"]["sortorder"] = str(self.sortOrderLayersTop)
        config["LayersTop"]["checked"] = str(self.checkedLayersTop)
        config["LayersTop"]["settings"] = str(self.settingsLayersTop)
        config["LayersBot"]["sortorder"] = str(self.sortOrderLayersBot)
        config["LayersBot"]["checked"] = str(self.checkedLayersBot)
        config["LayersBot"]["settings"] = str(self.settingsLayersBot)
        config["OutputSettings"]["Generatetopview"] = str(self.generateTopCheckBox.IsChecked())
        config["OutputSettings"]["Generatebotview"] = str(self.generateBotCheckBox.IsChecked())
        config["OutputSettings"]["Generatecombinedview"] = str(self.generateCombinedCheckBox.IsChecked())
        config["OutputSettings"]["mergefiles"] = str(self.mergeFilesCheckBox.IsChecked())
        config["OutputSettings"]["autoscaling"] = str(self.autoScaleCheckBox.IsChecked())
        config["OutputSettings"]["layerscale"] = str(self.layerScaleTextBox.GetValue())
        config["OutputSettings"]["onlyboardedges"] = str(self.boundingBoxCheckBox.IsChecked())
        config["OutputSettings"]["indicatednp"] = str(self.indicateDNP.IsChecked())
        config["OutputSettings"]["dnphide"] = str(self.DNPHide.GetValue())
        config["OutputSettings"]["dnpcross"] = str(self.DNPCrossOut.GetValue())

        pluginDir = os.path.dirname(os.path.dirname(__file__))
        configPath = os.path.join(pluginDir, "config.ini")
        with open(configPath, 'w') as configfile:
            config.write(configfile)

    def onClickExit(self, event):
        self.EndModal(wx.ID_CANCEL)

    def onClickGenerate(self, event):
        self.statusText.SetLabel("Generating... This may take a while depending on the complexity of your design.")
        self.statusText.Update()
        self.generateFunc(self)
        self.statusText.SetLabel("Done!")
        