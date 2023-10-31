import httpx


async def upload_pdf_to_pdfco():
    api_key = "YOUR_API_KEY"  # Replace with your PDF.co API key
    url = "https://api.pdf.co/v1/file/upload"

    headers = {
        "x-api-key": api_key,
    }

    # Replace 'yourfile.pdf' with the actual path to your PDF file
    files = {'file': ('yourfile.pdf', open('yourfile.pdf', 'rb'))}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, files=files)

        if response.status_code == 200:
            json_response = response.json()
            if json_response["error"] == False:
                print("PDF upload successful!")
                print(f"File ID: {json_response['body']['fileId']}")
            else:
                print(f"PDF upload failed: {json_response['message']}")
        else:
            print(f"PDF upload failed with status code: {response.status_code}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(upload_pdf_to_pdfco())
