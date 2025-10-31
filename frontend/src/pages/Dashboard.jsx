import React, { useEffect, useState } from "react";
import dayjs from "dayjs";
import {
  MegaphoneIcon,
  CalendarDaysIcon,
  BanknotesIcon,
  ShieldCheckIcon,
  UsersIcon,
  BriefcaseIcon,
  MapPinIcon
} from "@heroicons/react/24/outline";

import DashboardLayout from "../layouts/DashboardLayout";
import StatCard from "../components/StatCard";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

export default function Dashboard() {
  const { user } = useAuth();
  const [announcements, setAnnouncements] = useState([]);
  const [events, setEvents] = useState([]);
  const [donationSummary, setDonationSummary] = useState(null);
  const [adminSummary, setAdminSummary] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [annRes, eventRes] = await Promise.all([
          api.get("/announcements"),
          api.get("/events?scope=global")
        ]);
        setAnnouncements(annRes.data.slice(0, 4));
        setEvents(eventRes.data.slice(0, 4));
      } catch (err) {
        setError(err.response?.data?.message || "Impossible de charger les informations.");
      }

      try {
        const donationRes = await api.get("/donations/summary");
        setDonationSummary(donationRes.data);
      } catch {
        setDonationSummary(null);
      }

      if (user.role === "admin") {
        try {
          const summaryRes = await api.get("/admin/dashboard");
          setAdminSummary(summaryRes.data);
        } catch (err) {
          setError(err.response?.data?.message || "Erreur lors du chargement du tableau admin.");
        }
      }
    };

    loadData();
  }, [user.role]);

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        {error && <p className="text-sm text-red-600">{error}</p>}
        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          <StatCard title="Annonces actives" value={announcements.length} icon={MegaphoneIcon} />
          <StatCard title="Evenements a venir" value={events.length} icon={CalendarDaysIcon} />
          <StatCard
            title="Mes dons"
            value={donationSummary ? `${donationSummary.total_amount} ${donationSummary.currency}` : "—"}
            icon={BanknotesIcon}
          />
          <StatCard title="Mon role" value={user.role} icon={ShieldCheckIcon} />
        </section>

        {adminSummary && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-primary-600">Vue admin</h2>
            <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
              <StatCard title="Membres" value={adminSummary.members} icon={UsersIcon} />
              <StatCard title="Departements" value={adminSummary.departments} icon={BriefcaseIcon} />
              <StatCard title="Familles" value={adminSummary.families} icon={MapPinIcon} />
              <StatCard title="Total dons" value={adminSummary.donations_total} icon={BanknotesIcon} />
            </div>
          </section>
        )}

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-primary-600">Annonces</h2>
            <ul className="mt-4 space-y-4">
              {announcements.map((announcement) => (
                <li key={announcement.id} className="rounded-lg border border-slate-100 p-4">
                  <h3 className="font-medium text-slate-700">{announcement.title}</h3>
                  <p className="mt-1 text-sm text-slate-500 line-clamp-3">{announcement.body}</p>
                </li>
              ))}
              {announcements.length === 0 && (
                <p className="text-sm text-slate-500">Aucune annonce pour le moment.</p>
              )}
            </ul>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-primary-600">Evenements</h2>
            <ul className="mt-4 space-y-4">
              {events.map((event) => (
                <li key={event.id} className="rounded-lg border border-slate-100 p-4">
                  <h3 className="font-medium text-slate-700">{event.title}</h3>
                  <p className="mt-1 text-sm text-slate-500">
                    {dayjs(event.start_at).format("DD MMM YYYY HH:mm")}
                  </p>
                  <p className="mt-1 text-sm text-slate-500">{event.location || "Lieu a confirmer"}</p>
                </li>
              ))}
              {events.length === 0 && (
                <p className="text-sm text-slate-500">Aucun evenement a venir.</p>
              )}
            </ul>
          </div>
        </section>
      </div>
    </DashboardLayout>
  );
}
