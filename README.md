# Open Source Hardware Project

This repository contains the complete design files and documentation for an open source hardware project.

## Project Structure

### 📁 Printed Parts
- **Shell**: `printed-parts/shells/shell.STEP`
- **Layers**: 
  - Layer 1: `printed-parts/layers/layer1.STEP`
  - Layer 2: `printed-parts/layers/layer2.STEP`
  - Layer 3: `printed-parts/layers/layer3.STEP`
  - Layer 4: `printed-parts/layers/Layer4.STEP`
- **Head**: `printed-parts/heads/head.STEP`
- **Arm Links**: 
  - Link 1: `printed-parts/arm/link1.STEP`
  - Link 2: `printed-parts/arm/link2.STEP`
  - Link 3: `printed-parts/arm/link3.STEP`
  - Link 4: `printed-parts/arm/link4.STEP`
  - Link 5: `printed-parts/arm/link5.STEP`
  - Link 6-1: `printed-parts/arm/link61.STEP`
  - Link 6-2: `printed-parts/arm/link62.STEP`
- **Layer Components**:
  - Battery Cover: `printed-parts/layer-components/batter_holder_2_cover.STEP`
  - USB Holder: `printed-parts/layer-components/usb_holder.STEP`

### 📁 PCBs
- **Head PCB**: 
  - KiCad Project: `pcbs/head-pcb/leader.kicad_pro`
  - Production Files: `pcbs/head-pcb/production/`
  - BOM: `pcbs/head-pcb/production/bom.csv`
- **Main Dev Board**:
  - KiCad Project: `pcbs/main-dev-board/innate dev pcb.kicad_pro`
  - Production Files: `pcbs/main-dev-board/production/`
  - BOM: `pcbs/main-dev-board/production/bom.csv`

### 📁 Documentation
- **Bill of Materials**: [BOM.md](BOM.md)
- **Assemblies**: [assemblies.zip](assemblies.zip)

## Getting Started

1. Review the [Bill of Materials](BOM.md) for a complete parts list
2. Check the PCB production files in the `pcbs/` directory for manufacturing
3. Use the STEP files in `printed-parts/` for 3D printing
4. Refer to the KiCad project files for PCB modifications

## Manufacturing

### PCB Fabrication
- Use the production files in each PCB directory
- Submit the `.zip` files along with the BOM and positions CSV to your PCB manufacturer

### 3D Printing
- All STEP files are ready for 3D printing
- Recommended materials and settings can be found in the BOM

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this project.

## License

This project is open source hardware. Please see the license file for details.
