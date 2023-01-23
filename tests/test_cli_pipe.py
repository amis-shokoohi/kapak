from pathlib import Path

from kapak.cli.pipe import Pipe


def test_pipe_filein_fileout(tmp_path: Path):
    temp_filein = Path(tmp_path, "temp_filein")
    temp_fileout = Path(tmp_path, "temp_fileout")

    expect = b"rYDaPST0EqAFMe0B"
    temp_filein.write_bytes(expect)

    with Pipe(temp_filein, temp_fileout) as pipe:
        assert pipe.src_is_file is True
        assert pipe.dst_is_file is True

        pipe.dst.write(pipe.src.read())

    assert temp_fileout.read_bytes() == expect
