import { motion } from "framer-motion";
import {
  Camera,
  Upload,
  Receipt,
  Search,
  Filter,
  PieChart,
  TrendingUp,
  User,
  Bell,
  Shield,
  Palette,
} from "lucide-react";
import { mockReceipts, mockMonthlyStats } from "../mocks/data.js";

/* =====================================================
   SCAN RECEIPT PAGE
===================================================== */
export const ScanReceiptPage = () => {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="font-display text-3xl font-bold">Scan Receipt</h1>
        <p className="text-muted-foreground mt-2">
          Upload or capture a receipt to extract data
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="grid grid-cols-1 md:grid-cols-2 gap-6"
      >
        <div className="group rounded-2xl border border-border/50 bg-card/50 p-8 cursor-pointer">
          <div className="text-center">
            <Camera className="mx-auto w-8 h-8 text-primary mb-4" />
            <h3 className="font-display text-xl font-semibold">Take Photo</h3>
            <p className="text-muted-foreground text-sm">
              Use your camera to capture a receipt
            </p>
          </div>
        </div>

        <div className="group rounded-2xl border border-border/50 bg-card/50 p-8 cursor-pointer">
          <div className="text-center">
            <Upload className="mx-auto w-8 h-8 text-accent mb-4" />
            <h3 className="font-display text-xl font-semibold">Upload Image</h3>
            <p className="text-muted-foreground text-sm">
              Select an image from your device
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

/* =====================================================
   RECEIPTS PAGE
===================================================== */
export const ReceiptsPage = () => {
  const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString("ro-RO", {
    day: "numeric",
    month: "short",
    year: "numeric",
  });
};

  return (
    <div className="p-8 max-w-6xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }} className="mb-8">
        <h1 className="font-display text-3xl font-bold">All Receipts</h1>
        <p className="text-muted-foreground mt-2">
          View and manage all your scanned receipts
        </p>
      </motion.div>

      {/* Search */}
      <div className="flex gap-4 mb-6">
        <div className="relative flex-1">
          <label htmlFor="receipt-search" className="sr-only">
            Search receipts
          </label>
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
          <input
            id="receipt-search"
            type="text"
            placeholder="Search receipts..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-card/50 border border-border/50"
          />
        </div>

        <button className="flex items-center gap-2 px-4 py-2.5 rounded-xl border border-border/50">
          <Filter className="w-4 h-4" />
          Filter
        </button>
      </div>

      {/* List */}
      <div className="space-y-4">
        {mockReceipts.map((receipt) => (
          <div
            key={receipt.id}
            className="flex justify-between items-center p-4 rounded-xl border border-border/50 bg-card/50"
          >
            <div className="flex items-center gap-4">
              <Receipt className="w-6 h-6 text-primary" />
              <div>
                <h3 className="font-semibold">{receipt.store}</h3>
                <p className="text-sm text-muted-foreground">
                  {formatDate(receipt.date)}
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-semibold">{receipt.total.toFixed(2)} RON</p>
              <p className="text-sm text-muted-foreground">
                {receipt.produse.length} products
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

/* =====================================================
   ANALYTICS PAGE (no form inputs → OK)
===================================================== */
export const AnalyticsPage = () => {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="font-display text-3xl font-bold mb-6">Analytics</h1>
      <p className="text-muted-foreground">
        Insights into your spending habits
      </p>
    </div>
  );
};

/* =====================================================
   SETTINGS PAGE
===================================================== */
export const SettingsPage = () => {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="font-display text-3xl font-bold mb-8">Settings</h1>

      {/* Profile */}
      <div className="p-6 rounded-2xl border border-border/50 bg-card/50 space-y-4">
        <div className="flex items-center gap-2">
          <User className="w-5 h-5 text-primary" />
          <h2 className="font-display text-xl font-semibold">Profile</h2>
        </div>

        <div>
          <label htmlFor="username" className="text-sm text-muted-foreground">
            Username
          </label>
          <input
            id="username"
            type="text"
            defaultValue="alex"
            className="w-full mt-1 px-4 py-2.5 rounded-xl bg-secondary/30 border border-border/50"
          />
        </div>

        <div>
          <label htmlFor="email" className="text-sm text-muted-foreground">
            Email
          </label>
          <input
            id="email"
            type="email"
            defaultValue="alex@test.com"
            className="w-full mt-1 px-4 py-2.5 rounded-xl bg-secondary/30 border border-border/50"
          />
        </div>

        <button className="px-6 py-2.5 rounded-xl bg-primary text-primary-foreground">
          Save Changes
        </button>
      </div>
    </div>
  );
};
