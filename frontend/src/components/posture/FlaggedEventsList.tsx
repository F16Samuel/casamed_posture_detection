import { motion } from "framer-motion";
import { FlaggedEvent } from "@/types/posture";
import { AlertTriangle } from "lucide-react";

interface FlaggedEventsListProps {
  events: FlaggedEvent[];
  onEventClick: (timestamp: number) => void;
}

function formatTimestamp(seconds: number): string {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${m}:${s.toString().padStart(2, "0")}`;
}

const FlaggedEventsList = ({ events, onEventClick }: FlaggedEventsListProps) => {
  if (events.length === 0) {
    return (
      <div className="rounded-2xl border border-border bg-card p-5 shadow-card">
        <h3 className="text-sm font-semibold text-foreground mb-3">Flagged Events</h3>
        <p className="text-sm text-muted-foreground">No posture issues detected — great job!</p>
      </div>
    );
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.4 }}
      className="rounded-2xl border border-border bg-card p-5 shadow-card"
    >
      <h3 className="text-sm font-semibold text-foreground mb-3">
        Flagged Events ({events.length})
      </h3>
      <ul className="space-y-2 max-h-60 overflow-y-auto pr-1">
        {events.map((event, i) => {
          const scoreColor =
            event.score >= 85
              ? "text-score-good"
              : event.score >= 65
              ? "text-score-fair"
              : "text-score-poor";

          return (
            <li
              key={i}
              onClick={() => onEventClick(event.timestamp)}
              className="flex items-center gap-3 rounded-xl p-3 cursor-pointer border border-transparent hover:border-border hover:bg-secondary/50 transition-colors"
            >
              <AlertTriangle className="h-4 w-4 text-score-fair shrink-0" />
              <div className="flex-1 min-w-0">
                <p className="text-sm text-foreground truncate">{event.primary_issue}</p>
                <p className="text-xs text-muted-foreground">
                  at {formatTimestamp(event.timestamp)}
                </p>
              </div>
              <span className={`text-sm font-semibold ${scoreColor}`}>
                {event.score}
              </span>
            </li>
          );
        })}
      </ul>
    </motion.div>
  );
};

export default FlaggedEventsList;
