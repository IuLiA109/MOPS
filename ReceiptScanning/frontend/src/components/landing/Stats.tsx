import { motion } from "framer-motion";

const stats = [
  { value: "2M+", label: "Receipts Scanned" },
  { value: "99.2%", label: "OCR Accuracy" },
  { value: "50K+", label: "Happy Users" },
  { value: "<2s", label: "Scan Time" },
];

const Stats = () => {
  return (
    <section className="py-20 border-y border-border/50">
      <div className="container px-6">
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-0 lg:divide-x divide-border/50">
          {stats.map((stat, index) => (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              className="text-center"
            >
              <p className="font-display text-4xl sm:text-5xl font-bold gradient-text mb-2">
                {stat.value}
              </p>
              <p className="text-muted-foreground">{stat.label}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Stats;