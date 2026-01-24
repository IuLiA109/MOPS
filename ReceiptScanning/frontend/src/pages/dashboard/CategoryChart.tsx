import { motion } from "framer-motion";
import { PieChart } from "lucide-react";
import { ExpensesByCategory } from "../../api/dashboard";

interface CategoryChartProps {
  expensesByCategory: ExpensesByCategory | null;
}

// Color palette for categories
const categoryColors: string[] = [
  "from-cyan-400 to-cyan-600",
  "from-amber-400 to-amber-600",
  "from-emerald-400 to-emerald-600",
  "from-rose-400 to-rose-600",
  "from-violet-400 to-violet-600",
  "from-blue-400 to-blue-600",
  "from-orange-400 to-orange-600",
  "from-pink-400 to-pink-600",
];

const CategoryChart = ({ expensesByCategory }: CategoryChartProps) => {
  const categories = expensesByCategory?.categories || [];
  const totalExpenses = expensesByCategory?.total_expenses || 0;

  const formatCurrency = (amount: number) => {
    return `${amount.toFixed(2)} RON`;
  };

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

      {categories.length === 0 ? (
        <div className="text-center py-8">
          <PieChart className="w-12 h-12 text-muted-foreground/50 mx-auto mb-3" />
          <p className="text-muted-foreground">No expenses this month</p>
          <p className="text-sm text-muted-foreground/70">
            Your spending breakdown will appear here
          </p>
        </div>
      ) : (
        <>
          <div className="space-y-4">
            {categories.slice(0, 5).map((category, index) => {
              const colorClass = categoryColors[index % categoryColors.length];
              
              return (
                <motion.div
                  key={category.category_id || "uncategorized"}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.3, delay: 0.5 + index * 0.1 }}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium">{category.category_name}</span>
                    <span className="text-sm text-muted-foreground">
                      {formatCurrency(category.total)} ({category.percentage}%)
                    </span>
                  </div>
                  <div className="h-2 rounded-full bg-secondary/50 overflow-hidden">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${category.percentage}%` }}
                      transition={{ duration: 0.8, delay: 0.6 + index * 0.1, ease: "easeOut" }}
                      className={`h-full rounded-full bg-gradient-to-r ${colorClass}`}
                    />
                  </div>
                </motion.div>
              );
            })}
          </div>

          {categories.length > 5 && (
            <p className="text-sm text-muted-foreground mt-4">
              +{categories.length - 5} more categories
            </p>
          )}

          <div className="mt-6 pt-6 border-t border-border/50">
            <div className="flex items-center justify-between">
              <span className="text-muted-foreground">Total this month</span>
              <span className="font-display font-bold text-xl">
                {formatCurrency(totalExpenses)}
              </span>
            </div>
          </div>
        </>
      )}
    </motion.div>
  );
};

export default CategoryChart;