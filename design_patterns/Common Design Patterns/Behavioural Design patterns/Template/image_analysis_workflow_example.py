"""
Image Analysis Workflow Example (Template Method Pattern)
"""

from abc import ABC, abstractmethod
import asyncio

class ImageAnalysisWorkflow(ABC):
    """Base class defining the image analysis workflow (Template Method Pattern)"""

    async def process(self, image, extra_data):
        meta = await self.receive_image(image, extra_data)
        s3_url = await self.upload_dms(meta)
        ai_result = await self.analyse_with_ai(s3_url, meta)
        response = await self.formulate_response(ai_result)
        return response

    async def receive_image(self, image, extra_data):
        print("Receiving image and extra data...")
        # Simulate extracting metadata
        meta = {"filename": image, "extra": extra_data}
        return meta

    async def upload_dms(self, meta):
        print(f"Uploading {meta['filename']} to S3...")
        # Simulate S3 upload
        s3_url = f"https://s3.amazonaws.com/bucket/{meta['filename']}"
        return s3_url

    @abstractmethod
    async def analyse_with_ai(self, s3_url, meta):
        pass

    @abstractmethod
    async def formulate_response(self, ai_result):
        pass

class OdometerReadingAnalysis(ImageAnalysisWorkflow):
    async def analyse_with_ai(self, s3_url, meta):
        print(f"Calling Odometer Reading AI on {s3_url}...")
        # Simulate AI extracting odometer reading
        return {"odometer_reading": 45231}

    async def formulate_response(self, ai_result):
        print("Formulating odometer reading response...")
        return {"odometer_reading": ai_result["odometer_reading"]}

class ChassisNumberAnalysis(ImageAnalysisWorkflow):
    async def analyse_with_ai(self, s3_url, meta):
        print(f"Calling Chassis Number AI on {s3_url}...")
        # Simulate AI extracting chassis number
        return {"chassis_number": "ABC123XYZ456"}

    async def formulate_response(self, ai_result):
        print("Formulating chassis number response...")
        return {"chassis_number": ai_result["chassis_number"]}

async def main():
    image = "sample.jpg"
    extra_data = {"user_id": 123}

    print("--- Odometer Reading ---")
    odo_api = OdometerReadingAnalysis()
    print(await odo_api.process(image, extra_data))

    print("\n--- Chassis Number ---")
    chassis_api = ChassisNumberAnalysis()
    print(await chassis_api.process(image, extra_data))

if __name__ == "__main__":
    asyncio.run(main())
