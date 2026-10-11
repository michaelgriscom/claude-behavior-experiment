def handler(event):
    return {"status": "ok", "items": len(event.get("items", []))}
