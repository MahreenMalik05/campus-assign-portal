
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from datetime import datetime, timezone

HOST = "127.0.0.1"
PORT = 5001

REPORT_FILE = Path(__file__).resolve().parent / "test-report.json"


class ReportHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/report":
            self.send_error(404, "Endpoint not found")
            return

        try:
            content_length = int(self.headers.get("Content-Length", 0))

            if content_length <= 0 or content_length > 1_000_000:
                self.send_error(400, "Invalid report size")
                return

            raw_data = self.rfile.read(content_length)
            report = json.loads(raw_data.decode("utf-8"))

            if not isinstance(report, dict):
                self.send_error(400, "JSON object required")
                return

            report["received_at"] = datetime.now(
                timezone.utc
            ).isoformat()

            REPORT_FILE.write_text(
                json.dumps(report, indent=4),
                encoding="utf-8",
            )

            response = json.dumps({
                "message": "Report saved successfully",
                "file": str(REPORT_FILE),
            }).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            print(f"Report saved to: {REPORT_FILE}")

        except (ValueError, UnicodeDecodeError, OSError) as error:
            self.send_error(400, f"Could not process report: {error}")

    def log_message(self, format_string, *args):
        print(f"[Receiver] {format_string % args}")


if __name__ == "__main__":
    server = HTTPServer((HOST, PORT), ReportHandler)

    print(f"Report receiver running at http://{HOST}:{PORT}/report")
    print(f"Output file: {REPORT_FILE}")
    print("Press Ctrl+C to stop.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping report receiver.")
    finally:
        server.server_close()
