import { motion } from "framer-motion";
import { AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";

interface ErrorDisplayProps {
  message: string;
  onRetry: () => void;
}

const ErrorDisplay = ({ message, onRetry }: ErrorDisplayProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md mx-auto rounded-2xl border border-destructive/20 bg-card p-8 text-center shadow-card"
    >
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-destructive/10">
        <AlertCircle className="h-7 w-7 text-destructive" />
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">Analysis Failed</h3>
      <p className="text-sm text-muted-foreground mb-6">{message}</p>
      <Button onClick={onRetry} variant="outline" className="h-10 px-6">
        Try Again
      </Button>
    </motion.div>
  );
};

export default ErrorDisplay;
