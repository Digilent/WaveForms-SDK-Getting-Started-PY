## Description
Demo package for the WaveForms SDK Getting Started guide and multiple test scripts for different instruments.

Check: [Getting Started with the WaveForms SDK](https://digilent.com/reference/test-and-measurement/guides/waveforms-sdk-getting-started) for more details.

***

## Available tests:
* empty test template
* analog signal generation and recording test
* digital signal generation and recording test
* blinking LEDs with the Suplpies and the Static I/O instruments
* UART in/out test using the Pmod CLS and the Pmod MAXSonar
* SPI in/out test using the Pmod CLS and the Pmod ALS
* I2C in/out test using the Pmod CLS and the Pmod TMP2

***

## Available instruments and functions:
### Device
* open
* check_error
* close

### Oscilloscope
* open
* measure
* trigger
* record
* close

### Waveform Generator
* generate
* close

### Power Supplies
* switch
* switch_fixed (for Analog Discovery)
* switch_variable (for Analog Discovery 2 and Studio)
* switch_digital (for Digital Discovery and Analog Discovery Pro 3X50)
* switch_6V (for Analog Discovery Pro 5250)
* switch_25V (for Analog Discovery Pro 5250)
* close

### Digital Multimeter
* open
* measure - **UNTESTED**
* close

### Logic Analyzer
* open
* trigger
* record
* close

### Pattern Generator
* generate
* close

### Static I/O
* set_mode
* get_state
* set_state
* set_current - **UNTESTED**
* set_pull - **UNTESTED**
* close

### Protocol
#### UART
* open
* read
* write
* close

#### SPI
* open
* read
* write
* echange
* spy - **UNTESTED**
* close

#### I2C
* open
* read
* write
* echange
* spy - **UNTESTED**
* close
