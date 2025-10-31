import React from "react";
import { NavLink } from "react-router-dom";
import {
  HomeModernIcon,
  UserCircleIcon,
  BriefcaseIcon,
  MapPinIcon,
  CalendarDaysIcon,
  MegaphoneIcon,
  PlayCircleIcon,
  BanknotesIcon,
  WrenchScrewdriverIcon
} from "@heroicons/react/24/outline";

const links = [
  { to: "/", label: "Dashboard", icon: HomeModernIcon },
  { to: "/profile", label: "Mon profil", icon: UserCircleIcon },
  { to: "/departments", label: "Mes départements", icon: BriefcaseIcon },
  { to: "/families", label: "Ma Famille d'Impact", icon: MapPinIcon },
  { to: "/events", label: "Événements", icon: CalendarDaysIcon },
  { to: "/announcements", label: "Annonces", icon: MegaphoneIcon },
  { to: "/media", label: "Médias", icon: PlayCircleIcon },
  { to: "/donations", label: "Dons", icon: BanknotesIcon }
];

export default function Sidebar({ role }) {
  const adminLinks = [{ to: "/admin", label: "Administration", icon: WrenchScrewdriverIcon }];

  return (
    <aside className="bg-white border-r border-slate-200 w-64 px-4 py-6 hidden md:flex flex-col gap-4">
      <div>
        <h1 className="text-xl font-semibold text-primary-600">Impact Sherbrooke</h1>
        <p className="text-sm text-slate-500">Vie communautaire</p>
      </div>
      <nav className="flex-1 space-y-1">
        {links.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className={({ isActive }) =>
              `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium ${
                isActive ? "bg-primary-50 text-primary-600" : "text-slate-600 hover:bg-slate-100"
              }`
            }
          >
            <link.icon className="h-5 w-5" />
            {link.label}
          </NavLink>
        ))}
        {role === "admin" && (
          <div className="pt-4 border-t border-slate-200">
            {adminLinks.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2 rounded-md text-sm font-medium ${
                    isActive ? "bg-primary-50 text-primary-600" : "text-slate-600 hover:bg-slate-100"
                  }`
                }
              >
                <link.icon className="h-5 w-5" />
                {link.label}
              </NavLink>
            ))}
          </div>
        )}
      </nav>
    </aside>
  );
}
