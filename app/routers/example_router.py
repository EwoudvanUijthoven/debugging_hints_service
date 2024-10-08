from fastapi import APIRouter, Body
from app.schemas.hint_request import HintRequest

router = APIRouter()


# Just a test endpoint to see how error handling works in FastAPI and if we can return custom error messages and
# display them in the frontend
@router.get("/debugging_hints/{error_id}")
def debugging_hints(error_id: int):
    if error_id == 1:
        hint = "There was a division by zero. Please check your code."
        return {"hint_text": hint}
    else:
        raise NotImplementedError("This error_id is not implemented.")


# This endpoint will be used by the frontend to generate a debugging hint a random error
@router.post("/get_debugging_hint")
def get_debugging_hint(hint_request: HintRequest):
    # Extract data from the request for processing if needed
    code = hint_request.code
    output = hint_request.output
    error = hint_request.error

    # Generate the hint based on the input (example logic)
    hint = f"Received code: {code}. Output: {output}. Error: {error}"
    return {"hint_text": hint}
