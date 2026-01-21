import { motion } from "framer-motion";
import { ArrowRight, Scan } from "lucide-react";
import ReceiptVisual from "./ReceiptVisual";
import { Link } from "react-router-dom";

const Hero = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden pt-20">
      {/* Background gradient orbs */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 -left-1/4 w-[600px] h-[600px] rounded-full bg-primary/10 blur-[120px] animate-pulse-glow" />
        <div className="absolute bottom-1/4 -right-1/4 w-[500px] h-[500px] rounded-full bg-accent/10 blur-[100px] animate-pulse-glow" style={{ animationDelay: '1.5s' }} />
      </div>

      {/* Grid pattern overlay */}
      <div 
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(hsl(var(--foreground)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--foreground)) 1px, transparent 1px)`,
          backgroundSize: '60px 60px'
        }}
      />

      <div className="container relative z-10 px-6">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          {/* Left content */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="text-center lg:text-left"
          >
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-full glass-card mb-8"
            >
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span className="text-sm text-muted-foreground">Now with AI-powered extraction</span>
            </motion.div>

            <h1 className="font-display text-5xl sm:text-6xl lg:text-7xl font-bold leading-[1.1] tracking-tight mb-6">
              Scan receipts.
              <br />
              <span className="gradient-text">Track everything.</span>
            </h1>

            <p className="text-lg sm:text-xl text-muted-foreground max-w-lg mx-auto lg:mx-0 mb-10 leading-relaxed">
              Transform paper chaos into organized finances. Our OCR technology instantly captures and categorizes your expenses.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
            <Link
                to="/register" className="group inline-flex items-center justify-center gap-2 h-14 px-8 text-base font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors">
                Start for free
                <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
            </Link>
            {/*
            <a href="#" className="inline-flex items-center justify-center gap-2 h-14 px-8 text-base font-medium border border-border/50 rounded-md hover:bg-secondary transition-colors">
                <Scan className="h-5 w-5" />
                See demo
            </a>
            */}
            </div>



            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="flex items-center gap-8 mt-12 justify-center lg:justify-start"
            >
              <div className="flex -space-x-3">
                {[1, 2, 3, 4].map((i) => (
                  <div 
                    key={i} 
                    className="w-10 h-10 rounded-full border-2 border-background bg-gradient-to-br from-primary/30 to-accent/30"
                  />
                ))}
              </div>
              <div className="text-left">
                <p className="font-display font-semibold">50,000+</p>
                <p className="text-sm text-muted-foreground">receipts scanned daily</p>
              </div>
            </motion.div>
          </motion.div>

          {/* Right visual */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 1, delay: 0.3, ease: [0.16, 1, 0.3, 1] }}
            className="relative"
          >
            <ReceiptVisual />
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default Hero;