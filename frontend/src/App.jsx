import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

import "./App.css";


const API_URL =
  import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";


function App() {
  const [summary, setSummary] = useState(null);
  const [methods, setMethods] = useState([]);
  const [daily, setDaily] = useState([]);

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);


  async function loadDashboard(showRefresh = false) {
    try {
      if (showRefresh) {
        setRefreshing(true);
      } else {
        setLoading(true);
      }

      setError("");

      const [
        summaryResponse,
        methodsResponse,
        dailyResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/api/summary`),
        fetch(`${API_URL}/api/payment-methods`),
        fetch(`${API_URL}/api/daily-payments`),
      ]);


      if (
        !summaryResponse.ok ||
        !methodsResponse.ok ||
        !dailyResponse.ok
      ) {
        throw new Error(
          "Unable to retrieve data from the API."
        );
      }


      const summaryData = await summaryResponse.json();
      const methodsData = await methodsResponse.json();
      const dailyData = await dailyResponse.json();


      setSummary(summaryData[0]);
      setMethods(methodsData);
      setDaily(dailyData);

      setLastUpdated(new Date());

    } catch (error) {
      console.error(error);

      setError(
        "Unable to connect to the data API. Make sure FastAPI is running."
      );

    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }


  useEffect(() => {
  let cancelled = false;

  async function fetchInitialDashboard() {
    try {
      const [
        summaryResponse,
        methodsResponse,
        dailyResponse,
      ] = await Promise.all([
        fetch(`${API_URL}/api/summary`),
        fetch(`${API_URL}/api/payment-methods`),
        fetch(`${API_URL}/api/daily-payments`),
      ]);

      if (
        !summaryResponse.ok ||
        !methodsResponse.ok ||
        !dailyResponse.ok
      ) {
        throw new Error(
          "Unable to retrieve data from the API."
        );
      }

      const summaryData = await summaryResponse.json();
      const methodsData = await methodsResponse.json();
      const dailyData = await dailyResponse.json();

      if (cancelled) return;

      setSummary(summaryData[0]);
      setMethods(methodsData);
      setDaily(dailyData);
      setLastUpdated(new Date());

    } catch (error) {
      if (cancelled) return;

      console.error(error);

      setError(
        "Unable to connect to the data API. Make sure FastAPI is running."
      );

    } finally {
      if (!cancelled) {
        setLoading(false);
      }
    }
  }

  fetchInitialDashboard();

  return () => {
    cancelled = true;
  };
}, []);


  if (loading) {
    return (
      <div className="screen-state">
        <div className="loader"></div>
        <h2>Loading dashboard...</h2>
        <p>
          Connecting to Databricks Gold data
        </p>
      </div>
    );
  }


  if (error) {
    return (
      <div className="screen-state">
        <div className="error-icon">!</div>

        <h2>Dashboard unavailable</h2>

        <p>{error}</p>

        <button
          className="primary-button"
          onClick={() => loadDashboard()}
        >
          Try Again
        </button>
      </div>
    );
  }


  const averagePayment =
    summary.total_payment_amount /
    summary.total_payments;


  const statusData = [
    {
      name: "Successful",
      value: summary.successful_payments,
    },
    {
      name: "Failed",
      value: summary.failed_payments,
    },
    {
      name: "Pending",
      value: summary.pending_payments,
    },
  ];


  const highestSuccessMethod =
    methods.length > 0
      ? [...methods].sort(
          (a, b) =>
            b.success_rate_percentage -
            a.success_rate_percentage
        )[0]
      : null;


  const highestRevenueMethod =
    methods.length > 0
      ? [...methods].sort(
          (a, b) =>
            b.total_payment_amount -
            a.total_payment_amount
        )[0]
      : null;


  return (
    <div className="app">

      {/* Header */}

      <header className="header">

        <div>
          <div className="brand">
            <div className="brand-icon">
              $
            </div>

            <span>
              E-Commerce Analytics
            </span>
          </div>

          <h1>
            Payment Intelligence Dashboard
          </h1>

          <p className="subtitle">
            Real-time analytics powered by
            Databricks Gold Delta tables
          </p>
        </div>


        <div className="header-actions">

          <div className="live-status">
            <span className="live-dot"></span>
            Live Data
          </div>


          <button
            className="refresh-button"
            onClick={() =>
              loadDashboard(true)
            }
            disabled={refreshing}
          >
            {refreshing
              ? "Refreshing..."
              : "↻ Refresh"}
          </button>

        </div>

      </header>


      {/* Last updated */}

      {lastUpdated && (
        <div className="updated">
          Last updated{" "}
          {lastUpdated.toLocaleTimeString()}
        </div>
      )}


      {/* KPI Cards */}

      <section className="metrics">

        <Metric
          title="Total Payments"
          value={formatNumber(
            summary.total_payments
          )}
          icon="↗"
        />

        <Metric
          title="Total Revenue"
          value={formatCurrency(
            summary.total_payment_amount
          )}
          icon="$"
        />

        <Metric
          title="Average Payment"
          value={formatCurrency(
            averagePayment
          )}
          icon="≈"
        />

        <Metric
          title="Successful"
          value={formatNumber(
            summary.successful_payments
          )}
          icon="✓"
          positive
        />

        <Metric
          title="Failed"
          value={formatNumber(
            summary.failed_payments
          )}
          icon="!"
          negative
        />

        <Metric
          title="Success Rate"
          value={`${summary.success_rate_percentage}%`}
          icon="%"
          positive
        />

      </section>


      {/* Insight cards */}

      <section className="insights">

        <div className="insight-card">

          <div className="insight-label">
            BEST SUCCESS RATE
          </div>

          <div className="insight-value">
            {highestSuccessMethod?.payment_method ||
              "N/A"}
          </div>

          <div className="insight-detail">
            {highestSuccessMethod
              ? `${highestSuccessMethod.success_rate_percentage}% success rate`
              : ""}
          </div>

        </div>


        <div className="insight-card">

          <div className="insight-label">
            TOP REVENUE METHOD
          </div>

          <div className="insight-value">
            {highestRevenueMethod?.payment_method ||
              "N/A"}
          </div>

          <div className="insight-detail">
            {highestRevenueMethod
              ? formatCurrency(
                  highestRevenueMethod.total_payment_amount
                )
              : ""}
          </div>

        </div>


        <div className="insight-card">

          <div className="insight-label">
            PAYMENT PERIOD
          </div>

          <div className="insight-value">
            {daily.length > 0
              ? `${formatDate(
                  daily[0].payment_date
                )} → ${formatDate(
                  daily[daily.length - 1]
                    .payment_date
                )}`
              : "N/A"}
          </div>

          <div className="insight-detail">
            {daily.length} days of payment data
          </div>

        </div>

      </section>


      {/* Charts */}

      <section className="chart-grid">


        {/* Daily Revenue */}

        <div className="panel panel-large">

          <PanelHeader
            title="Daily Revenue"
            description="Payment revenue over time"
          />

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <LineChart data={daily}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="payment_date"
                tick={{ fontSize: 11 }}
                tickFormatter={formatShortDate}
                minTickGap={35}
              />

              <YAxis
                tick={{ fontSize: 11 }}
                tickFormatter={formatCompactCurrency}
              />

              <Tooltip
                formatter={(value) =>
                  formatCurrency(value)
                }
                labelFormatter={(label) =>
                  formatDate(label)
                }
              />

              <Line
                type="monotone"
                dataKey="total_payment_amount"
                stroke="#4f46e5"
                strokeWidth={3}
                dot={false}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>


        {/* Revenue by Method */}

        <div className="panel">

          <PanelHeader
            title="Revenue by Payment Method"
            description="Total payment amount by method"
          />

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <BarChart data={methods}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="payment_method"
                tick={{ fontSize: 11 }}
              />

              <YAxis
                tick={{ fontSize: 11 }}
                tickFormatter={formatCompactCurrency}
              />

              <Tooltip
                formatter={(value) =>
                  formatCurrency(value)
                }
              />

              <Bar
                dataKey="total_payment_amount"
                fill="#4f46e5"
                radius={[6, 6, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>


        {/* Success Rate */}

        <div className="panel">

          <PanelHeader
            title="Success Rate by Method"
            description="Payment processing performance"
          />

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <BarChart data={methods}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="payment_method"
                tick={{ fontSize: 11 }}
              />

              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 11 }}
              />

              <Tooltip
                formatter={(value) =>
                  `${value}%`
                }
              />

              <Bar
                dataKey="success_rate_percentage"
                fill="#16a34a"
                radius={[6, 6, 0, 0]}
              />

            </BarChart>

          </ResponsiveContainer>

        </div>


        {/* Status Distribution */}

        <div className="panel">

          <PanelHeader
            title="Payment Status"
            description="Distribution of payment outcomes"
          />

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <PieChart>

              <Pie
                data={statusData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={115}
                innerRadius={65}
                paddingAngle={3}
                label
              >

                {statusData.map(
                  (_, index) => (
                    <Cell
                      key={index}
                      fill={
                        [
                          "#16a34a",
                          "#dc2626",
                          "#f59e0b",
                        ][index]
                      }
                    />
                  )
                )}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>

        </div>


        {/* Daily Success Rate */}

        <div className="panel panel-large">

          <PanelHeader
            title="Daily Success Rate"
            description="Daily payment processing performance"
          />

          <ResponsiveContainer
            width="100%"
            height={350}
          >

            <LineChart data={daily}>

              <CartesianGrid
                strokeDasharray="3 3"
                vertical={false}
              />

              <XAxis
                dataKey="payment_date"
                tick={{ fontSize: 11 }}
                tickFormatter={formatShortDate}
                minTickGap={35}
              />

              <YAxis
                domain={[0, 100]}
                tick={{ fontSize: 11 }}
                tickFormatter={(value) =>
                  `${value}%`
                }
              />

              <Tooltip
                formatter={(value) =>
                  `${value}%`
                }
                labelFormatter={(label) =>
                  formatDate(label)
                }
              />

              <Line
                type="monotone"
                dataKey="success_rate_percentage"
                stroke="#16a34a"
                strokeWidth={3}
                dot={false}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </section>


      {/* Method table */}

      <section className="panel table-panel">

        <PanelHeader
          title="Payment Method Performance"
          description="Detailed Gold-layer payment analytics"
        />


        <div className="table-wrapper">

          <table>

            <thead>

              <tr>
                <th>Payment Method</th>
                <th>Total Payments</th>
                <th>Revenue</th>
                <th>Successful</th>
                <th>Success Rate</th>
              </tr>

            </thead>


            <tbody>

              {methods.map((method) => (

                <tr
                  key={method.payment_method}
                >

                  <td>
                    <strong>
                      {method.payment_method}
                    </strong>
                  </td>

                  <td>
                    {formatNumber(
                      method.total_payments
                    )}
                  </td>

                  <td>
                    {formatCurrency(
                      method.total_payment_amount
                    )}
                  </td>

                  <td>
                    {formatNumber(
                      method.successful_payments
                    )}
                  </td>

                  <td>

                    <div className="rate-cell">

                      <div className="rate-bar">

                        <div
                          className="rate-fill"
                          style={{
                            width: `${method.success_rate_percentage}%`,
                          }}
                        />

                      </div>

                      <span>
                        {method.success_rate_percentage}%
                      </span>

                    </div>

                  </td>

                </tr>

              ))}

            </tbody>

          </table>

        </div>

      </section>


      {/* Architecture */}

      <section className="architecture">

        <div>
          <span>DATA SOURCE</span>
          <strong>PostgreSQL / CSV</strong>
        </div>

        <div className="arrow">→</div>

        <div>
          <span>STREAMING</span>
          <strong>Apache Kafka</strong>
        </div>

        <div className="arrow">→</div>

        <div>
          <span>PROCESSING</span>
          <strong>Databricks</strong>
        </div>

        <div className="arrow">→</div>

        <div>
          <span>ANALYTICS</span>
          <strong>Gold Delta</strong>
        </div>

        <div className="arrow">→</div>

        <div>
          <span>APPLICATION</span>
          <strong>FastAPI + React</strong>
        </div>

      </section>


      <footer>

        <p>
          E-Commerce Data Engineering Platform
        </p>

        <span>
          PostgreSQL • Kafka • PySpark •
          Databricks • Delta Lake • FastAPI • React
        </span>

      </footer>

    </div>
  );
}


/* ---------------------------------------------------------
   Components
--------------------------------------------------------- */

function Metric({
  title,
  value,
  icon,
  positive,
  negative,
}) {
  return (
    <div className="metric">

      <div
        className={`metric-icon ${
          positive
            ? "positive"
            : negative
            ? "negative"
            : ""
        }`}
      >
        {icon}
      </div>

      <div className="metric-content">

        <span>{title}</span>

        <strong>{value}</strong>

      </div>

    </div>
  );
}


function PanelHeader({
  title,
  description,
}) {
  return (
    <div className="panel-header">

      <div>
        <h2>{title}</h2>

        <p>{description}</p>
      </div>

    </div>
  );
}


/* ---------------------------------------------------------
   Formatting
--------------------------------------------------------- */

function formatNumber(value) {
  return Number(value).toLocaleString();
}


function formatCurrency(value) {
  return `$${Number(value).toLocaleString(
    undefined,
    {
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }
  )}`;
}


function formatCompactCurrency(value) {
  const number = Number(value);

  if (number >= 1000000) {
    return `$${(number / 1000000).toFixed(1)}M`;
  }

  if (number >= 1000) {
    return `$${(number / 1000).toFixed(0)}K`;
  }

  return `$${number}`;
}


function formatDate(value) {
  if (!value) return "";

  return new Date(value).toLocaleDateString(
    undefined,
    {
      year: "numeric",
      month: "short",
      day: "numeric",
    }
  );
}


function formatShortDate(value) {
  if (!value) return "";

  return new Date(value).toLocaleDateString(
    undefined,
    {
      month: "short",
      day: "numeric",
    }
  );
}


export default App;