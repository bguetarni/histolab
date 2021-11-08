# flake8: noqa

# in legacy datasets we need to put our sample data within the data dir
legacy_datasets = ["cmu_small_region.svs"]

# Registry of datafiles that can be downloaded along with their SHA256 hashes
# To generate the SHA256 hash, use the command
# openssl sha256 filename
registry = {
    "histolab/broken.svs": "b1325916876afa17ad5e02d2e7298ee883e758ed25369470d85bc0990e928e11",
    "histolab/kidney.png": "5c6dc1b9ae10a2865302d9c8eda360362ec47732cb3e9766c38ed90cb9f4c371",
    "data/cmu_small_region.svs": "ed92d5a9f2e86df67640d6f92ce3e231419ce127131697fbbce42ad5e002c8a7",
    "aperio/JP2K-33003-1.svs": "6205ccf75a8fa6c32df7c5c04b7377398971a490fb6b320d50d91f7ba6a0e6fd",
    "aperio/JP2K-33003-2.svs": "1a13cef86b55b51127cebd94a1f6069f7de494c98e3e708640d1ce7181d9e3fd",
    "tcga/breast/TCGA-A8-A082-01A-01-TS1.3cad4a77-47a6-4658-becf-d8cffa161d3a.svs": "e955f47b83c8a5ae382ff8559493548f90f85c17c86315dd03134c041f44df70",
    "tcga/breast/TCGA-A1-A0SH-01Z-00-DX1.90E71B08-E1D9-4FC2-85AC-062E56DDF17C.svs": "6de90fe92400e592839ab7f87c15d9924bc539c61ee3b3bc8ef044f98d16031b",
    "tcga/breast/31e248bf-ee24-4d18-bccb-47046fccb461": "95163831d9076bb5e5b21790933dee9535a3607ba35bd6ae425374a45ecb1ba6",
    "tcga/prostate/6b725022-f1d5-4672-8c6c-de8140345210": "305c80e28227b25fdd0cc24726da4cf038380b4326e25c6518ffe23051a25ac0",
    "tcga/ovarian/b777ec99-2811-4aa4-9568-13f68e380c86": "f8e5059a0c9f8c026cfb2613cddef6562f8cdbd5954580282e2afa41d2f86a8c",
    "9798433/?format=tif": "7db49ff9fc3f6022ae334cf019e94ef4450f7d4cf0d71783e0f6ea82965d3a52",
    "9798554/?format=tif": "8a4318ac713b4cf50c3314760da41ab7653e10e90531ecd0c787f1386857a4ef",
}

APERIO_REPO_URL = "http://openslide.cs.cmu.edu/download/openslide-testdata/Aperio"
TCGA_REPO_URL = "https://api.gdc.cancer.gov/data"
IDR_REPO_URL = "https://idr.openmicroscopy.org/webclient/render_image_download"

registry_urls = {
    "histolab/broken.svs": "https://raw.githubusercontent.com/histolab/histolab/master/tests/fixtures/svs-images/broken.svs",
    "histolab/kidney.png": "https://user-images.githubusercontent.com/4196091/100275351-132cc880-2f60-11eb-8cc8-7a3bf3723260.png",
    "aperio/JP2K-33003-1.svs": f"{APERIO_REPO_URL}/JP2K-33003-1.svs",
    "aperio/JP2K-33003-2.svs": f"{APERIO_REPO_URL}/JP2K-33003-2.svs",
    "tcga/breast/TCGA-A8-A082-01A-01-TS1.3cad4a77-47a6-4658-becf-d8cffa161d3a.svs": f"{TCGA_REPO_URL}/ad9ed74a-2725-49e6-bf7a-ef100e299989",
    "tcga/breast/TCGA-A1-A0SH-01Z-00-DX1.90E71B08-E1D9-4FC2-85AC-062E56DDF17C.svs": f"{TCGA_REPO_URL}/3845b8bd-cbe0-49cf-a418-a8120f6c23db",
    "tcga/breast/31e248bf-ee24-4d18-bccb-47046fccb461": f"{TCGA_REPO_URL}/31e248bf-ee24-4d18-bccb-47046fccb461",
    "tcga/prostate/6b725022-f1d5-4672-8c6c-de8140345210": f"{TCGA_REPO_URL}/6b725022-f1d5-4672-8c6c-de8140345210",
    "tcga/ovarian/b777ec99-2811-4aa4-9568-13f68e380c86": f"{TCGA_REPO_URL}/b777ec99-2811-4aa4-9568-13f68e380c86",
    "9798433/?format=tif": f"{IDR_REPO_URL}/9798433/?format=tif",
    "9798554/?format=tif": f"{IDR_REPO_URL}/9798554/?format=tif",
}

legacy_registry = {
    ("data/" + filename): registry["data/" + filename] for filename in legacy_datasets
}