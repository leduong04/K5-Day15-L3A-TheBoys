"""Model connector used by the prototype.

Set MODEL_PROVIDER=gemini, MODEL_NAME, and API_KEY in the ignored .env file.
The fake provider remains available for local flow work, but its zero-token
outputs must never be reported as a real evaluation.
"""
import json
import os
import time
import urllib.error
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_env(path=os.path.join(ROOT, ".env")):
    """Load KEY=VALUE pairs without overwriting values already in the environment."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or os.environ.get("GEMINI_API_KEY") or "").strip()


def _post_json(url, headers, body, timeout=45, retries=1):
    payload = json.dumps(body, ensure_ascii=False).encode("utf-8")
    req_headers = {"Content-Type": "application/json", **headers}
    for attempt in range(retries + 1):
        request = urllib.request.Request(url, data=payload, method="POST", headers=req_headers)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            # Do not include request headers or credentials in diagnostics.
            detail = exc.read().decode("utf-8", "replace")[:500]
            if exc.code == 503 and attempt < retries:
                time.sleep(3)
                continue
            raise RuntimeError("Gemini API HTTP %d: %s" % (exc.code, detail)) from None
        except TimeoutError:
            if attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError("Gemini API quá thời gian chờ (%ds)." % timeout) from None
        except urllib.error.URLError as exc:
            if isinstance(exc.reason, TimeoutError) and attempt < retries:
                time.sleep(2)
                continue
            raise RuntimeError("Không kết nối được Gemini API: %s" % exc.reason) from None


def _call_gemini(system, user):
    if not MODEL_NAME:
        raise RuntimeError("Thiếu MODEL_NAME trong .env (ví dụ model Gemini được phép dùng).")
    if not API_KEY:
        raise RuntimeError("Thiếu API_KEY hoặc GEMINI_API_KEY trong .env.")
    url = "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % MODEL_NAME
    body = {
        "systemInstruction": {"parts": [{"text": system}]} if system else None,
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2},
    }
    body = {key: value for key, value in body.items() if value is not None}
    data = _post_json(url, {"x-goog-api-key": API_KEY}, body)
    candidates = data.get("candidates") or []
    if not candidates:
        reason = (data.get("promptFeedback") or {}).get("blockReason", "không có candidate")
        raise RuntimeError("Gemini không trả câu trả lời: %s" % reason)
    text = "".join(part.get("text", "") for part in candidates[0].get("content", {}).get("parts", []))
    usage = data.get("usageMetadata") or {}
    tokens_in = int(usage.get("promptTokenCount", 0))
    tokens_out = int(usage.get("candidatesTokenCount", 0)) + int(usage.get("thoughtsTokenCount", 0))
    if not tokens_out and usage.get("totalTokenCount") is not None:
        tokens_out = max(0, int(usage["totalTokenCount"]) - tokens_in)
    if not text:
        raise RuntimeError("Gemini trả về nội dung rỗng.")
    return {"text": text, "model": MODEL_NAME, "tokens_in": tokens_in, "tokens_out": tokens_out}


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {"text": "[câu trả lời giả — chưa nối model] " + last[:60], "model": "fake", "tokens_in": 0, "tokens_out": 0}
    if MODEL_PROVIDER == "gemini":
        return _call_gemini(system, user)
    raise RuntimeError("MODEL_PROVIDER=%s chưa được hỗ trợ; chọn gemini hoặc fake." % MODEL_PROVIDER)
