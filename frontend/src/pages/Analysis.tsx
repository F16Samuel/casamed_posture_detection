import { useState, useCallback, useEffect } from "react";
import Header from "@/components/Header";
import UploadSection from "@/components/posture/UploadSection";
import ResultsDashboard from "@/components/posture/ResultsDashboard";
import AnalyzingLoader from "@/components/posture/AnalyzingLoader";
import ErrorDisplay from "@/components/posture/ErrorDisplay";
import { analyzePosture, ApiError, checkHealth } from "@/lib/api";
import { AnalysisState, PostureAnalysisResult } from "@/types/posture";
import { AnimatePresence, motion } from "framer-motion";

const Analysis = () => {
  const [state, setState] = useState<AnalysisState>("idle");
  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<PostureAnalysisResult | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  // Optional health check on mount
  useEffect(() => {
    checkHealth().catch(() => {});
  }, []);

  const handleFileSelected = useCallback((f: File) => {
    setFile(f);
    setState("file_selected");
    setErrorMessage("");
  }, []);

  const handleClear = useCallback(() => {
    setFile(null);
    setState("idle");
    setResult(null);
    setErrorMessage("");
  }, []);

  const handleAnalyze = useCallback(async () => {
    if (!file) return;
    setState("uploading");
    try {
      setState("analyzing");
      const data = await analyzePosture(file);
      setState("rendering_video");
      // Brief pause to let annotated video become available
      await new Promise((r) => setTimeout(r, 1500));
      setResult(data);
      setState("success");
    } catch (err) {
      const message =
        err instanceof ApiError
          ? err.message
          : "An unexpected error occurred. Please try again.";
      setErrorMessage(message);
      setState("error");
    }
  }, [file]);

  const handleReset = useCallback(() => {
    setFile(null);
    setResult(null);
    setState("idle");
    setErrorMessage("");
  }, []);

  const stateMessage = (() => {
    switch (state) {
      case "idle":
      case "file_selected":
        return "Upload a 10–15 second video to begin your assessment.";
      case "uploading":
      case "analyzing":
        return "Please wait while we process your video.";
      case "rendering_video":
        return "Finalizing annotated video...";
      case "success":
        return "Your posture analysis results are ready.";
      case "error":
        return "Something went wrong during analysis.";
    }
  })();

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="container mx-auto px-4 py-10 md:py-16">
        <div className="text-center mb-10">
          <h1 className="text-2xl md:text-3xl font-bold text-foreground">
            Posture Analysis
          </h1>
          <p className="mt-2 text-muted-foreground">{stateMessage}</p>
        </div>

        <AnimatePresence mode="wait">
          {(state === "idle" || state === "file_selected" || state === "uploading") && (
            <motion.div key="upload" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <UploadSection
                onFileSelected={handleFileSelected}
                onAnalyze={handleAnalyze}
                isUploading={state === "uploading"}
                selectedFile={file}
                onClear={handleClear}
              />
            </motion.div>
          )}

          {(state === "analyzing" || state === "rendering_video") && (
            <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <AnalyzingLoader
                message={
                  state === "rendering_video"
                    ? "Finalizing annotated video..."
                    : "Analyzing posture using AI..."
                }
              />
            </motion.div>
          )}

          {state === "success" && result && (
            <motion.div key="results" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <ResultsDashboard result={result} onReset={handleReset} />
            </motion.div>
          )}

          {state === "error" && (
            <motion.div key="error" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <ErrorDisplay message={errorMessage} onRetry={handleReset} />
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
};

export default Analysis;
