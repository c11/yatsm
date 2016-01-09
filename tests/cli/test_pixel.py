""" Test ``yatsm line``
"""
import os

from click.testing import CliRunner
import matplotlib as mpl
import matplotlib.cm  # noqa
import pytest

from yatsm.cli.main import cli
import yatsm.cli.pixel

mpl_skip = pytest.mark.skipif(
    mpl.get_backend() != 'agg' and "DISPLAY" not in os.environ,
    reason='Requires either matplotlib "agg" backend or that DISPLAY" is set')


@mpl_skip
def test_cli_pixel_pass_1(example_timeseries):
    """ Correctly run for one pixel
    """
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['-v', 'pixel',
         '--band', '5',
         '--plot', 'TS',
         '--style', 'ggplot',
         example_timeseries['config'], '1', '1'
         ])
    assert result.exit_code == 0


@mpl_skip
def test_cli_pixel_pass_2(example_timeseries):
    """ Correctly run for one pixel for 3 plots
    """
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['-v', 'pixel',
         '--band', '5',
         '--plot', 'TS', '--plot', 'DOY', '--plot', 'VAL',
         '--style', 'ggplot',
         example_timeseries['config'], '1', '1'
         ])
    assert result.exit_code == 0


@mpl_skip
def test_cli_pixel_pass_3(example_timeseries, monkeypatch):
    """ Correctly run for one pixel when default colormap isn't available
    """
    cmap_d = mpl.cm.cmap_d.copy()
    cmap_d.pop(yatsm.cli.pixel._DEFAULT_PLOT_CMAP, None)
    monkeypatch.setattr('matplotlib.cm.cmap_d', cmap_d)
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['-v', 'pixel',
         '--band', '5',
         '--plot', 'TS', '--plot', 'DOY', '--plot', 'VAL',
         '--style', 'ggplot',
         example_timeseries['config'], '1', '1'
         ])
    assert result.exit_code == 0


# FAILURES
@mpl_skip
def test_cli_pixel_fail_1(example_timeseries):
    """ Fail because of non-existent colormap
    """
    runner = CliRunner()
    result = runner.invoke(
        cli,
        ['-v', 'pixel',
         '--band', '5',
         '--plot', 'TS',
         '--style', 'ggplot', '--cmap', 'NOT_A_COLORMAP_I_HOPE',
         example_timeseries['config'], '1', '1'
         ])
    assert result.exit_code == 1
    assert 'Cannot find specified colormap' in result.output
