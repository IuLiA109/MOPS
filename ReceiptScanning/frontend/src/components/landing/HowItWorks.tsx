import { motion } from "framer-motion";

const steps = [
  {
    number: "01",
    title: "Snap a photo",
    description: "Open the app and take a quick photo of any receipt. Our camera is optimized for paper documents."
  },
  {
    number: "02",
    title: "AI extracts data",
    description: "Our OCR engine reads every line item, date, merchant, and total with 99.2% accuracy."
  },
  {
    number: "03",
    title: "Auto-categorize",
    description: "Machine learning categorizes your expense and suggests relevant tags based on patterns."
  },
  {
    number: "04",
    title: "Track & analyze",
    description: "View beautiful reports, set budgets, and get insights to optimize your spending."
  }
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="py-32 relative overflow-hidden">
      <div className="container px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
            How it <span className="gradient-text">works</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From paper to insights in four simple steps. No complicated setup required.
          </p>
        </motion.div>

        <div className="relative">
          {/* Connection line */}
          <div className="absolute top-1/2 left-0 right-0 h-px bg-gradient-to-r from-transparent via-border to-transparent hidden lg:block" />

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <motion.div
                key={step.number}
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: index * 0.15 }}
                className="relative"
              >
                <div className="text-center">
                  <div className="relative inline-flex mb-6">
                    <div className="w-20 h-20 rounded-2xl bg-card border border-border flex items-center justify-center relative z-10">
                      <span className="font-display text-2xl font-bold gradient-text">{step.number}</span>
                    </div>
                    {/* Glow effect */}
                    <div className="absolute inset-0 rounded-2xl bg-primary/20 blur-xl opacity-0 group-hover:opacity-100 transition-opacity" />
                  </div>
                  <h3 className="font-display text-xl font-semibold mb-3">{step.title}</h3>
                  <p className="text-muted-foreground">{step.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;