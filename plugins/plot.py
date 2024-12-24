import os
import shutil
import xml.etree.ElementTree as ET
import wx
import pcbnew
import sys

dirname = os.path.dirname(os.path.abspath(__file__))
dirname = os.path.join(dirname, "deps", "pypdf")
sys.path.insert(0, os.path.dirname(dirname))
from .deps import pypdf

def exportLayersFromKiCad(dialog, board, directory):
    topDir = os.path.join(directory, "top")
    botDir = os.path.join(directory, "bot")
    try:
        os.makedirs(topDir)
        os.makedirs(botDir)
    except:
        print("folder already exists.")
    # Initialize plot controller
    plotController = pcbnew.PLOT_CONTROLLER(board)
    plotOptions = plotController.GetPlotOptions()
    plotOptions.SetPlotFrameRef(False)
    try:
        plotOptions.SetPlotViaOnMaskLayer(False)
    except AttributeError:
        pass # Deprecated in KiCad V9
    plotOptions.SetAutoScale(False)
    plotOptions.SetMirror(False)
    plotOptions.SetUseGerberAttributes(False)
    plotOptions.SetScale(1)
    plotOptions.SetUseAuxOrigin(False)
    plotOptions.SetPlotInvisibleText(False)
    plotOptions.SetSubtractMaskFromSilk(False)
    plotOptions.SetOutputDirectory(directory)

    # Plot the Title Block and frame, will cause problems if User_9 layer is used...
    plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_NO_DRILL_SHAPE)
    plotOptions.SetPlotFrameRef(True)
    plotController.SetLayer(pcbnew.User_9)
    plotController.OpenPlotfile("Title_Block", pcbnew.PLOT_FORMAT_SVG,"")
    plotController.PlotLayer()
    plotController.ClosePlot()

    # Coloring is done after exporting, since we can't directly edit the color settings here.
    #settingsManager = pcbnew.GetSettingsManager() 
    #colorSettings = settingsManager.GetMigratedColorSettings()
    #plotOptions.SetColorSettings(colorSettings)
    #plotOptions.SetBlackAndWhite(True)
    plotController.SetColorMode(False)

    if dialog.indicateDNP.IsChecked():
        try:
            if dialog.indicateDNP.IsChecked():
                plotOptions.SetHideDNPFPsOnFabLayers(dialog.DNPHide.GetValue())
                plotOptions.SetCrossoutDNPFPsOnFabLayers(dialog.DNPCrossOut.GetValue())
            else:
                plotOptions.SetHideDNPFPsOnFabLayers(False)
                plotOptions.SetCrossoutDNPFPsOnFabLayers(False)
        except:
            pass
            #dlg=wx.MessageDialog(None, "'Indicate DNP on Fab layer' is only supported by KiCad version 9 and up.", "Not supported", wx.OK|wx.ICON_INFORMATION)
            #dlg.ShowModal()
            #dlg.Destroy()

    # Plot Layers
    plotOptions.SetPlotFrameRef(False)
    plotOptions.SetOutputDirectory(topDir)
    for layer in dialog.checkedLayersTop:

        if dialog.settingsLayersTop[layer]["DrillMarks"] == 0:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_NO_DRILL_SHAPE)
        elif dialog.settingsLayersTop[layer]["DrillMarks"] == 1:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_SMALL_DRILL_SHAPE)
        elif dialog.settingsLayersTop[layer]["DrillMarks"] == 2:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_FULL_DRILL_SHAPE)

        plotOptions.SetNegative(dialog.settingsLayersTop[layer]["Negative"])
        plotOptions.SetPlotReference(dialog.settingsLayersTop[layer]["PlotReferenceDesignators"])
        plotOptions.SetPlotValue(dialog.settingsLayersTop[layer]["PlotFootprintValues"])

        plotController.SetLayer(dialog.settingsLayersTop[layer]["ID"])
        plotController.OpenPlotfile(layer, pcbnew.PLOT_FORMAT_SVG,"")
        plotController.PlotLayer()
        plotController.ClosePlot()

    plotOptions.SetOutputDirectory(botDir)
    for layer in dialog.checkedLayersBot:

        if dialog.settingsLayersBot[layer]["DrillMarks"] == 0:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_NO_DRILL_SHAPE)
        elif dialog.settingsLayersBot[layer]["DrillMarks"] == 1:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_SMALL_DRILL_SHAPE)
        elif dialog.settingsLayersBot[layer]["DrillMarks"] == 2:
            plotOptions.SetDrillMarksType(pcbnew.DRILL_MARKS_FULL_DRILL_SHAPE)

        plotOptions.SetNegative(dialog.settingsLayersBot[layer]["Negative"])
        plotOptions.SetPlotReference(dialog.settingsLayersBot[layer]["PlotReferenceDesignators"])
        plotOptions.SetPlotValue(dialog.settingsLayersBot[layer]["PlotFootprintValues"])
        
        plotController.SetLayer(dialog.settingsLayersBot[layer]["ID"])
        plotController.OpenPlotfile(layer, pcbnew.PLOT_FORMAT_SVG,"")
        plotController.PlotLayer()
        plotController.ClosePlot()

