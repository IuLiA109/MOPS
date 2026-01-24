import apiClient from './client';

// ===== TYPES =====

export interface DashboardSummary {
  all_time: {
    total_income: number;
    total_expenses: number;
    balance: number;
  };
  current_month: {
    month: string;
    income: number;
    expenses: number;
    balance: number;
  };
  stats: {
    account_count: number;
    transaction_count: number;
  };
}

export interface CategoryExpense {
  category_id: number | null;
  category_name: string;
  total: number;
  transaction_count: number;
  percentage: number;
}

export interface ExpensesByCategory {
  period: {
    start: string;
    end: string;
  };
  total_expenses: number;
  categories: CategoryExpense[];
}

export interface MonthlyData {
  period: string;
  month_name: string;
  income: number;
  expenses: number;
  balance: number;
}

export interface IncomeVsExpenses {
  months: number;
  data: MonthlyData[];
}

export interface RecentTransaction {
  id: number;
  type: 'income' | 'expense';
  amount: number;
  currency: string;
  description: string;
  category_name: string | null;
  transaction_date: string;
}

// ===== API =====

export const dashboardApi = {
  /**
   * Get financial summary (all time + current month)
   */
  getSummary: async (): Promise<DashboardSummary> => {
    return apiClient.get<DashboardSummary>('/dashboard/summary');
  },

  /**
   * Get expenses grouped by category
   */
  getExpensesByCategory: async (
    startDate?: string,
    endDate?: string
  ): Promise<ExpensesByCategory> => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    
    const query = params.toString();
    const endpoint = query ? `/dashboard/expenses-by-category?${query}` : '/dashboard/expenses-by-category';
    
    return apiClient.get<ExpensesByCategory>(endpoint);
  },

  /**
   * Get income vs expenses over time
   */
  getIncomeVsExpenses: async (months: number = 6): Promise<IncomeVsExpenses> => {
    return apiClient.get<IncomeVsExpenses>(`/dashboard/income-vs-expenses?months=${months}`);
  },

  /**
   * Get recent transactions
   */
  getRecentTransactions: async (limit: number = 10): Promise<RecentTransaction[]> => {
    return apiClient.get<RecentTransaction[]>(`/dashboard/recent-transactions?limit=${limit}`);
  },
};

export default dashboardApi;