import { useRef } from "react";
import { PostureAnalysisResult, classifyScore } from "@/types/posture";
import { resolveArtifactUrl } from "@/lib/api";
import ScoreGauge from "./ScoreGauge";
import AnnotatedVideoPlayer from "./AnnotatedVideoPlayer";
import FlaggedEventsList from "./FlaggedEventsList";
import SuggestionsSection from "./SuggestionsSection";
import { Button } from "@/components/ui/button";
import { Download, RotateCcw, Film, BarChart3 } from "lucide-react";
import { motion } from "framer-motion";

interface ResultsDashboardProps {
  result: PostureAnalysisResult;
  onReset: () => void;
}

const ResultsDashboard = ({ result, onReset }: ResultsDashboardProps) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const classification = classifyScore(result.overall_score);

  const videoUrl = resolveArtifactUrl(result.artifacts.annotated_video_url);
  const pdfUrl = resolveArtifactUrl(result.artifacts.pdf_report_url);

  const handleEventClick = (timestamp: number) => {
    if (videoRef.current) {
      videoRef.current.currentTime = timestamp;
      videoRef.current.play();
    }
  };

  const flaggedIssues = result.flagged_events.map((e) => e.primary_issue);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="w-full max-w-7xl mx-auto"
    >
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
        {/* Left — Video (65%) */}
        <div className="lg:col-span-3 space-y-4">
          <AnnotatedVideoPlayer
            videoUrl={videoUrl}
            processingTime={result.processing_time_seconds}
            videoRef={videoRef}
          />
        </div>

        {/* Right — Results Panel (35%) */}
        <div className="lg:col-span-2 space-y-5">
          {/* Score */}
          <div className="flex flex-col items-center">
            <ScoreGauge score={result.overall_score} classification={classification} />
          </div>

          {/* Stats row */}
          <div className="grid grid-cols-2 gap-3">
            <div className="rounded-2xl border border-border bg-card p-4 shadow-card text-center">
              <Film className="h-5 w-5 text-primary mx-auto mb-1.5" />
              <p className="text-xl font-bold text-foreground">{result.frames_analyzed}</p>
              <p className="text-xs text-muted-foreground">Frames Analyzed</p>
            </div>
            <div className="rounded-2xl border border-border bg-card p-4 shadow-card text-center">
              <BarChart3 className="h-5 w-5 text-score-fair mx-auto mb-1.5" />
              <p className="text-xl font-bold text-foreground">{result.percent_time_bad.toFixed(1)}%</p>
              <p className="text-xs text-muted-foreground">Time in Bad Posture</p>
            </div>
          </div>

          {/* Flagged Events */}
          <FlaggedEventsList events={result.flagged_events} onEventClick={handleEventClick} />

          {/* Suggestions */}
          <SuggestionsSection percentTimeBad={result.percent_time_bad} flaggedIssues={flaggedIssues} />

          {/* Actions */}
          <div className="flex flex-col gap-2.5">
            <Button
              asChild
              className="gradient-hero text-primary-foreground hover:opacity-90 h-11"
            >
              <a href={pdfUrl} target="_blank" rel="noopener noreferrer" download>
                <Download className="mr-2 h-4 w-4" />
                Download Full Report
              </a>
            </Button>
            <Button variant="outline" onClick={onReset} className="h-11">
              <RotateCcw className="mr-2 h-4 w-4" />
              Analyze Another Video
            </Button>
          </div>
        </div>
      </div>
    </motion.div>
  );
};

export default ResultsDashboard;
