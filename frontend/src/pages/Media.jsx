import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

const initialForm = {
  title: "",
  description: "",
  media_type: "video",
  url: "",
  tags: ""
};

export default function Media() {
  const { user } = useAuth();
  const [mediaItems, setMediaItems] = useState([]);
  const [filter, setFilter] = useState("all");
  const [form, setForm] = useState(initialForm);
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  const canCreate = ["admin", "department_lead", "family_lead"].includes(user.role);

  const loadMedia = async () => {
    try {
      const query = filter === "all" ? "" : `?media_type=${filter}`;
      const { data } = await api.get(`/media${query}`);
      setMediaItems(data);
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de récupérer les médias.");
    }
  };

  useEffect(() => {
    loadMedia();
  }, [filter]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage(null);
    setError(null);
    try {
      await api.post("/media", form);
      setMessage("Média enregistré avec succès.");
      setForm(initialForm);
      loadMedia();
    } catch (err) {
      setError(err.response?.data?.message || "Impossible d'enregistrer le média.");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-2xl font-semibold text-primary-600">Médias</h1>
            <p className="mt-1 text-sm text-slate-500">
              Vidéos, audio et documents à partager avec la communauté.
            </p>
          </div>
          <select
            value={filter}
            onChange={(event) => setFilter(event.target.value)}
            className="w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500 md:w-48"
          >
            <option value="all">Tous</option>
            <option value="video">Vidéos</option>
            <option value="audio">Audio</option>
            <option value="document">Documents</option>
          </select>
        </header>

        {canCreate && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Ajouter un média</h2>
            <form onSubmit={handleSubmit} className="mt-4 grid gap-4 md:grid-cols-2">
              <div>
                <label className="block text-sm font-medium text-slate-600">Titre</label>
                <input
                  name="title"
                  required
                  value={form.title}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-600">Type</label>
                <select
                  name="media_type"
                  value={form.media_type}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                >
                  <option value="video">Vidéo</option>
                  <option value="audio">Audio</option>
                  <option value="document">Document</option>
                </select>
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-slate-600">URL</label>
                <input
                  name="url"
                  type="url"
                  required
                  value={form.url}
                  onChange={handleChange}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-slate-600">Description</label>
                <textarea
                  name="description"
                  value={form.description}
                  onChange={handleChange}
                  rows={3}
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-slate-600">Tags</label>
                <input
                  name="tags"
                  value={form.tags}
                  onChange={handleChange}
                  placeholder="louange, enseignement..."
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="md:col-span-2 flex justify-end">
                <button
                  type="submit"
                  className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
                >
                  Publier
                </button>
              </div>
            </form>
            {message && <p className="mt-3 text-sm text-green-600">{message}</p>}
            {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
          </section>
        )}

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {mediaItems.map((item) => (
            <article key={item.id} className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm">
              <p className="text-xs uppercase tracking-wide text-slate-400">{item.media_type}</p>
              <h3 className="mt-1 text-lg font-semibold text-slate-700">{item.title}</h3>
              <p className="mt-2 text-sm text-slate-500 line-clamp-3">{item.description}</p>
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer"
                className="mt-4 inline-flex text-sm font-medium text-primary-600"
              >
                Consulter
              </a>
            </article>
          ))}
          {mediaItems.length === 0 && (
            <p className="text-sm text-slate-500">Aucun média publié pour l'instant.</p>
          )}
        </section>
      </div>
    </DashboardLayout>
  );
}
