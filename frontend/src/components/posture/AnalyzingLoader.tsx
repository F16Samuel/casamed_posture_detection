import { motion } from "framer-motion";
import { Activity } from "lucide-react";

interface AnalyzingLoaderProps {
  message?: string;
}

const AnalyzingLoader = ({ message = "Analyzing posture using AI…" }: AnalyzingLoaderProps) => {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="flex flex-col items-center justify-center py-20 gap-6"
    >
      <div className="relative">
        <div className="h-20 w-20 rounded-full border-4 border-border" />
        <div className="absolute inset-0 h-20 w-20 rounded-full border-4 border-transparent border-t-primary animate-spin" />
        <div className="absolute inset-0 flex items-center justify-center">
          <Activity className="h-7 w-7 text-primary" />
        </div>
      </div>
      <div className="text-center">
        <p className="text-base font-semibold text-foreground">{message}</p>
        <p className="mt-1 text-sm text-muted-foreground">This may take a few moments</p>
      </div>
    </motion.div>
  );
};

export default AnalyzingLoader;
