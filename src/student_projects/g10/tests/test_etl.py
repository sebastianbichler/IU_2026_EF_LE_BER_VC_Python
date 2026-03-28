from foxpost.etl import run_pipeline
from pathlib import Path

def test_pipeline(tmp_path):

    input_file = Path("data/sample_parcels.csv")
    output = tmp_path / "out"

    run_pipeline(str(input_file), str(output))

    assert output.exists()