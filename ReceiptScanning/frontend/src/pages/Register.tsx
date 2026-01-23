import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Eye, EyeOff, ArrowRight, Loader2 } from "lucide-react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../components/AuthContext";

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);

  const { register, isLoading, error, clearError, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  // Redirect dacă e deja autentificat
  useEffect(() => {
    if (isAuthenticated) {
      navigate("/dashboard");
    }
  }, [isAuthenticated, navigate]);

  // Curăță eroarea când se schimbă input-urile
  useEffect(() => {
    if (error) clearError();
  }, [username, email, password]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const success = await register(username, email, password);
    if (success) {
      navigate("/dashboard");
    }
  };

  const getPasswordStrength = () => {
    if (password.length === 0) return { level: 0, text: "", color: "" };
    
    let score = 0;
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[@$!%*?&]/.test(password)) score++;

    if (score <= 1) return { level: 1, text: "Weak", color: "bg-destructive" };
    if (score <= 2) return { level: 2, text: "Medium", color: "bg-yellow-500" };
    return { level: 3, text: "Strong", color: "bg-primary" };
  };

  const strength = getPasswordStrength();

  // Validare username (live feedback)
  const getUsernameError = () => {
    if (username.length === 0) return null;
    if (username.length < 4) return "Username must be at least 4 characters";
    if (!/^[A-Za-z0-9_]+$/.test(username)) return "Only letters, numbers, and underscores allowed";
    return null;
  };

  const usernameError = getUsernameError();

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden px-6 py-12">
      {/* Background effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 -left-1/4 w-[600px] h-[600px] rounded-full bg-primary/10 blur-[120px] animate-pulse-glow" />
        <div
          className="absolute bottom-1/4 -right-1/4 w-[500px] h-[500px] rounded-full bg-accent/10 blur-[100px] animate-pulse-glow"
          style={{ animationDelay: "1.5s" }}
        />
      </div>

      {/* Grid pattern */}
      <div
        className="absolute inset-0 opacity-[0.03]"
        style={{
          backgroundImage: `linear-gradient(hsl(var(--foreground)) 1px, transparent 1px), linear-gradient(90deg, hsl(var(--foreground)) 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
        }}
      />

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="p-8 sm:p-10 rounded-3xl glass-card gradient-border">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 justify-center mb-8">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-primary to-accent flex items-center justify-center glow-sm">
              <span className="font-display font-bold text-primary-foreground text-xl">
                R
              </span>
            </div>
            <span className="font-display font-bold text-2xl">Receiptly</span>
          </Link>

          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="font-display text-3xl font-bold mb-2">Create account</h1>
            <p className="text-muted-foreground">Start tracking your receipts today</p>
          </div>

          {/* Error message */}
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              className="mb-6 p-4 rounded-xl bg-destructive/10 border border-destructive/20 text-destructive text-sm"
            >
              {error}
            </motion.div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="johndoe"
                required
                disabled={isLoading}
                className="w-full h-12 px-4 rounded-xl bg-secondary/50 border border-border/50 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              />
              {usernameError && (
                <p className="text-xs text-destructive">{usernameError}</p>
              )}
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
                disabled={isLoading}
                className="w-full h-12 px-4 rounded-xl bg-secondary/50 border border-border/50 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
              />
            </div>

            <div className="space-y-2">
              <label className="text-sm font-medium text-foreground">Password</label>
              <div className="relative">
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Create a password"
                  required
                  disabled={isLoading}
                  className="w-full h-12 px-4 pr-12 rounded-xl bg-secondary/50 border border-border/50 text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isLoading}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors disabled:opacity-50"
                >
                  {showPassword ? (
                    <EyeOff className="w-5 h-5" />
                  ) : (
                    <Eye className="w-5 h-5" />
                  )}
                </button>
              </div>

              {/* Password strength indicator */}
              {password && (
                <motion.div
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="space-y-2 pt-2"
                >
                  <div className="flex gap-1.5">
                    {[1, 2, 3].map((level) => (
                      <div
                        key={level}
                        className={`h-1.5 flex-1 rounded-full transition-all duration-300 ${
                          strength.level >= level ? strength.color : "bg-border"
                        }`}
                      />
                    ))}
                  </div>
                  <p
                    className={`text-xs ${
                      strength.level === 1
                        ? "text-destructive"
                        : strength.level === 2
                        ? "text-yellow-500"
                        : strength.level === 3
                        ? "text-primary"
                        : "text-muted-foreground"
                    }`}
                  >
                    {strength.text}
                  </p>
                  <p className="text-xs text-muted-foreground">
                    Use 8+ characters with uppercase, lowercase, number, and special character (@$!%*?&)
                  </p>
                </motion.div>
              )}
            </div>

            {/* Terms */}
            <p className="text-xs text-muted-foreground">
              By creating an account, you agree to our{" "}
              <a
                href="#"
                className="text-primary hover:text-primary/80 transition-colors"
              >
                Terms of Service
              </a>{" "}
              and{" "}
              <a
                href="#"
                className="text-primary hover:text-primary/80 transition-colors"
              >
                Privacy Policy
              </a>
            </p>

            <button
              type="submit"
              disabled={isLoading || !!usernameError}
              className="group w-full h-12 bg-primary text-primary-foreground font-medium rounded-xl hover:bg-primary/90 transition-all flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Creating account...
                </>
              ) : (
                <>
                  Create Account
                  <ArrowRight className="w-5 h-5 transition-transform group-hover:translate-x-1" />
                </>
              )}
            </button>
          </form>

          {/* Footer */}
          <p className="text-center text-muted-foreground mt-8">
            Already have an account?{" "}
            <Link
              to="/login"
              className="text-primary hover:text-primary/80 font-medium transition-colors"
            >
              Sign in
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default Register;