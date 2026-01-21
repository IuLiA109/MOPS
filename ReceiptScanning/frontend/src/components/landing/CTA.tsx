import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom"

const CTA = () => {
  return (
    <section className="py-32 relative overflow-hidden">
      {/* Background effects */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-1/4 w-[500px] h-[500px] rounded-full bg-primary/20 blur-[150px]" />
        <div className="absolute bottom-0 right-1/4 w-[400px] h-[400px] rounded-full bg-accent/20 blur-[120px]" />
      </div>

      <div className="container px-6 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-4xl mx-auto text-center"
        >
          <div className="p-12 sm:p-16 rounded-3xl gradient-border glow">
            <h2 className="font-display text-4xl sm:text-5xl lg:text-6xl font-bold mb-6">
              Ready to ditch the
              <br />
              <span className="gradient-text">receipt chaos?</span>
            </h2>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto mb-10">
              Start scanning for free today. No credit card required. Full access to all features for 14 days.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
                <Link
                    to="/register"
                    className="group inline-flex items-center justify-center gap-2 h-14 px-10 text-base font-medium bg-primary text-primary-foreground rounded-md hover:bg-primary/90 transition-colors"
                >
                    Get started free
                    <ArrowRight className="h-5 w-5 transition-transform group-hover:translate-x-1" />
                </Link>
                
                {/*
                <a href="#" className="inline-flex items-center justify-center h-14 px-10 text-base font-medium border border-border/50 rounded-md hover:bg-secondary transition-colors">
                    Schedule a demo
                </a>
                */}
                
                </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTA;