# PCBPatrol Agent

A **UiPath coded agent** (Python) that bridges UiPath Automation Cloud and the [PCBPatrol vision service](https://github.com/MohsenMaaleki/pcbpatrol). Built for UiPath AgentHack 2026 (Track 1).

The agent takes a PCB image, sends it to the vision service's `/inspect` endpoint — where three ML models (RF-DETR + PatchCore + Qwen3-VL) analyze it — and maps the structured findings back into the Orchestrator job: detected defects, anomaly score, severity, recommended disposition, and reasoning. It runs **serverless on UiPath Automation Cloud**.

**Agent type: Coded Agent** (Python, UiPath Python SDK), not low-code. Deployed to UiPath Automation Cloud and run serverless.

## How it fits

```
  Maestro / Orchestrator
          |
          v
  +--------------------+   POST /inspect   +-----------------------+
  |  PCBPatrol Agent   | ----------------> |  Vision service (GPU) |
  |  (this repo)       | <---------------- |  3 ML models          |
  +--------------------+    InspectOut     +-----------------------+
          |
          v
  Structured job output
```

## Inputs

Three optional inputs (the agent uses the first one provided, in this priority):

1. `image_base64` — a pre-encoded image.
2. `image_url` — a URL the agent downloads (used to bypass UiPath's 10,000-character input-argument limit; a base64 image exceeds it).
3. `image_path` — a local file path (works for local runs, not cloud).

## Output (`InspectOut`)

`is_anomaly`, `anomaly_score`, `num_detections`, `detections` (list of `{cls, confidence, bbox}`), `severity`, `recommended_disposition`, `disposition_confidence`, `description`, `probable_cause`, `corrective_measure`, `heatmap_png`.

## Configuration

Set `PCBPATROL_SERVICE_URL` to the running vision service URL (env var, overrides the default in `main.py`). When deployed, set it as an Environment Variable on the Orchestrator process.

## Run locally

```bash
uipath run main -f input.json
```

where `input.json` is, for example:

```json
{ "image_url": "https://raw.githubusercontent.com/MohsenMaaleki/pcbpatrol/main/demo_assets/short.jpg" }
```

## Deploy to UiPath Automation Cloud

```bash
uipath auth          # authenticate (use --staging for the hackathon tenant)
uipath pack          # build the .nupkg
uipath publish --my-workspace
```

Then in Orchestrator, set the `PCBPATROL_SERVICE_URL` environment variable on the process, provide `image_url` as input, and run.

## Example output

A run against a board with a soldering short returns:

```json
{
  "is_anomaly": true,
  "anomaly_score": 1.0,
  "num_detections": 1,
  "detections": [{ "cls": "short", "confidence": 0.85, "bbox": [528.2, 383.9, 36.5, 34.6] }],
  "severity": 5,
  "recommended_disposition": "scrap",
  "disposition_confidence": 0.85,
  "description": "Excessive solder forms a blob-like structure that can cause an electrical short...",
  "probable_cause": "Improper soldering technique...",
  "corrective_measure": "Use precise soldering equipment and add quality checks..."
}
```

## Built with

UiPath Python SDK · UiPath Automation Cloud · Python · requests

## License

Apache-2.0
