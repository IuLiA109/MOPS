import { useState, useEffect, useCallback } from 'react';
import {
  dashboardApi,
  DashboardSummary,
  ExpensesByCategory,
  IncomeVsExpenses,
  RecentTransaction,
} from '../api/dashboard';

interface UseDashboardReturn {
  summary: DashboardSummary | null;
  expensesByCategory: ExpensesByCategory | null;
  incomeVsExpenses: IncomeVsExpenses | null;
  recentTransactions: RecentTransaction[];
  isLoading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useDashboard = (): UseDashboardReturn => {
  const [summary, setSummary] = useState<DashboardSummary | null>(null);
  const [expensesByCategory, setExpensesByCategory] = useState<ExpensesByCategory | null>(null);
  const [incomeVsExpenses, setIncomeVsExpenses] = useState<IncomeVsExpenses | null>(null);
  const [recentTransactions, setRecentTransactions] = useState<RecentTransaction[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDashboardData = useCallback(async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Fetch all data in parallel
      const [summaryData, categoryData, incomeExpenseData, transactionsData] = await Promise.all([
        dashboardApi.getSummary(),
        dashboardApi.getExpensesByCategory(),
        dashboardApi.getIncomeVsExpenses(6),
        dashboardApi.getRecentTransactions(5),
      ]);

      setSummary(summaryData);
      setExpensesByCategory(categoryData);
      setIncomeVsExpenses(incomeExpenseData);
      setRecentTransactions(transactionsData);
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load dashboard data';
      setError(message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  return {
    summary,
    expensesByCategory,
    incomeVsExpenses,
    recentTransactions,
    isLoading,
    error,
    refetch: fetchDashboardData,
  };
};

export default useDashboard;