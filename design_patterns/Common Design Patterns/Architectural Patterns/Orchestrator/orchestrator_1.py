
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


# ---------------------------------------------------------------------------
# Core enums / dataclasses
# ---------------------------------------------------------------------------

class StepStatus(Enum):
    SUCCESS = auto()
    FAILED = auto()
    SKIPPED = auto()


@dataclass
class StepResult:
    step_name: str
    status: StepStatus
    message: str


@dataclass
class PdfContext:
    file_name: str
    file_bytes: bytes
    # populated during the workflow
    user_id: Optional[str] = None
    template_html: Optional[str] = None
    config: Optional[dict] = None
    rendered_html: Optional[str] = None
    pdf_bytes: Optional[bytes] = None
    s3_url: Optional[str] = None
    results: list[StepResult] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class WorkflowStep(ABC):
    @abstractmethod
    def execute(self, ctx: PdfContext) -> StepResult: ...

    @abstractmethod
    def rollback(self, ctx: PdfContext) -> None: ...


# ---------------------------------------------------------------------------
# Concrete steps
# ---------------------------------------------------------------------------

class AuthenticateStep(WorkflowStep):
    """Verify the caller's identity (e.g. validate a JWT token)."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [AuthenticateStep] Validating token...")
        # Simulate: token is present in file_name as a prefix "auth:..."
        if ctx.file_name.startswith("INVALID"):
            return StepResult("AuthenticateStep", StepStatus.FAILED,
                              "Token validation failed")
        ctx.user_id = "user_42"
        return StepResult("AuthenticateStep", StepStatus.SUCCESS,
                          f"Authenticated as {ctx.user_id}")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [AuthenticateStep] rollback – clearing user_id")
        ctx.user_id = None


class AuthorizeStep(WorkflowStep):
    """Check that the authenticated user has permission to generate PDFs."""

    _ALLOWED_USERS = {"user_42", "user_99"}

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [AuthorizeStep] Checking permissions...")
        if ctx.user_id not in self._ALLOWED_USERS:
            return StepResult("AuthorizeStep", StepStatus.FAILED,
                              f"{ctx.user_id} is not authorised")
        return StepResult("AuthorizeStep", StepStatus.SUCCESS,
                          f"{ctx.user_id} is authorised")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [AuthorizeStep] nothing to roll back")


class GetTemplateStep(WorkflowStep):
    """Fetch the HTML template from the database."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [GetTemplateStep] Fetching template from DB...")
        # Simulated DB result
        ctx.template_html = (
            "<html><body>"
            "<h1>{{title}}</h1>"
            "<p>Dear {{recipient}}, your document is ready.</p>"
            "</body></html>"
        )
        return StepResult("GetTemplateStep", StepStatus.SUCCESS,
                          "Template loaded")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [GetTemplateStep] rollback – clearing template")
        ctx.template_html = None


class GetConfigurationStep(WorkflowStep):
    """Fetch per-document configuration (watermark text, signature key, etc.)."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [GetConfigurationStep] Fetching config from DB...")
        ctx.config = {
            "watermark_text": "CONFIDENTIAL",
            "watermark_opacity": 0.15,
            "signature_key": "rsa-private-key-stub",
            "s3_bucket": "my-pdf-bucket",
        }
        return StepResult("GetConfigurationStep", StepStatus.SUCCESS,
                          "Configuration loaded")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [GetConfigurationStep] rollback – clearing config")
        ctx.config = None


class GenerateHtmlStep(WorkflowStep):
    """Render the HTML template with document-specific data."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [GenerateHtmlStep] Rendering HTML...")
        data = {"title": ctx.file_name, "recipient": "John Doe"}
        rendered = ctx.template_html
        for key, value in data.items():
            rendered = rendered.replace("{{" + key + "}}", value)
        ctx.rendered_html = rendered
        return StepResult("GenerateHtmlStep", StepStatus.SUCCESS,
                          "HTML rendered")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [GenerateHtmlStep] rollback – clearing rendered HTML")
        ctx.rendered_html = None


