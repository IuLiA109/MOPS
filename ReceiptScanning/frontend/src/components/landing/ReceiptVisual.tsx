import { motion } from "framer-motion";

const ReceiptVisual = () => {
  return (
    <div className="relative w-full max-w-md mx-auto">
      {/* Main receipt card */}
      <motion.div
        animate={{ y: [0, -10, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="relative z-20"
      >
        <div className="glass-card rounded-2xl p-6 glow">
          {/* Phone mockup */}
          <div className="bg-background rounded-xl overflow-hidden border border-border/50">
            {/* Status bar */}
            <div className="flex justify-between items-center px-4 py-2 border-b border-border/30">
              <span className="text-xs text-muted-foreground">9:41</span>
              <div className="flex gap-1">
                <div className="w-4 h-2 rounded-sm bg-primary" />
              </div>
            </div>
            
            {/* Receipt content */}
            <div className="p-4 space-y-4">
              <div className="flex items-center justify-between">
                <span className="font-display font-semibold text-lg">Receipt Scan</span>
                <span className="text-xs px-2 py-1 rounded-full bg-primary/20 text-primary">Processing</span>
              </div>

              {/* Fake receipt */}
              <div className="bg-card rounded-lg p-4 space-y-3 relative overflow-hidden">
                {/* Scan line animation */}
                <div className="absolute inset-x-0 h-8 scan-line animate-scan opacity-60" />
                
                <div className="text-center border-b border-dashed border-border/50 pb-3">
                  <p className="font-display font-semibold">COFFEE HOUSE</p>
                  <p className="text-xs text-muted-foreground">123 Main Street</p>
                </div>
                
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Latte</span>
                    <span>$5.50</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Croissant</span>
                    <span>$4.25</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Tip</span>
                    <span>$2.00</span>
                  </div>
                </div>
                
                <div className="flex justify-between pt-2 border-t border-dashed border-border/50 font-display font-semibold">
                  <span>Total</span>
                  <span className="gradient-text">$11.75</span>
                </div>
              </div>

              {/* Extracted data */}
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse" />
                  <span className="text-muted-foreground">Merchant detected:</span>
                  <span className="font-medium">Coffee House</span>
                </div>
                <div className="flex items-center gap-2 text-sm">
                  <div className="w-2 h-2 rounded-full bg-accent animate-pulse" style={{ animationDelay: '0.5s' }} />
                  <span className="text-muted-foreground">Category:</span>
                  <span className="font-medium">Food & Drink</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Floating elements */}
      <motion.div
        animate={{ y: [0, -15, 0], rotate: [0, 3, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        className="absolute -top-8 -right-8 z-10"
      >
        <div className="glass-card rounded-xl p-4 glow-sm">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center">
              <span className="text-lg">📊</span>
            </div>
            <div>
              <p className="font-display font-semibold text-sm">Monthly Total</p>
              <p className="gradient-text font-bold">$2,847.50</p>
            </div>
          </div>
        </div>
      </motion.div>

      <motion.div
        animate={{ y: [0, -12, 0], rotate: [0, -2, 0] }}
        transition={{ duration: 7, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        className="absolute -bottom-4 -left-8 z-30"
      >
        <div className="glass-card rounded-xl p-3 glow-sm">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-accent/20 flex items-center justify-center">
              <span className="text-sm">✓</span>
            </div>
            <p className="text-sm font-medium">Saved to expenses</p>
          </div>
        </div>
      </motion.div>

      {/* Background glow */}
      <div className="absolute inset-0 -z-10 blur-3xl opacity-30">
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 rounded-full bg-primary" />
      </div>
    </div>
  );
};

export default ReceiptVisual;