"""Package only maintained lab source files, excluding caches and local outputs."""
from pathlib import Path
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED
root=Path(__file__).resolve().parents[1]
source=root/'examples/canteen-starter'
with ZipFile(root/'downloads/canteen-starter.zip','w',ZIP_DEFLATED) as archive:
    for path in sorted(source.iterdir()):
        if path.suffix not in {'.py','.sql','.csv','.md'}: continue
        entry=ZipInfo('canteen-starter/'+path.name,date_time=(2026,11,13,0,0,0))
        entry.compress_type=ZIP_DEFLATED
        archive.writestr(entry,path.read_bytes())
print('Packaged canteen-starter.zip')
