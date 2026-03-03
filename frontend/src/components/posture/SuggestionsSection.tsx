import { motion } from "framer-motion";
import { Activity, BarChart3, Clock } from "lucide-react";
import { Tooltip, TooltipContent, TooltipTrigger } from "@/components/ui/tooltip";
import { Info } from "lucide-react";

interface SuggestionsProps {
  percentTimeBad: number;
  flaggedIssues: string[];
}

const SUGGESTION_MAP: Record<string, string> = {
  "forward head": "Practice chin tucks: gently draw your chin back to align your ears over your shoulders. Do 10 reps, 3 times daily.",
  "spinal deviation": "Strengthen your core with planks and bird-dog exercises. Consider ergonomic adjustments to your workstation.",
  "spine": "Strengthen your core with planks and bird-dog exercises. Consider ergonomic adjustments to your workstation.",
  "shoulder asymmetry": "Stretch tight shoulders with doorway stretches. Strengthen the weaker side with single-arm rows.",
  "shoulder": "Stretch tight shoulders with doorway stretches. Strengthen the weaker side with single-arm rows.",
  "pelvic imbalance": "Try hip flexor stretches and glute bridges to correct pelvic tilt. Consider a standing desk.",
  "hip": "Try hip flexor stretches and glute bridges to correct pelvic tilt. Consider a standing desk.",
  "neck": "Practice chin tucks and neck stretches. Ensure your monitor is at eye level to reduce strain.",
};

function deriveSuggestions(flaggedIssues: string[]): string[] {
  const seen = new Set<string>();
  const suggestions: string[] = [];

  for (const issue of flaggedIssues) {
    const lower = issue.toLowerCase();
    for (const [keyword, suggestion] of Object.entries(SUGGESTION_MAP)) {
      if (lower.includes(keyword) && !seen.has(suggestion)) {
        seen.add(suggestion);
        suggestions.push(suggestion);
      }
    }
  }

  if (suggestions.length === 0) {
    suggestions.push("Maintain regular posture check-ins and take movement breaks every 30 minutes.");
  }

  return suggestions;
}

const SuggestionsSection = ({ percentTimeBad, flaggedIssues }: SuggestionsProps) => {
  const suggestions = deriveSuggestions(flaggedIssues);

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.4, duration: 0.4 }}
      className="rounded-2xl border border-border bg-card p-5 shadow-card"
    >
      <div className="flex items-center justify-between mb-3">
        <h3 className="text-sm font-semibold text-foreground">Recommendations</h3>
        <Tooltip>
          <TooltipTrigger asChild>
            <button className="text-muted-foreground hover:text-foreground transition-colors">
              <Info className="h-4 w-4" />
            </button>
          </TooltipTrigger>
          <TooltipContent side="top" className="max-w-[240px] text-xs">
            Suggestions based on detected posture issues during your video analysis.
          </TooltipContent>
        </Tooltip>
      </div>
      <ul className="space-y-2.5">
        {suggestions.map((s, i) => (
          <li key={i} className="flex items-start gap-2.5">
            <Activity className="h-4 w-4 text-primary shrink-0 mt-0.5" />
            <span className="text-sm text-muted-foreground leading-relaxed">{s}</span>
          </li>
        ))}
      </ul>
    </motion.div>
  );
};

export default SuggestionsSection;
