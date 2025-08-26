import pydantic
class CoremarkProResults(pydantic.BaseModel):
        Test: str = pydantic.Field(description="Test running")
        Multi_iterations: float = pydantic.Field(description="Number of multiple iterations done.", allow_inf_nan=False, gt=0, validation_alias="Multi iterations")
        Single_Iterations: float = pydantic.Field(description="Number of test passes", allow_inf_nan=False, gt=0, validation_alias="Single Iterations")
        Scaling: float = pydantic.Field(description="Scaling Factor", allow_inf_nan=False, gt=0)
