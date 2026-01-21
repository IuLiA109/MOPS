import { motion } from "framer-motion";
import { Scan, Brain, PieChart, Shield, Zap, Smartphone } from "lucide-react";

const features = [
  {
    icon: Scan,
    title: "Instant OCR Scanning",
    description: "Point your camera at any receipt and watch the magic happen. Our OCR extracts every detail in seconds."
  },
  {
    icon: Brain,
    title: "AI Categorization",
    description: "Smart algorithms automatically categorize expenses. No more manual sorting through hundreds of receipts."
  },
  {
    icon: PieChart,
    title: "Visual Analytics",
    description: "Beautiful charts and insights show exactly where your money goes. Spot trends before they become problems."
  },
  {
    icon: Shield,
    title: "Bank-Grade Security",
    description: "Your financial data is encrypted end-to-end. We take security as seriously as you take your finances."
  },
  {
    icon: Zap,
    title: "Lightning Fast Sync",
    description: "Real-time sync across all devices. Scan on your phone, analyze on your desktop."
  },
  {
    icon: Smartphone,
    title: "Works Offline",
    description: "Capture receipts anywhere, anytime. Data syncs automatically when you're back online."
  }
];

const Features = () => {
  return (
    <section id="features" className="py-32 relative">
      {/* Background accent */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] rounded-full bg-primary/5 blur-[150px]" />
      
      <div className="container px-6 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
            Everything you need to
            <br />
            <span className="gradient-text">master your expenses</span>
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            From scanning to insights, Receiptly handles the heavy lifting so you can focus on what matters.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
            >
              <div className="group h-full p-8 rounded-2xl gradient-border transition-all duration-300 hover:scale-[1.02]">
                <div className="w-14 h-14 rounded-xl bg-primary/10 flex items-center justify-center mb-6 group-hover:bg-primary/20 transition-colors">
                  <feature.icon className="w-7 h-7 text-primary" />
                </div>
                <h3 className="font-display text-xl font-semibold mb-3">{feature.title}</h3>
                <p className="text-muted-foreground leading-relaxed">{feature.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;