"""Example of builder pattern"""

from abc import ABC, abstractmethod


class PDFDocument:
    def __init__(self):
        self.html: str | None = None
        self.pdf = None
        self.metadata = None

    def __str__(self):
        return f"PDFDocument(html={bool(self.html)}, pdf={bool(self.pdf)}, metadata={self.metadata})"


class PDFBuilder(ABC):
    @abstractmethod
    def generate_html(self, data):
        pass

    @abstractmethod
    def convert_to_pdf(self):
        pass

    @abstractmethod
    def post_process(self):
        pass

    @abstractmethod
    def upload_to_s3(self):
        pass

    @abstractmethod
    def call_service_1(self):
        pass

    @abstractmethod
    def call_service_2(self):
        pass

    @abstractmethod
    def build(self):
        pass


class ConcretePDFBuilder(PDFBuilder):
    def __init__(self):
        self.document = PDFDocument()

    def generate_html(self, data):
        print("Generating HTML...")
        self.document.html = f"<html><body>{data}</body></html>"
        return self

    def convert_to_pdf(self):
        print("Converting HTML to PDF...")
        self.document.pdf = b"%PDF-1.4..."  # Simulating PDF bytes
        return self

    def post_process(self):
        print("Applying post-processing...")
        self.document.metadata = {"watermark": "Confidential"}
        return self

    def upload_to_s3(self):
        print("Uploading PDF to S3...")
        return self

    def call_service_1(self):
        print("Calling first external service...")
        return self

    def call_service_2(self):
        print("Calling second external service...")
        return self

    def build(self):
        return self.document


class PDFDirector:
    @staticmethod
    def construct_standard_pdf(data):
        return (
            ConcretePDFBuilder()
            .generate_html(data)
            .convert_to_pdf()
            .post_process()
            .upload_to_s3()
            .call_service_1()
            .call_service_2()
            .build()
        )


pdf = PDFDirector.construct_standard_pdf("Hello, this is my PDF content!")
print(pdf)
