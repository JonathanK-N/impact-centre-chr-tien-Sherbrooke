import React from "react";

export default function StatCard({ title, value, icon: Icon, color = "bg-white" }) {
  return (
    <div className={`rounded-lg border border-slate-200 px-4 py-5 shadow-sm ${color}`}>
      <div className="flex items-center justify-between">
        <dt className="text-sm font-medium text-slate-500">{title}</dt>
        {Icon ? <Icon className="h-5 w-5 text-primary-500" /> : null}
      </div>
      <dd className="mt-2 text-2xl font-semibold text-primary-600">{value}</dd>
    </div>
  );
}
