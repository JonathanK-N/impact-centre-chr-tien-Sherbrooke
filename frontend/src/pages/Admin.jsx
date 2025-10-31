import React, { useEffect, useState } from "react";

import DashboardLayout from "../layouts/DashboardLayout";
import api from "../services/api";

const emptySummary = { members: 0, departments: 0, families: 0, donations_total: "0" };

export default function Admin() {
  const [summary, setSummary] = useState(emptySummary);
  const [departments, setDepartments] = useState([]);
  const [families, setFamilies] = useState([]);
  const [members, setMembers] = useState([]);
  const [error, setError] = useState(null);

  const loadData = async () => {
    try {
      const [summaryRes, departmentsRes, familiesRes, membersRes] = await Promise.all([
        api.get("/admin/dashboard"),
        api.get("/departments"),
        api.get("/families"),
        api.get("/members")
      ]);
      setSummary(summaryRes.data);
      setDepartments(departmentsRes.data);
      setFamilies(familiesRes.data);
      setMembers(membersRes.data);
    } catch (err) {
      setError(err.response?.data?.message || "Chargement impossible.");
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const assignDepartmentLead = async (departmentId, userId) => {
    await api.post(`/admin/departments/${departmentId}/assign`, { user_id: userId });
    loadData();
  };

  const assignFamilyLead = async (familyId, userId) => {
    await api.post(`/admin/families/${familyId}/assign`, { user_id: userId });
    loadData();
  };

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-6">
        <header>
          <h1 className="text-2xl font-semibold text-primary-600">Administration</h1>
          <p className="mt-1 text-sm text-slate-500">
            Vue globale de l'eglise et gestion des responsables.
          </p>
        </header>

        {error && <p className="text-sm text-red-600">{error}</p>}

        <section className="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">
          {[
            { label: "Membres", value: summary.members },
            { label: "Departements", value: summary.departments },
            { label: "Familles", value: summary.families },
            { label: "Total dons", value: summary.donations_total }
          ].map((item) => (
            <div key={item.label} className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
              <h2 className="text-sm font-medium text-slate-500">{item.label}</h2>
              <p className="mt-2 text-2xl font-semibold text-primary-600">{item.value}</p>
            </div>
          ))}
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Responsables de departements</h2>
            <ul className="mt-4 space-y-4">
              {departments.map((department) => (
                <li key={department.id} className="rounded-lg border border-slate-100 p-4">
                  <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                    <div>
                      <p className="font-medium text-slate-700">{department.name}</p>
                      <p className="text-sm text-slate-500">{department.description}</p>
                    </div>
                    <select
                      value={department.responsible_id || ""}
                      onChange={(event) => assignDepartmentLead(department.id, Number(event.target.value))}
                      className="rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="">Aucun responsable</option>
                      {members.map((member) => (
                        <option key={member.id} value={member.id}>
                          {member.first_name} {member.last_name}
                        </option>
                      ))}
                    </select>
                  </div>
                </li>
              ))}
            </ul>
          </div>
          <div className="rounded-xl border border-slate-200 bg-white p-6 shadow-sm">
            <h2 className="text-lg font-semibold text-slate-700">Responsables Familles d'Impact</h2>
            <ul className="mt-4 space-y-4">
              {families.map((family) => (
                <li key={family.id} className="rounded-lg border border-slate-100 p-4">
                  <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                    <div>
                      <p className="font-medium text-slate-700">{family.name}</p>
                      <p className="text-sm text-slate-500">
                        {family.meeting_day} {family.meeting_time}
                      </p>
                    </div>
                    <select
                      value={family.responsible_id || ""}
                      onChange={(event) => assignFamilyLead(family.id, Number(event.target.value))}
                      className="rounded-md border-slate-300 text-sm shadow-sm focus:border-primary-500 focus:ring-primary-500"
                    >
                      <option value="">Aucun responsable</option>
                      {members.map((member) => (
                        <option key={member.id} value={member.id}>
                          {member.first_name} {member.last_name}
                        </option>
                      ))}
                    </select>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>
    </DashboardLayout>
  );
}
