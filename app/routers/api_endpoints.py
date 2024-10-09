from fastapi import APIRouter, Body
from app.schemas.hint_request import HintRequest
from app.handlers.identify_error import identify_error_handler
from app.handlers.hint_generator.hint_generator_factory import hint_generator_factory

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

    # Identify the error
    error_name = identify_error_handler(error_message=error, code=code)

    # Generate the hint based on the error
    hint_generator = hint_generator_factory(error_name=error_name, code=code, error=error)
    hint = hint_generator.generate_hint()

    return {"hint_text": hint}
