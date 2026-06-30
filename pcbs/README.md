# PCBs

KiCad project files and production-ready outputs for all Mars robot circuit boards.

## 📋 Boards

### Head PCB
**Location**: `head-pcb/`

The head PCB controls sensors and actuators in the robot's head assembly.

- **KiCad Project**: [leader.kicad_pro](head-pcb/leader.kicad_pro)
- **Schematic**: [leader.kicad_sch](head-pcb/leader.kicad_sch)
- **PCB Layout**: [leader.kicad_pcb](head-pcb/leader.kicad_pcb)

**Production Files** (`head-pcb/production/`):
- [Gerbers & Drill Files](head-pcb/production/leader.zip)
- [BOM (Bill of Materials)](head-pcb/production/bom.csv)
- [Component Positions](head-pcb/production/positions.csv)
- [Designators Reference](head-pcb/production/designators.csv)
- [IPC Netlist](head-pcb/production/netlist.ipc)

### Main Development Board
**Location**: `main-dev-board/`

The main development board is the brain of the robot, handling computation and motor control."C:\Users\nick\Documents\Innate\mars\pcbs\main-dev-board\MARS%20Dev%20Board.kicad_pro"

- **KiCad Project**: [innate dev pcb.kicad_pro](main-dev-board/MARS%20Dev%20Board.kicad_pro)
- **Schematic**: [innate dev pcb.kicad_sch](main-dev-board/MARS%20Dev%20Board.kicad_sch)
- **PCB Layout**: [innate dev pcb.kicad_pcb](main-dev-board/MARS%20Dev%20Board.kicad_pcb)
- **3D Model**: [innate dev pcb.step](main-dev-board/MARS%20Dev%20Board.step)

**Production Files** (`main-dev-board/production/`):
- [Gerbers & Drill Files](main-dev-board/production/MARS_Dev_Board.zip)
- [BOM (Bill of Materials)](main-dev-board/production/bom.csv)
- [Component Positions](main-dev-board/production/positions.csv)
- [Designators Reference](main-dev-board/production/designators.csv)
- [IPC Netlist](main-dev-board/production/netlist.ipc)

## Design Modifications

To modify the PCB designs:
1. Install [KiCad 7.0+](https://www.kicad.org/)
2. Open the `.kicad_pro` file in KiCad
3. Make your changes to schematic and/or layout
4. Regenerate production files using KiCad's fabrication output tools

## 📐 Fabrication Toolkit

Both boards include `fabrication-toolkit-options.json` for automated production file generation.

## ⚡ Important Notes

- Always verify board revisions match your BOM
- Double-check component orientations before assembly
- Test boards thoroughly before integration
- Refer to the [main BOM](../BOM.md) for complete sourcing information

