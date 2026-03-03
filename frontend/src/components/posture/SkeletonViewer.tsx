import { motion } from "framer-motion";

interface SkeletonViewerProps {
  imageUrl: string;
}

const SkeletonViewer = ({ imageUrl }: SkeletonViewerProps) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.96 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="rounded-2xl border border-border bg-card p-4 shadow-card overflow-hidden"
    >
      <h3 className="text-sm font-semibold text-foreground mb-3">Skeleton Overlay</h3>
      <div className="rounded-xl overflow-hidden bg-muted">
        <img
          src={imageUrl}
          alt="Annotated skeleton overlay showing posture analysis"
          className="w-full h-auto object-contain"
          style={{ maxHeight: 480 }}
        />
      </div>
    </motion.div>
  );
};

export default SkeletonViewer;
