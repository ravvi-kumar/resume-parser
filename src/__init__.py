from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import time
from markitdown import MarkItDown
from openai import OpenAI
import tempfile
import os
from pypdf import PdfReader
from .schema import Response

app = FastAPI()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
md = MarkItDown()

class Resume(BaseModel):
    name: str
    skills: list[str]

def extract_markdown_from_pdf(pdf_file: UploadFile) -> str:
    """Extract markdown content from a PDF file."""
    try:
        if pdf_file.filename.split(".")[-1] != "pdf":
            raise HTTPException(status_code=400, detail="Invalid PDF file. Please upload a PDF file.")
        start_time = time.time()

        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file.file.read())
            temp_file_path = temp_file.name

        # Convert the PDF to markdown using the file path
        result = md.convert(temp_file_path)

        # Debugging: Check if the result is None
        if result is None:
            raise ValueError("md.convert() returned None. Check the PDF file and MarkItDown library.")

        # Ensure the result has a `text_content` attribute
        if not hasattr(result, "text_content"):
            raise ValueError("The result object does not have a 'text_content' attribute.")

        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken for markdown extraction: {elapsed_time:.2f} seconds")

        # Clean up the temporary file
        os.unlink(temp_file_path)

        return result.text_content, elapsed_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

def extract_text_from_pdf(pdf_file: UploadFile) -> str:
    """Extract text content from a PDF file."""
    try:
        if pdf_file.filename.split(".")[-1]!= "pdf":
            raise HTTPException(status_code=400, detail="Invalid PDF file. Please upload a PDF file.")
        start_time = time.time()
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(pdf_file.file.read())
            temp_file_path = temp_file.name
        # Open the PDF file
        with open(temp_file_path, "rb") as file:
            pdf_reader = PdfReader(file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text()
        # Clean up the temporary file
        os.unlink(temp_file_path)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time taken for text extraction: {elapsed_time:.2f} seconds")
        return text_content, elapsed_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

def get_structured_output_from_markdown(content: str) -> Response:
    """Get structured output from markdown content using OpenAI."""
    try:
        start_time = time.time()
        llm_response = client.beta.chat.completions.parse(
            # model="gpt-4o-2024-08-06",
            model="gpt-4o-mini-2024-07-18",
            messages=[{"role": "user", "content": content}],
            response_format=Response,
        )
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"OpenAI Time taken for structured output: {elapsed_time:.2f} seconds")
        print(llm_response.choices[0].message.parsed)
        return llm_response.choices[0].message.parsed, elapsed_time
        # return Resume.model_validate_json(llm_response.choices[0].message.parsed), elapsed_time
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating structured output: {str(e)}")

class ResumeResponse(BaseModel):
    name: str
    skills: list[str]
    total_time_taken: float

@app.post("/resume")
async def extract_resume(pdf_file: UploadFile = File(...)):
    """API endpoint to extract structured resume data from a PDF."""
    try:
        # Step 1: Extract markdown content from the PDF
        # markdown_content, markdown_time = extract_markdown_from_pdf(pdf_file)
        markdown_content, markdown_time = extract_text_from_pdf(pdf_file)

        # Step 2: Get structured output from the markdown content
        structured_output, openai_time = get_structured_output_from_markdown(markdown_content)

        # Step 3: Calculate total time taken
        total_time = markdown_time + openai_time

        # Step 4: Return the structured output with total time
        return {
            "data": structured_output.model_dump(),
            # "name": structured_output.name,
            # "skills": structured_output.skills,
            "total_time_taken": total_time,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run the FastAPI app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)