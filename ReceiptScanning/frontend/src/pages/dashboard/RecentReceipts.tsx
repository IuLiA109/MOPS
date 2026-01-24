import { motion } from "framer-motion";
import { Receipt, ChevronRight, TrendingUp, TrendingDown } from "lucide-react";
import { Link } from "react-router-dom";
import { RecentTransaction } from "../../api/dashboard";

interface RecentReceiptsProps {
  transactions: RecentTransaction[];
}

const RecentReceipts = ({ transactions }: RecentReceiptsProps) => {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString("ro-RO", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  };

  const formatCurrency = (amount: number, currency: string = "RON") => {
    return `${amount.toFixed(2)} ${currency}`;
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
          <h3 className="font-display font-semibold text-lg">Recent Transactions</h3>
        </div>
        <Link
          to="/dashboard/receipts"
          className="text-sm text-primary hover:text-primary/80 font-medium flex items-center gap-1"
        >
          View all <ChevronRight className="w-4 h-4" />
        </Link>
      </div>

      {transactions.length === 0 ? (
        <div className="text-center py-8">
          <Receipt className="w-12 h-12 text-muted-foreground/50 mx-auto mb-3" />
          <p className="text-muted-foreground">No transactions yet</p>
          <p className="text-sm text-muted-foreground/70">
            Scan a receipt to get started
          </p>
        </div>
      ) : (
        <div className="space-y-4">
          {transactions.map((transaction, index) => (
            <motion.div
              key={transaction.id}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3, delay: 0.4 + index * 0.1 }}
              className="flex items-center gap-4 p-4 rounded-xl bg-secondary/30 hover:bg-secondary/50 transition-colors cursor-pointer group"
            >
              <div
                className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                  transaction.type === "income"
                    ? "bg-gradient-to-br from-emerald-500/20 to-emerald-600/20"
                    : "bg-gradient-to-br from-primary/20 to-accent/20"
                }`}
              >
                {transaction.type === "income" ? (
                  <TrendingUp className="w-6 h-6 text-emerald-500" />
                ) : (
                  <TrendingDown className="w-6 h-6 text-primary" />
                )}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">
                  {transaction.description || "No description"}
                </p>
                <p className="text-sm text-muted-foreground">
                  {transaction.category_name || "Uncategorized"} •{" "}
                  {formatDate(transaction.transaction_date)}
                </p>
              </div>
              <div className="text-right">
                <p
                  className={`font-display font-semibold ${
                    transaction.type === "income" ? "text-emerald-500" : "text-foreground"
                  }`}
                >
                  {transaction.type === "income" ? "+" : "-"}
                  {formatCurrency(transaction.amount, transaction.currency)}
                </p>
              </div>
              <ChevronRight className="w-5 h-5 text-muted-foreground group-hover:text-foreground transition-colors" />
            </motion.div>
          ))}
        </div>
      )}
    </motion.div>
  );
};

export default RecentReceipts;