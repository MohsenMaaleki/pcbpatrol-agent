# PCBPatrol Agent

A UiPath coded agent that calls the PCBPatrol vision service `/inspect` and returns structured PCB inspection results into a Maestro case.

## Input
- `image_path` — local path to a PCB image, **or**
- `image_base64` — a pre-encoded image (used if provided, otherwise `image_path` is read and base64-encoded)

## Output (`InspectOut`)
`is_anomaly`, `anomaly_score`, `num_detections`, `detections`, `severity`, `recommended_disposition`, `disposition_confidence`, `description`, `probable_cause`, `corrective_measure`, `heatmap_png`.

## Configuration
Set `PCBPATROL_SERVICE_URL` to the running vision service URL. The hardcoded default in `main.py` is a temporary demo URL and will rot.

## Run locally
```
uipath run main '{"image_path": "path/to/pcb.jpg"}'
```
