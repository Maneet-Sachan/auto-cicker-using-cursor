import PyInstaller.__main__
import os
import shutil
from PIL import Image
import tempfile

def create_icon(icon_path):
    # Create a simple icon if it doesn't exist
    if not os.path.exists(icon_path):
        # Create a 32x32 image with a mouse cursor
        img = Image.new('RGB', (32, 32), color='white')
        # Draw a simple mouse cursor
        pixels = img.load()
        for i in range(32):
            for j in range(32):
                if i < 16 and j < 16 and i + j < 16:
                    pixels[i, j] = (0, 0, 0)
        img.save(icon_path)

# Create a temporary directory for building
temp_dir = tempfile.mkdtemp()
os.chdir(temp_dir)

# Define paths
original_dir = os.path.dirname(__file__)
icon_path = os.path.join(original_dir, "clicker_icon.ico")
temp_icon_path = os.path.join(temp_dir, "clicker_icon.ico")
script_path = os.path.join(original_dir, "auto_clicker_gui.py")
temp_script_path = os.path.join(temp_dir, "auto_clicker_gui.py")

# Create icon in original directory
create_icon(icon_path)

# Copy necessary files to temp directory
shutil.copy(script_path, temp_script_path)
shutil.copy(icon_path, temp_icon_path)

# Build the executable
PyInstaller.__main__.run([
    'auto_clicker_gui.py',
    '--onefile',
    '--windowed',
    '--name=AutoClicker',
    '--icon=clicker_icon.ico',
    '--add-data=clicker_icon.ico;.',
    '--clean',
    '--noconfirm',
    '--distpath=' + os.path.join(original_dir, 'dist')
])

# Clean up temp directory
shutil.rmtree(temp_dir)

print("\nBuild completed! Your executable is in the 'dist' folder.")
print("You can find AutoClicker.exe in:", os.path.join(original_dir, 'dist')) 