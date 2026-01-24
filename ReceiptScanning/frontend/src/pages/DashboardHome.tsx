import { motion } from "framer-motion";
import { Receipt, Wallet, TrendingUp, PiggyBank, Loader2, AlertCircle, RefreshCw } from "lucide-react";
import StatsCard from "./dashboard/StatsCard";
import RecentReceipts from "./dashboard/RecentReceipts";
import CategoryChart from "./dashboard/CategoryChart";
import QuickScan from "./dashboard/QuickScan";
import { useAuth } from "../components/AuthContext";
import { useDashboard } from "../hooks/useDashboard";

const DashboardHome = () => {
  const { user } = useAuth();
  const { summary, expensesByCategory, recentTransactions, isLoading, error, refetch } = useDashboard();

  // Format currency
  const formatCurrency = (amount: number) => {
    return `${amount.toFixed(2)} RON`;
  };

  if (isLoading) {
    return (
      <div className="p-8 max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <Loader2 className="w-12 h-12 animate-spin text-primary mx-auto mb-4" />
          <p className="text-muted-foreground">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8 max-w-7xl mx-auto flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <AlertCircle className="w-12 h-12 text-destructive mx-auto mb-4" />
          <p className="text-destructive mb-4">{error}</p>
          <button
            onClick={refetch}
            className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Try again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="font-display text-3xl font-bold">
          Welcome back,{" "}
          <span className="gradient-text">{user?.username || "User"}</span>
        </h1>
        <p className="text-muted-foreground mt-2">
          Here's an overview of your spending{" "}
          {summary?.current_month.month ? `in ${summary.current_month.month}` : "this month"}
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Balance"
          value={formatCurrency(summary?.all_time.balance || 0)}
          subtitle="All time"
          icon={Wallet}
        />
        <StatsCard
          title="Monthly Expenses"
          value={formatCurrency(summary?.current_month.expenses || 0)}
          subtitle={summary?.current_month.month || "This month"}
          icon={Receipt}
        />
        <StatsCard
          title="Monthly Income"
          value={formatCurrency(summary?.current_month.income || 0)}
          subtitle={summary?.current_month.month || "This month"}
          icon={TrendingUp}
        />
        <StatsCard
          title="Transactions"
          value={summary?.stats.transaction_count?.toString() || "0"}
          subtitle="Total recorded"
          icon={PiggyBank}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <RecentReceipts transactions={recentTransactions} />
        </div>
        <div className="space-y-6">
          <QuickScan />
          <CategoryChart expensesByCategory={expensesByCategory} />
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;