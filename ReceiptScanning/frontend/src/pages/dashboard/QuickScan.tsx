import { motion } from "framer-motion";
import { Scan, Upload, Camera } from "lucide-react";

const QuickScan = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="p-6 rounded-2xl glass-card gradient-border"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
          <Scan className="w-5 h-5 text-primary" />
        </div>
        <h3 className="font-display font-semibold text-lg">Quick Scan</h3>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="flex flex-col items-center justify-center gap-3 p-6 rounded-xl bg-gradient-to-br from-primary/10 to-accent/10 border border-primary/20 hover:border-primary/40 transition-colors"
        >
          <div className="w-14 h-14 rounded-full bg-primary/20 flex items-center justify-center">
            <Camera className="w-7 h-7 text-primary" />
          </div>
          <span className="font-medium">Take Photo</span>
        </motion.button>

        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="flex flex-col items-center justify-center gap-3 p-6 rounded-xl bg-secondary/30 border border-border/50 hover:border-border transition-colors"
        >
          <div className="w-14 h-14 rounded-full bg-secondary flex items-center justify-center">
            <Upload className="w-7 h-7 text-muted-foreground" />
          </div>
          <span className="font-medium">Upload File</span>
        </motion.button>
      </div>

      <p className="text-sm text-muted-foreground text-center mt-4">
        Scan a receipt to automatically extract items and totals
      </p>
    </motion.div>
  );
};

export default QuickScan;