def scaleTitleBlock(titleBlockSVG):
    tree = ET.parse(titleBlockSVG)
    root = tree.getroot()

    width = float(root.attrib.get("width")[:-2])
    
    width_max = 297.0022

    scalingFactor = round(width_max / width, 4)
    
    # Create a new group element and add it to the root
    groupElement = ET.Element("g")
    groupElement.attrib["transform"] = f"scale({scalingFactor},{scalingFactor})"

    for element in root:
        groupElement.append(element)

    root.clear()
    root.append(groupElement)
    root.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"
    root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
    root.attrib["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
    root.attrib["version"] = "1.1"
    root.attrib["width"] = "297.0022mm"
    root.attrib["height"] = "210.0072mm"
    root.attrib["viewBox"] = "0 0 297.0022 210.0072"
    tree.write(titleBlockSVG)

# Currently no way to set color during KiCad export, so we have to edit the svg itself
def colorSVG(svgFile, colorRGB):
    if colorRGB != 0:
        with open(svgFile, 'r') as file:
            svg = file.read()

        wxcolor = wx.Colour()
        wxcolor.SetRGB(colorRGB)
        colorHTML = wxcolor.GetAsString(wx.C2S_HTML_SYNTAX)
        coloredSVG = svg.replace("#000000", colorHTML)
            
        with open(svgFile, 'w') as file:
            file.write(coloredSVG)

def getBoundingBox(dialog, board):
    if dialog.boundingBoxCheckBox.IsChecked():
        boundingBox = board.ComputeBoundingBox(True)
    else:
        # only get bb for selected layers, otherwise all shown layers will be included and may cause issues with scaling
        originalVisibleLayerSet = board.GetVisibleLayers()
        originalVisibleElements = board.GetVisibleElements()
        visibleLayerSet = pcbnew.LSET()
        visibleElements = pcbnew.GAL_SET()
        for layer in dialog.checkedLayersTop + dialog.checkedLayersBot:
            visibleLayerSet.AddLayer(board.GetLayerID(layer))
        board.SetVisibleLayers(visibleLayerSet)
        board.SetVisibleElements(visibleElements)
        boundingBox = board.ComputeBoundingBox(False)
        board.SetVisibleLayers(originalVisibleLayerSet)
        board.SetVisibleElements(originalVisibleElements)
    
    return boundingBox

def mergeLayersSingleView(dialog, board, filename, tempDirectory, outputFileName):
    if os.path.basename(tempDirectory) == "top": 
        plotTopView = True
    else:
        plotTopView = False
    
    rootCombined = ET.Element("{http://www.w3.org/2000/svg}svg")

    boundingBox = getBoundingBox(dialog, board)

    marginTitleBlock = 35.0000 # 3,5cm margin
    margin = 30.0000 # 3cm margin
    width_max = 297.0022
    height_max = 210.0072
    
    scalingFactorWidth = ((width_max) - margin) / (boundingBox.GetWidth() / 1000000)
    scalingFactorHeight = ((height_max) - margin - marginTitleBlock) / (boundingBox.GetHeight() / 1000000)
    
    if scalingFactorWidth < scalingFactorHeight:
        scalingFactor = round(scalingFactorWidth, 4)
    else:
        scalingFactor = round(scalingFactorHeight, 4)

    if not dialog.autoScaleCheckBox.IsChecked():
        try:
            if scalingFactor < float(dialog.layerScaleTextBox.GetValue()):
                dlg=wx.MessageDialog(None, "Entered scale factor is too large. Auto scale factor:" + str(scalingFactor) + " is used.", "Scaling issue", wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                scalingFactor = float(dialog.layerScaleTextBox.GetValue())
        except ValueError:
            dlg=wx.MessageDialog(None, "Entered scale factor is not a number. Auto scale factor:" + str(scalingFactor) + " is used.", "Scaling issue", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
    
    moveX = round((width_max / 2 / scalingFactor) - ((boundingBox.GetX() / 1000000) + ((boundingBox.GetWidth() / 1000000) / 2)), 4)
    moveY = round(-(boundingBox.GetY() / 1000000) + (height_max / 2 / scalingFactor) - ((boundingBox.GetHeight() / 1000000) / 2) - marginTitleBlock / 2 / scalingFactor, 4)

    for layer in reversed(dialog.checkedLayersTop if plotTopView == True else dialog.checkedLayersBot):
        # replace . in layername with _ to match output file names
        layername = layer.replace(".", "_")
        svgFile = os.path.join(tempDirectory, f"{filename}-{layername}.svg")
        colorSVG(svgFile, dialog.settingsLayersTop[layer]["Color"] if plotTopView == True else dialog.settingsLayersBot[layer]["Color"])
        tree = ET.parse(svgFile)
        root = tree.getroot()

        groupElement = ET.Element("g")
            
        if plotTopView:
            if bool(dialog.settingsLayersTop[layer]["Mirrored"]):
                groupElement.attrib["transform"] = f"scale({-scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX - width_max / scalingFactor},{moveY})"
            else:
                groupElement.attrib["transform"] = f"scale({scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX},{moveY})"
            layerOpacity = int(dialog.settingsLayersTop[layer]["Opacity"]) / 100
        else:
            if bool(dialog.settingsLayersBot[layer]["Mirrored"]):
                groupElement.attrib["transform"] = f"scale({-scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX - width_max / scalingFactor},{moveY})"
            else:
                groupElement.attrib["transform"] = f"scale({scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX},{moveY})"
            layerOpacity = int(dialog.settingsLayersBot[layer]["Opacity"]) / 100
        
        groupElement.attrib["style"] = f"opacity:{layerOpacity}"

        for element in root:
            groupElement.append(element)

        root.clear()
        root.append(groupElement)
        root.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"
        root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
        root.attrib["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        root.attrib["version"] = "1.1"
        root.attrib["width"] = "297.0022mm"
        root.attrib["height"] = "210.0072mm"
        root.attrib["viewBox"] = "0 0 297.0022 210.0072"

        tree.write(svgFile)
        
        treeCombined = ET.parse(svgFile)
        svg = treeCombined.getroot()
        for child in svg:
            rootCombined.append(child)

    rootCombined.attrib["width"] = "297.0022mm"
    rootCombined.attrib["height"] = "210.0072mm"
    rootCombined.attrib["viewBox"] = "0 0 297.0022 210.0072"

    treeCombined = ET.ElementTree(rootCombined)
    treeCombined.write(outputFileName)

def mergeLayersCombinedView(dialog, board, filename, tempDirectory, outputFileName):
    if os.path.basename(tempDirectory) == "top": 
        plotTopView = True
    else:
        plotTopView = False

    rootCombined = ET.Element("{http://www.w3.org/2000/svg}svg")

    boundingBox = getBoundingBox(dialog, board)

    marginTitleBlock = 35.0000 # 3,5cm margin
    marginFrame = 10.0000 # 1cm margin
    margin = 30.0000 # 3cm margin
    width_max = 297.0022
    height_max = 210.0072
    
    scalingFactorWidth = ((width_max / 2) - margin / 2 - marginFrame / 2) / (boundingBox.GetWidth() / 1000000)
    scalingFactorHeight = ((height_max) - margin - marginTitleBlock) / (boundingBox.GetHeight() / 1000000)
    
    if scalingFactorWidth < scalingFactorHeight:
        scalingFactor = round(scalingFactorWidth, 4)
    else:
        scalingFactor = round(scalingFactorHeight, 4)

    if not dialog.autoScaleCheckBox.IsChecked():
        try:
            if scalingFactor < float(dialog.layerScaleTextBox.GetValue()):
                dlg=wx.MessageDialog(None, "Entered scale factor is too large. Auto scale factor:" + str(scalingFactor) + " is used.", "Scaling issue", wx.OK|wx.ICON_INFORMATION)
                dlg.ShowModal()
                dlg.Destroy()
            else:
                scalingFactor = float(dialog.layerScaleTextBox.GetValue())
        except ValueError:
            dlg=wx.MessageDialog(None, "Entered scale factor is not a number. Auto scale factor:" + str(scalingFactor) + " is used.", "Scaling issue", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
    
    moveX = round((width_max / 4 / scalingFactor) - ((boundingBox.GetX() / 1000000) + ((boundingBox.GetWidth() / 1000000) / 2)) + marginFrame / 2 / scalingFactor, 4)
    moveY = round(-(boundingBox.GetY() / 1000000) + (height_max / 2 / scalingFactor) - ((boundingBox.GetHeight() / 1000000) / 2) - marginTitleBlock / 2 / scalingFactor, 4)

    for layer in reversed(dialog.checkedLayersTop if plotTopView == True else dialog.checkedLayersBot):
        # replace . in layername with _ to match output file names
        layername = layer.replace(".", "_")
        svgFile = os.path.join(tempDirectory, f"{filename}-{layername}.svg")
        colorSVG(svgFile, dialog.settingsLayersTop[layer]["Color"] if plotTopView == True else dialog.settingsLayersBot[layer]["Color"])
        tree = ET.parse(svgFile)
        root = tree.getroot()

        groupElement = ET.Element("g")
            
        if plotTopView:
            if bool(dialog.settingsLayersTop[layer]["Mirrored"]):
                groupElement.attrib["transform"] = f"scale({-scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX - width_max / 2 / scalingFactor - marginFrame / scalingFactor},{moveY})"
            else:
                groupElement.attrib["transform"] = f"scale({scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX},{moveY})"
            layerOpacity = int(dialog.settingsLayersTop[layer]["Opacity"]) / 100
        else:
            if bool(dialog.settingsLayersBot[layer]["Mirrored"]):
                groupElement.attrib["transform"] = f"scale({-scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX - width_max / scalingFactor},{moveY})"
            else:
                groupElement.attrib["transform"] = f"scale({scalingFactor},{scalingFactor})"
                groupElement.attrib["transform"] += f"translate({moveX + width_max / 2 / scalingFactor - marginFrame / scalingFactor},{moveY})"
            layerOpacity = int(dialog.settingsLayersBot[layer]["Opacity"]) / 100
        
        groupElement.attrib["style"] = f"opacity:{layerOpacity}"

        for element in root:
            groupElement.append(element)

        root.clear()
        root.append(groupElement)
        root.attrib["xmlns:svg"] = "http://www.w3.org/2000/svg"
        root.attrib["xmlns"] = "http://www.w3.org/2000/svg"
        root.attrib["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        root.attrib["version"] = "1.1"
        root.attrib["width"] = "297.0022mm"
        root.attrib["height"] = "210.0072mm"
        root.attrib["viewBox"] = "0 0 297.0022 210.0072"

        tree.write(svgFile)
        
        treeCombined = ET.parse(svgFile)
        svg = treeCombined.getroot()
        for child in svg:
            rootCombined.append(child)

    rootCombined.attrib["width"] = "297.0022mm"
    rootCombined.attrib["height"] = "210.0072mm"
    rootCombined.attrib["viewBox"] = "0 0 297.0022 210.0072"

    treeCombined = ET.ElementTree(rootCombined)
    treeCombined.write(outputFileName)

def mergeSVGs(svgFiles, outputFileName):
    root = ET.Element("{http://www.w3.org/2000/svg}svg")
    for file in svgFiles:

        tree = ET.parse(file)
        svg = tree.getroot()
        for child in svg:
            root.append(child)

    root.attrib["width"] = "297.0022mm"
    root.attrib["height"] = "210.0072mm"
    root.attrib["viewBox"] = "0 0 297.0022 210.0072"

    tree = ET.ElementTree(root)
    tree.write(outputFileName)

def generateAssembly(dialog):
    try:
        import cairosvg
    except ImportError as e:
        dlg=wx.MessageDialog(None, "CairoSVG is not installed. Run 'python -m pip install cairosvg' from kicad command prompt and restart kicad.", "Error", wx.OK|wx.ICON_INFORMATION)
        dlg.ShowModal()
        dlg.Destroy()
        return

    board = pcbnew.GetBoard()
    pcbFileName = os.path.basename(board.GetFileName())
    filename = os.path.splitext(os.path.split(pcbFileName)[1])[0]
    outputDirectory = os.path.join(dialog.dirPicker.GetPath(),"Assembly Drawing")
    tempDirectory = os.path.join(outputDirectory, "temp")
    try:
        os.makedirs(tempDirectory)
    except:
        print("folder already exists.")

    if dialog.generateTopCheckBox.IsChecked():

        # Export Layers from KiCad
        exportLayersFromKiCad(dialog, board, tempDirectory)
        scaleTitleBlock(os.path.join(tempDirectory,filename + "-Title_Block.svg"))

        # Combine SVG for the Top view
        mergeLayersSingleView(dialog, board, filename, os.path.join(tempDirectory, "top"), os.path.join(tempDirectory, "combined_top.svg"))

        # Combine all files into one final output file
        mergeSVGs([os.path.join(tempDirectory, "combined_top.svg"), os.path.join(tempDirectory,filename +"-Title_Block.svg")], os.path.join(tempDirectory, "final.svg"))
        try:
            f = open(os.path.join(tempDirectory, "final.svg"))
            cairosvg.svg2pdf(file_obj=f, write_to=os.path.join(outputDirectory, filename + " - Assembly Drawing Top.pdf"))
            
        except:
            dlg=wx.MessageDialog(None, "Can't access PDF, is it still open?", "Error", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            f.close()

    if dialog.generateBotCheckBox.IsChecked():

        # Export Layers from KiCad
        exportLayersFromKiCad(dialog, board, tempDirectory)
        scaleTitleBlock(os.path.join(tempDirectory,filename + "-Title_Block.svg"))

        # Combine SVG for the Bot view
        mergeLayersSingleView(dialog, board, filename, os.path.join(tempDirectory, "bot"), os.path.join(tempDirectory, "combined_bot.svg"))

        # Combine all files into one final output file
        mergeSVGs([os.path.join(tempDirectory, "combined_bot.svg"), os.path.join(tempDirectory,filename +"-Title_Block.svg")], os.path.join(tempDirectory, "final.svg"))
        try:
            f = open(os.path.join(tempDirectory, "final.svg"))
            cairosvg.svg2pdf(file_obj=f, write_to=os.path.join(outputDirectory, filename + " - Assembly Drawing Bot.pdf"))
        except:
            dlg=wx.MessageDialog(None, "Can't access PDF, is it still open?", "Error", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            f.close()

    if dialog.generateCombinedCheckBox.IsChecked():

        # Export Layers from KiCad
        exportLayersFromKiCad(dialog, board, tempDirectory)
        scaleTitleBlock(os.path.join(tempDirectory,filename + "-Title_Block.svg"))

        # Combine SVG for the Top view
        mergeLayersCombinedView(dialog, board, filename, os.path.join(tempDirectory, "top"), os.path.join(tempDirectory, "combined_top.svg"))

        # Combine SVG for the Bot view
        mergeLayersCombinedView(dialog, board, filename, os.path.join(tempDirectory, "bot"), os.path.join(tempDirectory, "combined_bot.svg"))

        mergeSVGs([os.path.join(tempDirectory, "combined_top.svg"), os.path.join(tempDirectory, "combined_bot.svg"), os.path.join(tempDirectory,filename +"-Title_Block.svg")], os.path.join(tempDirectory, "final.svg"))
        try:
            f = open(os.path.join(tempDirectory, "final.svg"))
            cairosvg.svg2pdf(file_obj=f, write_to=os.path.join(outputDirectory, filename + " - Assembly Drawing Top + Bot.pdf"))
        except:
            dlg=wx.MessageDialog(None, "Can't access PDF, is it still open?", "Error", wx.OK|wx.ICON_INFORMATION)
            dlg.ShowModal()
            dlg.Destroy()
        finally:
            f.close()

    if dialog.mergeFilesCheckBox.IsChecked():
        
        merger = pypdf.PdfWriter()

        pdfFiles = []

        if dialog.generateTopCheckBox.IsChecked():
            pdfFiles.append(os.path.join(outputDirectory, filename + " - Assembly Drawing Top.pdf"))
        if dialog.generateBotCheckBox.IsChecked():
            pdfFiles.append(os.path.join(outputDirectory, filename + " - Assembly Drawing Bot.pdf"))
        if dialog.generateCombinedCheckBox.IsChecked():
            pdfFiles.append(os.path.join(outputDirectory, filename + " - Assembly Drawing Top + Bot.pdf"))

        for pdf in pdfFiles:
            merger.append(pdf)
        merger.write(os.path.join(outputDirectory, filename + " - Assembly Drawing.pdf"))
        merger.close()

        for pdf in pdfFiles:
            os.remove(pdf)

    # Remove temp directory
    shutil.rmtree(tempDirectory, ignore_errors = True)