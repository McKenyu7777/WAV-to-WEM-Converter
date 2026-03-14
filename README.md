f# WAV to WEM Converter

A Python script that batch converts `.wav` audio files to `.wem` format using **Audiokinetic Wwise 2024**. Built for Fromsoft modding workflows where you need properly named WEM files without dealing with Wwise's GUI or its cryptic numeric output filenames.

---

## Features

- Batch converts all WAV files in a folder to WEM
- Output WEM files are **named after the original WAV files** (not Wwise's numeric IDs)
- Non-destructive — original WAV files are never modified or deleted
- Uses **PCM As Input** preset for lossless, uncompressed output
- Simple CMD interface — just run and follow the prompts

---

## Requirements

### 1. Python 3.x
Download from [python.org](https://www.python.org/downloads/)

No additional Python packages are needed — only standard library modules are used.

### 2. Audiokinetic Wwise 2024
Download and install from [audiokinetic.com](https://www.audiokinetic.com/en/download)

- During installation, make sure **Windows** platform support is included
- A free account is required to download Wwise

### 3. A Wwise Project
You need an existing Wwise project. The script uses your project's conversion settings to produce WEM files.

To create one:
1. Open Wwise
2. Go to **File → New Project**
3. Name it anything (e.g. `WEM Converter`)
4. Save it somewhere permanent

---

## Setup — Edit the Script

Before running, you **must update 4 hardcoded paths** at the top of `wav_to_wem.py`:

```python
WWISE_CONSOLE  = r"C:\Program Files (x86)\Audiokinetic\Wwise2024.1.4.8780\Authoring\x64\Release\bin\WwiseConsole.exe"
WWISE_PROJECT  = r"C:\Users\LENOVO LOQ\Documents\WwiseProjects\New Audio\New Audio.wproj"
WWISE_GEN_DIR  = Path(r"C:\Users\LENOVO LOQ\Documents\WwiseProjects\New Audio\GeneratedSoundBanks\Windows")
CONVERSION_PRESET = "Vorbis Quality High"
```

### WWISE_CONSOLE
Path to `WwiseConsole.exe` on your machine. The version number in the path will differ depending on what you installed.

Find it at:
```
C:\Program Files (x86)\Audiokinetic\Wwise<VERSION>\Authoring\x64\Release\bin\WwiseConsole.exe
```

Replace `<VERSION>` with your installed version, for example:
```
Wwise2024.1.4.8780
```

### WWISE_PROJECT
Full path to your `.wproj` file. Example:
```
C:\Users\YourName\Documents\WwiseProjects\MyProject\MyProject.wproj
```

### WWISE_GEN_DIR
This is where Wwise outputs the converted WEM files. It's always inside your Wwise project folder:
```
C:\Users\YourName\Documents\WwiseProjects\MyProject\GeneratedSoundBanks\Windows
```

> **Note:** This folder is created automatically by Wwise the first time you convert. You don't need to create it manually.

### CONVERSION_PRESET
The name of the conversion preset to use. `"PCM As Input"` is the default and recommended for modding since it preserves the original audio quality without re-encoding.

Other available presets from your Wwise project's `Factory Conversion Settings`:
| Preset Name | Format | Quality |
|---|---|---|
| `PCM As Input` | PCM | Lossless ✅ Recommended |
| `Vorbis Quality High` | Vorbis | Compressed, high quality |
| `Vorbis Quality Medium` | Vorbis | Compressed, medium quality |
| `Vorbis Quality Low` | Vorbis | Compressed, low quality |
| `ADPCM As Input` | ADPCM | Compressed, older format |

---

## Usage

1. Open CMD
2. Navigate to the folder containing the script:
   ```
   cd "D:\Your\Script\Folder"
   ```
3. Run the script:
   ```
   python wav_to_wem.py
   ```
4. Follow the prompts:
   - **Step 1:** Enter the folder path containing your WAV files
   - **Step 2:** Enter the folder path where WEM files will be saved
   - **Step 3:** Confirm and the conversion starts automatically

### Example Session
```
==================================================
         WAV  -->  WEM  CONVERTER
    (Powered by Audiokinetic Wwise 2024)
==================================================

  Project  : C:\Users\YourName\Documents\WwiseProjects\MyProject\MyProject.wproj
  Preset   : PCM As Input

[STEP 1] Enter the folder path containing your WAV files:
  Path: D:\Mods\MyMod\sounds\wav

  Found 5 WAV file(s):
    - SE_PC_Attack_01.wav
    - SE_PC_Attack_02.wav
    - SE_PC_FootStep_01.wav
    - SE_PC_FootStep_02.wav
    - SE_PC_Death_01.wav

[STEP 2] Enter the folder path where WEM files will be saved:
  Path: D:\Mods\MyMod\sounds\wem

  Proceed? (y/n): y

  [OK]   SE_PC_Attack_01.wav  -->  SE_PC_Attack_01.wem
  [OK]   SE_PC_Attack_02.wav  -->  SE_PC_Attack_02.wem
  [OK]   SE_PC_FootStep_01.wav  -->  SE_PC_FootStep_01.wem
  [OK]   SE_PC_FootStep_02.wav  -->  SE_PC_FootStep_02.wem
  [OK]   SE_PC_Death_01.wav  -->  SE_PC_Death_01.wem

==================================================
  DONE!
  Successfully converted : 5 file(s)
  Saved to               : D:\Mods\MyMod\sounds\wem
  Original files kept    : YES
==================================================
```

---

## How It Works

1. Scans the input folder for `.wav` files
2. Generates a `.wsources` XML file listing all WAVs with the selected conversion preset
3. Calls `WwiseConsole.exe` with the `convert-external-source` command
4. Wwise converts the files and outputs WEMs to `GeneratedSoundBanks\Windows` inside your project folder
5. The script copies the WEMs to your chosen output folder, **renaming each one to match its original WAV filename**

---

## Troubleshooting

**`WwiseConsole.exe not found`**
- Double-check the `WWISE_CONSOLE` path in the script
- Make sure Wwise is fully installed and not just the launcher

**`No WEM files found after conversion`**
- Verify `WWISE_GEN_DIR` points to the correct `GeneratedSoundBanks\Windows` path inside your project folder
- Make sure the `CONVERSION_PRESET` name exactly matches a preset in your Wwise project (case-sensitive)
- Open Wwise and check **Project → Conversion Settings** to confirm preset names

**`No WAV files found`**
- Make sure your WAV files are directly in the input folder (not in subfolders)
- The script only scans one folder level deep

**Wwise opens its GUI instead of running silently**
- Make sure you're pointing to `WwiseConsole.exe` and **not** `Wwise.exe`

---

## Notes

- The script clears old WEMs from the Wwise output folder before each run to prevent stale files from being copied
- WAV files in subfolders are not scanned — all files must be in the root of the input folder
- The `.wsources` temp file is automatically cleaned up after conversion

---

## Related Tools

| Tool | Purpose |
|---|---|
| [vgmstream](https://github.com/vgmstream/vgmstream) | Extract / preview WEM files |
| [WWISER](https://github.com/bnnm/wwiser) | Analyze Wwise `.bnk` soundbank files |
| [elden-ring-mod-tools](https://github.com/soulsmods/ModEngine2) | Mod Engine for Fromsoft games |
