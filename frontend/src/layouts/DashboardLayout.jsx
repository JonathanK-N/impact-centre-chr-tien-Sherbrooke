import React, { useState } from "react";
import Sidebar from "../components/Sidebar";
import Topbar from "../components/Topbar";
import useAuth from "../hooks/useAuth";

export default function DashboardLayout({ children }) {
  const { user } = useAuth();
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <div className="min-h-screen bg-slate-50 flex">
      <Sidebar role={user?.role} />
      {mobileOpen && (
        <div className="fixed inset-0 z-40 flex md:hidden">
          <div className="w-64 bg-white shadow-lg">
            <Sidebar role={user?.role} />
          </div>
          <div className="flex-1 bg-black/30" onClick={() => setMobileOpen(false)} aria-hidden="true" />
        </div>
      )}
      <div className="flex-1 flex flex-col">
        <Topbar onToggleMenu={() => setMobileOpen((prev) => !prev)} />
        <main className="flex-1 p-4 md:p-6">{children}</main>
      </div>
    </div>
  );
}
