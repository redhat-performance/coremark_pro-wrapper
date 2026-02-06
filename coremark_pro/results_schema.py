import pydantic
import datetime

from enum import Enum

class testname(Enum):
    cjpeg-rose7-preset = "cjpeg-rose7-preset"
    core = "core"
    linear_alg-mid-100x100-sp = "linear_alg-mid-100x100-sp"
    loops-all-mid-10k-sp = "loops-all-mid-10k-sp"
    nnet_test = "nnet_test"
    parser-125k = "parser-125k"
    radix2-big-64k = "radix2-big-64k"
    sha-test = "sha-test"
    zip-test = "zip-test"
    Score = "Score"

class Coremark_pro_Results(pydantic.BaseModel):
    Test: testname
    Multi_iterations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Single_iterations: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Scaling: float = pydantic.Field(gt=0, allow_inf_nan=False)
    Start_Date: datetime.datetime
    End_Date: datetime.datetime
