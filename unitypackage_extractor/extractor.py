import tarsafe
import tempfile
import sys
import os
import time
import shutil
import re
from pathlib import Path


global totalloggers
totalloggers = 0
def extractPackage(packagePath, outputPath=None, encoding='utf-8'):
  """
  Extracts a .unitypackage into the current directory
  @param {string} packagePath The path to the .unitypackage
  @param {string} [outputPath=os.getcwd()] Optional output path, otherwise will use cwd
  """
  #totalloggers = 0
  if not outputPath:
    outputPath = os.getcwd() # If not explicitly set, WindowsPath("") has no parents, and causes the escape test to fail

  with tempfile.TemporaryDirectory() as tmpDir:
    # Unpack the whole thing in one go (faster than traversing the tar)
    with tarsafe.open(name=packagePath, encoding=encoding) as upkg:
      upkg.extractall(tmpDir)

    # Extract each file in tmpDir to final destination
    for dirEntry in os.scandir(tmpDir):
      assetEntryDir = f"{tmpDir}/{dirEntry.name}"
      if not os.path.exists(f"{assetEntryDir}/pathname") or \
          not os.path.exists(f"{assetEntryDir}/asset"):
        continue #Doesn't have the required files to extract it

      # Has the required info to extract
      # Get the path to output to from /pathname
      with open(f"{assetEntryDir}/pathname", encoding=encoding) as f:
        pathname = f.readline()
        pathname = pathname[:-1] if pathname[-1] == '\n' else pathname #Remove newline
        pathname3 = pathname
        # Replace windows reserved chars with '_' that arent '/'
        if os.name == 'nt':
          pathname = re.sub(r'[\>\:\"\|\?\*]', '_', pathname)

      # Figure out final path, make sure that it's inside the write directory
      assetOutPath = os.path.join(outputPath, pathname)
      if Path(outputPath).resolve() not in Path(assetOutPath).resolve().parents:
        print(f"WARNING: Skipping '{dirEntry.name}' as '{assetOutPath}' is outside of '{outputPath}'.")
        continue

      #Extract to the pathname
      print(f"Extracting '{dirEntry.name}' as '{pathname}'")
      os.makedirs(os.path.dirname(assetOutPath), exist_ok=True) #Make the dirs up to the given folder
      shutil.move(f"{assetEntryDir}/asset", assetOutPath)

      


#check for tokenloggers
      
      flag4 = 0
      index4 = 0
      stringext = '.cs'
      file_extension = Path(pathname).suffix
      whattofind = 'discord'
      if stringext in file_extension:
        f6 = open(assetOutPath, "r")
        for line in f6:  
          index4 = index4 + 1 
      
            # checking string is present in line or not
          if whattofind in line:
        
            flag4 = 1
            break
        f6.close()
        
        if flag4 == 0: 
          print('file should be clean') 
        else: 
          print('there is a tokenlogger in this file' , 'Found In Line', index4)
          global totalloggers
          totalloggers = totalloggers + 1




#end of check for tokenloggers - tokenlogger checker made by TheMaskedMan00

def cli(args):
  """
  CLI entrypoint, takes CLI arguments array
  """
  if not args:
    raise TypeError("No .unitypackage path was given. \n\nUSAGE: unitypackage_extractor [XXX.unitypackage] (optional/output/path)")
  startTime = time.time()
  extractPackage(args[0], args[1] if len(args) > 1 else "")
  print("--- Finished in %s seconds ---" % (time.time() - startTime))
  print('--- There were a total of', totalloggers , 'Token loggers in your package ---')

if __name__ == "__main__":
  cli(sys.argv[1:])
