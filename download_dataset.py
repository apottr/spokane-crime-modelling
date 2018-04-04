from zipfile import ZipFile
from pathlib import Path
from io import BytesIO
import requests


data_dir = Path(__file__).parent.resolve() / "data" #pylint: disable=no-member

files = [
    {"filename": "Crime_2014", "url": "https://opendata.arcgis.com/datasets/ae670ed69125469ca86d5648a86423f0_0.zip?outSR=%7B%22wkt%22%3A%22PROJCS%5B%5C%22NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet%5C%22%2CGEOGCS%5B%5C%22GCS_North_American_1983_HARN%5C%22%2CDATUM%5B%5C%22D_North_American_1983_HARN%5C%22%2CSPHEROID%5B%5C%22GRS_1980%5C%22%2C6378137.0%2C298.257222101%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Lambert_Conformal_Conic%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C1640416.666666667%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-120.8333333333333%5D%2CPARAMETER%5B%5C%22Standard_Parallel_1%5C%22%2C47.5%5D%2CPARAMETER%5B%5C%22Standard_Parallel_2%5C%22%2C48.73333333333333%5D%2CPARAMETER%5B%5C%22Latitude_Of_Origin%5C%22%2C47.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%2CVERTCS%5B%5C%22NAVD_1988%5C%22%2CVDATUM%5B%5C%22North_American_Vertical_Datum_1988%5C%22%5D%2CPARAMETER%5B%5C%22Vertical_Shift%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Direction%5C%22%2C1.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%22%7D"},
    {"filename": "Crime_2013", "url": "https://opendata.arcgis.com/datasets/9980849b2b8c4cdda41207db2b0381ea_0.zip?outSR=%7B%22wkt%22%3A%22PROJCS%5B%5C%22NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet%5C%22%2CGEOGCS%5B%5C%22GCS_North_American_1983_HARN%5C%22%2CDATUM%5B%5C%22D_North_American_1983_HARN%5C%22%2CSPHEROID%5B%5C%22GRS_1980%5C%22%2C6378137.0%2C298.257222101%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Lambert_Conformal_Conic%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C1640416.666666667%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-120.8333333333333%5D%2CPARAMETER%5B%5C%22Standard_Parallel_1%5C%22%2C47.5%5D%2CPARAMETER%5B%5C%22Standard_Parallel_2%5C%22%2C48.73333333333333%5D%2CPARAMETER%5B%5C%22Latitude_Of_Origin%5C%22%2C47.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%2CVERTCS%5B%5C%22NAVD_1988%5C%22%2CVDATUM%5B%5C%22North_American_Vertical_Datum_1988%5C%22%5D%2CPARAMETER%5B%5C%22Vertical_Shift%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Direction%5C%22%2C1.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%22%7D"},
    {"filename": "Crime_2015", "url": "https://opendata.arcgis.com/datasets/eb2cc2e4750344099db2df8db0a896c7_0.zip?outSR=%7B%22wkt%22%3A%22PROJCS%5B%5C%22NAD_1983_HARN_StatePlane_Washington_North_FIPS_4601_Feet%5C%22%2CGEOGCS%5B%5C%22GCS_North_American_1983_HARN%5C%22%2CDATUM%5B%5C%22D_North_American_1983_HARN%5C%22%2CSPHEROID%5B%5C%22GRS_1980%5C%22%2C6378137.0%2C298.257222101%5D%5D%2CPRIMEM%5B%5C%22Greenwich%5C%22%2C0.0%5D%2CUNIT%5B%5C%22Degree%5C%22%2C0.0174532925199433%5D%5D%2CPROJECTION%5B%5C%22Lambert_Conformal_Conic%5C%22%5D%2CPARAMETER%5B%5C%22False_Easting%5C%22%2C1640416.666666667%5D%2CPARAMETER%5B%5C%22False_Northing%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Central_Meridian%5C%22%2C-120.8333333333333%5D%2CPARAMETER%5B%5C%22Standard_Parallel_1%5C%22%2C47.5%5D%2CPARAMETER%5B%5C%22Standard_Parallel_2%5C%22%2C48.73333333333333%5D%2CPARAMETER%5B%5C%22Latitude_Of_Origin%5C%22%2C47.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%2CVERTCS%5B%5C%22NAVD_1988%5C%22%2CVDATUM%5B%5C%22North_American_Vertical_Datum_1988%5C%22%5D%2CPARAMETER%5B%5C%22Vertical_Shift%5C%22%2C0.0%5D%2CPARAMETER%5B%5C%22Direction%5C%22%2C1.0%5D%2CUNIT%5B%5C%22Foot_US%5C%22%2C0.3048006096012192%5D%5D%22%7D"}
]

def get_file(fobj):
    r = requests.get(fobj["url"])
    with ZipFile(BytesIO(r.content)) as zf:
        zf.extractall(path=str(data_dir))
    print("extracted",fobj["filename"])


def exec_dl():
    data_dir.mkdir(exist_ok=True) #pylint:disable=no-member
    if len(list(data_dir.iterdir())) == 0: #pylint:disable=no-member
        for f in files:
            print("getting",f["filename"])
            get_file(f)
    else:
        print("files already exist")

if __name__ == "__main__":
    exec_dl()
