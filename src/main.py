# Import FastAPI and HTTPException for API creation and error handling
from fastapi import FastAPI, HTTPException
# Import httpx for making async HTTP requests
import httpx

# Create FastAPI app instance
app = FastAPI()

# GitHub API endpoint template for fetching user gists
GITHUB_API_URL = "https://api.github.com/users/{username}/gists"

# Define endpoint to get public gists for a given username
@app.get("/{username}")
async def get_gists(username: str):
    try:
        # Create an async HTTP client
        async with httpx.AsyncClient() as client:
            # Make a GET request to the GitHub API
            response = await client.get(GITHUB_API_URL.format(username=username))
            # If the response is not successful, raise a 404 error
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="User not found or GitHub API error.")
            try:
                # Parse the JSON response
                gists = response.json()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Error parsing response: {str(e)}")
            # Return a simplified list of gists with id, description, and URL
            return [{
                "id": gist.get("id"),
                "description": gist.get("description"),
                "url": gist.get("html_url")
            } for gist in gists]
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
