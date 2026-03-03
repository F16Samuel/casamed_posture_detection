import { useCallback, useRef, useState } from "react";
import { Upload, FileVideo, X, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { motion, AnimatePresence } from "framer-motion";

const ACCEPTED_TYPES = ["video/mp4", "video/quicktime", "video/x-msvideo", "video/avi"];
const ACCEPTED_EXTENSIONS = [".mp4", ".mov", ".avi"];

interface UploadSectionProps {
  onFileSelected: (file: File) => void;
  onAnalyze: () => void;
  isUploading: boolean;
  selectedFile: File | null;
  onClear: () => void;
}

const UploadSection = ({ onFileSelected, onAnalyze, isUploading, selectedFile, onClear }: UploadSectionProps) => {
  const [dragOver, setDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [videoUrl, setVideoUrl] = useState<string | null>(null);
  const [durationValid, setDurationValid] = useState<boolean | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const validateAndSet = useCallback((file: File) => {
    setError(null);
    setDurationValid(null);

    const ext = "." + file.name.split(".").pop()?.toLowerCase();
    if (!ACCEPTED_TYPES.includes(file.type) && !ACCEPTED_EXTENSIONS.includes(ext)) {
      setError("Invalid format. Please upload an MP4, MOV, or AVI file.");
      return;
    }

    const url = URL.createObjectURL(file);
    const video = document.createElement("video");
    video.preload = "metadata";
    video.onloadedmetadata = () => {
      URL.revokeObjectURL(video.src);
      if (video.duration < 10 || video.duration > 15) {
        setError(`Video must be 10–15 seconds. Yours is ${video.duration.toFixed(1)}s.`);
        setDurationValid(false);
        return;
      }
      setDurationValid(true);
      setVideoUrl(URL.createObjectURL(file));
      onFileSelected(file);
    };
    video.src = url;
  }, [onFileSelected]);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) validateAndSet(file);
  }, [validateAndSet]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) validateAndSet(file);
  };

  const handleClear = () => {
    setError(null);
    setVideoUrl(null);
    setDurationValid(null);
    if (inputRef.current) inputRef.current.value = "";
    onClear();
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <AnimatePresence mode="wait">
        {!selectedFile ? (
          <motion.div
            key="upload"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
          >
            <div
              onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
              onDragLeave={() => setDragOver(false)}
              onDrop={handleDrop}
              onClick={() => inputRef.current?.click()}
              className={`relative cursor-pointer rounded-2xl border-2 border-dashed p-12 text-center transition-all duration-200 ${
                dragOver
                  ? "border-primary bg-primary/5 shadow-soft"
                  : "border-border hover:border-primary/40 hover:bg-secondary/50"
              }`}
            >
              <input
                ref={inputRef}
                type="file"
                accept=".mp4,.mov,.avi"
                onChange={handleFileChange}
                className="hidden"
              />
              <div className="flex flex-col items-center gap-4">
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
                  <Upload className="h-7 w-7 text-primary" />
                </div>
                <div>
                  <p className="text-base font-semibold text-foreground">
                    Drop your posture video here
                  </p>
                  <p className="mt-1 text-sm text-muted-foreground">
                    or click to browse · MP4, MOV, AVI · 10–15 seconds
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="preview"
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -12 }}
            className="rounded-2xl border border-border bg-card p-6 shadow-card"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10">
                  <FileVideo className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <p className="text-sm font-medium text-foreground truncate max-w-[240px]">
                    {selectedFile.name}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    {(selectedFile.size / (1024 * 1024)).toFixed(1)} MB
                    {durationValid && " · Duration OK"}
                  </p>
                </div>
              </div>
              <button
                onClick={handleClear}
                className="rounded-lg p-2 text-muted-foreground hover:bg-secondary hover:text-foreground transition-colors"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {videoUrl && (
              <video
                src={videoUrl}
                controls
                className="w-full rounded-xl bg-muted mb-4"
                style={{ maxHeight: 320 }}
              />
            )}

            <Button
              onClick={onAnalyze}
              disabled={isUploading}
              className="w-full h-12 text-base font-semibold gradient-hero text-primary-foreground hover:opacity-90 transition-opacity"
            >
              {isUploading ? "Uploading…" : "Analyze Posture"}
            </Button>
          </motion.div>
        )}
      </AnimatePresence>

      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="mt-4 flex items-start gap-3 rounded-xl border border-destructive/20 bg-destructive/5 p-4"
          >
            <AlertCircle className="h-5 w-5 text-destructive shrink-0 mt-0.5" />
            <p className="text-sm text-destructive">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default UploadSection;
