import os
from zipfile import ZipFile
import json

def get_provenance_graph(entity_iri:str, data_root:str) -> dict:
    """
    Uses the entity's IRI (i.e. its OMID) and finds the exact 
    path of the file storing its provenance graph in a subdirectory of data_root. 
    Then, it reads the file and returns the provenance graph as a dictionary.
    
    param entity_iri: The IRI of the entity whose provenance graph is to be retrieved.
    param data_root: The path to the root directory storing the provenance data, i.e. the folder resulting from decompression of a .tar.gz file.
    return: The provenance graph of the entity as a dictionary.
    """
    digits = entity_iri.split('/')[-1] 
    supplier_prefix = digits[:digits.find('0', 1)+1]
    sequential_number = int(digits.removeprefix(supplier_prefix))
    for dir in os.listdir(data_root):
        if dir == supplier_prefix:
            dir1_path = os.path.join(data_root, dir)
            for subdir in sorted(os.listdir(dir1_path), key=lambda x: int(x)):
                if sequential_number < int(subdir):
                    dir2_path = os.path.join(dir1_path, subdir)
                    for subsubdir in sorted([d for d in os.listdir(dir2_path) if d.isdigit()], key=lambda x: int(x)):
                        if sequential_number < int(subsubdir):
                            dir3_path = os.path.join(dir2_path, subsubdir)
                            prov_dir_path = os.path.join(dir3_path, 'prov')
                            with ZipFile(os.path.join(prov_dir_path, 'se.zip')) as archive:
                                with archive.open('se.json') as f:
                                    data: list = json.load(f)
                                    for obj in data:
                                        if obj['@id'] == entity_iri + '/prov/':
                                            return obj
                            break
                    break
    return None