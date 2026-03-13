import os
import sys
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

WWISE_CONSOLE  = r"C:\Program Files (x86)\Audiokinetic\Wwise2024.1.4.8780\Authoring\x64\Release\bin\WwiseConsole.exe"
WWISE_PROJECT  = r"C:\Users\LENOVO LOQ\Documents\WwiseProjects\New Audio\New Audio.wproj"
WWISE_GEN_DIR  = Path(r"C:\Users\LENOVO LOQ\Documents\WwiseProjects\New Audio\GeneratedSoundBanks\Windows")
CONVERSION_PRESET = "PCM As Input"

def check_wwise():
    if not os.path.exists(WWISE_CONSOLE):
        print(f"  ERROR: WwiseConsole.exe not found at:\n  {WWISE_CONSOLE}")
        input("\n  Press Enter to exit...")
        sys.exit(1)

def find_wav_files(folder_path):
    return list(Path(folder_path).glob("*.wav"))

def create_wsources(wsources_path, wav_files):
    lines = ['<?xml version="1.0" encoding="utf-8"?>']
    lines.append('<ExternalSourcesList SchemaVersion="1" Root="">')
    for wav in wav_files:
        lines.append(f'    <Source Path="{wav}" Conversion="{CONVERSION_PRESET}" />')
    lines.append("</ExternalSourcesList>")
    with open(str(wsources_path), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def clear_old_wems():
    if WWISE_GEN_DIR.exists():
        for wem in WWISE_GEN_DIR.rglob("*.wem"):
            try:
                wem.unlink()
            except Exception:
                pass

def run_conversion(wsources_file):
    # Correct syntax: --source-file FLAG for the wsources file
    cmd = [
        WWISE_CONSOLE,
        "convert-external-source",
        WWISE_PROJECT,
        "--source-file", str(wsources_file),
        "--platform", "Windows",
        "--verbose"
    ]
    print(f"\n  Running WwiseConsole...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    output = (result.stdout + result.stderr).strip()
    return result.returncode, output

def collect_and_rename_wems(wav_files, output_dir):
    time.sleep(1)
    wem_files = list(WWISE_GEN_DIR.rglob("*.wem")) if WWISE_GEN_DIR.exists() else []

    print(f"\n  Found {len(wem_files)} WEM(s) in Wwise output folder.")

    if not wem_files:
        print(f"\n  ERROR: No WEMs found in:\n  {WWISE_GEN_DIR}")
        return 0, len(wav_files)

    out_path   = Path(output_dir)
    wav_lookup = {wav.stem.lower(): wav for wav in wav_files}
    success    = 0
    failed     = 0

    for wem in wem_files:
        stem = wem.stem.lower()
        if stem in wav_lookup:
            original   = wav_lookup[stem]
            target_wem = out_path / f"{original.stem}.wem"
            shutil.copy2(str(wem), str(target_wem))
            print(f"  [OK]   {original.name}  -->  {original.stem}.wem")
            success += 1
        else:
            target_wem = out_path / wem.name
            shutil.copy2(str(wem), str(target_wem))
            print(f"  [WEM]  {wem.name}  (copied as-is)")
            success += 1

    produced_stems = {wem.stem.lower() for wem in wem_files}
    for wav in wav_files:
        if wav.stem.lower() not in produced_stems:
            print(f"  [FAIL] {wav.name} — no WEM produced")
            failed += 1

    return success, failed

def main():
    os.system("cls" if os.name == "nt" else "clear")
    print("=" * 50)
    print("         WAV  -->  WEM  CONVERTER")
    print("    (Powered by Audiokinetic Wwise 2024)")
    print("=" * 50)

    check_wwise()
    print(f"\n  Project  : {WWISE_PROJECT}")
    print(f"  Preset   : {CONVERSION_PRESET}")
    print(f"  WEM out  : {WWISE_GEN_DIR}")

    # --- Step 1: Input folder ---
    while True:
        print("\n[STEP 1] Enter the folder path containing your WAV files:")
        input_path = input("  Path: ").strip().strip('"')

        if not os.path.exists(input_path):
            print("  ERROR: Path does not exist. Try again.")
            continue

        wav_files = find_wav_files(input_path)

        if not wav_files:
            print("  ERROR: No WAV files found in that folder.")
            continue

        print(f"\n  Found {len(wav_files)} WAV file(s):")
        for f in wav_files:
            print(f"    - {f.name}")
        break

    # --- Step 2: Output folder ---
    print("\n[STEP 2] Enter the folder path where WEM files will be saved:")
    output_path = input("  Path: ").strip().strip('"')
    os.makedirs(output_path, exist_ok=True)

    # --- Step 3: Confirm ---
    print(f"\n{'='*50}")
    print(f"  SUMMARY")
    print(f"{'='*50}")
    print(f"  Input folder  : {input_path}")
    print(f"  Output folder : {output_path}")
    print(f"  Files         : {len(wav_files)}")
    print(f"  Preset        : {CONVERSION_PRESET}")
    confirm = input("\n  Proceed? (y/n): ").strip().lower()

    if confirm != "y":
        print("\n  Cancelled.")
        sys.exit(0)

    # --- Step 4: Clear old WEMs ---
    print(f"\n  Clearing old WEMs from Wwise output folder...")
    clear_old_wems()

    # --- Step 5: Convert ---
    print(f"\n{'='*50}")
    print(f"  Converting {len(wav_files)} file(s)...")
    print(f"{'='*50}")

    with tempfile.TemporaryDirectory() as temp_dir:
        wsources_file = Path(temp_dir) / "sources.wsources"
        create_wsources(wsources_file, wav_files)

        returncode, log = run_conversion(wsources_file)
        print(f"\n  WwiseConsole output:")
        print(f"  {log[:1500]}")

    # --- Step 6: Collect and rename ---
    print(f"\n{'='*50}")
    print(f"  Collecting WEM files...")
    print(f"{'='*50}")
    success, failed = collect_and_rename_wems(wav_files, output_path)

    # --- Done ---
    print(f"\n{'='*50}")
    print(f"  DONE!")
    print(f"  Successfully converted : {success} file(s)")
    if failed:
        print(f"  Failed                 : {failed} file(s)")
    print(f"  Saved to               : {output_path}")
    print(f"  Original files kept    : YES")
    print(f"{'='*50}")
    input("\n  Press Enter to exit...")

if __name__ == "__main__":
    main()
