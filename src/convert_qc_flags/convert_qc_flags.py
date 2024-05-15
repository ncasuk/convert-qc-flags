from netCDF4 import Dataset
import numpy as np


def convert_flag_values(var, verbose=False):
    """
    Convert flag values from string to list of values of correct type
    """
    init_values = var.getncattr("flag_values")
    if isinstance(init_values, str):
        value_list = [ i.rstrip("b") for i in init_values.split(",") ]
        var_type = var.dtype
        value_array = np.array(value_list, dtype=var_type)
        var.setncattr("flag_values", value_array)
        if verbose:
            print(f"[SUCCESS] Edited flag_values for variable {var.name}")


def convert_flag_meanings(var, verbose=False):
    """
    Change separation on flag meanings.
    """
    init_meanings = var.getncattr("flag_meanings")
    number_values = len(var.getncattr("flag_values"))
    if len(init_meanings.split(" ")) != number_values:
        curr_sep = init_meanings.split("good_data")[0].split("not_used")[1]
        split_meanings = init_meanings.split(curr_sep)
        if len(split_meanings) == number_values:
            meanings = " ".join(split_meanings)
            var.setncattr("flag_meanings", meanings)
            if verbose:
                print(f"[SUCCESS] Edited flag_meanings for variable {var.name}")
        else:
            print(f"[ERROR] Unable to convert flag_meanings for variable {var.name}")


def convert_qc_flag_attributes(ncfile, verbose=False):
    """
    Check all QC flag variables in netCDF file and rewrite attributes where necessary
    """
    nc = Dataset(ncfile, "a")
    for var in nc.variables.keys():
        if var.startswith("qc_flag"):
            if verbose:
                print(f"[INFO] Found QC Flag variable {var}")
            convert_flag_values(nc.variables[var], verbose=verbose)
            convert_flag_meanings(nc.variables[var], verbose=verbose)
    nc.close()

