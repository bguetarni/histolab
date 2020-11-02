import argparse
import os
from typing import List, Tuple

import pandas as pd
import requests
from histolab.slide import SlideSet
from histolab.tiler import RandomTiler
from tqdm import tqdm
import numpy as np
import time
from sklearn.model_selection import train_test_split

URL_ROOT = "https://brd.nci.nih.gov/brd/imagedownload"


def download_wsi_gtex(dataset_dir: str, sample_ids: List[str]) -> None:
    """Download into ``dataset_dir`` all the GTEx WSIs corresponding to ``sample_ids``

    Parameters
    ----------
    dataset_dir : str
        Path where to save the WSIs
    sample_ids : List[str]
        List of GTEx WSI ids
    """
    for sample_id in tqdm(sample_ids):
        if f"{sample_id}.svs" not in os.listdir(dataset_dir):

            r = requests.get(f"{URL_ROOT}/{sample_id}")
            with open(
                os.path.join(dataset_dir, f"{sample_id}.svs"), "wb"
            ) as output_file:
                output_file.write(r.content)

            time.sleep(np.random.randint(60, 100))


def extract_random_tiles(
    dataset_dir: str,
    processed_path: str,
    tile_size: Tuple[int, int],
    n_tiles: int,
    level: int,
    seed: int,
    check_tissue: bool,
) -> None:
    """Save random tiles extracted from WSIs in `dataset_dir` into `processed_path`/tiles

    Parameters
    ----------
    dataset_dir : str
        Path were the WSIs are saved
    processed_path : str
        Path where to store the tiles (will be concatenated with /tiles)
    tile_size : Tuple[int, int]
        width and height of the cropped tiles
    n_tiles : int
        Maximum number of tiles to extract
    level : int
        Magnification level from which extract the tiles
    seed : int
        Seed for RandomState
    check_tissue : bool
        Whether to check if the tile has enough tissue to be saved
    """
    slideset = SlideSet(dataset_dir, processed_path, valid_extensions=[".svs"])

    for slide in tqdm(slideset.slides):
        prefix = f"{slide.name}_"

        random_tiles_extractor = RandomTiler(
            tile_size=tile_size,
            n_tiles=n_tiles,
            level=level,
            seed=seed,
            check_tissue=check_tissue,
            prefix=prefix,
        )

        random_tiles_extractor.extract(slide)


