import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

const editableFields = [
  "first_name",
  "last_name",
  "phone",
  "address",
  "city",
  "postal_code",
  "country",
  "gender",
  "marital_status",
  "church_role"
];

export default function Profile() {
  const { user, updateUser } = useAuth();
  const [details, setDetails] = useState(null);
  const [form, setForm] = useState({});
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadProfile = async () => {
      try {
        const { data } = await api.get(`/members/${user.id}`);
        setDetails(data);
        const initialForm = {};
        editableFields.forEach((field) => {
          initialForm[field] = data[field] || "";
        });
        setForm(initialForm);
      } catch (err) {
        setError(err.response?.data?.message || "Impossible de charger le profil.");
      }
    };

    loadProfile();
  }, [user.id]);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage(null);
    setError(null);
    try {
      const { data } = await api.patch("/auth/me", form);
      updateUser({ ...user, ...data });
      setDetails((prev) => ({ ...prev, ...data }));
      setMessage("Profil mis a jour avec succes.");
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de mettre a jour le profil.");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Mon profil</h1>
          <p className="mt-1 text-sm text-slate-500">
            Mettez a jour vos informations personnelles et suivez vos engagements.
          </p>
        </header>

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-700">Informations personnelles</h2>
          <form onSubmit={handleSubmit} className="mt-4 grid gap-4 md:grid-cols-2">
            {editableFields.map((field) => (
              <div key={field} className="flex flex-col">
                <label className="text-sm font-medium text-slate-600 capitalize">
                  {field.replace("_", " ")}
                </label>
                <input
                  name={field}
                  value={form[field] || ""}
                  onChange={handleChange}
                  className="mt-1 rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
            ))}
            <div className="md:col-span-2 flex justify-end">
              <button
                type="submit"
                className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
              >
                Enregistrer
              </button>
            </div>
          </form>
          {message && <p className="mt-3 text-sm text-green-600">{message}</p>}
          {error && <p className="mt-3 text-sm text-red-600">{error}</p>}
        </section>

        {details && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Synthese</h2>
            <dl className="mt-4 grid grid-cols-1 gap-4 md:grid-cols-2">
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">Departements</dt>
                <dd className="mt-1 text-sm text-slate-700">
                  {details.departments?.map((dep) => dep.name).join(", ") || "Aucun"}
                </dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">Famille d impact</dt>
                <dd className="mt-1 text-sm text-slate-700">{details.family?.name || "Non attribue"}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">Statut adhesion</dt>
                <dd className="mt-1 text-sm text-slate-700">{details.membership_status}</dd>
              </div>
              <div>
                <dt className="text-xs uppercase tracking-wide text-slate-500">Role</dt>
                <dd className="mt-1 text-sm text-slate-700">{details.role}</dd>
              </div>
            </dl>
          </section>
        )}
      </div>
    </DashboardLayout>
  );
}
