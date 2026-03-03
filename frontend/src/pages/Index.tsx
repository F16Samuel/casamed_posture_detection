import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import Header from "@/components/Header";
import { ArrowRight, Scan, ArrowUpDown, Move, Spline } from "lucide-react";
import { motion } from "framer-motion";

const FEATURES = [
  {
    icon: Scan,
    title: "Neck Alignment",
    description: "Measures the angle of your neck relative to the vertical axis to detect forward head posture.",
  },
  {
    icon: ArrowUpDown,
    title: "Shoulder Symmetry",
    description: "Compares left and right shoulder height to identify imbalances and drooping.",
  },
  {
    icon: Move,
    title: "Hip Balance",
    description: "Analyzes hip alignment differences that may indicate pelvic tilt or lateral shift.",
  },
  {
    icon: Spline,
    title: "Spine Alignment",
    description: "Evaluates spinal deviation from the vertical axis to detect scoliosis or slouching.",
  },
];

const container = {
  hidden: {},
  show: { transition: { staggerChildren: 0.1 } },
};

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5 } },
};

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      <Header />

      {/* Hero */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 gradient-hero opacity-[0.03]" />
        <div className="container mx-auto px-4 py-24 md:py-32 relative">
          <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-2xl mx-auto text-center"
          >
            <div className="inline-flex items-center gap-2 rounded-full border border-primary/20 bg-primary/5 px-4 py-1.5 text-sm font-medium text-primary mb-6">
              <span className="relative flex h-2 w-2">
                <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-primary opacity-75" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-primary" />
              </span>
              AI-Powered Analysis
            </div>
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold tracking-tight text-foreground leading-tight">
              AI-Powered{" "}
              <span className="bg-clip-text text-transparent" style={{ backgroundImage: "var(--gradient-hero)" }}>
                Posture Analysis
              </span>
            </h1>
            <p className="mt-5 text-lg text-muted-foreground max-w-lg mx-auto leading-relaxed">
              Upload a short video and receive an instant, comprehensive posture assessment powered by advanced computer vision.
            </p>
            <div className="mt-8">
              <Button
                asChild
                size="lg"
                className="h-13 px-8 text-base font-semibold gradient-hero text-primary-foreground hover:opacity-90 transition-opacity shadow-elevated"
              >
                <Link to="/analysis">
                  Start Analysis
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Link>
              </Button>
            </div>
          </motion.div>
        </div>
      </section>

      {/* How it works */}
      <section className="py-20 md:py-28">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <h2 className="text-2xl md:text-3xl font-bold text-foreground">What We Analyze</h2>
            <p className="mt-3 text-muted-foreground max-w-md mx-auto">
              Our AI examines four key postural dimensions to give you a complete assessment.
            </p>
          </motion.div>

          <motion.div
            variants={container}
            initial="hidden"
            whileInView="show"
            viewport={{ once: true }}
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5 max-w-5xl mx-auto"
          >
            {FEATURES.map((f) => (
              <motion.div
                key={f.title}
                variants={item}
                className="rounded-2xl border border-border bg-card p-6 shadow-card hover:shadow-elevated transition-shadow duration-300"
              >
                <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 mb-4">
                  <f.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-base font-semibold text-foreground mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{f.description}</p>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Steps */}
      <section className="py-20 border-t border-border">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-14"
          >
            <h2 className="text-2xl md:text-3xl font-bold text-foreground">How It Works</h2>
          </motion.div>
          <div className="flex flex-col md:flex-row items-center justify-center gap-8 md:gap-16 max-w-3xl mx-auto">
            {[
              { step: "1", title: "Record Video", desc: "Film a 10–15 second posture video" },
              { step: "2", title: "Upload & Analyze", desc: "Our AI processes your video instantly" },
              { step: "3", title: "Get Results", desc: "View scores, metrics & download report" },
            ].map((s, i) => (
              <motion.div
                key={s.step}
                initial={{ opacity: 0, y: 16 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: 0.1 * i }}
                className="flex flex-col items-center text-center"
              >
                <div className="flex h-14 w-14 items-center justify-center rounded-full gradient-hero text-primary-foreground text-lg font-bold mb-3">
                  {s.step}
                </div>
                <h3 className="font-semibold text-foreground mb-1">{s.title}</h3>
                <p className="text-sm text-muted-foreground">{s.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} PostureAI. Professional posture analysis powered by artificial intelligence.
        </div>
      </footer>
    </div>
  );
};

export default Index;