def train_test_df_patient_wise(
    dataset_df: pd.DataFrame,
    patient_col: str,
    label_col: str,
    test_size: float = 0.2,
    seed: int = 1234,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split ``dataset_df`` into train/test partitions following a patient-wise protocol.

    Parameters
    ----------
    dataset_df : pd.DataFrame
        DataFrame containing the data to split
    patient_col : str
        Name of the patient column in ``dataset_df``
    label_col : str
        Name of the target column in ``dataset_df``
    test_size : float, optional
        Ratio of test set samples over the entire dataset, by default 0.2
    seed : int, optional
        Seed for RandomState, by default 1234

    Returns
    -------
    pd.DataFrame
        Training dataset
    pd.DataFrame
        Test dataset
    """

    patient_with_labels = (
        dataset_df.groupby(patient_col)[label_col].unique().apply(list)
    )
    unique_patients = patient_with_labels.index.values

    train_patients, test_patients = train_test_split(
        unique_patients, test_size=test_size, random_state=seed
    )

    dataset_train_df = dataset_df.loc[dataset_df[patient_col].isin(train_patients)]
    dataset_test_df = dataset_df.loc[dataset_df[patient_col].isin(test_patients)]

    return dataset_train_df, dataset_test_df


def split_tiles_patient_wise(
    tiles_dir: str,
    metadata_df: pd.DataFrame,
    train_csv_path: str,
    test_csv_path: str,
    label_col: str,
    patient_col: str,
    test_size: float = 0.2,
    seed: int = 1234,
) -> None:
    """Split a tile dataset into train-test following a patient-wise partitioning protocol.

    Save two CSV files containing the train-test partition for the tile dataset.

    Parameters
    ----------
    tiles_dir : str
        Tile dataset directory.
    metadata_df : pd.DataFrame
        CSV of patient metadata.
    train_csv_path : str
        Path where to save the CSV file for the training set.
    test_csv_path : str
        Path where to save the CSV file for the test set.
    label_col : str
        Name of the target column in ``dataset_df``
    patient_col : str
        Name of the patient column in ``dataset_df``
    test_size : float, optional
        Ratio of test set samples over the entire dataset, by default 0.2
    seed : int, optional
        Seed for RandomState, by default 1234
    """
    tiles_filenames = [
        f for f in os.listdir(tiles_dir) if os.path.splitext(f)[1] == ".png"
    ]
    tiles_filenames_df = pd.DataFrame(
        {
            "tile_filename": tiles_filenames,
            "Tissue Sample ID": [f.split("_")[0] for f in tiles_filenames],
        }
    )

    tiles_metadata = metadata_df.join(
        tiles_filenames_df.set_index("Tissue Sample ID"), on="Tissue Sample ID"
    )

    train_df, test_df = train_test_df_patient_wise(
        tiles_metadata, patient_col, label_col, test_size, seed,
    )

    train_df.to_csv(train_csv_path, index=None)
    test_df.to_csv(test_csv_path, index=None)


def main():
    parser = argparse.ArgumentParser(
        description="Retrieve a leakage-free dataset of tiles using a collection of WSI"
        "from the GTEx repository. The WSIs that will be used for tile extraction are "
        "specified in the 'metadata_csv'. First, slides are downloaded from the GTEx "
        "portal. Then, tiles are randomly cropped from each WSI and saved only if they "
        "consist of, at least, 80% of tissue. Finally, tiles are sorted ...."
    )
    parser.add_argument(
        "--metadata_csv",
        type=str,
        default="examples/GTEx_AIDP2021.csv",
        help="CSV with WSI metadata",
    )
    parser.add_argument(
        "--wsi_dataset_dir",
        type=str,
        default="WSI_GTEx",
        help="Path where to save the WSIs",
    )
    parser.add_argument(
        "--tile_dataset_dir",
        type=str,
        default="tiles_GTEx",
        help="Path where to save the WSIs",
    )
    parser.add_argument(
        "--tile_size",
        type=int,
        nargs=2,
        default=(512, 512),
        help="width and height of the cropped tiles",
    )
    parser.add_argument(
        "--n_tiles", type=int, default=100, help="Maximum number of tiles to extract"
    )
    parser.add_argument(
        "--level",
        type=int,
        default=2,
        help="Magnification level from which extract the tiles",
    )
    parser.add_argument(
        "--seed", type=int, default=7, help="Seed for RandomState",
    )
    parser.add_argument(
        "--check_tissue",
        type=bool,
        default=True,
        help="Whether to check if the tile has enough tissue to be saved",
    )
    args = parser.parse_args()

    metadata_csv = args.metadata_csv
    wsi_dataset_dir = args.wsi_dataset_dir
    tile_dataset_dir = args.tile_dataset_dir
    tile_size = args.tile_size
    n_tiles = args.n_tiles
    level = args.level
    seed = args.seed
    check_tissue = args.check_tissue

    gtex_df = pd.read_csv(metadata_csv)
    os.makedirs(wsi_dataset_dir)

    sample_ids = gtex_df["Tissue Sample ID"].tolist()

    download_wsi_gtex(wsi_dataset_dir, sample_ids)

    extract_random_tiles(
        wsi_dataset_dir, tile_dataset_dir, tile_size, n_tiles, level, seed, check_tissue
    )

    split_tiles_patient_wise(
        tiles_dir=os.path.join(tile_dataset_dir, "tiles"),
        metadata_df=gtex_df,
        train_csv_path=os.path.join(
            tile_dataset_dir, f"train_tiles_PW_{os.path.basename(metadata_csv)}"
        ),
        test_csv_path=os.path.join(
            tile_dataset_dir, f"test_tiles_PW_{os.path.basename(metadata_csv)}"
        ),
        label_col="Tissue",
        patient_col="Subject ID",
        test_size=0.2,
        seed=1234,
    )


if __name__ == "__main__":
    main()
