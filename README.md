# Kicad Assembly Drawing Generator Plugin
![icon](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/resources/icon.png?ref_type=heads)

A tool that makes exporting good looking assembly drawings simple. Select the layers you want as part of the drawing and the plugin will take care of exporting, merging as well as scaling and generate a pdf document.

Example:
- [Assembly Drawing Top View](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/doc/nanoLogger%20-%20Assembly%20Drawing%20Top.pdf?ref_type=heads)
- [Assembly Drawing Top + Bot View](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/doc/PrecisionCurrentSource%20-%20Assembly%20Drawing%20Top%20+%20Bot.pdf)

## Usage

Configure `Top` and `Bottom` views of your board:
- Simply select and sort the layers you want shown in your assembly drawing
- Layer properties can be configured to your liking for each layer separately

Configure `output`:
- A `Assembly Drawing` folder containing the expported files will be created in the output directory
- Manually select a scale factor or use the auto scaling option
- Select files to export

Make sure to save your configuration once you're happy with it!

![dialog](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/doc/dialog.png?ref_type=heads)

## Installation

**Note:** [CairoSVG](https://github.com/Kozea/CairoSVG) needs to be installed in order for the plugin to convert svg files into pdfs.
- To install it simply open `KiCad Command Prompt` and run `python -m pip install cairosvg`


Kicad assembly generator is currently not part of the official Kicad addons repository and has to be manually installed.
- Download the current release
- Open the Kicad PCM and select `Install from File...`
- Select the downloaded `.zip` archive containing the plugin
- The plugin should now show up in the installed tab

![installation](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/doc/installation.png?ref_type=heads)
![installed](https://gitlab.com/TobiasNetzer/kicad-assembly-generator/-/raw/main/doc/installed.png?ref_type=heads)

# Disclaimer

This plugin was created for my specific needs and probably won't cover all edge cases.

## Licence and credits

Plugin code licensed under MIT, see `LICENSE` for more info.
- Python PDF library: [PyPDF](https://github.com/py-pdf/pypdf)
- SVG to PDF converter: [CairoSVG](https://github.com/Kozea/CairoSVG)
