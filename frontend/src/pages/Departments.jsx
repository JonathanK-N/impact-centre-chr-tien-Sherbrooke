import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import useAuth from "../hooks/useAuth";
import api from "../services/api";

export default function Departments() {
  const { user } = useAuth();
  const [departments, setDepartments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [createForm, setCreateForm] = useState({ name: "", description: "" });

  const canManage = user.role === "admin" || user.role === "department_lead";

  const loadDepartments = async () => {
    setLoading(true);
    try {
      const { data } = await api.get("/departments");
      setDepartments(data);
    } catch (err) {
      setError(err.response?.data?.message || "Impossible de charger les départements");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDepartments();
  }, []);

  const handleCreate = async (event) => {
    event.preventDefault();
    try {
      await api.post("/departments", createForm);
      setCreateForm({ name: "", description: "" });
      loadDepartments();
    } catch (err) {
      setError(err.response?.data?.message || "Création impossible");
    }
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Départements</h1>
          <p className="mt-1 text-sm text-slate-500">
            Gérez les ministères et consultez les membres associés.
          </p>
        </header>

        {canManage && (
          <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Créer un département</h2>
            <form onSubmit={handleCreate} className="mt-4 grid gap-4 md:grid-cols-2">
              <div className="md:col-span-1">
                <label className="block text-sm font-medium text-slate-600">Nom</label>
                <input
                  name="name"
                  required
                  value={createForm.name}
                  onChange={(event) =>
                    setCreateForm((prev) => ({ ...prev, name: event.target.value }))
                  }
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="md:col-span-1">
                <label className="block text-sm font-medium text-slate-600">Description</label>
                <input
                  name="description"
                  value={createForm.description}
                  onChange={(event) =>
                    setCreateForm((prev) => ({ ...prev, description: event.target.value }))
                  }
                  className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                />
              </div>
              <div className="md:col-span-2 flex justify-end">
                <button
                  type="submit"
                  className="rounded-md bg-primary-600 px-4 py-2 text-sm font-medium text-white hover:bg-primary-500"
                >
                  Créer
                </button>
              </div>
            </form>
          </section>
        )}

        <section className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-700">Liste des départements</h2>
          {loading && <p className="mt-4 text-sm text-slate-500">Chargement...</p>}
          {error && <p className="mt-4 text-sm text-red-600">{error}</p>}
          <ul className="mt-4 divide-y divide-slate-200">
            {departments.map((department) => (
              <li key={department.id} className="py-4">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-slate-700">{department.name}</p>
                    <p className="text-sm text-slate-500">{department.description}</p>
                  </div>
                  {department.responsible_id && (
                    <span className="rounded-full bg-primary-50 px-3 py-1 text-xs font-semibold text-primary-600">
                      Responsable #{department.responsible_id}
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ul>
        </section>
      </div>
    </DashboardLayout>
  );
}
