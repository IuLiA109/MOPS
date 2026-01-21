import { motion } from "framer-motion";
import { Receipt, Wallet, TrendingUp, CalendarDays } from "lucide-react";
import DashboardSidebar from "./dashboard/DashboardSidebar";
import StatsCard from "./dashboard/StatsCard";
import RecentReceipts from "./dashboard/RecentReceipts";
import CategoryChart from "./dashboard/CategoryChart";
import QuickScan from "./dashboard/QuickScan";
import { mockUser, mockMonthlyStats } from "../mocks/data.js";

const Dashboard = () => {
  return (
    <div className="min-h-screen flex bg-background">
      {/* Background effects */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-0 right-1/4 w-[500px] h-[500px] rounded-full bg-primary/5 blur-[150px]" />
        <div className="absolute bottom-1/4 left-1/4 w-[400px] h-[400px] rounded-full bg-accent/5 blur-[120px]" />
      </div>

      <DashboardSidebar />

      <main className="flex-1 overflow-auto">
        <div className="p-8 max-w-7xl mx-auto">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <h1 className="font-display text-3xl font-bold">
              Welcome back, <span className="gradient-text">{mockUser.username}</span>
            </h1>
            <p className="text-muted-foreground mt-2">
              Here's an overview of your spending this month
            </p>
          </motion.div>

          {/* Stats Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <StatsCard
              title="Total Spent"
              value={`${mockMonthlyStats.totalSpent.toFixed(2)} RON`}
              subtitle="This month"
              icon={Wallet}
              trend={{ value: 12, isPositive: false }}
              delay={0}
            />
            <StatsCard
              title="Receipts"
              value={mockMonthlyStats.receiptCount.toString()}
              subtitle="Scanned this month"
              icon={Receipt}
              trend={{ value: 8, isPositive: true }}
              delay={0.1}
            />
            <StatsCard
              title="Avg. per Receipt"
              value={`${(mockMonthlyStats.totalSpent / mockMonthlyStats.receiptCount).toFixed(2)} RON`}
              subtitle="This month"
              icon={TrendingUp}
              delay={0.15}
            />
            <StatsCard
              title="Last Scan"
              value="Today"
              subtitle="20 Jan 2025"
              icon={CalendarDays}
              delay={0.2}
            />
          </div>

          {/* Content Grid */}
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
      </main>
    </div>
  );
};

export default Dashboard;
