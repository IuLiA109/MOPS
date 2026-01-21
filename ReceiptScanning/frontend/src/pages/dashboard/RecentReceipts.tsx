import { motion } from "framer-motion";
import { Receipt, ChevronRight, Store } from "lucide-react";
import { mockReceipts } from "../../mocks/data.js";

const RecentReceipts = () => {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("ro-RO", {
      day: "numeric",
      month: "short",
      year: "numeric"
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.3 }}
      className="p-6 rounded-2xl glass-card gradient-border"
    >
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
            <Receipt className="w-5 h-5 text-primary" />
          </div>
          <h3 className="font-display font-semibold text-lg">Recent Receipts</h3>
        </div>
        <button className="text-sm text-primary hover:text-primary/80 font-medium flex items-center gap-1">
          View all <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      <div className="space-y-4">
        {mockReceipts.map((receipt, index) => (
          <motion.div
            key={receipt.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.3, delay: 0.4 + index * 0.1 }}
            className="flex items-center gap-4 p-4 rounded-xl bg-secondary/30 hover:bg-secondary/50 transition-colors cursor-pointer group"
          >
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center">
              <Store className="w-6 h-6 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-medium truncate">{receipt.store}</p>
              <p className="text-sm text-muted-foreground">{formatDate(receipt.date)}</p>
            </div>
            <div className="text-right">
              <p className="font-display font-semibold">{receipt.total.toFixed(2)} RON</p>
              <p className="text-sm text-muted-foreground">{receipt.produse.length} items</p>
            </div>
            <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default RecentReceipts;
