export type PostureClassification = "Good" | "Fair" | "Poor";

export type AnalysisState =
  | "idle"
  | "file_selected"
  | "uploading"
  | "analyzing"
  | "rendering_video"
  | "success"
  | "error";

export interface FlaggedEvent {
  timestamp: number;
  score: number;
  primary_issue: string;
}

export interface PostureArtifacts {
  annotated_video_url: string;
  pdf_report_url: string;
}

export interface PostureAnalysisResult {
  status: string;
  report_id: string;
  overall_score: number;
  frames_analyzed: number;
  percent_time_bad: number;
  flagged_events: FlaggedEvent[];
  artifacts: PostureArtifacts;
  processing_time_seconds: number;
}

export function classifyScore(score: number): PostureClassification {
  if (score >= 85) return "Good";
  if (score >= 65) return "Fair";
  return "Poor";
}
