<div align="center">

<!-- Add your banner image here -->
<!-- ![Mars Robot Banner](./assets/banner.png) -->

# Mars v0.9 - Open Source Hardware

*Complete design files and documentation for the Mars robot platform*

[![Discord](https://img.shields.io/badge/Discord-Join%20our%20community-5865F2?style=for-the-badge&logo=discord&logoColor=white)](https://discord.gg/your-invite-link)
[![Documentation](https://img.shields.io/badge/Docs-Read%20the%20docs-blue?style=for-the-badge&logo=readthedocs&logoColor=white)](https://docs.yoursite.com)
[![Website](https://img.shields.io/badge/Website-Visit%20us-orange?style=for-the-badge&logo=safari&logoColor=white)](https://yourwebsite.com)
[![License: CERN-OHL-S-2.0](https://img.shields.io/badge/Hardware%20License-CERN--OHL--S--2.0-green?style=for-the-badge)](LICENSE-HARDWARE)
[![License: GPL v3](https://img.shields.io/badge/Software%20License-GPL%20v3-blue?style=for-the-badge)](LICENSE-SOFTWARE)

</div>

---

> [!WARNING]
> ## ⚠️ Important Disclaimer
>
> This open-source hardware release is part of our ongoing development process. While we're committed to transparency and community collaboration, please note:
>
> - **This is a v0.9 release** - The design may undergo revisions and improvements
> - **Breaking changes are possible** - We may introduce modifications that are not backward compatible
> - **No warranty for DIY builds** - Self-built robots are provided as-is without guarantees
>
> ### 🛡️ Upgrade Guarantee
>
> **If you purchase a Mars robot directly from us**, you'll receive:
> - ✅ Full hardware and software support
> - ✅ Guaranteed upgrades to future versions
> - ✅ Access to our technical support team
> - ✅ Quality-tested components and assembly

---

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

We welcome contributions from the community! Feel free to:
- 🐛 Report bugs and issues
- 💡 Suggest new features and improvements
- 🔧 Submit pull requests
- 📖 Improve documentation

Please join our [Discord community](https://discord.gg/your-invite-link) to discuss your ideas before making major changes.

---

## 📜 License

This project uses dual licensing to cover hardware and software components:

### Hardware License: CERN-OHL-S-2.0

All hardware designs, PCB files, 3D models, and related documentation in this repository are licensed under the **CERN Open Hardware Licence Version 2 - Strongly Reciprocal** (CERN-OHL-S-2.0).

This is a copyleft license that ensures any modifications or derivative works must also be released under the same license, promoting open collaboration while protecting the open-source nature of the hardware.

📄 [View Hardware License](LICENSE-HARDWARE)  
🔗 [Learn more about CERN-OHL-S](https://ohwr.org/cern_ohl_s_v2.txt)

### Software License: GPL v3

The software components for this robot (to be released separately) are licensed under the **GNU General Public License v3.0** (GPL v3).

This ensures that any software modifications or derivative works remain open source and available to the community.

📄 [View Software License](LICENSE-SOFTWARE) *(Software repository coming soon)*  
🔗 [Learn more about GPL v3](https://www.gnu.org/licenses/gpl-3.0.en.html)

---

<div align="center">

**Built with ❤️ by the Innate community**

[Discord](https://discord.gg/your-invite-link) • [Documentation](https://docs.yoursite.com) • [Website](https://yourwebsite.com)

</div>
