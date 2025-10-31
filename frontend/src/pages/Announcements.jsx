import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

const initialForm = {
  title: "",
  body: "",
  scope: "global",
  department_id: "",
  family_id: "",
  expires_at: ""
};

export default function Announcements() {
  const { user } = useAuth();
  const [announcements, setAnnouncements] = useState([]);
  const [departments, setDepartments] = useState([]);
  const [families, setFamilies] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [error, setError] = useState(null);

  const canPublish = ["admin", "department_lead", "family_lead"].includes(user.role);

  const loadData = async () => {
    try {
      const [annRes, depRes, famRes] = await Promise.all([
        api.get("/announcements"),
        api.get("/departments"),
        api.get("/families")
      ]);
      setAnnouncements(annRes.data);
      setDepartments(depRes.data);
      setFamilies(famRes.data);
    } catch (err) {
      setError(err.response?.data?.message || "Erreur lors du chargement");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const payload = { ...form };
      if (!payload.department_id) delete payload.department_id;
      if (!payload.family_id) delete payload.family_id;
      if (!payload.expires_at) delete payload.expires_at;
      await api.post("/announcements", payload);
      setForm(initialForm);
      loadData();
    } catch (err) {
      setError(err.response?.data?.message || "Publication impossible");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Annonces</h1>
          <p className="mt-1 text-sm text-slate-500">
            Retrouvez les communications importantes pour l&apos;église et vos équipes.
          </p>
        </header>

        {canPublish && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Publier une annonce</h2>
            <form onSubmit={handleSubmit} className="mt-4 grid gap-4 lg:grid-cols-2">
              <div className="lg:col-span-2">
                <label className="block text-sm font-medium text-slate-600">Titre</label>
                <input
                  name="title"
                  value={form.title}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="lg:col-span-2">
                <label className="block text-sm font-medium text-slate-600">Message</label>
                <textarea
                  name="body"
                  value={form.body}
                  onChange={handleChange}
                  rows={4}
                  required
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600">Portée</label>
                <select
                  name="scope"
                  value={form.scope}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="global">Globale</option>
                  <option value="department">Département</option>
                  <option value="family">Famille d&apos;Impact</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600">Département</label>
                <select
                  name="department_id"
                  value={form.department_id}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="">—</option>
                  {departments.map((department) => (
                    <option key={department.id} value={department.id}>
                      {department.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600">Famille</label>
                <select
                  name="family_id"
                  value={form.family_id}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="">—</option>
                  {families.map((family) => (
                    <option key={family.id} value={family.id}>
                      {family.name}
                    </option>
                  ))}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600">Expiration</label>
                <input
                  type="date"
                  name="expires_at"
                  value={form.expires_at}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="lg:col-span-2 flex justify-end">
                <button
                  type="submit"
                  className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
                >
                  Publier
                </button>
              </div>
            </form>
            {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          </section>
        )}

        <section className="grid gap-4">
          {announcements.map((announcement) => (
            <article
              key={announcement.id}
              className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
            >
              <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                <div>
                  <h2 className="text-lg font-semibold text-slate-700">{announcement.title}</h2>
                  <p className="mt-1 text-sm text-slate-500">{announcement.body}</p>
                </div>
                <span className="self-start rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold uppercase text-primary-600">
                  {announcement.scope}
                </span>
              </div>
            </article>
          ))}
          {announcements.length === 0 && (
            <p className="text-sm text-slate-500">Aucune annonce pour le moment.</p>
          )}
        </section>
      </div>
    </DashboardLayout>
  );
}