class ConvertHtmlToPdfStep(WorkflowStep):
    """Convert the rendered HTML into PDF bytes."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [ConvertHtmlToPdfStep] Converting HTML → PDF...")
        # Simulate PDF generation (real impl: weasyprint / pdfkit / etc.)
        ctx.pdf_bytes = f"%PDF-1.4 ... [{ctx.rendered_html[:40]}...]".encode()
        return StepResult("ConvertHtmlToPdfStep", StepStatus.SUCCESS,
                          f"PDF generated ({len(ctx.pdf_bytes)} bytes)")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [ConvertHtmlToPdfStep] rollback – discarding PDF bytes")
        ctx.pdf_bytes = None


class AddDigitalSignatureStep(WorkflowStep):
    """Embed a digital signature in the PDF."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [AddDigitalSignatureStep] Signing PDF...")
        key = ctx.config["signature_key"]
        # Simulate appending a signature block
        ctx.pdf_bytes += f"\n%%Signature:{key}%%".encode()
        return StepResult("AddDigitalSignatureStep", StepStatus.SUCCESS,
                          "Digital signature applied")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [AddDigitalSignatureStep] rollback – removing signature")
        if ctx.pdf_bytes:
            ctx.pdf_bytes = ctx.pdf_bytes.split(b"\n%%Signature:")[0]


class AddWatermarkStep(WorkflowStep):
    """Overlay a watermark on every page of the PDF."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [AddWatermarkStep] Adding watermark...")
        text = ctx.config["watermark_text"]
        opacity = ctx.config["watermark_opacity"]
        # Simulate embedding watermark metadata
        ctx.pdf_bytes += f"\n%%Watermark:{text}@{opacity}%%".encode()
        return StepResult("AddWatermarkStep", StepStatus.SUCCESS,
                          f"Watermark '{text}' applied at opacity {opacity}")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [AddWatermarkStep] rollback – removing watermark")
        if ctx.pdf_bytes:
            ctx.pdf_bytes = ctx.pdf_bytes.split(b"\n%%Watermark:")[0]


class UploadToS3Step(WorkflowStep):
    """Upload the final PDF to S3 and store the resulting URL."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [UploadToS3Step] Uploading to S3...")
        bucket = ctx.config["s3_bucket"]
        # Simulate upload (real impl: boto3.client('s3').put_object(...))
        ctx.s3_url = f"https://{bucket}.s3.amazonaws.com/{ctx.file_name}.pdf"
        return StepResult("UploadToS3Step", StepStatus.SUCCESS,
                          f"Uploaded to {ctx.s3_url}")

    def rollback(self, ctx: PdfContext) -> None:
        print(f"  [UploadToS3Step] rollback – deleting {ctx.s3_url} from S3")
        ctx.s3_url = None


class ReturnResponseStep(WorkflowStep):
    """Build and record the final response payload."""

    def execute(self, ctx: PdfContext) -> StepResult:
        print("  [ReturnResponseStep] Building response...")
        response = {
            "status": "success",
            "file": ctx.file_name,
            "url": ctx.s3_url,
            "signed_by": ctx.user_id,
        }
        print(f"  Response: {response}")
        return StepResult("ReturnResponseStep", StepStatus.SUCCESS,
                          f"Response ready – {ctx.s3_url}")

    def rollback(self, ctx: PdfContext) -> None:
        print("  [ReturnResponseStep] nothing to roll back")


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

class PdfOrchestrator:

    def __init__(self, steps: list[WorkflowStep]) -> None:
        self._steps = steps

    def execute(self, ctx: PdfContext) -> PdfContext:
        completed: list[WorkflowStep] = []
        for step in self._steps:
            result = step.execute(ctx)
            ctx.results.append(result)
            if result.status == StepStatus.FAILED:
                print(f"\n  Step '{result.step_name}' FAILED: {result.message}")
                print("  Starting rollback...\n")
                self._rollback(completed, ctx)
                break
            completed.append(step)
        return ctx

    def _rollback(self, completed: list[WorkflowStep], ctx: PdfContext) -> None:
        for step in reversed(completed):
            step.rollback(ctx)


# ---------------------------------------------------------------------------
# Sample usage
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    orchestrator = PdfOrchestrator([
        AuthenticateStep(),
        AuthorizeStep(),
        GetTemplateStep(),
        GetConfigurationStep(),
        GenerateHtmlStep(),
        ConvertHtmlToPdfStep(),
        AddWatermarkStep(),
        AddDigitalSignatureStep(),
        UploadToS3Step(),
        ReturnResponseStep(),
    ])

    print("=== Happy path ===")
    ctx = PdfContext(file_name="invoice_2026_04", file_bytes=b"")
    orchestrator.execute(ctx)

    # print("\n=== Step results ===")
    # for r in ctx.results:
    #     print(f"  [{r.status.name:7}] {r.step_name}: {r.message}")

    # print("\n\n=== Failure path (unauthenticated) ===")
    # bad_ctx = PdfContext(file_name="INVALID_invoice", file_bytes=b"")
    # orchestrator.execute(bad_ctx)

    # print("\n=== Step results ===")
    # for r in bad_ctx.results:
    #     print(f"  [{r.status.name:7}] {r.step_name}: {r.message}")
