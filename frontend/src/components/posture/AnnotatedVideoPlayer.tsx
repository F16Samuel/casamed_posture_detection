import { useRef, useState } from "react";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

interface AnnotatedVideoPlayerProps {
  videoUrl: string;
  processingTime: number;
  onSeek?: (time: number) => void;
  videoRef?: React.RefObject<HTMLVideoElement>;
}

const AnnotatedVideoPlayer = ({ videoUrl, processingTime, videoRef: externalRef }: AnnotatedVideoPlayerProps) => {
  const [loading, setLoading] = useState(true);
  const internalRef = useRef<HTMLVideoElement>(null);
  const ref = externalRef || internalRef;

  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-3"
    >
      <div className="relative rounded-2xl overflow-hidden border border-border bg-card shadow-card">
        {loading && (
          <div className="absolute inset-0 flex items-center justify-center bg-muted/80 z-10">
            <Loader2 className="h-8 w-8 text-primary animate-spin" />
          </div>
        )}
        <video
          ref={ref}
          src={videoUrl}
          controls
          className="w-full"
          onCanPlay={() => setLoading(false)}
          onLoadedData={() => setLoading(false)}
          style={{ maxHeight: 480 }}
        />
      </div>
      <p className="text-xs text-muted-foreground text-center">
        Processed in {processingTime.toFixed(2)} seconds
      </p>
    </motion.div>
  );
};

export default AnnotatedVideoPlayer;
