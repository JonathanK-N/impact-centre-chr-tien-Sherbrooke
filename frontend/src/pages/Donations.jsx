import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import api from "../services/api";

const initialForm = {
  amount: "",
  payment_method: "stripe",
  currency: "CAD",
  receipt_url: ""
};

export default function Donations() {
  const [form, setForm] = useState(initialForm);
  const [history, setHistory] = useState([]);
  const [error, setError] = useState(null);
  const [message, setMessage] = useState(null);

  const loadHistory = async () => {
    try {
      const { data } = await api.get("/donations");
      setHistory(data);
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de récupérer l'historique.");
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setError(null);
    setMessage(null);
    try {
      await api.post("/donations", { ...form, amount: Number(form.amount || 0) });
      setMessage("Merci pour votre générosité ! Le don a été enregistré.");
      setForm(initialForm);
      loadHistory();
    } catch (err) {
      setError(err.response?.data?.message || "Impossible d'enregistrer le don.");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Dons en ligne</h1>
          <p className="mt-1 text-sm text-slate-500">
            Soutenez la mission d&apos;Impact Centre Chrétien Sherbrooke et suivez vos contributions.
          </p>
        </header>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-700">Faire un don</h2>
          <form onSubmit={handleSubmit} className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <label className="block text-sm font-medium text-slate-600">Montant (CAD)</label>
              <input
                name="amount"
                type="number"
                min="1"
                required
                value={form.amount}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600">Méthode de paiement</label>
              <select
                name="payment_method"
                value={form.payment_method}
                onChange={handleChange}
                className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="stripe">Stripe</option>
                <option value="paypal">PayPal</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-600">Lien de reçu (optionnel)</label>
              <input
                name="receipt_url"
                value={form.receipt_url}
                onChange={handleChange}
                placeholder="URL du reçu"
                className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div className="md:col-span-2 flex justify-end">
              <button
                type="submit"
                className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
              >
                Donner
              </button>
            </div>
          </form>
          {message && <p className="mt-3 text-sm text-green-600">{message}</p>}
          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
        </section>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-700">Historique des dons</h2>
          <div className="mt-4 overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-200 text-sm">
              <thead className="bg-slate-50">
                <tr>
                  <th className="px-4 py-2 text-left font-medium text-slate-600">Date</th>
                  <th className="px-4 py-2 text-left font-medium text-slate-600">Montant</th>
                  <th className="px-4 py-2 text-left font-medium text-slate-600">Statut</th>
                  <th className="px-4 py-2 text-left font-medium text-slate-600">Reçu</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-200 bg-white">
                {history.map((donation) => (
                  <tr key={donation.id}>
                    <td className="px-4 py-2">
                      {new Date(donation.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-4 py-2">
                      {donation.amount} {donation.currency}
                    </td>
                    <td className="px-4 py-2 capitalize">{donation.status}</td>
                    <td className="px-4 py-2">
                      {donation.receipt_url ? (
                        <a
                          href={donation.receipt_url}
                          className="text-primary-600 underline"
                          target="_blank"
                          rel="noreferrer"
                        >
                          Voir le reçu
                        </a>
                      ) : (
                        "—"
                      )}
                    </td>
                  </tr>
                ))}
                {history.length === 0 && (
                  <tr>
                    <td colSpan={4} className="px-4 py-4 text-center text-slate-500">
                      Aucun don enregistré pour le moment.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </DashboardLayout>
  );
}
