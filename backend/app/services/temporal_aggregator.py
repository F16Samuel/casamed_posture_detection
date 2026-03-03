from statistics import mean


def weighted_overall_score(frame_results):

    scores = [f["score"] for f in frame_results]

    bad_scores = [s for s in scores if s < 65]
    good_scores = [s for s in scores if s >= 65]

    if bad_scores:
        bad_mean = mean(bad_scores)
        good_mean = mean(good_scores) if good_scores else bad_mean
        overall = 0.75 * bad_mean + 0.25 * good_mean
    else:
        overall = mean(scores)

    return round(overall, 2)