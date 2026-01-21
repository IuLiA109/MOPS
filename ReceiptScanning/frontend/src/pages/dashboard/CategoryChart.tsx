import { motion } from "framer-motion";
import { PieChart } from "lucide-react";
import { mockMonthlyStats } from "../../mocks/data.js";

const categoryColors: Record<string, string> = {
  "Lactate": "from-cyan-400 to-cyan-600",
  "Panificatie": "from-amber-400 to-amber-600",
  "Fructe": "from-emerald-400 to-emerald-600",
  "Carne": "from-rose-400 to-rose-600",
};

const CategoryChart = () => {
  const totalAmount = mockMonthlyStats.byCategory.reduce((sum, cat) => sum + cat.amount, 0);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.4 }}
      className="p-6 rounded-2xl glass-card gradient-border"
    >
      <div className="flex items-center gap-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center">
          <PieChart className="w-5 h-5 text-primary" />
        </div>
        <h3 className="font-display font-semibold text-lg">Spending by Category</h3>
      </div>

      <div className="space-y-4">
        {mockMonthlyStats.byCategory.map((category, index) => {
          const percentage = (category.amount / totalAmount) * 100;
          return (
            <motion.div
              key={category.category}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: 0.5 + index * 0.1 }}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="font-medium">{category.category}</span>
                <span className="text-sm text-muted-foreground">
                  {category.amount.toFixed(2)} RON ({percentage.toFixed(0)}%)
                </span>
              </div>
              <div className="h-2 rounded-full bg-secondary/50 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${percentage}%` }}
                  transition={{ duration: 0.8, delay: 0.6 + index * 0.1, ease: "easeOut" }}
                  className={`h-full rounded-full bg-gradient-to-r ${categoryColors[category.category] || "from-primary to-accent"}`}
                />
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="mt-6 pt-6 border-t border-border/50">
        <div className="flex items-center justify-between">
          <span className="text-muted-foreground">Total this month</span>
          <span className="font-display font-bold text-xl">{totalAmount.toFixed(2)} RON</span>
        </div>
      </div>
    </motion.div>
  );
};

export default CategoryChart;
