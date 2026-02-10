import pydantic
import datetime

from enum import Enum

class testname(Enum):
    cjpeg_rose7_preset = "cjpeg-rose7-preset"
    core = "core"
    linear_alg_mid_100x100_sp = "linear_alg-mid-100x100-sp"
    loops_all_mid_10k_sp = "loops-all-mid-10k-sp"
    nnet_test = "nnet_test"
    parser_125k = "parser-125k"
    radix2_big_64k = "radix2-big-64k"
    sha_test = "sha-test"
    zip_test = "zip-test"
    Score = "Score"

class Coremark_Pro_Results(pydantic.BaseModel):
    Test: testname
    Multi_iterations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Single_iterations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Scaling: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Start_Date: datetime.datetime
    End_Date: datetime.datetime
