import base64
import os
from dataclasses import dataclass

import requests

SERVICE_URL = os.environ.get(
    "PCBPATROL_SERVICE_URL",
    "https://8000-01kvnaypcqys2237n7jb5t6p3z.cloudspaces.litng.ai",
)


@dataclass
class InspectIn:
    image_path: str = ""
    image_base64: str = ""
    image_url: str = ""


@dataclass
class InspectOut:
    is_anomaly: bool
    anomaly_score: float
    num_detections: int
    detections: list
    severity: int
    recommended_disposition: str
    disposition_confidence: float
    description: str
    probable_cause: str
    corrective_measure: str
    heatmap_png: str


def main(input: InspectIn) -> InspectOut:
    if input.image_base64:
        b64 = input.image_base64
    elif input.image_url:
        img = requests.get(input.image_url, timeout=30)
        img.raise_for_status()
        b64 = base64.b64encode(img.content).decode()
    elif input.image_path:
        with open(input.image_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
    else:
        raise ValueError("Provide image_url, image_base64, or image_path")

    resp = requests.post(f"{SERVICE_URL}/inspect", json={"image": b64}, timeout=120)
    if resp.status_code != 200:
        raise RuntimeError(f"vision service returned {resp.status_code}: {resp.text}")
    r = resp.json()

    reasoning = r["reasoning"]
    detections = r["detections"]
    return InspectOut(
        is_anomaly=r["is_anomaly"],
        anomaly_score=r["anomaly_score"],
        num_detections=len(detections),
        detections=detections,
        severity=r["severity"],
        recommended_disposition=r["recommended_disposition"],
        disposition_confidence=r["disposition_confidence"],
        description=reasoning["description"],
        probable_cause=reasoning["probable_cause"],
        corrective_measure=reasoning["corrective_measure"],
        heatmap_png=r["heatmap_png"],
    )
