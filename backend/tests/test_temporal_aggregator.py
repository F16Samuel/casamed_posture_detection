from app.services.temporal_aggregator import weighted_overall_score


def test_weighted_aggregation():
    frame_results = [
        {"score": 90},
        {"score": 85},
        {"score": 40},
        {"score": 50}
    ]

    overall = weighted_overall_score(frame_results)

    assert 0 <= overall <= 100
    assert overall < 85