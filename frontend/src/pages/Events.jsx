import React, { useEffect, useState } from "react";
import dayjs from "dayjs";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

export default function Events() {
  const { user } = useAuth();
  const [scope, setScope] = useState("global");
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  const loadEvents = async (selectedScope) => {
    try {
      const params = new URLSearchParams();
      params.set("scope", selectedScope);
      const { data } = await api.get(`/events?${params.toString()}`);
      setEvents(data);
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de charger les événements");
    }
  };

  useEffect(() => {
    loadEvents(scope);
  }, [scope]);

  const handleRegister = async (eventId) => {
    try {
      await api.post(`/events/${eventId}/participants`);
      loadEvents(scope);
    } catch (err) {
      setError(err.response?.data?.message || "Inscription impossible");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <h1 className="text-2xl font-semibold text-primary-600">Événements</h1>
            <p className="mt-1 text-sm text-slate-500">
              Visualisez les événements globaux, de votre département ou de votre famille.
            </p>
          </div>
          <div className="flex items-center gap-2">
            <label className="text-sm text-slate-600">Filtrer par</label>
            <select
              value={scope}
              onChange={(event) => setScope(event.target.value)}
              className="rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
            >
              <option value="global">Global</option>
              <option value="department">Département</option>
              <option value="family">Famille d&apos;Impact</option>
            </select>
          </div>
        </header>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <section className="grid gap-4">
          {events.map((event) => (
            <article
              key={event.id}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <h2 className="text-lg font-semibold text-slate-700">{event.title}</h2>
                  <p className="mt-1 text-sm text-slate-500">{event.description}</p>
                  <p className="mt-2 text-sm text-primary-600">
                    {dayjs(event.start_at).format("DD MMM YYYY HH:mm")} —{" "}
                    {dayjs(event.end_at).format("HH:mm")}
                  </p>
                  <p className="text-xs uppercase tracking-wide text-slate-400">
                    {event.location || "Lieu à confirmer"}
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  {event.max_attendees && (
                    <span className="rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold text-primary-600">
                      {event.participants?.length || 0}/{event.max_attendees}
                    </span>
                  )}
                  <button
                    type="button"
                    onClick={() => handleRegister(event.id)}
                    className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
                  >
                    Participer
                  </button>
                </div>
              </div>
            </article>
          ))}
          {events.length === 0 && (
            <p className="text-sm text-slate-500">Aucun événement disponible pour ce filtre.</p>
          )}
        </section>
      </div>
    </DashboardLayout>
  );
}
