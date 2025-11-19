import React, { useEffect, useState } from "react";

function formatDate(dt) {
  try {
    return new Date(dt).toLocaleString();
  } catch {
    return dt;
  }
}

export default function App() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/reviews")
      .then((r) => r.json())
      .then((data) => {
        setReviews(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: 24, fontFamily: "Inter, Arial" }}>
      <h1>WhatsApp Product Reviews</h1>
      {loading ? <p>Loading…</p> : null}
      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th style={{ textAlign: "left", padding: 8 }}>User</th>
            <th style={{ textAlign: "left", padding: 8 }}>Product</th>
            <th style={{ textAlign: "left", padding: 8 }}>Review</th>
            <th style={{ textAlign: "left", padding: 8 }}>Time</th>
          </tr>
        </thead>
        <tbody>
          {reviews.map((r) => (
            <tr key={r.id} style={{ borderTop: "1px solid #eee" }}>
              <td style={{ padding: 8 }}>{r.user_name}</td>
              <td style={{ padding: 8 }}>{r.product_name}</td>
              <td style={{ padding: 8 }}>{r.product_review}</td>
              <td style={{ padding: 8 }}>{formatDate(r.created_at)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
