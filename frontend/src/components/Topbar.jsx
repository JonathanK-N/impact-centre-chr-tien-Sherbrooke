import React from "react";
import useAuth from "../hooks/useAuth";

export default function Topbar({ onToggleMenu }) {
  const { user, logout } = useAuth();

  return (
    <header className="flex items-center justify-between border-b border-slate-200 bg-white px-4 py-3 shadow-sm">
      <div className="flex items-center gap-2">
        <button
          type="button"
          className="md:hidden rounded-md border border-slate-200 px-2 py-1 text-sm"
          onClick={onToggleMenu}
        >
          ☰
        </button>
        <span className="text-sm text-slate-500">Bonjour,</span>
        <span className="font-semibold text-primary-600">
          {user?.first_name} {user?.last_name}
        </span>
      </div>
      <div className="flex items-center gap-3">
        <span className="hidden sm:block text-xs uppercase tracking-wide text-slate-400">
          Rôle: {user?.role}
        </span>
        <button
          type="button"
          onClick={logout}
          className="rounded-md bg-primary-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-primary-500"
        >
          Se déconnecter
        </button>
      </div>
    </header>
  );
}
