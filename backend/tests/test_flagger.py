from app.services.temporal_flagger import extract_flagged_events


def test_flagged_event_extraction():
    frame_results = [
        {
            "frame_index": 0,
            "timestamp": 0.0,
            "score": 50,
            "metrics": {
                "neck_angle": 30,
                "spine_vertical_deviation": 12,
                "shoulder_alignment_difference": 2,
                "hip_alignment_difference": 1
            }
        }
    ]

    result = extract_flagged_events(frame_results)

    assert result["percent_time_bad"] > 0
    assert len(result["events"]) == 1