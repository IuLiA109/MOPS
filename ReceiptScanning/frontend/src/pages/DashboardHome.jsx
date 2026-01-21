import { motion } from "framer-motion";
import { Receipt, Wallet, TrendingUp, CalendarDays } from "lucide-react";
import StatsCard from "./dashboard/StatsCard";
import RecentReceipts from "./dashboard/RecentReceipts";
import CategoryChart from "./dashboard/CategoryChart";
import QuickScan from "./dashboard/QuickScan";
import { mockUser, mockMonthlyStats } from "../mocks/data.js";

const DashboardHome = () => {
  return (
    <div className="p-8 max-w-7xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="font-display text-3xl font-bold">
          Welcome back,{" "}
          <span className="gradient-text">{mockUser.username}</span>
        </h1>
        <p className="text-muted-foreground mt-2">
          Here's an overview of your spending this month
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <StatsCard
          title="Total Spent"
          value={`${mockMonthlyStats.totalSpent.toFixed(2)} RON`}
          subtitle="This month"
          icon={Wallet}
        />
        <StatsCard
          title="Receipts"
          value={mockMonthlyStats.receiptCount.toString()}
          subtitle="Scanned this month"
          icon={Receipt}
        />
        <StatsCard
          title="Avg. per Receipt"
          value={`${(
            mockMonthlyStats.totalSpent / mockMonthlyStats.receiptCount
          ).toFixed(2)} RON`}
          subtitle="This month"
          icon={TrendingUp}
        />
        <StatsCard
          title="Last Scan"
          value="Today"
          subtitle="20 Jan 2025"
          icon={CalendarDays}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <RecentReceipts />
        </div>
        <div className="space-y-6">
          <QuickScan />
          <CategoryChart />
        </div>
      </div>
    </div>
  );
};

export default DashboardHome;
