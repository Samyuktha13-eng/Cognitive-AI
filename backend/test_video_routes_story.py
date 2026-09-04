from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def test_get_story_route_uses_definition_not_generation(monkeypatch):
    def fake_get_story_definition(scene_limit=None):
        return {
            "story_id": "lakshmi-anu",
            "title": "Lakshmi Memories",
            "scenes": [{"id": "intro", "title": "intro", "video": None}],
        }

    def fake_generate_story_videos(*args, **kwargs):
        raise AssertionError("GET /video/story/lakshmi-anu should not trigger generation")

    monkeypatch.setattr("backend.api.video_routes.get_story_definition", fake_get_story_definition)
    monkeypatch.setattr("backend.api.video_routes.generate_story_videos", fake_generate_story_videos)

    response = client.get("/video/story/lakshmi-anu?limit=4")

    assert response.status_code == 200
    body = response.json()
    assert body["story_id"] == "lakshmi-anu"
    assert body["scenes"][0]["id"] == "intro"
